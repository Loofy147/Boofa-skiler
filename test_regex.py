import re

def extract_v1(text):
    boxed = re.findall(r'\\boxed{(.*?)}', text)
    return boxed

def extract_v2(text):
    boxed = re.findall(r'\boxed{(.*?)}', text)
    return boxed

text = "The answer is \boxed{336}."
print(f"Text: {text}")
print(f"V1 (\\\\boxed): {extract_v1(text)}")
print(f"V2 (\\boxed): {extract_v2(text)}")

text_raw = r"The answer is \boxed{336}."
print(f"Text Raw: {text_raw}")
print(f"V1 Raw: {extract_v1(text_raw)}")
print(f"V2 Raw: {extract_v2(text_raw)}")
