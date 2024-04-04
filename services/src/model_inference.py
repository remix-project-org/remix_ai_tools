from exceptiongroup import catch
from src.prompts import *
from src.llm_output_parser import get_string_between, stopping_criteria
from src.llm_output_parser import StopOnTokens
import torch, os
from threading import Thread
from typing import Iterator
from time import time
from transformers import BitsAndBytesConfig, AutoConfig, AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, StoppingCriteriaList
device = "cuda" if torch.cuda.is_available() else 'cpu'


bnb_config = BitsAndBytesConfig(
load_in_4bit=True,
bnb_4bit_use_double_quant=True,
bnb_4bit_quant_type="nf4",
bnb_4bit_compute_dtype=torch.bfloat16
)

m_times = []

if torch.cuda.is_available():
    config = AutoConfig.from_pretrained(hu_model)
    config.pretraining_tp = 1
    model = AutoModelForCausalLM.from_pretrained(
        hu_model,
        config=config,
        torch_dtype=torch.float16,
        quantization_config=bnb_config,
        device_map=device,
        use_safetensors=False,
    )
else:
    model = None

print('INFO: Model size is:', model.get_memory_footprint())
tokenizer = AutoTokenizer.from_pretrained(hu_model)


def run_code_completion(
    context_code: str,
    comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    
    try:
        prompt = context_code #get_cocom_prompt(message=comment, context=context_code)
        stop = StoppingCriteriaList([StopOnTokens(tokenizer)]) #stopping_criteria(tokenizer, device, completion=True)
        start = time()
        print('INFO - Code Completion')
        inputs = tokenizer([prompt], return_tensors='pt', add_special_tokens=False).to(device)

        streamer = TextIteratorStreamer(tokenizer,
                                        timeout=10.,
                                        skip_prompt=True,
                                        skip_special_tokens=True)
        generate_kwargs = dict(
            inputs,
            streamer=streamer if stream_result else None,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            num_beams=1,
            stopping_criteria=[stop],
            pad_token_id=tokenizer.eos_token_id,
        )

        if stream_result: 
            t = Thread(target=model.generate, kwargs=generate_kwargs)
            t.start()

            outputs = []
            for text in streamer:
                outputs.append(text)
                yield ''.join(outputs)
        else: 
            outputs = model.generate(**generate_kwargs)
            text = tokenizer.batch_decode(outputs[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)[0]
            text = get_string_between(text, "```", "```") if '```' in text else text
            end = time()
            m_times.append(end-start)
            print(str(os.getpid()) + " - Average Response time:", sum(m_times)/len(m_times))
    
            yield text
    except Exception as ex:
        print('ERROR - Code Completion', ex)
        return "Server error"



def run_code_generation(
    gen_comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:

    try:
        prompt = get_cogen_prompt(gen_comment)
        stop = StoppingCriteriaList([StopOnTokens(tokenizer)])#stopping_criteria(tokenizer, device, completion=False)
        
        print('INFO - Code Generation')
        inputs = tokenizer([prompt], return_tensors='pt', add_special_tokens=False).to(device)

        streamer = TextIteratorStreamer(tokenizer,
                                        timeout=10.,
                                        skip_prompt=True,
                                        skip_special_tokens=True)
        generate_kwargs = dict(
            inputs,
            streamer=streamer if stream_result else None,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            num_beams=1,
            pad_token_id=tokenizer.eos_token_id,
            stopping_criteria=[stop],
        )

        if stream_result: 
            t = Thread(target=model.generate, kwargs=generate_kwargs)
            t.start()

            outputs = []
            for text in streamer:
                outputs.append(text)
                yield ''.join(outputs)
        else: 
            outputs = model.generate(**generate_kwargs)
            text = tokenizer.batch_decode(outputs[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)[0]
            text = get_string_between(text, "```", "```") if '```' in text else text
            yield text
    except Exception as ex:
        print('ERROR - Code generation', ex)
        return "Server error"


def run_code_explaining(
    code: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:

    try:
        prompt = get_codexplain_prompt(code)
        
        print('INFO - Code Explaining')
        inputs = tokenizer([prompt], return_tensors='pt', add_special_tokens=False).to(device)

        streamer = TextIteratorStreamer(tokenizer,
                                        timeout=10.,
                                        skip_prompt=True,
                                        skip_special_tokens=True)
        generate_kwargs = dict(
            inputs,
            streamer=streamer if stream_result else None,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            num_beams=1,
            pad_token_id=tokenizer.eos_token_id,
        )

        if stream_result: 
            t = Thread(target=model.generate, kwargs=generate_kwargs)
            t.start()

            outputs = []
            for text in streamer:
                outputs.append(text)
                yield ''.join(outputs)
        else: 
            outputs = model.generate(**generate_kwargs)
            text = tokenizer.batch_decode(outputs[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)[0]
            text = get_string_between(text, "```", "```") if '```' in text else text
            yield text
    except Exception as ex:
        print('ERROR - Code explaining', ex)
        return "Server error"

def run_err_explaining(
    error_or_warning: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:

    try:
        prompt = get_errexplain_prompt(error_or_warning)
        
        print('INFO - Error Explaining:')
        inputs = tokenizer([prompt], return_tensors='pt', add_special_tokens=False).to(device)

        streamer = TextIteratorStreamer(tokenizer,
                                        timeout=10.,
                                        skip_prompt=True,
                                        skip_special_tokens=True)
        generate_kwargs = dict(
            inputs,
            streamer=streamer if stream_result else None,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            num_beams=1,
            pad_token_id=tokenizer.eos_token_id,
        )

        if stream_result: 
            t = Thread(target=model.generate, kwargs=generate_kwargs)
            t.start()

            outputs = []
            for text in streamer:
                outputs.append(text)
                yield ''.join(outputs)
        else: 
            outputs = model.generate(**generate_kwargs)
            text = tokenizer.batch_decode(outputs[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)[0]
            yield text
    except Exception as ex:
        print('ERROR - Error Explaining', ex)
        return "Server error"
    
def run_contract_generation(
    contract_description: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:

    try:
        prompt = get_contractgen_prompt(contract_description)
        
        print('INFO - Error Explaining')
        inputs = tokenizer([prompt], return_tensors='pt', add_special_tokens=False).to(device)
        stop = StoppingCriteriaList([StopOnTokens(tokenizer)])#stopping_criteria(tokenizer, device, completion=False)

        streamer = TextIteratorStreamer(tokenizer,
                                        timeout=10.,
                                        skip_prompt=True,
                                        skip_special_tokens=True)
        generate_kwargs = dict(
            inputs,
            streamer=streamer if stream_result else None,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            num_beams=1,
            stopping_criteria=[stop],
            pad_token_id=tokenizer.eos_token_id,
        )

        if stream_result: 
            t = Thread(target=model.generate, kwargs=generate_kwargs)
            t.start()

            outputs = []
            for text in streamer:
                outputs.append(text)
                yield ''.join(outputs)
        else: 
            outputs = model.generate(**generate_kwargs)
            text = tokenizer.batch_decode(outputs[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)[0]
            text = get_string_between(text, "```", "```") if '```' in text else text
            yield text
    except Exception as ex:
        print('ERROR - Contract Generation', ex)
        return "Server error"

def run_answering(
    prompt: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:

    try:
        prompt = get_answer_prompt(message=prompt) #get_cocom_prompt(message=comment, context=context_code)
        
        print('INFO - Solidity answering')
        inputs = tokenizer([prompt], return_tensors='pt', add_special_tokens=False).to(device)

        streamer = TextIteratorStreamer(tokenizer,
                                        timeout=10.,
                                        skip_prompt=True,
                                        skip_special_tokens=True)
        generate_kwargs = dict(
            inputs,
            streamer=streamer if stream_result else None,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            num_beams=1,
            pad_token_id=tokenizer.eos_token_id,
        )

        if stream_result: 
            t = Thread(target=model.generate, kwargs=generate_kwargs)
            t.start()

            outputs = []
            for text in streamer:
                outputs.append(text)
                yield ''.join(outputs)
        else: 
            outputs = model.generate(**generate_kwargs)
            text = tokenizer.batch_decode(outputs[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)[0]
            yield text
    except Exception as ex:
        print('ERROR - Question Answering', ex)
        return "Server error"