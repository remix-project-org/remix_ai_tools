COMPLETION_SYSTEM_PROMPT = "You are a Solidity AI Assistant that complete user code with provided context. You provide accurate solution and always answer as helpfully as possible, while being safe. You only provide code using this context:\n"

completion_model_path = "../../models/llama3_1_8B-q4_0_instruct.gguf"
insertsion_model_path = "../../models/llama3_1_8B-q4_0_instruct.gguf"

def get_cocom_prompt(message: str, is_model_deep_seek: bool) -> str:
    return get_cogen_prompt(message, is_model_deep_seek)

def get_cogen_prompt(message: str, is_model_deep_seek: bool) -> str:
    rag_prompt = ""# get_RAG_results(user_prompt=message)
    text = f"{COMPLETION_SYSTEM_PROMPT} {rag_prompt}\n### Instruction:\n{message}\n ### Response: " if is_model_deep_seek \
            else f"<|im_start|>system{COMPLETION_SYSTEM_PROMPT}<|im_end|><|im_start|>user{message}<|im_end|><|im_start|>assistant"
    return text

def get_coinsert_prompt(msg_prefix, msg_surfix):
    return "<｜fim▁begin｜>" + msg_prefix + "\n" +  "<｜fim▁hole｜>\n" + msg_surfix + " <｜fim▁end｜>"

# def get_RAG_results(user_prompt):
#     try:
#         start = time.time()
#         if use_rag:
#             retriever = VectorDBRetriever(rag_vector_store, query_mode="default", similarity_top_k=2)
#             results = retriever.retrieve(user_prompt)

#             rag_prompt = ""
#             for idx in range(len(results)):
#                 rag_prompt += results[idx].node.get_content() + "\n" 
#                 print('INFO: retrieved result with score', results[idx].score)
            
#             print('INFO: Local RAG retrieval took', time.time() - start, "seconds")
#             return rag_prompt
#         else:
#             print('INFO: RAG retrieval took', time.time() - start, "seconds")
#             return ""
#     except:
#         print('INFO: RAG retrieval took', time.time() - start, "seconds")
#         return ""