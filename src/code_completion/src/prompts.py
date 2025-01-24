import json
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound

COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe. You only provide code using this context:\n"

completion_model_path = "../../models/deepseek-coder-1.3b-base-q4.gguf"
insertsion_model_path = "../../models/deepseek-coder-1.3b-base-q4.gguf"

def get_cocom_prompt(message: str, is_model_deep_seek: bool) -> str:
    return get_cogen_prompt(message, is_model_deep_seek)

def get_cogen_prompt(message: str, is_model_deep_seek: bool) -> str:
    rag_prompt = ""# get_RAG_results(user_prompt=message)
    text = f"{COMPLETION_SYSTEM_PROMPT} {rag_prompt}\n### Instruction:\n{message}\n ### Response: " if is_model_deep_seek \
            else f"<|im_start|>system{COMPLETION_SYSTEM_PROMPT}<|im_end|><|im_start|>user{message}<|im_end|><|im_start|>assistant"
    return text

def get_coinsert_prompt(msg_prefix, msg_surfix):
    return "<｜fim▁begin｜>" + msg_prefix +  "<｜fim▁hole｜>" + msg_surfix + "<｜fim▁end｜>"


def add_workspace_ctx(ctxFiles, currentFileName, prompt):
    if ctxFiles is None:
        return prompt
    comment_str = detect_language_comments(prompt)
    new_prompt = ""
    for ctx in ctxFiles:
        new_prompt += f"{comment_str} {ctx['file']}\n {ctx['content']}\n"

    return new_prompt + comment_str + " " + currentFileName + "\n" + prompt
        

def detect_language_comments(code_snippet):
    try:
        # Detect the language
        lexer = guess_lexer(code_snippet)
        # Retrieve single-line comment syntax (if available)
        single_line_comment = "//"  # Default to C-style comments
        for _, ttype, value in lexer.get_tokens_unprocessed(code_snippet):
            if 'Comment' in str(ttype):
                single_line_comment = value.split()[0]
                break

        return  single_line_comment
    except ClassNotFound:
        return '//'  # Default to C-style comments
