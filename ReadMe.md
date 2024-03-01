# Remix AI Tools and Services
Implements AI endpoints for the Remix-IDE

## Implemented Function
### Code Completion 
### Code Generation 
### Code Explaining
### Error Correction and Explaining 

### Run server

```bash
$ git fetch && git pull && gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7860 --access-logfile - --workers 2 --threads 1 --timeout 600
```

### Install requirements 
```bash 
$ pip install -r requirements.txt
$ CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

### Download Models Locally
```bash
$ huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-code-ft-GGUF mistral-7b-instruct-v0.2-code-ft.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False

$ huggingface-cli download TheBloke/CodeLlama-13B-Instruct-GGUF codellama-13b-instruct.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False


```