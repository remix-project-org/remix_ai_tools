pip install -r requirements.txt
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
export HF_HUB_ENABLE_HF_TRANSFER=1 