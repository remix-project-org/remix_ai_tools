import os
from src.prompts import *
from src.llm_output_parser import StopOnTokens, StopOnTokensNL
from llama_cpp import Llama, StoppingCriteriaList
import threading
from src.utils.sysInfos import collect_system_info
import json
from flask import Flask, request, jsonify, Response, g

app = Flask(__name__)
DEFAULT_CONTEXT_SIZE = 2048

multitask_model:Llama = None # type: ignore
completion_model:Llama = None # type: ignore

completion_lock = threading.Lock()
general_lock = threading.Lock()


def unpack_req_params(data):
    try:
        #unpack objects
        stream_result = data.get('stream_result', False)
        max_new_tokens = int(data.get('max_new_tokens', 20))
        max_new_tokens = 1000 if max_new_tokens>1000 else max_new_tokens
        temperature = float(data.get('temperature', 0.8))
        top_p = float(data.get('top_p', 0.9))
        top_k = int(data.get('top_k', 50))
        repeat_penalty= float(data.get('repeat_penalty', 1.2))
        frequency_penalty= float(data.get('frequency_penalty', 0.2))
        presence_penalty= float(data.get('presence_penalty', 0.2))
        if data.get('msg_pfx', "") == "":
            prompt = data.get('prompt', "")
            context = data.get('context', "")
        else:
            prompt = data.get('msg_pfx', "")
            context = data.get('msg_sfx', "")
        return [prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty]
            
    except Exception as ex:
        app.logger.info(ex)
        prompt = data.get('prompt', "No input")
        context = data.get('context', "")
        stream_result = data.get('stream_result', False)
        max_new_tokens = int(data.get('max_new_tokens', 20))
        temperature = float(data.get('temperature', 0.8))
        top_p = float(data.get('top_p', 0.9))
        top_k = int(data.get('top_k', 50))
        repeat_penalty= float(data.get('repeat_penalty', 1.2))
        frequency_penalty= float(data.get('frequency_penalty', 0.2))
        presence_penalty= float(data.get('presence_penalty', 0.2))
        return [prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty]
           
async def code_completion():
    try:
        app.logger.info('INFO - Code Completion')
        data = request.json 
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
   
        # prompt = get_cocom_prompt(message=context_code, is_model_deep_seek=use_deep_seek)
        stopping_criteria = StoppingCriteriaList([StopOnTokensNL(completion_model.tokenizer())])
        if len(context) >= 1: # use context as surfix
            app.logger.info('INFO - Using context as surfix')
            prompt = get_coinsert_prompt(msg_prefix=prompt, msg_surfix=context, modelName=determine_model(completion_model.model_path))
                
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            repeat_penalty=repeat_penalty,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stopping_criteria=stopping_criteria
        )

        with completion_lock:
            outputs = completion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return jsonify({ "generatedText":text })
    except Exception as ex:
        app.logger.info('ERROR - Code Completion', ex)
        return jsonify({ "error":ex })
    
async def code_insertion():
    try:
        data = request.json 
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        prompt = get_coinsert_prompt(msg_prefix=prompt, msg_surfix=context, modelName=determine_model(completion_model.model_path))

        # No stopping criteria as the in filling pushes in what is good
        # TODO: only allow 1 artifact generation: example 1 function, 1 contract, 1 struct, 1 interface, 1 for loop or similar. single {}
        stopping_criteria = StoppingCriteriaList([StopOnTokensNL(completion_model.tokenizer())])

        app.logger.info('INFO - Code Insertion')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            # repeat_penalty=repeat_penalty,
            # frequency_penalty=frequency_penalty,
            # presence_penalty=presence_penalty,
            stopping_criteria=stopping_criteria
        )

        with completion_lock:
            outputs = completion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return jsonify({ "generatedText":text })
    except Exception as ex:
        app.logger.info('ERROR - Code Insertion', ex)
        return jsonify({ "error":ex })

async def code_generation():
    try:
        data = request.json 
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        prompt = get_cogen_prompt(prompt, determine_model(multitask_model.model_path))
        stopping_criteria = StoppingCriteriaList([StopOnTokens(multitask_model.tokenizer())])
        
        app.logger.info('INFO - Code Generation')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stopping_criteria=stopping_criteria
        )

        return Response(generate(stream_result, generate_kwargs),  mimetype='text/event-stream')
    
    except Exception as ex:
        app.logger.info('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'error': ex})}")  

async def state():
    return jsonify({ "status":"running",
                     "completion": True if completion_model!=None else False,
                     "general": True if multitask_model!=None else False})

async def sysinfos():
    return jsonify(collect_system_info())

async def killServer():
    os._exit(0)

async def init_completion():
    global completion_model
    try:
        data = request.json
        model_path = data.get('model_path') # type: ignore
        completion_model = Llama(
            model_path=model_path, 
            n_threads=16,           
            n_gpu_layers=-1,
            n_ctx=DEFAULT_CONTEXT_SIZE*15,
            verbose=False
        )
        return jsonify({ "status":"success" })
    except Exception as ex:
        return jsonify({ "error":'Error while initializing the completion model' + str(ex) })

async def init_general():
    global multitask_model
    try:
        data = request.json
        model_path = data.get('model_path') # type: ignore
        app.logger.info('INFO - Initializing the general model with backend prompts', determine_model(model_path))
        multitask_model = Llama(
            model_path=model_path, 
            n_threads=16,           
            n_gpu_layers=-1,
            n_ctx=DEFAULT_CONTEXT_SIZE*5,
            verbose=False
        )
        return jsonify({ "status":"success" })
    except Exception as ex:
        return jsonify({ "error":'Error while initializing the general model' + str(ex) })

def generate(stream_result, generate_kwargs):
    with general_lock:
        if stream_result:
            for outputs in multitask_model(**generate_kwargs):
                text = outputs["choices"][0]["text"]
                yield f"{json.dumps({'generatedText': text, 'isGenerating': True})}"
            yield f"{json.dumps({'generatedText': '', 'isGenerating': False})}"
        else:
            outputs = multitask_model(**generate_kwargs)
            text = outputs["choices"][0]["text"]
            yield  f"{json.dumps({'generatedText': text, 'isGenerating': False})}"

async def code_explaining():
    try:
        data = request.json 
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        prompt = get_codexplain_prompt(prompt, determine_model(multitask_model.model_path), context)

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stream=stream_result,
            # repeat_penalty=repeat_penalty,
            # frequency_penalty=frequency_penalty,
            # presence_penalty=presence_penalty,
        )
        
        return Response(generate(stream_result, generate_kwargs),  mimetype='text/event-stream')
    except Exception as ex:
        app.logger.info('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'error': ex})}")
    
async def error_explaining ():
    
    try:
        data = request.json 
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        prompt = get_errexplain_prompt(prompt, determine_model(multitask_model.model_path)) 

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stream=stream_result,
            # repeat_penalty=repeat_penalty,
            # frequency_penalty=frequency_penalty,
            # presence_penalty=presence_penalty,
        )

        return Response(generate(stream_result, generate_kwargs),  mimetype='text/event-stream')
    except Exception as ex:
        app.logger.info('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'error': ex})}")
    
async def run_answering ():
    try:
        data = request.json 
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        prompt = get_answer_prompt(prompt, determine_model(multitask_model.model_path)) 

        app.logger.info('INFO - Answering')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stream=stream_result,
            # repeat_penalty=repeat_penalty,
            # frequency_penalty=frequency_penalty,
            # presence_penalty=presence_penalty,
        )
        return Response(generate(stream_result, generate_kwargs),  mimetype='text/event-stream')
    except Exception as ex:
        app.logger.info('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'error': ex})}")  

