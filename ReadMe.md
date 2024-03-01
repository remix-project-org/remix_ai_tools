# Remix AI Tools and Services
Implements AI endpoints for the Remix-IDE

## Implemented Function
### Code Completion 
### Code Generation 
### Code Explaining
### Error Correction and Explaining 

### Run server

```bash
git fetch && git pull && gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7860 --access-logfile - --workers 2 --threads 1 --timeout 600
```

### Install requirements 
```bash 
pip install -r requirements.txt
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```