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
