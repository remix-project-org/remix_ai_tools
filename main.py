import os

from fastapi import FastAPI
from deploy_service import gr, gr_app
from src.model_inference_cpp import *

m_times = []
app = FastAPI()

@app.get("/")
def read_main():
    return {"message": "Welcome to REMIX-IDE AI services"}


app = gr.mount_gradio_app(app, gr_app, path="/ai")