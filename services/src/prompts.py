import os, time
from rag.utils.utils import VectorDBRetriever, elastic_vector_store, soldoc_db_name, is_rag_initialized
from rag.elastic_search import get_relevant_solidity_topics

use_rag = is_rag_initialized(soldoc_db_name)
use_elastic = False # overriddes userag

if use_rag:
    print('INFO: RAG database initialized!')
else:
    print('Warning: RAG database NOT initialized!')

print('INFO: Using Model', os.getenv("MODEL", 'llama13b'))

SOLIDITY_VERSION_LATEST_SUPPORTED = "0.8.20"

GENERATION_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that generates code in this format ``` ```. You provide accurate solution and always answer as helpfully as possible, while being safe."
COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe."
EXPLAIN_SYSTEM_PROMPT = "You are Solidity AI Assistant that explain Solidity code. You provide accurate solution and always answer as helpfully as possible, while being safe. Summarize the answer to be short and accurate. Ignore any provided comments and do not describe them"
ERROR_SYSTEM_PROMPT = "You are AI Assistant that explains solidity errors and warnings. You provide accurate error description and respective solution. Always answer as helpfully as possible, while being safe."
CONTRACT_SYSTEM_PROMPT = "You respond as Solidity AI Assistant that generates smart contracts contracts using the solidity pragma versions greater or equal " + SOLIDITY_VERSION_LATEST_SUPPORTED + ". Include the SPDX license identifier. You make use of import statements for libraries, provide accurate and safe solutions and always answer as helpfully as possible, while being safe."
ANSWERING_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that provides correct answers to user requests. You provide accurate solution and always answer as helpfully as possible, while being safe."


model_name = os.getenv("MODEL", "llama13b")
hu_model = None
if model_name == "llama13b":
    model_path = "../../codellama-13b-instruct.Q4_K_M.gguf"
    prompt_builder = lambda sys, msg: f'<s>[INST] <<SYS>>\n{sys}\n<</SYS>>\n\n{msg} [/INST]'
elif model_name == "deepseek":
    model_path = "../../deepseek-coder-6.7b-instruct.Q4_K_M.gguf"
    prompt_builder = lambda sys, msg: f'{sys}\n### INSTRUCTION:\n{msg}\n### RESPONSE:\n'
    hu_model = "deepseek-ai/deepseek-coder-6.7b-instruct"
elif model_name == "mistral":
    model_path = "../../mistral-7b-instruct-v0.2-code-ft.Q4_K_M.gguf"
    prompt_builder = lambda sys, msg: f'<|im_start|>system\n{sys}<|im_end|>\n<|im_start|>user\n{msg}<|im_end|>\n<|im_start|>assistant"'
elif model_name == "stability":
    model_path = "../../stable-code-3b-q5_k_m.gguf"
    prompt_builder = lambda sys, msg: f'<|im_start|>system\n{sys}<|im_end|>\n<|im_start|>user\n{msg}<|im_end|>\n<|im_start|>assistant"'
    hu_model = "stabilityai/stable-code-instruct-3b"
else:
    raise ValueError('Wrong model specified. The given model is not supported yet')


def get_cocom_prompt(message: str, context: str) -> str:
    msg = ""
    if len(context):
        msg = f'Using this Solidity code context ```\n{context}\n``` \n'
    message = message.strip()
    msg += message
    return prompt_builder(COMPLETION_SYSTEM_PROMPT, msg)

def get_cogen_prompt(message: str) -> str:
    message = message.strip()
    return prompt_builder(GENERATION_SYSTEM_PROMPT, message)

def get_answer_prompt(message: str):
    message = message.split('sol-gpt')[-1]
    rag_prompt, links = get_RAG_results(user_prompt=message)
    sys_prompt = ANSWERING_SYSTEM_PROMPT + "\n Use the following context to answer the user request:\n" + rag_prompt
    message = message.strip()
    return prompt_builder(sys_prompt, message), links

def get_codexplain_prompt(message: str, context="") -> str:
    if context != "":
        message = f'Using this context ```{context} ```, explain the following Solidity code:\n ```{message.strip()}```'
        print('INFO: Got explaining context')
    else:
        message = f'Explain the following Solidity code:\n ```{message.strip()}```'
    return prompt_builder(EXPLAIN_SYSTEM_PROMPT, message)

def get_errexplain_prompt(message: str) -> str:
    message = message.strip()
    message = f'Explain the following Solidity error message and how to resolve it:\n ```{message.strip()}```'
    return prompt_builder(ERROR_SYSTEM_PROMPT, message)

def get_contractgen_prompt(message: str) -> str:
    message = message.strip()
    message = f'Only provide a smart contract respective code: {message.strip()}'
    return prompt_builder(CONTRACT_SYSTEM_PROMPT, message)

def get_RAG_results(user_prompt):
    try:
        start = time.time()
        if use_elastic:
            result = get_relevant_solidity_topics(user_prompt=user_prompt, k=2)
            rag_prompt = ""
            urls = []
            for url, content in result:
                rag_prompt += content[:4000] + "\n" 
                urls.append(url)

            print('INFO: Elastic RAG retrieval took', time.time() - start, "seconds")
            return[rag_prompt, urls]
        elif use_rag:
            retriever = VectorDBRetriever(elastic_vector_store, query_mode="default", similarity_top_k=2)
            results = retriever.retrieve(user_prompt)

            rag_prompt = ""
            urls = []
            for idx in range(len(results)):
                rag_prompt += results[idx].node.get_content()[:4000] + "\n" 
                urls.append([results[idx].node.metadata['url'], results[idx].node.metadata['title']])
                print('INFO: retrieved result with score', results[idx].score)
            
            print('INFO: Local RAG retrieval took', time.time() - start, "seconds")
            return[rag_prompt, urls]
        else:
            print('INFO: RAG retrieval took', time.time() - start, "seconds")
            return ["", None]
    except Exception as ex:
        print('INFO: RAG retrieval took', time.time() - start, "seconds")
        print(ex)
        return ["", None]
    
def add_read_more(urls:list):
    complete_str = "\nClick on following links for more information:\n\t"
    for url, title in urls:
        complete_str += f"-  [{title}]({url}) \n\t"
    return complete_str
    