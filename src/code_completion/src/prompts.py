COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe. You only provide code using this context:\n"

completion_model_path = "../../models/Qwen2.5-Coder-7B.Q4_K_M.gguf"
insertsion_model_path = "../../models/Qwen2.5-Coder-7B.Q4_K_M.gguf"

def get_cocom_prompt(message: str, is_model_deep_seek: bool) -> str:
    return get_cogen_prompt(message, is_model_deep_seek)

def get_cogen_prompt(message: str, is_model_deep_seek: bool) -> str:
    rag_prompt = ""# get_RAG_results(user_prompt=message)
    text = f"{COMPLETION_SYSTEM_PROMPT} {rag_prompt}\n### Instruction:\n{message}\n ### Response: " if is_model_deep_seek \
            else f"<|im_start|>system{COMPLETION_SYSTEM_PROMPT}<|im_end|><|im_start|>user{message}<|im_end|><|im_start|>assistant"
    return text

def get_coinsert_prompt(msg_prefix, msg_surfix):
    return "<|fim_prefix|>" + msg_prefix +  "<|fim_middle|>" + msg_surfix + "<|fim_suffix|>"