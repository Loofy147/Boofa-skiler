import gradio as gr
import json
import os
from competitions.medgemma.agentic_workflow import BoofaMedWorkflow

def process_clinical_case(query):
    if not query:
        return "Please enter a clinical query."

    workflow = BoofaMedWorkflow()
    result = workflow.run(query)

    # Format the output for the UI
    report = f"## 🩺 Boofa-Med Workflow Results\n\n"
    report += f"**Query:** {result['query']}\n\n"
    report += f"### 🏁 Final Recommendation\n> {result['final_recommendation']}\n\n"
    report += f"**Status:** {'✅ STABLE' if result['final_status'] == 'STABLE' else '⚠️ HIGH RISK'}\n\n"

    report += "### 🔍 Audit Trail\n"
    report += "| Metric | Value |\n"
    report += "| :--- | :--- |\n"
    report += f"| Decisions Audited | {result['audit_trail']['decisions_audited']} |\n"
    report += f"| Safety Pass Rate | {result['audit_trail']['safety_pass_rate']:.2f} |\n"
    report += f"| Anomalies Detected | {result['audit_trail']['anomalies_detected']} |\n"

    if result['audit_trail']['anomalies']:
        report += "\n#### 🚩 Detected Risks:\n"
        for anomaly in result['audit_trail']['anomalies']:
            report += f"- **Risk Type:** {anomaly['risk_type']} | **Q-Score:** {anomaly['q_score']}\n"

    return report

with gr.Blocks(title="Boofa-Med: Clinical Protocol Auditor") as demo:
    gr.Markdown("# 🏥 Boofa-Med: Autonomous Clinical Protocol Auditor")
    gr.Markdown("Building human-centered AI for the **MedGemma Impact Challenge**.")

    with gr.Row():
        with gr.Column(scale=1):
            query_input = gr.Textbox(
                label="Enter Clinical Case / Query",
                placeholder="e.g., Patient with acute chest pain...",
                lines=5
            )
            run_btn = gr.Button("🚀 Run Agentic Workflow", variant="primary")

        with gr.Column(scale=2):
            output_display = gr.Markdown(label="Boofa-Med Output")

    gr.Examples(
        examples=[
            ["Patient with history of asthma reporting new onset wheezing and cough."],
            ["Complex case: Patient with multiple comorbidities presenting with atypical symptoms."],
            ["Routine checkup for a 45-year-old patient with no known issues."]
        ],
        inputs=query_input
    )

    gr.Markdown("---")
    gr.Markdown("### 🏗️ Agentic Architecture")
    gr.Markdown("- **MedGemma Brain**: Core diagnostic inference.")
    gr.Markdown("- **Medical Ethics Auditor**: PCA-based safety monitoring.")
    gr.Markdown("- **Recursive Refinement**: Continuous Q-Score optimization.")

if __name__ == "__main__":
    # For testing in the environment, we don't necessarily need to launch
    # but we'll ensure it can be launched.
    print("✅ Boofa-Med Demo App Ready.")
    # demo.launch() # Uncomment for local use
