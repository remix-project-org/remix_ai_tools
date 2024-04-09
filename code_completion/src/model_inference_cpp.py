from src.prompts import *
from src.llm_output_parser import StopOnTokens, StopOnTokensNL
from typing import Iterator
from llama_cpp import Llama, StoppingCriteriaList
import threading

use_deep_seek = True
completion_model = Llama(
  model_path=completion_model_path, 
  #model_path="../../deepseek-coder-6.7b-instruct.Q4_K_M.gguf" if use_deep_seek else "../../mistral-7b-instruct-v0.2-code-ft.Q4_K_M.gguf", 
  n_threads=16,           
  n_gpu_layers=-1,
  n_ctx=2048,
  verbose=False
)

insertion_model = Llama(
  model_path=insertsion_model_path, 
  n_threads=16,           
  n_gpu_layers=-1,
  n_ctx=4096,
  verbose=False
)

lock = threading.Lock()


async def run_code_completion(
    context_code: str,
    comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    
    try:
        prompt = context_code 
        # prompt = get_cocom_prompt(message=comment, is_model_deep_seek=use_deep_seek)
        stopping_criteria = StoppingCriteriaList([StopOnTokensNL(completion_model.tokenizer())])

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            stopping_criteria=stopping_criteria
        )

        with lock:
            outputs = completion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return text
    except Exception as ex:
        print('ERROR - Code Completion', ex)
        return "Server error"


async def run_code_insertion(
    code_pfx: str,
    code_sfx: str,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:
    
    try:
        prompt = get_coinsert_prompt(msg_prefix=code_pfx, msg_surfix=code_sfx)

        # No stopping criteria as the in filling pushes in what is good
        # TODO: only allow 1 artifact generation: example 1 function, 1 contract, 1 struct, 1 interface, 1 for loop or similar. single {}
        # stopping_criteria = StoppingCriteriaList([StopOnTokensNL(insertion_model.tokenizer())])

        generate_kwargs = dict(
            prompt=prompt,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            #stopping_criteria=stopping_criteria
        )

        with lock:
            outputs = insertion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return text
    except Exception as ex:
        print('ERROR - Code Insertion', ex)
        return "Server error"


async def run_code_generation(
    gen_comment: str,
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50) -> Iterator[str]:

    try:
        prompt = get_cogen_prompt(gen_comment, is_model_deep_seek=use_deep_seek)
        stopping_criteria = StoppingCriteriaList([StopOnTokens(completion_model.tokenizer())])
        
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
            outputs = completion_model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        text = text.replace("```solidity \n", "").replace("```", "")
        return text
    except Exception as ex:
        print('ERROR - Code generation', ex)
        return "Server error"