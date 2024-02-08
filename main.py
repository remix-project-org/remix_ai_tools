from fastapi import FastAPI
from deploy_service import gr, gr_app
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["remix.beta.ethereum.org",
            "remix.alpha.ethereum.org",
            "remix.ethereum.org",
            "http://localhost:7861",
            "http://127.0.0.1:7861"
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_main():
    return {"message": "Welcome to REMIX-IDE AI services"}

app = gr.mount_gradio_app(app, gr_app, path="/ai")