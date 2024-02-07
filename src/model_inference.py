from src.prompts import *
from src.llm_output_parser import get_string_between, stopping_criteria
import torch
from threading import Thread
from typing import Iterator
from transformers import BitsAndBytesConfig, AutoConfig, AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, StoppingCriteriaList
device = "cuda:0" if torch.cuda.is_available() else 'cpu'

model_id = 'codellama/CodeLlama-13b-Instruct-hf'
bnb_config = BitsAndBytesConfig(
load_in_4bit=True,
bnb_4bit_use_double_quant=True,
bnb_4bit_quant_type="nf4",
bnb_4bit_compute_dtype=torch.bfloat16
)

if torch.cuda.is_available():
    config = AutoConfig.from_pretrained(model_id)
    config.pretraining_tp = 1
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        config=config,
        torch_dtype=torch.float16,
        quantization_config=bnb_config,
        device_map=device,
        use_safetensors=False,
    )
else:
    model = None

print('INFO: Model size is:', model.get_memory_footprint())
tokenizer = AutoTokenizer.from_pretrained(model_id)


def run_code_completion(
    context_code: str,
    comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    prompt = context_code #get_cocom_prompt(message=comment, context=context_code)
    stop = stopping_criteria(tokenizer, device, completion=True)
    
    print('INFO - Code Completion: model input:', prompt)
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
        yield text


def run_code_generation(
    gen_comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    prompt = get_cogen_prompt(gen_comment)
    stop = stopping_criteria(tokenizer, device, completion=False)
    
    print('INFO - Code Generation: model input:', prompt)
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


def run_code_explaining(
    code: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    prompt = get_codexplain_prompt(code)
    
    print('INFO - Code Explaining: model input:', prompt)
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

def run_err_explaining(
    error_or_warning: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    prompt = get_errexplain_prompt(error_or_warning)
    
    print('INFO - Error Explaining: model input:', prompt)
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
    
def run_contract_generation(
    contract_description: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    prompt = get_contractgen_prompt(contract_description)
    
    print('INFO - Error Explaining: model input:', prompt)
    inputs = tokenizer([prompt], return_tensors='pt', add_special_tokens=False).to(device)
    stop = stopping_criteria(tokenizer, device, completion=False)

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

def run_answering(
    prompt: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    prompt = get_answer_prompt(message=prompt) #get_cocom_prompt(message=comment, context=context_code)
    
    print('INFO - Solidit answering: model input:', prompt)
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