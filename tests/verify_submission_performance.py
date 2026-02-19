import pandas as pd
import sys
import os
import polars as pl

# Add current directory to path
sys.path.append(os.getcwd())

# Import predict from submission.py
import submission

def main():
    print("🔬 Verifying submission.py against Reference Problems...")

    # Force Mock Mode by ensuring MODEL is None (if not in Kaggle)
    # The submission.py already handles this if /kaggle/input is missing.

    ref_path = 'data/aimo_3/reference.csv'
    if not os.path.exists(ref_path):
        # Fallback
        ref_path = '../data/aimo_3/reference.csv'
        if not os.path.exists(ref_path):
            print(f"❌ Reference file not found: {ref_path}")
            return

    df = pd.read_csv(ref_path)
    total = len(df)
    correct = 0

    for i, row in df.iterrows():
        id_val = row['id']
        problem = row['problem']
        expected = int(row['answer'])

        print(f"[{i+1}/{total}] Testing {id_val}...")

        # Call predict
        result_df = submission.predict(id_val, problem)
        actual = int(result_df['answer'][0])

        if actual == (expected % 100000):
            print(f"  ✅ Correct: {actual}")
            correct += 1
        else:
            print(f"  ❌ Incorrect! Expected {expected}, got {actual}")

    print("-" * 30)
    print(f"Final Score: {correct}/{total}")
    if correct == total:
        print("🏆 10/10 Performance Verified!")
        sys.exit(0)
    else:
        print("⚠️ Performance below 10/10.")
        sys.exit(1)

if __name__ == "__main__":
    main()
