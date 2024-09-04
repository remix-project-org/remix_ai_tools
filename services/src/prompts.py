import os, time
from enum import Enum

# from rag.utils.utils import VectorDBRetriever, elastic_vector_store, soldoc_db_name, is_rag_initialized
# from rag.elastic_search import get_relevant_solidity_topics

# use_rag = is_rag_initialized(soldoc_db_name)
# use_elastic = False # overriddes userag

# if use_rag:
#     print('INFO: RAG database initialized!')
# else:
#     print('Warning: RAG database NOT initialized!')

print('INFO: Using Model', os.getenv("MODEL", 'llama3_1'))

SOLIDITY_VERSION_LATEST_SUPPORTED = "0.8.20"

GENERATION_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that generates code. You only provide implementation code with no headers. You provide accurate solution and always answer as helpfully as possible, while being safe."
COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe."
EXPLAIN_SYSTEM_PROMPT = "You are Solidity AI Assistant that explain Solidity code in a brief manner. You provide accurate solution and always answer as helpfully as possible, while being safe. Summarize the answer to be short and accurate. Ignore any provided comments and do not describe them"
ERROR_SYSTEM_PROMPT = "You are AI Assistant that explains solidity errors and warnings in a brief manner. You provide accurate error description and respective solution. Always answer as helpfully as possible, while being safe."
CONTRACT_SYSTEM_PROMPT = "You respond as Solidity AI Assistant that generates smart contracts contracts using the solidity pragma versions greater or equal " + SOLIDITY_VERSION_LATEST_SUPPORTED + ". You only provide implementation code with no headers, Include the SPDX license identifier. You make use of import statements for libraries, provide accurate and safe solutions and always answer as helpfully as possible, while being safe."
ANSWERING_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that provides correct answers to user requests in a brief manner. You only provide implementation code with no headers. You provide accurate solution and always answer as helpfully as possible, while being safe."


model_name = os.getenv("MODEL", "llama3_1")
hu_model = None
if model_name == "llama3_1":
    model_path = "../../llama3_1_8B-q4_0_instruct.gguf"
elif model_name == "deepseek":
    model_path = "../../deepseek-coder-6.7b-instruct.Q4_K_M.gguf"
elif model_name == "mistral":
    model_path = "../../mistral-7b-instruct-v0.2-code-ft.Q4_K_M.gguf"
elif model_name == "stability":
    model_path = "../../stable-code-3b-q5_k_m.gguf"
else:
    raise ValueError('Wrong model specified. The given model is not supported yet')


class SupportedModel (Enum):
    llama3_1 = "llama3_1"
    deepseek = "deepseek"
    mistral = "mistral"
    stability = "stability"
    any = "any"

def determine_model():
    if "llama3_1" in model_path:
        return SupportedModel.llama3_1
    elif "deepseek" in model_path:
        return SupportedModel.deepseek
    elif "mistral" in model_path:
        return SupportedModel.mistral
    elif "stability" in model_path:
        return SupportedModel.stability
    else:
        return SupportedModel.any
    

def apply_generation_template(sys, msg, model: SupportedModel):
    if model== SupportedModel.llama3_1:
        return f'''<|start_header_id|>system<|end_header_id|>
        {sys}.<|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        {msg}<|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>'''
    elif model == SupportedModel.deepseek:
        return f'{sys}\n### INSTRUCTION:\n{msg}\n### RESPONSE:\n'
    elif model == SupportedModel.mistral:
        return f'<|im_start|>system\n{sys}<|im_end|>\n<|im_start|>user\n{msg}<|im_end|>\n<|im_start|>assistant"'
    elif model == SupportedModel.stability:
        return f'<|im_start|>system\n{sys}<|im_end|>\n<|im_start|>user\n{msg}<|im_end|>\n<|im_start|>assistant"'
    else:
        raise ValueError('Wrong model specified. The given model is not supported yet')

def apply_chat_generation_template(sys, msg, model: SupportedModel):
    # the frontend app is using the correct prompt special tokens for building the chat
    if model== SupportedModel.llama3_1:
        return f'''<|start_header_id|>system<|end_header_id|>
        {sys}.<|eot_id|>
        {msg} 
        '''
    elif model == SupportedModel.deepseek:
        return f'{sys}{msg}'
    elif model == SupportedModel.mistral:
        return f'<|im_start|>system\n{sys}<|im_end|>\n<|im_start|>user\n{msg}<|im_end|>\n<|im_start|>assistant"'
    elif model == SupportedModel.stability:
        return f'<|im_start|>system\n{sys}<|im_end|>\n<|im_start|>user\n{msg}<|im_end|>\n<|im_start|>assistant"'
    else:
        raise ValueError('Wrong model specified. The given model is not supported yet')


def apply_insertsion_template(sys, msg_prefix, msg_surfix, model: SupportedModel):
    if model== SupportedModel.llama3_1:
        return f'''<|start_header_id|>system<|end_header_id|>
        {sys}.<|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        {msg_prefix}<|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        <|start_header_id|>user<|end_header_id|>
        {msg_surfix}<|eot_id|>'''
    elif model == SupportedModel.deepseek:
        return "<｜fim▁begin｜>" + msg_prefix + "<｜fim▁hole｜>" + msg_surfix + " <｜fim▁end｜>"
    else:
        return "<｜fim▁begin｜>" + msg_prefix + "<｜fim▁hole｜>" + msg_surfix + " <｜fim▁end｜>"



def get_coinsert_prompt(msg_prefix, msg_surfix, modelName: SupportedModel=determine_model()) -> str:
    return apply_insertsion_template(COMPLETION_SYSTEM_PROMPT, msg_prefix, msg_surfix, modelName)

def get_cocom_prompt(message: str, context: str, modelName: SupportedModel) -> str:
    msg = ""
    if len(context):
        msg = f'Using this Solidity code context ```\n{context}\n``` \n'
    message = message.strip()
    msg += message
    return apply_generation_template(COMPLETION_SYSTEM_PROMPT, msg, modelName)

def get_cogen_prompt(message: str, modelName: SupportedModel=determine_model()) -> str:
    message = message.strip()
    return apply_generation_template(GENERATION_SYSTEM_PROMPT, message, modelName)

def get_answer_prompt(message: str, modelName: SupportedModel=determine_model()) -> str:
    message = message.split('sol-gpt')[-1]
    if ( message.count('start_header_id')>0 or message.count('INSTRUCTION')>0 ):
        return apply_chat_generation_template(ANSWERING_SYSTEM_PROMPT, message, modelName)
    else:   
        return apply_generation_template(ANSWERING_SYSTEM_PROMPT, message, modelName)

def get_codexplain_prompt(message: str, modelName: SupportedModel=determine_model(), context="") -> str:
    if context != "":
        message = f'Using this context ```{context} ```, explain the following Solidity code:\n ```{message.strip()}```'
    else:
        message = f'Explain the following code:\n ```{message.strip()}```'
    return apply_generation_template(EXPLAIN_SYSTEM_PROMPT, message, modelName)

def get_errexplain_prompt(message: str, modelName: SupportedModel=determine_model()) -> str:
    message = message.strip()
    message = f'Explain the following error message and how to resolve it:\n ```{message.strip()}```'
    return apply_generation_template(ERROR_SYSTEM_PROMPT, message, modelName)


def get_contractgen_prompt(message: str) -> str:
    message = message.strip()
    message = f'Only provide a smart contract respective code: {message.strip()}'
    return apply_generation_template(CONTRACT_SYSTEM_PROMPT, message, determine_model())

# def get_RAG_results(user_prompt):
#     try:
#         start = time.time()
#         if use_elastic:
#             result = get_relevant_solidity_topics(user_prompt=user_prompt, k=2)
#             rag_prompt = ""
#             urls = []
#             for url, content in result:
#                 rag_prompt += content[:4000] + "\n" 
#                 urls.append(url)

#             print('INFO: Elastic RAG retrieval took', time.time() - start, "seconds")
#             return[rag_prompt, urls]
#         elif use_rag:
#             retriever = VectorDBRetriever(elastic_vector_store, query_mode="default", similarity_top_k=2)
#             results = retriever.retrieve(user_prompt)

#             rag_prompt = ""
#             urls = []
#             for idx in range(len(results)):
#                 rag_prompt += results[idx].node.get_content()[:4000] + "\n" 
#                 urls.append([results[idx].node.metadata['url'], results[idx].node.metadata['title']])
#                 print('INFO: retrieved result with score', results[idx].score)
            
#             print('INFO: Local RAG retrieval took', time.time() - start, "seconds")
#             return[rag_prompt, urls]
#         else:
#             print('INFO: RAG retrieval took', time.time() - start, "seconds")
#             return ["", None]
#     except Exception as ex:
#         print('INFO: RAG retrieval took', time.time() - start, "seconds")
#         print(ex)
#         return ["", None]
    
# def add_read_more(urls:list):
#     complete_str = "\nClick on following links for more information:\n\t"
#     for url, title in urls:
#         complete_str += f"-  [{title}]({url}) \n\t"
#     return complete_str
    