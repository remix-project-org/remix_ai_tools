import code

import test
from src.prompts import *
from src.llm_output_parser import StopOnTokens, StopOnTokensNL
from typing import Iterator
from llama_cpp import Llama, StoppingCriteriaList
import threading, json
from flask import request, Response

DEFAULT_CONTEXT_SIZE = 2148
use_deep_seek = True
# completion_model = Llama(
#   model_path=completion_model_path, 
#   #model_path="../../deepseek-coder-6.7b-instruct.Q4_K_M.gguf" if use_deep_seek else "../../mistral-7b-instruct-v0.2-code-ft.Q4_K_M.gguf", 
#   n_threads=16,           
#   n_gpu_layers=-1,
#   n_ctx=DEFAULT_CONTEXT_SIZE*10,
#   verbose=False
# )

insertion_model = Llama(
  model_path=insertsion_model_path, 
  n_threads=16,           
  n_gpu_layers=-1,
  n_ctx=DEFAULT_CONTEXT_SIZE*6,
  verbose=False
)

lock = threading.Lock()

def unpack_req_params(data):
    try:
        arr_obj = data.get('data', None)

        if arr_obj is not None:
            # unpack payload array
            msg_pfx = arr_obj[0]
            msg_sfx = arr_obj[1]

            if msg_sfx == "":
                stream_result = arr_obj[2]
                max_new_tokens = arr_obj[3]
                max_new_tokens = 1000 if max_new_tokens>1000 else max_new_tokens
                temperature =float(arr_obj[4])
                top_p = float(arr_obj[5])
                top_k = int(arr_obj[6]) if len(arr_obj)-1>5 else 50
            else:
                stream_result = False
                max_new_tokens = arr_obj[2]
                max_new_tokens = 1000 if max_new_tokens>1000 else max_new_tokens
                temperature =float(arr_obj[3])
                top_p = float(arr_obj[4])
                top_k = int(arr_obj[5]) if len(arr_obj)-1>4 else 50

            repeat_penalty= float(data.get('repeat_penalty', 1.2))
            frequency_penalty= float(data.get('frequency_penalty', 0.2))
            presence_penalty= float(data.get('presence_penalty', 0.2))

        else:
            #unpack objects
            stream_result = data.get('stream_result', False)
            max_new_tokens = int(data.get('max_new_tokens', 20))
            max_new_tokens = 1000 if max_new_tokens>1000 else max_new_tokens
            temperature = float(data.get('temperature', 0.8))
            top_p = float(data.get('top_p', 0.9))
            top_k = int(data.get('top_k', 50))

            if data.get('msg_pfx', "") == "":
                msg_pfx = data.get('prompt', "")
                msg_sfx = data.get('context', "")
            else:
                msg_pfx = data.get('msg_pfx', "")
                msg_sfx = data.get('msg_sfx', "")

            repeat_penalty= float(data.get('repeat_penalty', 1.2))
            frequency_penalty= float(data.get('frequency_penalty', 0.2))
            presence_penalty= float(data.get('presence_penalty', 0.2))
        return [msg_pfx, msg_sfx, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty]
            
    except Exception as ex:
        print(ex)
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
            

async def run_code_completion() -> str:
    
    try:
        data = request.json
        # return json obj if request body is json
        r_obj_type = True if data.get('data', None) == None else False
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        
        if len(context) > 1: # use context as surfix
            prompt = get_coinsert_prompt(msg_prefix=prompt, msg_surfix=context)
        
        stopping_criteria = StoppingCriteriaList([StopOnTokensNL(insertion_model.tokenizer())])

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stopping_criteria=stopping_criteria
        )

        with lock:
            outputs = insertion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        print('INFO - Code Completion', text)
        return  Response(f"{json.dumps({'generatedText': text})}") if r_obj_type else Response(f"{json.dumps({'data': [text]})}")
        
    except Exception as ex:
        print('ERROR - Code Completion', ex)
        return  Response(f"{json.dumps({'generatedText': ''})}") if r_obj_type else Response(f"{json.dumps({'data': ['']})}")


async def run_code_insertion() -> str:
    
    try:
        data = request.json
        r_obj_type = True if data.get('data', None) == None else False
        (code_pfx, code_sfx, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        prompt = get_coinsert_prompt(msg_prefix=code_pfx, msg_surfix=code_sfx)

        # No stopping criteria as the in filling pushes in what is good
        # TODO: only allow 1 artifact generation: example 1 function, 1 contract, 1 struct, 1 interface, 1 for loop or similar. single {}
        stopping_criteria = StoppingCriteriaList([StopOnTokens(insertion_model.tokenizer())])

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stopping_criteria=stopping_criteria
        )

        with lock:
            outputs = insertion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        print('INFO - Code Insertion', text)
        return  Response(f"{json.dumps({'generatedText': text})}") if r_obj_type else Response(f"{json.dumps({'data': [text]})}")
    except Exception as ex:
        print('ERROR - Code Insertion', ex)
        return  Response(f"{json.dumps({'generatedText': ''})}") if r_obj_type else Response(f"{json.dumps({'data': ['']})}")


async def run_code_generation() -> str:

    try:
        data = request.json
        r_obj_type = True if data.get('data', None) == None else False
        print('Using json object request:', r_obj_type)
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        
        prompt = get_cogen_prompt(prompt, is_model_deep_seek=use_deep_seek)
        stopping_criteria = StoppingCriteriaList([StopOnTokens(insertion_model.tokenizer())])
        
        print('INFO - Code Generation')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stopping_criteria=stopping_criteria
        )

        with lock:
            outputs = insertion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        text = text.replace("```solidity \n", "").replace("```", "")
        return  Response(f"{json.dumps({'generatedText': text})}") if r_obj_type else Response(f"{json.dumps({'data': [text]})}")
    except Exception as ex:
        print('ERROR - Code generation', ex)
        return  Response(f"{json.dumps({'generatedText': ''})}") if r_obj_type else Response(f"{json.dumps({'data': ['']})}")