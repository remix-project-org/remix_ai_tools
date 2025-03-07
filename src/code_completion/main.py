import runpod
from src.model_inference_cpp import rp_handler


if __name__ == "__main__":
    runpod.serverless.start({"handler": rp_handler})