import os, sys, time, logging
sys.path.append('..')
from src.entry import app
from src.model_inference_cpp_flask import code_completion, code_explaining, code_insertion
from src.model_inference_cpp_flask import error_explaining, solidity_answer, vulnerability_check
from flask import request, Response, g

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
servertype = os.getenv("SERVERTYPE", 'fastapi')

if servertype == 'flask':
    app.add_url_rule( '/ai/api/code_explaining', 'code_explaining', code_explaining, methods = ['POST'])
    app.add_url_rule( '/ai/api/solidity_answer', 'solidity_answer', solidity_answer, methods = ['POST'])
    app.add_url_rule( '/ai/api/error_explaining', 'error_explaining', error_explaining, methods = ['POST'])
    app.add_url_rule( '/ai/api/code_completion', 'code_completion', code_completion, methods = ['POST'])
    app.add_url_rule( '/ai/api/code_insertion', 'code_insertion', code_insertion, methods = ['POST'])
    app.add_url_rule( '/ai/api/vulnerability_check', 'vulenerability_check', vulnerability_check, methods = ['POST'])

@app.get("/ai/api")
def read_main():
    print("Welcome to REMIX-IDE AI services")
    return {"message": "Welcome to REMIX-IDE AI services"}


@app.before_request
def start_timer():
    """Start the timer before processing a request."""
    g.start_time = time.time()

@app.after_request
def log_response(response):
    """Log the response time after processing a request."""
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        logger.info(f"Request: {request.method} {request.path} - Response time: {duration:.4f}s")
        response.headers['X-Process-Time'] = str(duration)  # Add time to response headers
    return response

if __name__ == "__main__":
    app.run()