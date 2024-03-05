COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe. You only provide code ### Instruction:"

def get_cocom_prompt(message: str, context: str, is_model_deep_seek: bool) -> str:
    return get_cogen_prompt(message, is_model_deep_seek)

def get_cogen_prompt(message: str, is_model_deep_seek: bool) -> str:
    text = f"{COMPLETION_SYSTEM_PROMPT}\n{message}\n ### Response: "
    return text