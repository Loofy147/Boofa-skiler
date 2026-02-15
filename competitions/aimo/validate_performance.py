import pandas as pd
import os
import sys
from layers.layer_2_core.aimo_math_solver import AIMOMathSolver

def main():
    print("🏆 AIMO 3 Performance Validation (Winning Numbers Showcase)")
    print("="*60)

    ref_path = "data/aimo_3/reference.csv"
    if not os.path.exists(ref_path):
        print(f"❌ Error: Reference file not found at {ref_path}")
        return

    df = pd.read_csv(ref_path)
    solver = AIMOMathSolver()

    correct = 0
    total = len(df)

    results = []

    for _, row in df.iterrows():
        problem_id = row['id']
        problem_text = row['problem']
        true_answer = int(row['answer'])

        prediction = solver.solve_problem(problem_text, id=problem_id)
        pred_answer = prediction['answer']

        is_correct = (pred_answer == true_answer)
        if is_correct:
            correct += 1

        status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
        print(f"[{problem_id}] Predicted: {pred_answer} | True: {true_answer} | {status}")

        results.append({
            "id": problem_id,
            "predicted": pred_answer,
            "true": true_answer,
            "status": status
        })

    accuracy = (correct / total) * 100
    print("="*60)
    print(f"📊 FINAL SCORE: {correct}/{total} ({accuracy:.1f}%)")
    print("="*60)

    # Save validation results
    os.makedirs("outcomes/technical", exist_ok=True)
    with open("outcomes/technical/AIMO_PERFORMANCE_METRICS.json", "w") as f:
        import json
        json.dump({
            "score": f"{correct}/{total}",
            "accuracy": f"{accuracy:.1f}%",
            "details": results
        }, f, indent=2)

if __name__ == "__main__":
    main()
