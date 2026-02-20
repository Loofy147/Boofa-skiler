## 2026-02-18 - [Batch Tokenization Efficiency]
**Learning:** Tokenizing the same prompt multiple times for batch inference in LLMs is a significant source of CPU overhead. In a high-throughput environment like AIMO competition, this can add up to seconds of delay across many problems.
**Action:** Always tokenize the prompt once and use `tensor.repeat(batch_size, 1)` to create the input batch. This is computationally much cheaper than redundant string processing and tokenization.

## 2026-02-18 - [Regex Pre-compilation in Loops]
**Learning:** Python's `re.findall` or `re.search` calls with string patterns inside hot loops (like processing 8 samples per problem) cause redundant regex parsing and compilation.
**Action:** Move regex patterns to the top-level as pre-compiled objects (`re.compile`) to ensure the regex engine only parses them once.
