import sys
import os

# Add mock API path
sys.path.append('data/aimo_3')
sys.path.append('.')

# Import and run the bundled script logic
import competitions.aimo.bundled_submission as sub

# Mock data
import polars as pl
id_ser = pl.Series('id', ['test_1'])
prob_ser = pl.Series('problem', ['1+1'])

print("Testing predict call...")
res = sub.predict(id_ser, prob_ser)
print(f"Result:\n{res}")

print("\nTesting full server simulation (no rerun)...")
# We need to mock /kaggle/input/ai-mathematical-olympiad-progress-prize-3/test.csv
os.makedirs('/kaggle/input/ai-mathematical-olympiad-progress-prize-3', exist_ok=True)
pl.DataFrame({'id': ['t1'], 'problem': ['2+2']}).write_csv('/kaggle/input/ai-mathematical-olympiad-progress-prize-3/test.csv')

# Run main
sub.__name__ = '__main__'
# Ensure it doesn't try to serve
os.environ['KAGGLE_IS_COMPETITION_RERUN'] = ''
try:
    # This will call run_local_gateway
    # We need to make sure 'predict' is the one we defined
    import kaggle_evaluation.aimo_3_inference_server
    server = kaggle_evaluation.aimo_3_inference_server.AIMO3InferenceServer(sub.predict)
    server.run_local_gateway(('/kaggle/input/ai-mathematical-olympiad-progress-prize-3/test.csv',))
except Exception as e:
    print(f"Server simulation error: {e}")
