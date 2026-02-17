import polars as pl
import os
import sys

# Mock kaggle_evaluation
sys.path.append('data/aimo_3')

def predict(id_series, problem_series, *args, **kwargs):
    print(f"Received ID: {id_series.item(0)}")
    print(f"Received Problem: {problem_series.item(0)}")
    return pl.DataFrame({'id': [id_series.item(0)], 'answer': [42]})

try:
    import kaggle_evaluation.aimo_3_inference_server
    server = kaggle_evaluation.aimo_3_inference_server.AIMO3InferenceServer(predict)
    # Simulate a local gateway run
    server.run_local_gateway(('competitions/aimo/reference.csv',))
except Exception as e:
    print(f"Caught expected/unexpected error: {e}")
