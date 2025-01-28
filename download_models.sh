mkdir -p ./models

#uggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-code-ft-GGUF mistral-7b-instruct-v0.2-code-ft.Q4_K_M.gguf --local-dir ./models --local-dir-use-symlinks False
#huggingface-cli download TheBloke/deepseek-coder-1.3b-base-GGUF deepseek-coder-1.3b-base.Q4_K_M.gguf --local-dir ./models --local-dir-use-symlinks False
#huggingface-cli download TheBloke/stable-code-3b-GGUF stable-code-3b.Q4_K_M.gguf --local-dir ./models --local-dir-use-symlinks False
#curl -L "https://drive.usercontent.google.com/download?id=1P-MEH7cPxaR20v7W1qbOEPBzgiY2RDLx&confirm=xxx" > llama3_1_8B-q4_0_instruct.gguf && mv llama3_1_8B-q4_0_instruct.gguf ./models/llama3_1_8B-q4_0_instruct.gguf
#curl -L "https://drive.usercontent.google.com/download?id=13sz7lnEhpQ6EslABpAKl2HWZdtX3d9Nh&confirm=xxx" > deepseek-coder-6.7b-instruct-q4.gguf && mv deepseek-coder-6.7b-instruct-q4.gguf ./models/deepseek-coder-6.7b-instruct-q4.gguf
curl -L "https://drive.usercontent.google.com/download?id=13UNJuB908kP0pWexrT5n8i2LrhFaWo92&confirm=xxx" > deepseek-coder-1.3b-base-q4.gguf && mv deepseek-coder-1.3b-base-q4.gguf ./models/deepseek-coder-1.3b-base-q4.gguf