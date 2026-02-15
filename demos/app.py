import gradio as gr
import os
from demo_engine import run_synthesis_flow

def run_demo(k_token, h_token):
    # Set tokens in environment if provided via UI, otherwise use existing
    if k_token:
        os.environ["KAGGLE_API_TOKEN"] = k_token
    if h_token:
        os.environ["HF_TOKEN"] = h_token

    report, metrics = run_synthesis_flow()
    return report

with gr.Blocks(title="Boofa-skiler Grand Showcase") as demo:
    gr.Markdown("# 🚀 Boofa-skiler: Self-Evolving AI Showcase")
    gr.Markdown("This demo showcases the **Boofa-skiler** pipeline bridging **Hugging Face** and **Kaggle**, powered by the **Singularity Realization Engine**.")

    with gr.Row():
        k_input = gr.Textbox(label="Kaggle API Token (Optional if set in Env)", type="password", placeholder="KGAT_...")
        h_input = gr.Textbox(label="HF Token (Optional if set in Env)", type="password", placeholder="hf_...")

    run_btn = gr.Button("🚀 Run Full Synthesis Flow", variant="primary")

    output = gr.Markdown(label="Showcase Report")

    run_btn.click(fn=run_demo, inputs=[k_input, h_input], outputs=output)

    gr.Markdown("---")
    gr.Markdown("### 🏗️ Technical Foundation")
    gr.Markdown("- **Model**: MiniMaxAI/MiniMax-M2.5")
    gr.Markdown("- **Cognitive Layers**: 0 (Universal) to 5 (Consciousness)")
    gr.Markdown("- **Framework**: Q-Score Optimization (> 1.2 achieved)")

if __name__ == "__main__":
    demo.launch()
