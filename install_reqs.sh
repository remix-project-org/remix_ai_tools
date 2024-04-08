pip install -r requirements.txt
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python==0.2.56
export HF_HUB_ENABLE_HF_TRANSFER=1
solc-select install all 