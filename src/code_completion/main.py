import os, sys
sys.path.append('..')
from src.entry import app

from src.model_inference_cpp import run_code_completion, run_code_generation, run_code_insertion
servertype = os.getenv("SERVERTYPE", 'fastapi')

if servertype == 'flask':
    app.add_url_rule( '/ai/api/code_insertion', 'code_insertion', run_code_insertion, methods = ['POST'])
    app.add_url_rule( '/ai/api/code_generation', 'code_generation', run_code_generation, methods = ['POST'])
    app.add_url_rule( '/ai/api/code_completion', 'code_completion', run_code_completion, methods = ['POST'])
    print('added all rules!')

@app.get("/ai/api")
def read_main():
    print("Welcome to REMIX-IDE AI services")
    return {"message": "Welcome to REMIX-IDE AI services"}

if __name__ == "__main__":
    app.run()