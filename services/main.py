import os
from deploy_service import gr, gr_app
from fastapi import FastAPI, Body
from src.model_inference_cpp import *
from time import time

app = FastAPI()

@app.get("/")
def read_main():
    return {"message": "Welcome to REMIX-IDE AI services"}

app = gr.mount_gradio_app(app, gr_app, path="/ai")

# @app.post("/ai/api/code_completion")
# async def code_completion(payload=Body(),
#     stream_result: bool=True,
#     temperature: float = 0.1,
#     top_p: float = 0.9,
#     top_k: int = 50):
#     start = time()
#     res = run_code_completion(payload["context_code"], payload["comment"], stream_result, payload["max_new_tokens"], temperature, top_p, top_k)
#     end = time()
#     m_times.append(end-start)
#     print(str(os.getpid()) + " - Response time:", end-start)
#     return res

# @app.post("/ai/api/code_generation")
# async def code_generation(context_code:str=Body(),
#     stream_result: bool=True,
#     max_new_tokens: int = 1000,
#     temperature: float = 0.1,
#     top_p: float = 0.9,
#     top_k: int = 50):
#     start = time()
#     res = run_code_generation(context_code, stream_result, max_new_tokens, temperature, top_p, top_k)
#     end = time()
#     m_times.append(end-start)
#     print(str(os.getpid()) + " - Average Response time:", sum(m_times)/len(m_times))
#     return res

# @app.post("/ai/api/code_explaining")
# async def code_explaining(context_code: str=Body(),
#     stream_result: bool=True,
#     max_new_tokens: int = 2000,
#     temperature: float = 0.1,
#     top_p: float = 0.9,
#     top_k: int = 50):
#     start = time()
#     res = run_code_explaining(context_code, stream_result, max_new_tokens, temperature, top_p, top_k)
#     end = time()
#     m_times.append(end-start)
#     print(str(os.getpid()) + " - Average Response time:", sum(m_times)/len(m_times))
#     return res

# @app.post("/ai/api/error_explaining")
# async def error_explaining(err: str=Body(),
#     stream_result: bool=True,
#     max_new_tokens: int = 10,
#     temperature: float = 0.1,
#     top_p: float = 0.9,
#     top_k: int = 50):
#     start = time()
#     res = run_err_explaining(err, stream_result, max_new_tokens, temperature, top_p, top_k)
#     end = time()
#     m_times.append(end-start)
#     print(str(os.getpid()) + " - Average Response time:", sum(m_times)/len(m_times))
#     return res


# @app.post("/ai/api/contract_generation")
# async def contract_generation(desc: str=Body(),
#     stream_result: bool=True,
#     max_new_tokens: int = 2000,
#     temperature: float = 0.1,
#     top_p: float = 0.9,
#     top_k: int = 50):
#     start = time()
#     res = run_contract_generation(desc, stream_result, max_new_tokens, temperature, top_p, top_k)
#     end = time()
#     m_times.append(end-start)
#     print(str(os.getpid()) + " - Average Response time:", sum(m_times)/len(m_times))
#     return res

# @app.post("/ai/api/answering")
# async def answering(question: str=Body(),
#     stream_result: bool=True,
#     max_new_tokens: int = 2000,
#     temperature: float = 0.1,
#     top_p: float = 0.9,
#     top_k: int = 50):
#     start = time()
#     res = run_answering(question, stream_result, max_new_tokens, temperature, top_p, top_k)
#     end = time()
#     m_times.append(end-start)
#     print(str(os.getpid()) + " - Average Response time:", sum(m_times)/len(m_times))
#     return res

app = gr.mount_gradio_app(app, gr_app, path="/ai")