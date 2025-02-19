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
cd src/code_completion
git fetch && git pull && TOKENIZERS_PARALLELISM=true SERVERTYPE=flask  gunicorn --workers=1 --bind=0.0.0.0:7851 main:app --workers 6 --threads 10 --timeout 600
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
git fetch && git pull && SERVERTYPE=flask MODEL=llama3_1 TOKENIZERS_PARALLELISM=true gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7861 --access-logfile - --workers 3 --threads 64 --timeout 600
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

## Curl test
```
 curl --connect-timeout 1 -m 5 -H 'Content-Type: application/json' \
    -d '{"data":["pragma solidity 0.8.0 //function add 3 numbers\n", "", false,200,1,0.8,50]}' \
    -X POST http://0.0.0.0:7861/ai/api/code_completion
```


```
 curl --connect-timeout 1 -m 5 -H 'Content-Type: application/json' \
    -d '{"data":["pragma solidity 0.8.0\n", "", false,200,1,0.8,50]}' \
    -X POST http://0.0.0.0:7860/ai/api/code_completion
```


## Load balance on multiple process workers
Add the fgollowing in the `/etc/nginx/nginx.conf`
```
    upstream gunicorn_servers {
        server 127.0.0.1:7861;  # Gunicorn for GPU 0
        server 127.0.0.1:7862;  # Gunicorn for GPU 1
    }

    server {
        listen 7860;  # Nginx listens on port 7860

        location / {
            proxy_pass http://gunicorn_servers;  # Proxy requests to the upstream servers
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
```

Now depending on the amount of GPUs `0`, `1`, launch the workers
```
export CUDA_VISIBLE_DEVICES=0
TOKENIZERS_PARALLELISM=true SERVERTYPE=flask  gunicorn --bind=0.0.0.0:7862 main:app --access-logfile - --workers 10 --threads 10 --timeout 600
```