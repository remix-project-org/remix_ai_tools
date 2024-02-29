from fastapi import FastAPI, Query
#from deploy_service import gr, gr_app
from src.model_inference_cpp import *


app = FastAPI()

@app.get("/")
def read_main():
    return {"message": "Welcome to REMIX-IDE AI services"}

@app.post("/ai/api/code_completion")
async def code_completion(context_code: str=Query(None),
    comment: str= Query(None),
    stream_result: bool=True,
    max_new_tokens: int = 1024,
    temperature: float = 0.1,
    top_p: float = 0.9,
    top_k: int = 50):
    print('INFO - Code Completion:', context_code)
    print('INFO - Code Completion:', comment)
    return run_code_completion(context_code, comment, stream_result, max_new_tokens, temperature, top_p, top_k)

#app = gr.mount_gradio_app(app, gr_app, path="/ai")