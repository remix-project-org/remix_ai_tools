import sys

from rag.rag import get_search_result

COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe. You only provide code ### Instruction:"

completion_model_path = "../../deepseek-coder-1.3b-instruct.Q4_K_M.gguf"
insertsion_model_path = "../../deepseek-coder-1.3b-base.Q4_K_M.gguf"

def get_cocom_prompt(message: str, is_model_deep_seek: bool) -> str:
    return get_cogen_prompt(message, is_model_deep_seek)

def get_cogen_prompt(message: str, is_model_deep_seek: bool) -> str:
    text = f"{COMPLETION_SYSTEM_PROMPT}\n{message}\n ### Response: " if is_model_deep_seek \
            else f"<|im_start|>system{COMPLETION_SYSTEM_PROMPT}<|im_end|><|im_start|>user{message}<|im_end|><|im_start|>assistant"
    return text

def get_coinsert_prompt(msg_prefix, msg_surfix):
    return "<｜fim▁begin｜>" + msg_prefix + "\n" +  "<｜fim▁hole｜>\n" + msg_surfix + " <｜fim▁end｜>"