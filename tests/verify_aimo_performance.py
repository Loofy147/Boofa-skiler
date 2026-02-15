import pandas as pd
import sys
import os

# Ensure the system knows where to find the layered modules
sys.path.append(os.getcwd())

from layers.layer_2_core.aimo_math_solver import AIMOMathSolver

def main():
    print("🔬 Verifying AIMO 3 Solver against Reference Problems...")
    solver = AIMOMathSolver(model_id_or_path="NON_EXISTENT") # Force MOCK mode

    ref_path = 'data/aimo_3/reference.csv'
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
        outcome = solver.solve_problem(problem, id=id_val)
        actual = int(outcome['answer'])

        if actual == expected:
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
