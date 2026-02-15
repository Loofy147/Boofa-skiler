import os
import pandas as pd
from layers.layer_2_core.aimo_math_solver import AIMOMathSolver

def run_submission():
    print("🚀 Starting AIMO 3 Submission Baseline...")

    # Initialize the Solver Engine
    solver = AIMOMathSolver()

    # 1. Load data
    # Priority: 1. test.csv (Production), 2. reference.csv (Local Validation)
    if os.path.exists("test.csv"):
        test_path = "test.csv"
    elif os.path.exists("reference.csv"):
        test_path = "reference.csv"
    else:
        # Create a mock test.csv if missing (for demo)
        test_path = "test.csv"
        df_test = pd.DataFrame({
            "id": ["test_1", "test_2"],
            "problem": [
                "Find the remainder when 123*456 is divided by 100.",
                "Solve for x: 2x + 5 = 15."
            ]
        })
        df_test.to_csv(test_path, index=False)
        print("Created mock test.csv for demo.")

    test_df = pd.read_csv(test_path)
    print(f"Loaded {len(test_df)} problems from {test_path}.")

    # 2. Process problems
    results = []
    for _, row in test_df.iterrows():
        outcome = solver.solve_problem(row['problem'], id=row['id'])
        results.append({
            "id": row['id'],
            "answer": outcome['answer'] or 0
        })

    # 3. Save submission
    submission_df = pd.DataFrame(results)
    submission_df.to_csv("submission.csv", index=False)
    print("✅ submission.csv generated successfully.")
    print(submission_df)

if __name__ == "__main__":
    run_submission()
