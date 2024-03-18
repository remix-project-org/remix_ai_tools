# Remix AI Tools and Services
Implements AI endpoints for the Remix-IDE

## Implemented Function

### Code Completion
This service provides the endpoint for code completion at `localhost:7860`

Run 
```bash
cd code_completion
git fetch && git pull && gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7860 --access-logfile - --workers 4 --threads 1 --timeout 600
```
to start the multiworker service.

## Other Ai services

The folder `services` implements the services ```Code Generation```, ```Code Explaining```, ```Error Correction and Explaining```

## Download the open source LLMs
Make sure you are logged in using the `hugginface-cli`.
```bash
huggingface-cli download TheBloke/deepseek-coder-1.3b-instruct-GGUF deepseek-coder-1.3b-instruct.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
huggingface-cli download TheBloke/deepseek-coder-6.7B-instruct-GGUF deepseek-coder-6.7b-instruct.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-code-ft-GGUF mistral-7b-instruct-v0.2-code-ft.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
huggingface-cli download TheBloke/CodeLlama-13B-Instruct-GGUF codellama-13b-instruct.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
```

## Test the server load
```bash
cd experiments
locust -f load_test.py  -u 10 -r 5 -t 5m --html report.html
```

