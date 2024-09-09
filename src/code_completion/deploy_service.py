import gradio as gr
import sys
sys.path.append('../')
from src.model_inference_cpp import *

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

codeinsert = gr.Interface(
    fn=run_code_insertion,
    inputs=["text", "text", gr.Slider(0, 2000,200), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.9), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Code Inserttion",
    api_name="code_insertion",
)



gr_app = gr.TabbedInterface([codecomp, codegen, codeinsert],
                         ["code_completion", "code_generation", "code_insertion"])

if __name__ == "__main__":
    gr_app.queue(max_size=100).launch(share=True, max_threads=50, show_api=True)
    # app.queue(5).launch(share=True, root_path="/ai-tools", auth=(os.getenv('GRADIO_ADMIN'), os.getenv('GRADIO_ADMIN_PASS')))
