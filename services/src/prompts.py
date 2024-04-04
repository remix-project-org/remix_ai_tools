import os 
print('INFO: Using Model', os.getenv("MODEL", 'llama13b'))

SOLIDITY_VERSION_LATEST_SUPPORTED = "0.8.20"

GENERATION_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that generates code in this format ``` ```. You provide accurate solution and always answer as helpfully as possible, while being safe."
COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe."
EXPLAIN_SYSTEM_PROMPT = "You are Solidity AI Assistant that explain Solidity code. You provide accurate solution and always answer as helpfully as possible, while being safe"
ERROR_SYSTEM_PROMPT = "You are AI Assistant that explains solidity errors and warnings. You provide accurate error description and respective solution. Always answer as helpfully as possible, while being safe."
CONTRACT_SYSTEM_PROMPT = "You respond as Solidity AI Assistant that generates smart contracts contracts using the solidity version " + SOLIDITY_VERSION_LATEST_SUPPORTED + " or later. Avoid using the `import` statement. You provide accurate solution and always answer as helpfully as possible, while being safe."
ANSWERING_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that provides correct answers to user requests. You provide accurate solution and always answer as helpfully as possible, while being safe."


model_name = os.getenv("MODEL")
hu_model = None
if model_name == "llama13b":
    model_path = "../../codellama-13b-instruct.Q4_K_M.gguf"
    prompt_builder = lambda sys, msg: f'<s>[INST] <<SYS>>\n{sys}\n<</SYS>>\n\n{msg} [/INST]'
elif model_name == "deepseek":
    model_path = "../../deepseek-coder-6.7b-instruct.Q4_K_M.gguf"
    prompt_builder = lambda sys, msg: f'{sys}\n### INSTRUCTION:\n{msg}\n### RESPONSE:\n'
    hu_model = "deepseek-ai/deepseek-coder-1.3b-instruct"
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

def get_answer_prompt(message: str) -> str:
    message = message.split('sol-gpt')[-1]
    message = message.strip()
    return prompt_builder(ANSWERING_SYSTEM_PROMPT, message)

def get_codexplain_prompt(message: str) -> str:
    message = f'Explain the following Solidity code:\n ```{message.strip()}```'
    return prompt_builder(EXPLAIN_SYSTEM_PROMPT, message)


def get_errexplain_prompt(message: str) -> str:
    message = message.strip()
    message = f'Explain the following Solidity error message and how to resolve it:\n ```{message.strip()}```'
    return prompt_builder(ERROR_SYSTEM_PROMPT, message)

def get_contractgen_prompt(message: str) -> str:
    message = message.strip()
    message = f'Only write a smart contract respective code: {message.strip()}'
    return prompt_builder(CONTRACT_SYSTEM_PROMPT, message)
