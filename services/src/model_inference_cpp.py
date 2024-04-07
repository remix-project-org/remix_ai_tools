from src import compile
from src.prompts import *
from src.llm_output_parser import get_string_between
from typing import Iterator
from llama_cpp import Llama, StoppingCriteriaList
from src.llm_output_parser import StopOnTokens
import os, threading
model = Llama(
  model_path=model_path, 
  n_threads=1,           
  n_gpu_layers=-1,
  verbose=False, 
  n_ctx=2048, 
)


def run_code_completion(
    context_code: str,
    comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 30) -> Iterator[str]:
    
    try:
        prompt = context_code #get_cocom_prompt(message=comment, context=context_code)
        stopping_criteria = StoppingCriteriaList([StopOnTokens(model.tokenizer())])
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stopping_criteria=stopping_criteria
        )
        #model.reset()
        print('INFO: os PID', os.getpid(), "   Thread:", threading.current_thread().ident)

        threading.Lock()
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
        prompt = get_cogen_prompt(gen_comment)
        stopping_criteria = StoppingCriteriaList([StopOnTokens(model.tokenizer())])
        
        print('INFO - Code Generation')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stopping_criteria=stopping_criteria
        )

        threading.Lock()
        outputs = model(**generate_kwargs, stop=["<|im_end|>"])
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
        print('INFO: os PID', os.getpid(), "   Thread:", threading.current_thread().ident)
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature
        )

        model.context_params.n_ctx = 4096
        threading.Lock()
        outputs = model(**generate_kwargs, stop=["<|im_end|>"])
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

        outputs = model(**generate_kwargs, stop=["<|im_end|>"])
        text = outputs["choices"][0]["text"].strip()
        return text
    except Exception as ex:
        print('ERROR - Error Explaining', ex)
        return "Server error"
    
def run_contract_generation(
    contract_description: str,
    stream_result: bool=False,
    max_new_tokens: int = 1024,
    temperature: float = 0.8,
    top_p: float = 0.9,
    top_k: int = 30,
    min_p: float = 0.05,
    ) -> Iterator[str]:

    try:
        prompt = get_contractgen_prompt(contract_description)
        
        print('INFO - Contract Generation')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            min_p=min_p,
            temperature=temperature,
        )

        threading.Lock()
        outputs = model(**generate_kwargs, stop=["<|im_end|>"])
        text = outputs["choices"][0]["text"].strip()
        text = get_string_between(text, "```", "```") if '```' in text else text
        if compile.run(generated_contract=text):
            print('INFO: Contract compiles!')
            return text
        else:
            print('Contract does not compile. New generation!')
            if temperature-0.2 <=0:
                raise ValueError("No safe contract generated") 
            new_text = run_contract_generation(contract_description=contract_description,
                                    stream_result=stream_result,
                                    max_new_tokens=max_new_tokens,
                                    temperature=0.1 if temperature-0.2 <=0 else temperature-0.2,
                                    top_k=top_k,
                                    top_p=top_p,
                                    min_p=min_p-0.01)
            return new_text
    except Exception as ex:
        print('ERROR - Contract Generation', ex)
        return ex

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

        threading.Lock()
        outputs = model(**generate_kwargs, stop=["<|im_end|>"])
        text = outputs["choices"][0]["text"].strip()
        return text
    except Exception as ex:
        print('ERROR - Question Answering', ex)
        return "Server error"