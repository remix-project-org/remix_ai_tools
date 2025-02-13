from src import compile
from src.prompts import *
from src.llm_output_parser import get_string_between
from typing import Iterator
from llama_cpp import Llama, StoppingCriteriaList
from src.llm_output_parser import StopOnTokens
import threading, json

model = Llama(
  model_path=model_path, 
  n_threads=1,           
  n_gpu_layers=-1,
  verbose=False, 
  n_ctx=3500*3, 
)

lock = threading.Lock()

async def run_code_completion(
    context_code: str,
    comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 30):
    
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
        print('INFO - Code Completion')

        with lock:
            outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return text
    except Exception as ex:
        print('ERROR - Code Completion', ex)
        return "Context data is too long. Try it with less code context!"

async def run_code_generation(
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

        with lock:
            outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        # text = get_string_between(text, "```", "```") if '```' in text else text
        return text
    except Exception as ex:
        print('ERROR - Code generation', ex)
        return "Context data is too long. Try it with less code context!"

async def run_code_explaining(
    code: str,
    stream_result: bool = True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50,
    context: str = ""
    ) -> Iterator[str]:

    try:
        prompt = get_codexplain_prompt(code, context=context)
        
        print('INFO - Code Explaining')
        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature
        )

        with lock:
            outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return text
    except Exception as ex:
        print('ERROR - Code explaining', ex)
        return "Context data is too long. Try it with less code context!"

async def run_err_explaining(
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
        return "Context data is too long. Try it with less code context!"
    
async def run_contract_generation(
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

        with lock:
            outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        text = get_string_between(text, "```", "```") if '```' in text else text

        if model_name == "deepseek": 
            text = '\n'.join(text.splitlines()[1:]) # remove generated solidity prefix

        if compile.run(generated_contract=text):
            return text
        else:
            print('Contract does not compile. New generation!')
            if temperature-0.2 <=0:
                raise ValueError("No safe contract generated") 
            text = run_contract_generation(contract_description=contract_description,
                                    stream_result=stream_result,
                                    max_new_tokens=max_new_tokens,
                                    temperature=0.1 if temperature-0.2 <=0 else temperature-0.2,
                                    top_k=top_k,
                                    top_p=top_p,
                                    min_p=min_p-0.01)
            return text
    except Exception as ex:
        print('Generated contract\n', text)
        print('ERROR - Contract Generation', ex)
        return ex

async def run_answering(
    prompt: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> str:

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
        with lock:
            outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()

        # if links is not None:
        #     text += add_read_more(links)
            
        return text
    except Exception as ex:
        print('ERROR - Question Answering', ex)
        return "Context data is too long. Try it with less code context!"