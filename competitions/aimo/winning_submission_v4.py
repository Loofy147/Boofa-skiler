import os
import re
import time
import torch
import subprocess
import sys
import polars as pl
import pandas as pd
import json
from collections import Counter
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime

# --- 1. Winning Infrastructure (Boofa-Skiler v4.0) ---

class StrategicManager:
    def __init__(self, total_probs=50):
        self.start_time = time.time()
        self.limit = 9 * 3600 # 9 hour limit
        self.total_probs = total_probs
        self.solved = 0

    def get_budget(self, problem):
        elapsed = time.time() - self.start_time
        remaining = self.limit - elapsed
        probs_left = max(1, self.total_probs - self.solved)

        t_avg = remaining / probs_left

        # Determine sample count based on time pressure
        if t_avg > 600: return 24 # Generous
        if t_avg > 300: return 12 # Balanced
        if t_avg > 120: return 5  # Quick
        return 3 # Emergency

class RobustExtractor:
    @staticmethod
    def extract(text):
        patterns = [
            r'\\+boxed\s*\{(.*?)\}',
            r'final answer is\s*[:\s]*(\d+)',
            r'\\boxed\{(.*?)\}'
        ]
        for p in patterns:
            try:
                m = re.findall(p, text, re.IGNORECASE)
                if m:
                    ans_str = m[-1].replace(',', '').strip()
                    nums = re.findall(r'-?\d+', ans_str)
                    if nums: return max(0, int(nums[0])) % 100000
            except: continue
        nums = re.findall(r'\d+', text)
        return int(nums[-1]) % 100000 if nums else 0

# --- 2. Model Setup ---

MODEL_PATH = '/kaggle/input/deepseek-r1/transformers/distill-qwen-7b/1'
if not os.path.exists(MODEL_PATH):
    for root, dirs, files in os.walk('/kaggle/input'):
        if 'config.json' in files: MODEL_PATH = root; break

def load_engine():
    if not os.path.exists(MODEL_PATH): return None, None
    try:
        # Optimized for T4/P100/H100
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH, torch_dtype=torch.float16, device_map='auto', trust_remote_code=True
        )
        return tokenizer, model
    except: return None, None

TOKENIZER, MODEL = load_engine()
MANAGER = StrategicManager()
ALL_RESULTS = []

# --- 3. Prediction Core ---

def predict(test_df, sample_sub):
    id_v = test_df['id'].item(0)
    prob = test_df['problem'].item(0)
    print(f"🚀 [{id_v}] Starting V4 Inference...")

    n_samples = MANAGER.get_budget(prob)
    print(f"   Budget: {n_samples} samples")

    answers = []
    if MODEL:
        for i in range(n_samples):
            try:
                prompt = f"<|user|>\nProblem: {prob}\n<|assistant|>\n<|thought|>\n"
                inputs = TOKENIZER(prompt, return_tensors='pt').to(MODEL.device)
                with torch.no_grad():
                    out = MODEL.generate(**inputs, max_new_tokens=1024, temperature=0.6, do_sample=True)
                res = TOKENIZER.decode(out[0], skip_special_tokens=True)

                # RTC Check
                code = re.findall(r'```python\s*(.*?)\s*```', res, re.DOTALL)
                val = None
                if code:
                    try:
                        c = code[-1]
                        if "print" not in c: c = f"print({c})"
                        r = subprocess.run([sys.executable, "-c", c], capture_output=True, text=True, timeout=10)
                        nums = re.findall(r'-?\d+', r.stdout)
                        if nums: val = int(nums[-1]) % 100000
                    except: pass

                answers.append(val if val is not None else RobustExtractor.extract(res))
            except: answers.append(0)
    else:
        # Mock for validation
        answers = [0] * n_samples

    final = Counter([a for a in answers if a != 0] or answers).most_common(1)[0][0]
    MANAGER.solved += 1
    ALL_RESULTS.append({'id': id_v, 'answer': final})
    print(f"   Result: {final}")
    return sample_sub.with_columns(pl.lit(final).alias('answer'))

# --- 4. Main Loop ---

if __name__ == '__main__':
    try:
        import kaggle_evaluation.aimo_3_inference_server
        server = kaggle_evaluation.aimo_3_inference_server.AIMO3InferenceServer(predict)
        server.serve()
    except:
        # Local test fallback
        pl.DataFrame({'id':['dummy'],'answer':[0]}).write_parquet('submission.parquet')
