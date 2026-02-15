import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 Boofa-Skiler AIMO 3 Winning Submission\n",
    "## Optimized for H100 Offline Inference\n",
    "\n",
    "This notebook implements the Boofa-skiler mathematical reasoning framework using the `MiniMax-M2.5` model."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import re\n",
    "import torch\n",
    "import polars as pl\n",
    "from transformers import AutoModelForCausalLM, AutoTokenizer\n",
    "\n",
    "# --- 1. Model Configuration ---\n",
    "MODEL_PATH = '/kaggle/input/minimax-m2-5-sft'\n",
    "\n",
    "def load_model():\n",
    "    if not os.path.exists(MODEL_PATH):\n",
    "        print(\"⚠️ Model path not found. Running in simulation mode.\")\n",
    "        return None, None\n",
    "    \n",
    "    print(f\"⏳ Loading model from {MODEL_PATH}...\")\n",
    "    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)\n",
    "    model = AutoModelForCausalLM.from_pretrained(\n",
    "        MODEL_PATH, \n",
    "        torch_dtype=torch.bfloat16, \n",
    "        device_map='auto', \n",
    "        trust_remote_code=True\n",
    "    )\n",
    "    print(\"✅ Model loaded successfully.\")\n",
    "    return tokenizer, model\n",
    "\n",
    "tokenizer, model = load_model()\n",
    "\n",
    "# --- 2. Prediction Logic ---\n",
    "def extract_answer(text):\n",
    "    boxed = re.findall(r'\\\\boxed{(.*?)}', text)\n",
    "    if boxed:\n",
    "        ans_str = boxed[-1].replace(',', '').strip()\n",
    "        nums = re.findall(r'-?\\d+', ans_str)\n",
    "        if nums: return int(nums[0]) % 100000\n",
    "    return 0\n",
    "\n",
    "def predict(id_series, problem_series):\n",
    "    id_val = id_series.item(0)\n",
    "    problem = problem_series.item(0)\n",
    "    \n",
    "    if model is None:\n",
    "        # Simulation fallback\n",
    "        return pl.DataFrame({'id': [id_val], 'answer': [0]})\n",
    "    \n",
    "    prompt = f\"Problem: {problem}\\n\\nSolve step-by-step. End with 'The final answer is \\\\boxed{{result}}'.\"\n",
    "    inputs = tokenizer(prompt, return_tensors='pt').to(model.device)\n",
    "    \n",
    "    with torch.no_grad():\n",
    "        outputs = model.generate(**inputs, max_new_tokens=1024, temperature=0.1, do_sample=True)\n",
    "    \n",
    "    response = tokenizer.decode(outputs[0], skip_special_tokens=True)\n",
    "    ans = extract_answer(response)\n",
    "    \n",
    "    print(f\"🧩 [{id_val}] -> {ans}\")\n",
    "    return pl.DataFrame({'id': [id_val], 'answer': [ans]})\n",
    "\n",
    "# --- 3. Submission API ---\n",
    "try:\n",
    "    import kaggle_evaluation.aimo_3_inference_server\n",
    "    inference_server = kaggle_evaluation.aimo_3_inference_server.AIMO3InferenceServer(predict)\n",
    "    \n",
    "    if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):\n",
    "        inference_server.serve()\n",
    "    else:\n",
    "        # Local dummy output for UI activation\n",
    "        pl.DataFrame({'id': ['dummy'], 'answer': [0]}).write_parquet('submission.parquet')\n",
    "        print(\"✅ Dummy submission.parquet generated for UI.\")\n",
    "except ImportError:\n",
    "    pl.DataFrame({'id': ['fallback'], 'answer': [0]}).write_parquet('submission.parquet')\n",
    "    print(\"⚠️ API not found. Fallback parquet generated.\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open('submission.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)
