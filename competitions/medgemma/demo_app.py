import gradio as gr
import json
import os
from competitions.medgemma.agentic_workflow import BoofaMedWorkflow

def process_clinical_case(query, age, weight, meds, legacy_protocol):
    if not query:
        return "Please enter a clinical query."

    patient_data = {
        "age": int(age) if age else 45,
        "weight": float(weight) if weight else 75.0,
        "current_meds": [m.strip() for m in meds.split(",")] if meds else []
    }

    workflow = BoofaMedWorkflow()
    result = workflow.run(query, patient_data=patient_data, legacy_context=legacy_protocol)

    report = f"## 🩺 Boofa-Med Workflow Results\n\n"
    report += f"**Query:** {result['query']}\n\n"

    if 'executive_summary' in result:
        report += "### 📋 Executive Summary\n"
        report += f"```\n{result['executive_summary']}\n```\n\n"

    if result.get('tool_calls'):
        report += "### 🛠️ Tool Observations\n"
        for tool in result['tool_calls']:
            if 'calculated_dose' in tool:
                report += f"- **Dosage Calculator:** Recommended {tool['calculated_dose']} for {tool['drug']} ({tool['notes']})\n"
            elif 'interaction_status' in tool:
                report += f"- **Drug Interaction:** {tool['pair']} -> {tool['interaction_status']}\n"
            elif 'reference_range' in tool:
                report += f"- **Lab Checker:** {tool['lab'].upper()} is {tool['value']} (Ref: {tool['reference_range']}) -> **{tool['status']}**\n"
        report += "\n"

    report += f"### 🏁 Final Recommendation\n> {result['final_recommendation']}\n\n"
    report += f"**Status:** {'✅ STABLE' if result['final_status'] == 'STABLE' else '⚠️ HIGH RISK'}\n\n"

    if result.get('discovered_deltas'):
        report += "### 📉 Clinical Deltas Detected\n"
        for delta in result['discovered_deltas']:
            report += f"- **Type:** {delta['type']} | **Description:** {delta['description']}\n"
        report += "\n"

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
                placeholder="e.g., Patient with acute chest pain and troponin of 0.5...",
                lines=3
            )
            with gr.Row():
                age_input = gr.Number(label="Patient Age", value=45)
                weight_input = gr.Number(label="Patient Weight (kg)", value=75)
            meds_input = gr.Textbox(label="Current Medications (comma separated)", placeholder="aspirin, metformin")
            legacy_input = gr.Textbox(label="Legacy Protocol Context (Optional)", placeholder="Standard 1990s treatment for...")

            run_btn = gr.Button("🚀 Run Agentic Workflow", variant="primary")

        with gr.Column(scale=2):
            output_display = gr.Markdown(label="Boofa-Med Output")

    gr.Examples(
        examples=[
            ["Patient with history of asthma reporting new onset wheezing and cough.", 45, 75, "albuterol", "Use oral steroids immediately for all wheezing."],
            ["Elderly patient with heart failure and suspected interaction.", 78, 65, "aspirin, warfarin", "Administer high-dose aspirin for any chest pain."],
            ["Diabetic patient with HbA1c of 8.2 and metformin 500mg daily.", 55, 90, "metformin", ""],
            ["Acute chest pain patient with troponin of 0.08.", 62, 85, "", ""]
        ],
        inputs=[query_input, age_input, weight_input, meds_input, legacy_input]
    )

    run_btn.click(
        fn=process_clinical_case,
        inputs=[query_input, age_input, weight_input, meds_input, legacy_input],
        outputs=output_display
    )

    gr.Markdown("---")
    gr.Markdown("### 🏗️ Agentic Architecture")
    gr.Markdown("- **MedGemma Brain**: Core diagnostic inference.")
    gr.Markdown("- **Medical Ethics Auditor**: PCA-based safety monitoring.")
    gr.Markdown("- **Recursive Refinement**: Continuous Q-Score optimization.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    print(f"🚀 Launching Boofa-Med Demo on port {port}...")
    demo.launch(server_name="0.0.0.0", server_port=port)
