pip install -r requirements.txt
CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python==0.2.77
export HF_HUB_ENABLE_HF_TRANSFER=1
