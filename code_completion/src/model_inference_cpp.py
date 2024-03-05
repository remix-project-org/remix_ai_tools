from src.prompts import *
from src.llm_output_parser import StopOnTokens, StopOnTokensNL
from typing import Iterator
from llama_cpp import Llama, StoppingCriteriaList

use_deep_seek = False
model = Llama(
  #model_path="../deepseek-coder-1.3b-instruct.Q4_K_M.gguf", 
  model_path="../../deepseek-coder-6.7b-instruct.Q4_K_M.gguf" if use_deep_seek else "../../mistral-7b-instruct-v0.2-code-ft.Q4_K_M.gguf", 
  n_threads=16,           
  n_gpu_layers=-1,
  verbose=True
)


async def run_code_completion(
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
            #stopping_criteria=stopping_criteria
        )
        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return text
    except Exception as ex:
        print('ERROR - Code Completion', ex)
        return "Server error"



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
        )

        outputs = model(**generate_kwargs)
        text = outputs["choices"][0]["text"].strip()
        return text
    except Exception as ex:
        print('ERROR - Code generation', ex)
        return "Server error"