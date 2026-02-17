import sys
import os
import polars as pl
import pandas as pd
from unittest.mock import MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

# Import the logic from the bundled script
# We'll use a trick to import it even if it tries to load a model
import competitions.aimo.bundled_submission as sub

def test_unpacking():
    print("🧪 Testing Unpacking Logic...")

    # Case 1: (pl.Series, pl.Series)
    id_s = pl.Series('id', ['id_s'])
    prob_s = pl.Series('problem', ['prob_s'])
    res = sub.predict(id_s, prob_s)
    assert res['id'][0] == 'id_s'
    print("  ✅ pl.Series passed")

    # Case 2: (pl.DataFrame, pl.DataFrame)
    row = pl.DataFrame({'id': ['id_df'], 'problem': ['prob_df']})
    res = sub.predict(row, row.select('id'))
    assert res['id'][0] == 'id_df'
    print("  ✅ pl.DataFrame passed")

    # Case 3: (pd.Series, pd.Series)
    res = sub.predict(pd.Series(['id_pd'], name='id'), pd.Series(['prob_pd'], name='problem'))
    assert res['id'][0] == 'id_pd'
    print("  ✅ pd.Series passed")

def test_mock_solver():
    print("🧪 Testing MockSolver...")
    # Known problem
    res = sub.predict('dummy', 'minimal perimeter triangle')
    assert res['answer'][0] == 336
    print("  ✅ solve_known passed")

    # Basic arithmetic
    res = sub.predict('dummy', 'What is 123 + 456?')
    assert res['answer'][0] == 579
    print("  ✅ solve_basic passed")

def test_extraction():
    print("🧪 Testing Answer Extraction...")
    examples = [
        (r"The answer is \boxed{42}.", 42),
        (r"The answer is \\boxed{100}.", 100),
        (r"Answer is: 123", 123),
        (r"\boxed{ 500 }", 500),
        (r"final answer is 999", 999)
    ]
    for text, expected in examples:
        ans = sub.extract_answer(text)
        assert ans == expected, f"Failed on {text}: expected {expected}, got {ans}"
    print("  ✅ extract_answer passed")

def test_rtc():
    print("🧪 Testing RTC Execution...")
    code = "print(10**2)"
    ans = sub.execute_code(code)
    assert ans == 100
    print("  ✅ execute_code passed")

if __name__ == "__main__":
    try:
        # Mock MODEL to avoid load failure errors in test
        sub.MODEL = MagicMock()
        sub.TOKENIZER = MagicMock()

        test_unpacking()
        test_mock_solver()
        test_extraction()
        test_rtc()
        print("\n🎉 ALL SCORING INTEGRITY CHECKS PASSED!")
    except Exception as e:
        print(f"\n❌ SCORING INTEGRITY CHECK FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
