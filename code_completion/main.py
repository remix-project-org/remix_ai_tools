from fastapi import FastAPI
#from deploy_service import gr, gr_app
from src.model_inference_cpp import run_code_completion, run_code_generation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def read_main():
    return {"message": "Welcome to REMIX-IDE AI services"}

@app.post("/ai/api/code_completion")
async def code_completion(data: dict):
    context_code = data["data"][0]
    comment = data["data"][1]
    stream_result = data["data"][2]
    max_new_tokens = data["data"][3]
    temperature = data["data"][4]
    top_p = data["data"][5]
    top_k = data["data"][6]
    return run_code_completion(context_code, comment, stream_result, max_new_tokens, temperature, top_p, top_k)

@app.post("/ai/api/code_generation")
async def code_generation(data: dict):
    gen_comment = data["data"][0]
    stream_result = data["data"][1]
    max_new_tokens = data["data"][2]
    temperature = data["data"][3]
    top_p = data["data"][4]
    top_k = data["data"][5]
    return run_code_generation(gen_comment, stream_result, max_new_tokens, temperature, top_p, top_k)


#app = gr.mount_gradio_app(app, gr_app, path="/ai")