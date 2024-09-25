# RemixAI Desktop Inference Server
Provides a platform independen local inference endpoint for Remix AI

## Depenencies
- python 3.10
- llamacpp v0.2.88

## Setup Environment
It is important to create a dedicated virtual environment for the bin creation process, as the env libs will be copied in the executables. 

```bash
python -m venv desktop_venv
source desktop_venv/bin/activate
pip install -r requirements.txt
CMAKE_ARGS="-DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python==0.2.88 --force-reinstall --no-cache-dir
or pip install llama-cpp-python   --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 // for cuda 12.4
```

on mac arm devices
```
CMAKE_ARGS="-DLLAMA_METAL_EMBED_LIBRARY=ON -DLLAMA_METAL=on -DBUILD_SHARED_LIBS=OFF" pip install -U llama-cpp-python==0.2.88 --no-cache-dir

```

Run `pyinstaller` to create a target exec file
```
pyinstaller --collect-all llama_cpp --onefile InferenceServer.py
```

## Supported GPUs
nvidia GPUs

## API Docs
For detailed API documentation, please refer to the [API.md](API.md) file