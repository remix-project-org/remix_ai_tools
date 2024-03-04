from src.prompts import *
from src.llm_output_parser import get_string_between
import torch
from threading import Thread
from typing import Iterator
from llama_cpp import Llama

model = Llama(
  model_path="../codellama-13b-instruct.Q4_K_M.gguf", 
  n_threads=16,           
  n_gpu_layers=-1,
  verbose=False
)


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
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stop=["}\n"]
        )
        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return text
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
        prompt = gen_comment #get_cogen_prompt(gen_comment)
        
        print('INFO - Code Generation')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stop=["}\n"]
        )

        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        text = get_string_between(text, "```", "```") if '```' in text else text
        return text
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
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature
        )

        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        text = get_string_between(text, "```", "```") if '```' in text else text
        return text
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
        
        print('INFO - Error Explaining')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
        )

        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return text
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
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
        )

        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        text = get_string_between(text, "```", "```") if '```' in text else text
        return text
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
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
        )

        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        text = get_string_between(text, "```", "```") if '```' in text else text
        return text
    except Exception as ex:
        print('ERROR - Question Answering', ex)
        return "Server error"