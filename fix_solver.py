import re
path = 'layers/layer_2_core/aimo_math_solver.py'
with open(path, 'r') as f:
    content = f.read()

# Match the whole line and replace it
new_line = "        boxed = re.findall(r'\\boxed{(.*?)}', text)"
# The literal string we want in the file is:         boxed = re.findall(r'\boxed{(.*?)}', text)
# Wait, in a raw string r'\boxed', it has TWO backslashes.

content = re.sub(r'        boxed = re\.findall\(.*?, text\)', new_line, content)

with open(path, 'w') as f:
    f.write(content)
