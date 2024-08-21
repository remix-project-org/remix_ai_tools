import sys, os
from src.prompts import *
from src.llm_output_parser import StopOnTokens, StopOnTokensNL
from llama_cpp import Llama, StoppingCriteriaList
import threading
from flask import Flask, request, jsonify, Response
import json

app = Flask(__name__)

DEFAULT_CONTEXT_SIZE = 2048
isDesktopAlive = False

multitask_model = None
completion_model = None

completion_lock = threading.Lock()
general_lock = threading.Lock()


def watchdog():
    global isDesktopAlive
    print('INFO - Starting the server stopper thread.')
    while(1):
        time.sleep(40)
        if not isDesktopAlive:
            print('INFO - Stopping the server. No desktop client connected.')
            os._exit(0)
        else:
            isDesktopAlive = False



# kill daemon inference server releasing port
# dthr = threading.Thread(target=watchdog)
# dthr.start()

@app.route('/code_completion', methods=['POST'])
async def run_code_completion() -> str:
    data = request.json 

    context_code: str = data['context_code']
    stream_result = data.get('stream_result', False)
    max_new_tokens = int(data.get('max_new_tokens', 20))
    temperature = float(data.get('temperature', 0.8))
    top_p = float(data.get('top_p', 0.9))
    top_k = int(data.get('top_k', 50))
    repeat_penalty= float(data.get('repeat_penalty', 1.2))
    frequency_penalty= float(data.get('frequency_penalty', 0.2))
    presence_penalty= float(data.get('presence_penalty', 0.2))

    try:
        prompt = context_code 
        # prompt = get_cocom_prompt(message=context_code, is_model_deep_seek=use_deep_seek)
        stopping_criteria = StoppingCriteriaList([StopOnTokensNL(completion_model.tokenizer())])

        print('INFO - Code Completion')
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
        print('ERROR - Code Completion', ex)
        return jsonify({ "error":ex })

@app.route('/code_insertion', methods=['POST'])
async def run_code_instertionl() -> str:
    
    data = request.json
    code_pfx = data['code_pfx']
    code_sfx = data['code_sfx']
    max_new_tokens = int(data.get('max_new_tokens', 100))
    temperature = float(data.get('temperature', 0.4))
    top_p = float(data.get('top_p', 0.9))
    top_k = int(data.get('top_k', 50))
    repeat_penalty= float(data.get('repeat_penalty', 1.2))
    frequency_penalty= float(data.get('frequency_penalty', 0.2))
    presence_penalty= float(data.get('presence_penalty', 0.2))

    try:
        prompt = get_coinsert_prompt(msg_prefix=code_pfx, msg_surfix=code_sfx)

        # No stopping criteria as the in filling pushes in what is good
        # TODO: only allow 1 artifact generation: example 1 function, 1 contract, 1 struct, 1 interface, 1 for loop or similar. single {}
        # stopping_criteria = StoppingCriteriaList([StopOnTokensNL(completion_model.tokenizer())])

        print('INFO - Code Insertion')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            # repeat_penalty=repeat_penalty,
            # frequency_penalty=frequency_penalty,
            # presence_penalty=presence_penalty,
            # stopping_criteria=stopping_criteria
        )

        with completion_lock:
            outputs = completion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return jsonify({ "generatedText":text })
    except Exception as ex:
        print('ERROR - Code Insertion', ex)
        return jsonify({ "error":ex })

@app.route('/code_generation', methods=['POST'])
async def run_code_generation(
    gen_comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> str:

    try:
        prompt = get_cogen_prompt(gen_comment, is_model_deep_seek=use_deep_seek)
        stopping_criteria = StoppingCriteriaList([StopOnTokens(multitask_model.tokenizer())])
        
        print('INFO - Code Generation')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stopping_criteria=stopping_criteria
        )

        with completion_lock:
            outputs = multitask_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        text = text.replace("```solidity \n", "").replace("```", "")
        return jsonify({ "generatedText":text })
    except Exception as ex:
        print('ERROR - Code generation', ex)
        return jsonify({ "error":ex })

@app.route('/state', methods=['GET'])
async def state():
    global isDesktopAlive
    isDesktopAlive = True
    return jsonify({ "status":"running",
                     "completion": True if completion_model!=None else False,
                     "general": True if multitask_model!=None else False})
                   
@app.route('/init_completion', methods=['POST'])
async def init_insertion():
    global completion_model
    try:
        data = request.json
        model_path = data['model_path']
        completion_model = Llama(
            model_path=model_path, 
            n_threads=16,           
            n_gpu_layers=-1,
            n_ctx=DEFAULT_CONTEXT_SIZE*15,
            verbose=False
        )
        return jsonify({ "status":"success" })
    except Exception as ex:
        return jsonify({ "error":'Error while initializing the insertion model' })

@app.route('/init', methods=['POST'])
async def init_general():
    global multitask_model
    try:
        data = request.json
        model_path = data['model_path']
        multitask_model = Llama(
            model_path=model_path, 
            n_threads=16,           
            n_gpu_layers=-1,
            n_ctx=DEFAULT_CONTEXT_SIZE*5,
            verbose=False
        )
        return jsonify({ "status":"success" })
    except Exception as ex:
        return jsonify({ "error":'Error while initializing the general model' })

@app.route('/code_explaining', methods=['POST'])
def code_explaining():
    data = request.json 
    code: str = data['code']
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
        prompt = get_codexplain_prompt(code, context)

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
        def generate():
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
        return Response(generate(),  mimetype='text/event-stream')
    
    except Exception as ex:
        print('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'error': ex})}")
    
@app.route('/error_explaining', methods=['POST'])
async def error_explaining () -> str:
    data = request.json 
    prompt: str = data['prompt']
    stream_result = data.get('stream_result', False)
    max_new_tokens = int(data.get('max_new_tokens', 2000))
    temperature = float(data.get('temperature', 0.8))
    top_p = float(data.get('top_p', 0.9))
    top_k = int(data.get('top_k', 50))
    # repeat_penalty= float(data.get('repeat_penalty', 1.2))
    # frequency_penalty= float(data.get('frequency_penalty', 0.2))
    # presence_penalty= float(data.get('presence_penalty', 0.2))

    try:
        prompt = get_errexplain_prompt(prompt) 

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

        def generate():
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
        return Response(generate(),  mimetype='text/event-stream')
    
    except Exception as ex:
        print('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'error': ex})}")
    
@app.route('/solidity_answer', methods=['POST'])
async def run_answering () -> str:
    data = request.json 
    prompt: str = data['prompt']
    stream_result = data.get('stream_result', False)
    max_new_tokens = int(data.get('max_new_tokens', 2000))
    temperature = float(data.get('temperature', 0.8))
    top_p = float(data.get('top_p', 0.9))
    top_k = int(data.get('top_k', 50))
    repeat_penalty= float(data.get('repeat_penalty', 1.2))
    frequency_penalty= float(data.get('frequency_penalty', 0.2))
    presence_penalty= float(data.get('presence_penalty', 0.2))

    try:
        prompt = get_answer_prompt(prompt) 

        print('INFO - Answering')
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

        def generate():
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
        return Response(generate(),  mimetype='text/event-stream')
    
    except Exception as ex:
        print('ERROR - Code Explaining', ex)
        return Response(f"{json.dumps({'error': ex})}")  


if __name__ == '__main__':
    isDesktopAlive = True
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5501
    app.run(host='0.0.0.0', port=port, processes=1, threaded=True)

# TODO: Handle the context exeeding the model size
# TODO: handle harware generation speed in n-tokens/sec
# TODO: use reset to stop generation
# TODO: implement stop generation on user request