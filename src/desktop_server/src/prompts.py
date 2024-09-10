import time
from enum import Enum

COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe. You only provide code using this context:\n"
GENERATION_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that generates code in this format ``` ```. You provide accurate solution and always answer as helpfully as possible, while being safe."
COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe."
EXPLAIN_SYSTEM_PROMPT = "You are Solidity AI Assistant that explain Solidity code. You provide accurate solution and always answer as helpfully as possible, while being safe. Summarize the answer to be short and accurate. Ignore any provided comments and do not describe them"
ERROR_SYSTEM_PROMPT = "You are AI Assistant that explains solidity errors and warnings. You provide accurate error description and respective solution. Always answer as helpfully as possible, while being safe."
# CONTRACT_SYSTEM_PROMPT = "You respond as Solidity AI Assistant that generates smart contracts contracts using the solidity pragma versions greater or equal " + SOLIDITY_VERSION_LATEST_SUPPORTED + ". Include the SPDX license identifier. You make use of import statements for libraries, provide accurate and safe solutions and always answer as helpfully as possible, while being safe."
ANSWERING_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that provides correct answers to user requests. You provide accurate solution and always answer as helpfully as possible, while being safe."

class SupportedModel (Enum):
    llama3_1 = "llama3_1"
    deepseek = "deepseek"
    mistral = "mistral"
    stability = "stability"
    any = "any"

def determine_model(model_path):
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



def get_coinsert_prompt(msg_prefix, msg_surfix, modelName: SupportedModel) -> str:
    return apply_insertsion_template(COMPLETION_SYSTEM_PROMPT, msg_prefix, msg_surfix, modelName)

def get_cocom_prompt(message: str, context: str, modelName: SupportedModel) -> str:
    msg = ""
    if len(context):
        msg = f'Using this Solidity code context ```\n{context}\n``` \n'
    message = message.strip()
    msg += message
    return apply_generation_template(COMPLETION_SYSTEM_PROMPT, msg, modelName)

def get_cogen_prompt(message: str, modelName: SupportedModel) -> str:
    message = message.strip()
    return apply_generation_template(GENERATION_SYSTEM_PROMPT, message, modelName)

def get_answer_prompt(message: str, modelName: SupportedModel) -> str:
    message = message.split('sol-gpt')[-1]
    if ( message.count('start_header_id')>0 or message.count('INSTRUCTION')>0 ):
        return apply_chat_generation_template(ANSWERING_SYSTEM_PROMPT, message, modelName)
    else:   
        return apply_generation_template(ANSWERING_SYSTEM_PROMPT, message, modelName)

def get_codexplain_prompt(message: str, modelName: SupportedModel, context="") -> str:
    if context != "":
        message = f'Using this context ```{context} ```, explain the following Solidity code:\n ```{message.strip()}```'
    else:
        message = f'Explain the following code:\n ```{message.strip()}```'
    return apply_generation_template(EXPLAIN_SYSTEM_PROMPT, message, modelName)

def get_errexplain_prompt(message: str, modelName: SupportedModel) -> str:
    message = message.strip()
    message = f'Explain the following error message and how to resolve it:\n ```{message.strip()}```'
    return apply_generation_template(ERROR_SYSTEM_PROMPT, message, modelName)
