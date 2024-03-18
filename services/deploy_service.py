import gradio as gr
import os
from src.model_inference_cpp import *


codecomp = gr.Interface(
    fn=run_code_completion,
    inputs=["text", "text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Code Completion",
    api_name="code_completion",
    concurrency_limit=1,
)

codegen = gr.Interface(
    fn=run_code_generation,
    inputs=["text", "checkbox", gr.Slider(0, 2000,200), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.9), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Code Generation",
    api_name="code_generation",
)


codeexp = gr.Interface(
    fn=run_code_explaining,
    inputs=["text", "checkbox", gr.Slider(0, 2000,400), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Code Explaining",
    api_name="code_explaining"
)


errorexp = gr.Interface(
    fn=run_err_explaining,
    inputs=["text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Error and Warning Explaining",
    api_name="error_explaining"
)

contractgen = gr.Interface(
    fn=run_contract_generation,
    inputs=["text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Contract Generation",
    api_name="contract_generation"
)

answer = gr.Interface(
    fn=run_answering,
    inputs=["text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.9), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Solidity Question Answering",
    api_name="solidity_answer",
)




gr_app = gr.TabbedInterface([codecomp, codegen, codeexp, errorexp, contractgen, answer],
                         ["code_completion", "code_generation", "code_explaining",
                          "error_explaining", "contract_generation",
                          "solidity_answer"])

if __name__ == "__main__":
    gr_app.queue(max_size=100).launch(share=True, root_path="/ai-tools", max_threads=50, show_api=False)
    # app.queue(5).launch(share=True, root_path="/ai-tools", auth=(os.getenv('GRADIO_ADMIN'), os.getenv('GRADIO_ADMIN_PASS')))
