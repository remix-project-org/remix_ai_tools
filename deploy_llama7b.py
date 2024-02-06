
import gradio as gr
from src.model_inference import *

codecomp = gr.Interface(
    fn=run_code_completion,
    inputs=["text", "text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Llama 13B",
    allow_flagging="manual",
    api_name="code_completion",
    flagging_options=["wrong answer", "off topic"]
)

codegen = gr.Interface(
    fn=run_code_generation,
    inputs=["text", "checkbox", gr.Slider(0, 2000,200), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.9), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Llama 13B",
    api_name="code_generation",
    allow_flagging="manual",
    flagging_options=["wrong answer", "off topic"]
)


codeexp = gr.Interface(
    fn=run_code_explaining,
    inputs=["text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Llama 13B",
    api_name="code_explaining"
)


errorexp = gr.Interface(
    fn=run_err_explaining,
    inputs=["text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Llama 13B",
    api_name="error_explaining"
)

contractgen = gr.Interface(
    fn=run_contract_generation,
    inputs=["text", "checkbox", gr.Slider(0, 2000,300), gr.Slider(0.01, 1, 0.2),
            gr.Slider(0, 1, 0.8), gr.Slider(1, 200, 50)],
    outputs=["text"],
    title="Llama 13B",
    api_name="error_explaining"
)



app = gr.TabbedInterface([codecomp, codegen, codeexp, errorexp, contractgen],
                         ["code_completion", "code_generation", "code_explaining",
                          "error_explaining", "contract_generation"])

if __name__ == "__main__":
    app.launch(share=True).queue(3)
