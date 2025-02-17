import os, sys
servertype = os.getenv("SERVERTYPE", 'flask')
cuda_device = os.getenv("CUDA_VISIBLE_DEVICES")
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


@app.get("/ai/api")
def read_main():
    print("Welcome to REMIX-IDE AI services")
    return {"message": "Welcome to REMIX-IDE AI services"}
dashboard.bind(app)

@app.before_request
def start_timer():
    """Start the timer before processing a request."""
    g.start_time = time.time()

@app.after_request
def log_response(response):
    """Log the response time after processing a request."""
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        logger.info(f"Worker: {cuda_device} Request: {request.method} {request.path} - Response time: {duration:.4f}s")
        response.headers['X-Process-Time'] = str(duration)  # Add time to response headers
    return response

print(f"Worker dor device {cuda_device} started")

if __name__ == "__main__":
    app.run()