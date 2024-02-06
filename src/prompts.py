GENERATION_SYSTEM_PROMPT = "You only respond as Solidity AI Assistant that generates code in this format ``` ```. You provide accurate solution and always answer as helpfully as possible, while being safe."
COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe."
EXPLAIN_SYSTEM_PROMPT = "You are Solidity AI Assistant that explain Solidity code. You explain code using a JSON format. You provide accurate solution and always answer as helpfully as possible, while being safe"
ERROR_SYSTEM_PROMPT = "You are AI Assistant that explains solidity errors and warnings. You provide accurate error description and respective solution. Always answer as helpfully as possible, while being safe."
CONTRACT_SYSTEM_PROMPT = "You respond as Solidity AI Assistant that generates smart contracts contracts. You provide accurate solution and always answer as helpfully as possible, while being safe."

def get_cocom_prompt(message: str, context: str) -> str:
    texts = [f'<s>[INST] <<SYS>>\n{COMPLETION_SYSTEM_PROMPT}\n<</SYS>>\n\n']
    if len(context):
        texts.append(f'Using this Solidity code context ```\n{context}\n``` ')
    message = message.strip()
    texts.append(f'{message} [/INST]')
    return ''.join(texts)

def get_cogen_prompt(message: str) -> str:
    texts = [f'<s>[INST] <<SYS>>\n{GENERATION_SYSTEM_PROMPT}\n<</SYS>>\n\n']
    message = message.strip()
    texts.append(f'{message} [/INST]')
    return ''.join(texts)


def get_codexplain_prompt(message: str) -> str:
    texts = [f'<s>[INST] <<SYS>>\n{EXPLAIN_SYSTEM_PROMPT}\n<</SYS>>\n\n']
    
    message = message.strip()
    texts.append(f'Explain the following Solidity code:\n ```{message}``` [/INST]')
    return ''.join(texts)


def get_errexplain_prompt(message: str) -> str:
    texts = [f'<s>[INST] <<SYS>>\n{ERROR_SYSTEM_PROMPT}\n<</SYS>>\n\n']
    
    message = message.strip()
    texts.append(f'Explain the following Solidity error message and how to resolve it:\n ```{message}``` [/INST]')
    return ''.join(texts)

def get_contractgen_prompt(message: str) -> str:
    texts = [f'<s>[INST] <<SYS>>\n{CONTRACT_SYSTEM_PROMPT}\n<</SYS>>\n\n']
    message = message.strip()
    texts.append(f'Only write a smart contract respective code: {message} [/INST]')
    return ''.join(texts)
