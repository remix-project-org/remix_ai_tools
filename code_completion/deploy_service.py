import gradio as gr
import os
from dotenv import load_dotenv
from src.model_inference_cpp import *

load_dotenv()

codecomp = gr.Interface(
    fn=run_code_completion,
    inputs=["text", "text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Code Completion",
    api_name="code_completion",
)

codegen = gr.Interface(
    fn=run_code_generation,
    inputs=["text", "checkbox", gr.Slider(0, 2000,200), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.9), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Code Generation",
    api_name="code_generation",
)


gr_app = gr.TabbedInterface([codecomp, codegen],
                         ["code_completion", "code_generation"])

if __name__ == "__main__":
    gr_app.queue(max_size=100).launch(share=True, root_path="/ai-tools", max_threads=50, show_api=False)
    # app.queue(5).launch(share=True, root_path="/ai-tools", auth=(os.getenv('GRADIO_ADMIN'), os.getenv('GRADIO_ADMIN_PASS')))
