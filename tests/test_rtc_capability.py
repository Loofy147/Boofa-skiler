import sys
import os
import re

# Add current directory to path
sys.path.append(os.getcwd())

from layers.layer_2_core.aimo_math_solver import AIMOMathSolver

def test_rtc():
    print("🧪 Testing RTC Capability...")
    solver = AIMOMathSolver(model_id_or_path="NON_EXISTENT")

    # Problem that is easy to solve with code but hard for LLM directly
    problem = "Find the sum of all digits of 2^20."
    # The expected sum: 2^20 = 1048576. Digits: 1+0+4+8+5+7+6 = 31.

    # Mock a response that contains RTC
    mock_response = """
To solve this, let's use Python.
```python
n = 2**20
print(sum(int(d) for d in str(n)))
```
The final answer is \\boxed{31}.
"""

    # Test _execute_code
    code = "n = 2**20\nprint(sum(int(d) for d in str(n)))"
    ans = solver._execute_code(code)
    print(f"  RTC Execution Result: {ans}")
    if ans == 31:
        print("  ✅ RTC Execution Passed!")
    else:
        print(f"  ❌ RTC Execution Failed! Expected 31, got {ans}")
        return False

    # Test extraction with robust regex
    extracted = solver._extract_boxed_answer(mock_response)
    print(f"  Extracted Answer: {extracted}")
    if extracted == 31:
        print("  ✅ Regex Extraction Passed!")
    else:
        print(f"  ❌ Regex Extraction Failed! Expected 31, got {extracted}")
        return False

    return True

if __name__ == "__main__":
    if test_rtc():
        print("🎉 RTC Capability Verified!")
        sys.exit(0)
    else:
        print("💀 RTC Capability Test Failed!")
        sys.exit(1)
