import os, sys
servertype = os.getenv("SERVERTYPE", 'flask')
sys.path.append('..')

from src.entry import app
import logging, time
from flask import request, Response, g
from src.model_inference_cpp import run_code_completion, run_code_generation, run_code_insertion
import flask_monitoringdashboard as dashboard

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if servertype == 'flask':
    app.add_url_rule( '/ai/api/code_insertion', 'code_insertion', run_code_insertion, methods = ['POST'])
    app.add_url_rule( '/ai/api/code_generation', 'code_generation', run_code_generation, methods = ['POST'])
    app.add_url_rule( '/ai/api/code_completion', 'code_completion', run_code_completion, methods = ['POST'])
    app.debug = True
    print('added all rules!')

dashboard.config.init_from(file='../../monitoring.cfg')
dashboard.bind(app)

@app.get("/ai/api")
def read_main():
    print("Welcome to REMIX-IDE AI services")
    return {"message": "Welcome to REMIX-IDE AI services"}

if __name__ == "__main__":
    app.run()