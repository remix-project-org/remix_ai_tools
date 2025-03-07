# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy requirements.txt
COPY requirements.txt ./
COPY test_input.json ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    curl \
    wget \
    ca-certificates \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/debian10/x86_64/3bf863cc.pub

# Add CUDA repository
RUN echo "deb https://developer.download.nvidia.com/compute/cuda/repos/debian10/x86_64 /" > /etc/apt/sources.list.d/cuda.list

# Install CUDA 12.1
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-toolkit-12-1 \
    && rm -rf /var/lib/apt/lists/*

# Set CUDA environment variables
ENV PATH /usr/local/cuda-12.1/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda-12.1/lib64:${LD_LIBRARY_PATH}
ENV CUDA_HOME /usr/local/cuda-12.1


# # Install dependencies
# RUN pip install -r requirements.txt

#RUN nvcc --version



RUN pip install -r requirements.txt --ignore-installed blinker

RUN CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python==0.2.77


RUN mkdir -p ./models

COPY ./models/deepseek-coder-1.3b-base-q4.gguf ./models
#RUN curl -L "https://drive.usercontent.google.com/download?id=13UNJuB908kP0pWexrT5n8i2LrhFaWo92&confirm=xxx" > deepseek-coder-1.3b-base-q4.gguf && mv deepseek-coder-1.3b-base-q4.gguf ./models/deepseek-coder-1.3b-base-q4.gguf

# Copy the rest of the application code
COPY src src
COPY main.py .
COPY test_input.json .


# Command to run the application
CMD ["python", "-u",  "main.py"]