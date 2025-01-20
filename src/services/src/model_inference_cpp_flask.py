
import re
import threading, json
from src.entry import app
from src import compile
from src.prompts import *
from typing import Iterator
from llama_cpp import Llama, StoppingCriteriaList
from src.llm_output_parser import StopOnTokens, StopOnTokensNL
from flask import Flask, request, jsonify, Response, g


CONTEXT = 3500*6
model = Llama(
  model_path=model_path, 
  n_threads=1,           
  n_gpu_layers=-1,
  verbose=False, 
  chat_format="chatml",
  n_ctx=CONTEXT
)
EMPTY = ""
LARGE_CONTEXT = "High context size. Try again while reducing the request context size!"
TRY_LATER = "Try again later!"
lock = threading.Lock()
MAX_VULNERABILITY_CHECK_REQUESTS_PARALLEL = 3
requests_counter = 0

def is_prompt_covered(prompt: str) -> int:
    if len(model.tokenizer().encode(prompt)) > CONTEXT:
        print('Prompt is too large: ', len(model.tokenizer().encode(prompt)))
        return False
    return True

def is_prompt_covered_half(prompt: str) -> int:
    if len(model.tokenizer().encode(prompt)) > (CONTEXT // 2):
        return False
    return True

def unpack_req_params(data):
    try:
        arr_obj = data.get('data', None)

        if arr_obj is not None:
            # unpack payload array
            prompt = arr_obj[0]
            stream_result = arr_obj[1]
            max_new_tokens = arr_obj[2]
            max_new_tokens = 1000 if max_new_tokens>1000 else max_new_tokens
            temperature =float(arr_obj[3])
            top_p = float(arr_obj[4])
            top_k = int(arr_obj[5]) if len(arr_obj)-1>4 else 50
            context = arr_obj[6] if len(arr_obj)-1>5 else ""
            repeat_penalty= float(data.get('repeat_penalty', 1.2))
            frequency_penalty= float(data.get('frequency_penalty', 0.2))
            presence_penalty= float(data.get('presence_penalty', 0.2))

        else:
            #unpack objects
            prompt = data.get('prompt', "")
            context = data.get('context', "")
            stream_result = data.get('stream_result', False)
            max_new_tokens = int(data.get('max_new_tokens', 20))
            max_new_tokens = 1000 if max_new_tokens>1000 else max_new_tokens
            temperature = float(data.get('temperature', 0.8))
            top_p = float(data.get('top_p', 0.9))
            top_k = int(data.get('top_k', 50))
            repeat_penalty= float(data.get('repeat_penalty', 1.2))
            frequency_penalty= float(data.get('frequency_penalty', 0.2))
            presence_penalty= float(data.get('presence_penalty', 0.2))
        return [prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty]
            

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
            

def generate(generate_kwargs):
    with lock:
        for outputs in model(**generate_kwargs):
            text = outputs["choices"][0]["text"]
            yield f"{json.dumps({'generatedText': text, 'isGenerating': True})}"
        yield f"{json.dumps({'generatedText': '', 'isGenerating': False})}"

def code_explaining(): 
    try:
        print('INFO - Code Explaining')
        data = request.json
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        prompt = get_codexplain_prompt(prompt, context=context)

        if not is_prompt_covered(prompt):
            return Response(f"{json.dumps({'data': LARGE_CONTEXT, 'generatedText':LARGE_CONTEXT})}")

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stream=stream_result,
            repeat_penalty=repeat_penalty,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        if stream_result:
            return app.response_class(generate(generate_kwargs), content_type='application/json')
        else:
            with lock:
                outputs = model(**generate_kwargs)
            text = outputs["choices"][0]["text"]
            return  Response(f"{json.dumps({'data': [text], 'generatedText':text})}")
    except Exception as ex:
        print('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'data': EMPTY, 'generatedText':EMPTY})}")

def solidity_answer(): 
    try:
        print('INFO - solidity Answer')
        data = request.json
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        
        prompt = get_answer_prompt(prompt)
        if not is_prompt_covered(prompt):
            return Response(f"{json.dumps({'data': LARGE_CONTEXT, 'generatedText':LARGE_CONTEXT})}")


        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stream=stream_result,
            repeat_penalty=repeat_penalty,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        if stream_result:
            return app.response_class(generate(generate_kwargs), content_type='application/json')
        else:
            with lock:
                outputs = model(**generate_kwargs)
            text = outputs["choices"][0]["text"]
            return  Response(f"{json.dumps({'data': [text], 'generatedText':text})}")


    except Exception as ex:
        print('ERROR - Solidity Answer', ex)
        return Response(f"{json.dumps({'data': EMPTY, 'generatedText':EMPTY})}")

def error_explaining():
    try:
        print('INFO - Error Explaining')
        data = request.json
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        prompt = get_codexplain_prompt(prompt, context=context)
        if not is_prompt_covered(prompt):
            return Response(f"{json.dumps({'data': LARGE_CONTEXT, 'generatedText':LARGE_CONTEXT})}")

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stream=stream_result,
            repeat_penalty=repeat_penalty,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        if stream_result:
            return app.response_class(generate(generate_kwargs), content_type='application/json')
        else:
            with lock:
                outputs = model(**generate_kwargs)
            text = outputs["choices"][0]["text"]
            return  Response(f"{json.dumps({'data': [text], 'generatedText':text})}")
        
    except Exception as ex:
        print('ERROR - Error Explaining')
        return Response(f"{json.dumps({'data': EMPTY, 'generatedText':EMPTY})}")
    
def code_insertion(): 
    try:
        print('INFO - Code Insertion')
        data = request.json
        # parse all params
        code_pfx = data.get('msg_pfx', "")
        code_sfx = data.get('msg_sfx', "")
        stream_result = data.get('stream_result', False)
        max_new_tokens = int(data.get('max_new_tokens', 20))
        temperature = float(data.get('temperature', 0.8))
        top_p = float(data.get('top_p', 0.9))
        top_k = int(data.get('top_k', 50))
        repeat_penalty= float(data.get('repeat_penalty', 1.2))
        frequency_penalty= float(data.get('frequency_penalty', 0.2))
        presence_penalty= float(data.get('presence_penalty', 0.2))

        prompt = get_coinsert_prompt(msg_prefix=code_pfx, msg_surfix=code_sfx)
        if not is_prompt_covered(prompt):
            return Response(f"{json.dumps({'data': EMPTY, 'generatedText':EMPTY})}")

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stream=stream_result,
            repeat_penalty=repeat_penalty,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        with lock:
            outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"]
        return  Response(f"{json.dumps({'generatedText': text, 'isGenerating': False})}")
    except Exception as ex:
        print('ERROR - Code Insertion', ex)
        return Response(f"{json.dumps({'data': EMPTY, 'generatedText':EMPTY})}")
    
def code_completion(): 
    try:
        print('INFO - Code Completion')
        data = request.json
        # parse all params
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        
        stopping_criteria = StoppingCriteriaList([StopOnTokensNL(model.tokenizer())])
        if not is_prompt_covered(prompt):
            return Response(f"{json.dumps({'data': EMPTY, 'generatedText':EMPTY})}")

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stream=stream_result,
            repeat_penalty=repeat_penalty,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stopping_criteria=stopping_criteria
        )
        with lock:
            outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"]
        return  Response(f"{json.dumps({'generatedText': text, 'isGenerating': False})}")
    except Exception as ex:
        print('ERROR - Code Completion', ex)
        return Response(f"{json.dumps({'data': EMPTY, 'generatedText':EMPTY})}")


# Schemas endpoints

def vulnerability_check():
    global requests_counter
    try:
        print('INFO: Vulnerability check')
        data = request.json
        (prompt, context, stream_result, max_new_tokens, temperature, top_k, top_p, repeat_penalty, frequency_penalty, presence_penalty) = unpack_req_params(data)
        print('#'*100)
        print('Prompt:', prompt)
        print('#'*100)
        if requests_counter >= MAX_VULNERABILITY_CHECK_REQUESTS_PARALLEL:
            return Response(f"{json.dumps({'data': TRY_LATER, 'generatedText':TRY_LATER})}")
        
        requests_counter += 1

        if not is_prompt_covered_half(prompt):
            return Response(f"{json.dumps({'data': LARGE_CONTEXT, 'generatedText':LARGE_CONTEXT})}")

        prompt = schemaPromptGenerator(prompt)

        with lock:
            # No streaming support
            report = model.create_chat_completion(messages=prompt, max_tokens=max_new_tokens, top_p=top_p, top_k=top_k, temperature=temperature, repeat_penalty=repeat_penalty, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty)
            requests_counter -= 1

        if stream_result:
            return  Response(f"{json.dumps({'generatedText':report['choices'][0]['message']['content'], 'isGenerating': False})}")
        else:
            return  Response(f"{json.dumps({'data': [report['choices'][0]['message']['content']], 'generatedText':report['choices'][0]['message']['content']})}")
    except Exception as ex:
        print('ERROR -Vulnerability check', ex)
        return Response(f"{json.dumps({'data': EMPTY, 'generatedText':EMPTY})}")
    