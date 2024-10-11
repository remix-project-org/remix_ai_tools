import os, sys
sys.path.append('..')
from src.entry import app
from utils.middleware_logging import GradioProfilingMiddleware
from src.model_inference_cpp_flask import code_completion, code_explaining, code_insertion, error_explaining, solidity_answer

servertype = os.getenv("SERVERTYPE", 'fastapi')

if servertype == 'flask':
    app.add_url_rule( '/code_explaining', 'code_explaining', code_explaining, methods = ['POST'])
    app.add_url_rule( '/solidity_answer', 'solidity_answer', solidity_answer, methods = ['POST'])
    app.add_url_rule( '/error_explaining', 'error_explaining', error_explaining, methods = ['POST'])
    app.add_url_rule( '/code_completion', 'code_completion', code_completion, methods = ['POST'])
    app.add_url_rule( '/code_insertion', 'code_insertion', code_insertion, methods = ['POST'])

@app.get("/")
def read_main():
    print("Welcome to REMIX-IDE AI services")
    return {"message": "Welcome to REMIX-IDE AI services"}

if __name__ == "__main__":
    app.run()