import os
from utils.middleware_logging import GradioProfilingMiddleware

    
def get_app(servertype=None, profilMidlleware=None):
    if servertype == 'fastapi':
        from fastapi import FastAPI, Body
        from fastapi.middleware.cors import CORSMiddleware
        from deploy_service import gr, gr_app
        app = FastAPI()

        #Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.add_middleware(profilMidlleware)
        print("this code is should not be running"*10)
        gr_app = gr.mount_gradio_app(app, gr_app, path="/ai")

    elif servertype == 'flask':
        from flask import Flask
        from flask_cors import CORS 

        app = Flask(__name__)
        #app.wsgi_app = GradioProfilingMiddleware(app.wsgi_app)
        CORS(app)
        # app.wsgi_app = profilMidlleware(app.wsgi_app)
    else:
        raise Exception("Unknown server type")
    
    return app

app = get_app(os.getenv("SERVERTYPE", 'fastapi'))
