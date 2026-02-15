import os
import sys
import polars as pl
import pandas as pd

# Ensure the system knows where to find the layered modules
# Add current directory and the data/aimo_3 directory for local simulation
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "data/aimo_3"))

from layers.layer_2_core.aimo_math_solver import AIMOMathSolver

# Initialize the solver
# On Kaggle, the model is often in /kaggle/input/minimax-m2-5-sft
model_path = "/kaggle/input/minimax-m2-5-sft"
if not os.path.isdir(model_path):
    model_path = "MiniMaxAI/MiniMax-M2.5"

model = AIMOMathSolver(model_id_or_path=model_path)
all_predictions = []

def predict(id_: pl.Series, problem: pl.Series) -> pl.DataFrame:
    """
    Kaggle AIMO 3 Prediction Function.
    Processes one batch (usually 1 row) and returns the answer.
    """
    id_val = id_.item(0)
    problem_text = problem.item(0)

    # Solve the problem using our solver
    outcome = model.solve_problem(problem_text, id=id_val)
    answer = int(outcome.get('answer', 0))

    # Track predictions for final parquet write
    all_predictions.append({'id': id_val, 'answer': answer})

    return pl.DataFrame({'id': [id_val], 'answer': [answer]})

# Import the competition evaluation API
try:
    import kaggle_evaluation.aimo_3_inference_server
    inference_server = kaggle_evaluation.aimo_3_inference_server.AIMO3InferenceServer(predict)
    HAS_API = True
except ImportError:
    print("⚠️ Kaggle Evaluation API not found. Simulation mode only.")
    HAS_API = False

if __name__ == '__main__':
    try:
        if HAS_API and os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
            print("🚀 Starting AIMO 3 Inference Server (Private Rerun)...")
            inference_server.serve()
        elif HAS_API:
            # Local gateway simulation
            print("🔬 Starting local gateway simulation...")
            test_path = '/kaggle/input/ai-mathematical-olympiad-progress-prize-3/test.csv'
            if not os.path.exists(test_path):
                # Fallback to local data paths
                test_path = 'data/aimo_3/test.csv'
                if not os.path.exists(test_path):
                    test_path = 'reference.csv'

            print(f"Using test data from: {test_path}")
            inference_server.run_local_gateway((test_path,))
        else:
            # Absolute fallback simulation
            print("🔬 Starting manual simulation (No API)...")
            test_path = 'data/aimo_3/test.csv'
            if os.path.exists(test_path):
                df = pd.read_csv(test_path)
                for _, row in df.iterrows():
                    predict(pl.Series([row['id']]), pl.Series([row['problem']]))

    except Exception as e:
        print(f"❌ Error during execution: {e}")

    finally:
        # Final safety check: competition requires submission.parquet
        if all_predictions:
            print(f"💾 Saving {len(all_predictions)} predictions to submission.parquet...")
            df = pl.DataFrame(all_predictions)
            df.write_parquet('submission.parquet')
        else:
            # Absolute fallback to ensure the file exists even if something crashed early
            print("⚠️ No predictions found. Writing empty submission.parquet fallback.")
            pl.DataFrame({'id': ['fallback'], 'answer': [0]}).write_parquet('submission.parquet')

        print("✅ submission.parquet is ready.")
