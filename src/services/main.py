import os, sys
servertype = os.getenv("SERVERTYPE", 'fastapi')

sys.path.append('..')
from src.entry import app
from flask import g, request
from src.model_inference_cpp_flask import code_completion, code_explaining, code_insertion
from src.model_inference_cpp_flask import error_explaining, solidity_answer, vulnerability_check
import flask_monitoringdashboard as dashboard




if servertype == 'flask':
    app.add_url_rule( '/ai/api/code_explaining', 'code_explaining', code_explaining, methods = ['POST'])
    app.add_url_rule( '/ai/api/solidity_answer', 'solidity_answer', solidity_answer, methods = ['POST'])
    app.add_url_rule( '/ai/api/error_explaining', 'error_explaining', error_explaining, methods = ['POST'])
    app.add_url_rule( '/ai/api/code_completion', 'code_completion', code_completion, methods = ['POST'])
    app.add_url_rule( '/ai/api/code_insertion', 'code_insertion', code_insertion, methods = ['POST'])
    app.add_url_rule( '/ai/api/vulnerability_check', 'vulenerability_check', vulnerability_check, methods = ['POST'])
    app.debug = True

@app.get("/ai/api")
def read_main():
    print("Welcome to REMIX-IDE AI services")
    return {"message": "Welcome to REMIX-IDE AI services"}


dashboard.config.init_from(file='../../monitoring.cfg')
dashboard.bind(app)

if __name__ == "__main__":
    app.run(debug=True)