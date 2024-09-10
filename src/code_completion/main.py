from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deploy_service import gr, gr_app
from utils.middleware_logging import GradioProfilingMiddleware

from time import time

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GradioProfilingMiddleware)

@app.get("/")
def read_main():
    return {"message": "Welcome to REMIX-IDE AI services"}

app = gr.mount_gradio_app(app, gr_app, path="/ai")