# Remix AI Tools and Services
Implements AI endpoints for the Remix-IDE

## Install Requirements and Download Models
Make sure you are logged in using the `hugginface-cli` if requested.
```bash
sh install_reqs.sh
sh download_models.sh
```

## Code Completion
This service provides the endpoint for code completion at `localhost:7860`

Run 
```bash
cd code_completion
git fetch && git pull && gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7860 --access-logfile - --workers 4 --threads 1 --timeout 600
```
to start the multiworker service.

## Other AI services

The folder `services` implements the services 
- ```Code Generation```
- ```Code Explaining```
- ```Error Correction and Explaining```

First install node js and then run 
```bash
cd services
yarn install 
git fetch && git pull && MODEL=deepseek gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7861 --access-logfile - --workers 3 --threads 64 --timeout 600
```
Here is the list of supported models
* llama13b - default
* mistral
* deepseek
* stability

## Test the server load
```bash
cd experiments
locust -f load_test.py  -u 10 -r 5 -t 5m --html report.html
```

