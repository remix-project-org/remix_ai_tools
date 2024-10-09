
import threading, json
from src.entry import get_app
from src import compile
from src.prompts import *
from typing import Iterator
from llama_cpp import Llama, StoppingCriteriaList
from src.llm_output_parser import StopOnTokens, StopOnTokensNL
from flask import Flask, request, jsonify, Response

app = get_app('flask')
model = Llama(
  model_path=model_path, 
  n_threads=1,           
  n_gpu_layers=-1,
  verbose=False, 
  n_ctx=3500*3, 
)

lock = threading.Lock()

def generate(stream_result, generate_kwargs):
    with lock:
        if stream_result:
            for outputs in model(**generate_kwargs):
                text = outputs["choices"][0]["text"]
                yield f"{json.dumps({'generatedText': text, 'isGenerating': True})}"
            return f"{json.dumps({'generatedText': '', 'isGenerating': False})}"
        else:
            outputs = model(**generate_kwargs)
            text = outputs["choices"][0]["text"]
            return  f"{json.dumps({'generatedText': text, 'isGenerating': False})}"


async def code_explaining(): 
    print('INFO - Code Explaining')
    data = request.json
    # parse all params
    code = data.get('prompt', "")

    context = data.get('context', "")
    stream_result = data.get('stream_result', False)
    max_new_tokens = int(data.get('max_new_tokens', 20))
    temperature = float(data.get('temperature', 0.8))
    top_p = float(data.get('top_p', 0.9))
    top_k = int(data.get('top_k', 50))
    repeat_penalty= float(data.get('repeat_penalty', 1.2))
    frequency_penalty= float(data.get('frequency_penalty', 0.2))
    presence_penalty= float(data.get('presence_penalty', 0.2))

    try:
        prompt = get_codexplain_prompt(code, context=context)
        print('INFO - Code Explaining') 
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
        return Response(generate(stream_result, generate_kwargs))
    except Exception as ex:
        print('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'error': ex})}")

async def solidity_answer(): 
    print('INFO - solidity Answer')
    data = request.json
    # parse all params
    prompt = data.get('prompt', "")
    context = data.get('context', "")
    stream_result = data.get('stream_result', False)
    max_new_tokens = int(data.get('max_new_tokens', 20))
    temperature = float(data.get('temperature', 0.8))
    top_p = float(data.get('top_p', 0.9))
    top_k = int(data.get('top_k', 50))
    repeat_penalty= float(data.get('repeat_penalty', 1.2))
    frequency_penalty= float(data.get('frequency_penalty', 0.2))
    presence_penalty= float(data.get('presence_penalty', 0.2))

    try:
        prompt = get_answer_prompt(prompt)
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
        return Response(generate(stream_result, generate_kwargs))
    except Exception as ex:
        print('ERROR - Solidity Answer', ex)
        return Response(f"{json.dumps({'error': ex})}")

async def error_explaining():
    print('INFO - Error Explaining')
    data = request.json
    # parse all params
    prompt = data.get('prompt', "")
    context = data.get('context', "") # context is in prompt for now
    stream_result = data.get('stream_result', False)
    max_new_tokens = int(data.get('max_new_tokens', 20))
    temperature = float(data.get('temperature', 0.8))
    top_p = float(data.get('top_p', 0.9))
    top_k = int(data.get('top_k', 50))
    repeat_penalty= float(data.get('repeat_penalty', 1.2))
    frequency_penalty= float(data.get('frequency_penalty', 0.2))
    presence_penalty= float(data.get('presence_penalty', 0.2))

    try:
        prompt = get_errexplain_prompt(prompt)
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
        return Response(generate(stream_result, generate_kwargs))
    except Exception as ex:
        print('ERROR - Error Explaining')
        return Response(f"{json.dumps({'error': ex})}")
    
async def code_insertion(): 
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

    try:
        prompt = get_coinsert_prompt(msg_prefix=code_pfx, msg_surfix=code_sfx)
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
        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"]
        return  Response(f"{json.dumps({'generatedText': text, 'isGenerating': False})}")
    except Exception as ex:
        print('ERROR - Code Insertion', ex)
        return Response(f"{json.dumps({'error': ex})}")
    
async def code_completion(): 
    print('INFO - Code Completion')
    data = request.json
    # parse all params
    prompt = data.get('prompt', "") # the prompt provide the context
    context = data.get('context', "")
    stream_result = data.get('stream_result', False)
    max_new_tokens = int(data.get('max_new_tokens', 20))
    temperature = float(data.get('temperature', 0.8))
    top_p = float(data.get('top_p', 0.9))
    top_k = int(data.get('top_k', 50))
    repeat_penalty= float(data.get('repeat_penalty', 1.2))
    frequency_penalty= float(data.get('frequency_penalty', 0.2))
    presence_penalty= float(data.get('presence_penalty', 0.2))

    try:
        stopping_criteria = StoppingCriteriaList([StopOnTokensNL(model.tokenizer())])
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
        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"]
        return  Response(f"{json.dumps({'generatedText': text, 'isGenerating': False})}")
    except Exception as ex:
        print('ERROR - Code Completion', ex)
        return Response(f"{json.dumps({'error': ex})}")