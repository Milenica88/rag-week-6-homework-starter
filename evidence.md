# Week 6 RAG Homework Evidence

## Pair information

- **Milena Paripovic:** pokretala testove i CLI komande, proveravala rezultate i pripremila prezentaciju.
- **Dusan Nikolic:** pratio testiranje, pomagao u radu i proveravao rezultate zajedno sa Milenom.
- **Demo lead:** Milena Paripovic.

## Baseline setup

The first attempt to run the tests with `python -m pytest` failed because Python was not available through the `python` command:

```text
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
```

The environment was then prepared successfully with:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

After installing the project dependency, the tests were run again.

## Test result summary

Command:

```powershell
python -m pytest
```

Result:

```text
collected 9 items

tests\test_chunking.py ..                                                                       [ 22%]
tests\test_corpus.py ...                                                                        [ 55%]
tests\test_rag.py ..                                                                            [ 77%]
tests\test_retrieval.py ..                                                                      [100%]

9 passed in 0.32s
```

All 9 tests passed. This confirms that the baseline corpus loading, chunking validation, retrieval ordering, supported-answer behavior, and refusal behavior are working as expected.

## Outcome 1: Chunking impact on retrieval quality

Chunking divides a document into smaller pieces before retrieval. The project uses character-based chunks and an overlap between consecutive chunks. The overlap is intended to preserve context that might otherwise be split between two chunks.

### Configuration A

Command:

```powershell
python -m src.cli --question "What is retrieval augmented generation?" --chunk-size 140 --overlap 30
```

Output:

```text
Question:
What is retrieval augmented generation?

Answer:
Grounded response based on retrieved context:
[doc-1-chunk-0] Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than unsuppo
[doc-2-chunk-0] Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source tra

Corpus profile: default

Refused: False
Citations: doc-1-chunk-0, doc-2-chunk-0
```

Configuration A returned two chunks. The first chunk contains the direct definition of retrieval augmented generation, while the second chunk contains related information about chunking and retrieval quality. The 30-character overlap provides more context between neighboring chunks.

### Configuration B

Command:

```powershell
python -m src.cli --question "What is retrieval augmented generation?" --chunk-size 80 --overlap 10
```

Output:

```text
Question:
What is retrieval augmented generation?

Answer:
Grounded response based on retrieved context:
[doc-1-chunk-0] Retrieval augmented generation combines retrieval with text generation. The mode
[doc-2-chunk-1] lap improve retrieval quality. Metadata helps filtering and source traceability.

Corpus profile: default

Refused: False
Citations: doc-1-chunk-0, doc-2-chunk-1
```

Configuration B uses smaller chunks and less overlap. This changes the retrieved chunk IDs and produces shorter context. The output also shows that character-based splitting can cut words or phrases at chunk boundaries, for example `mode` is cut from the longer word in the first chunk and the second chunk starts with `lap`. This can reduce readability and may make the evidence less complete.

### Retrieval difference summary

- Both configurations returned a non-refused answer, so both had enough lexical evidence for the query.
- Configuration A returned `doc-1-chunk-0` and `doc-2-chunk-0`.
- Configuration B returned `doc-1-chunk-0` and `doc-2-chunk-1`.
- The larger chunk size preserved more surrounding context.
- The smaller chunk size produced more precise but more fragmented context.
- The experiment shows why chunk size and overlap affect retrieval quality and citation usefulness.

## Outcome 2: Top-k retrieval pipeline

The retrieval pipeline assigns every chunk a lexical relevance score, filters out chunks below the minimum score, sorts the remaining chunks from highest to lowest score, and returns only the first `k` results.

The scoring approach is based on token overlap:

1. The question and chunk are converted to lowercase tokens.
2. The number of query-token occurrences found in the chunk is counted.
3. The count is divided by the number of tokens in the chunk.
4. Results are sorted by score in descending order.

The unit test `test_retrieve_top_k_orders_by_score_desc` passed as part of the 9-test run. It verifies that the chunk with the stronger lexical match is returned first.

### Top-k = 2

Command:

```powershell
python -m src.cli --question "Why are citations important in RAG?" --top-k 2
```

Output:

```text
Question:
Why are citations important in RAG?

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.

Corpus profile: default

Refused: True
Citations: None
```

### Top-k = 3

Command:

```powershell
python -m src.cli --question "Why are citations important in RAG?" --top-k 3
```

Output:

```text
Question:
Why are citations important in RAG?

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.

Corpus profile: default

Refused: True
Citations: None
```

### Interpretation

Both commands used a different maximum number of retrieved chunks, but both returned no usable grounded answer. This is expected because the `default` corpus does not contain enough evidence for the question about the importance of citations. Increasing `top-k` cannot create evidence that is absent from the corpus.

These two commands demonstrate that refusal behavior is stable for both `top_k=2` and `top_k=3`. The separate retrieval-ordering unit test demonstrates that, when relevant chunks are available, they are sorted by descending score.

### Evidence limitation

The CLI output for the citations question does not print individual retrieval scores because the query is unsupported and the final result is an empty/refused answer. Therefore, this particular pair of CLI outputs cannot be used to compare the exact ranking of returned chunks. The passing retrieval unit test is the evidence for ranking correctness.

## Outcome 3: Citation quality

### Supported query

Command:

```powershell
python -m src.cli --question "What is retrieval augmented generation?"
```

The system returned:

```text
Grounded response based on retrieved context:
[doc-1-chunk-0] Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than unsuppo
[doc-2-chunk-0] Chunking splits documents into smaller parts. Good chunk size and overlap improve retrieval quality. Metadata helps filtering and source tra
```

The result was:

```text
Refused: False
Citations: doc-1-chunk-0, doc-2-chunk-0
```

### Why the citations are valid

- The answer explicitly includes the chunk IDs in square brackets.
- The final `Citations` field repeats the same chunk IDs.
- `doc-1-chunk-0` directly supports the definition of retrieval augmented generation.
- `doc-2-chunk-0` provides related context about chunking and retrieval quality.
- The answer is grounded in retrieved corpus text instead of presenting an unsupported external claim.

The displayed text ends in the middle of some words because the corpus is split by character count. This is a chunking artifact, not a citation mismatch: the cited IDs still identify the exact chunks used by the system.

## Outcome 4: Refusal behavior

### Unsupported query

Command:

```powershell
python -m src.cli --question "Who was emperor of Mars?"
```

Output:

```text
Question:
Who was emperor of Mars?

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.

Corpus profile: default

Refused: True
Citations: None
```

### Explanation

The corpus contains no relevant evidence about an emperor of Mars. Instead of hallucinating a name or inventing a fact, the RAG pipeline returns a clear refusal message and no citations.

This behavior is important for grounded RAG because a retrieved context that does not support the question should not be treated as proof. The refusal test `test_build_grounded_answer_refuses_unsupported_query` also passed in the test run.

## Outcome 5: Final evidence pair

### Supported case

Command:

```powershell
python -m src.cli --question "What is retrieval augmented generation?"
```

Result:

- `Refused: False`
- Citations: `doc-1-chunk-0, doc-2-chunk-0`
- The answer contains retrieved evidence and explicit chunk citations.

### Unsupported case

Command:

```powershell
python -m src.cli --question "Who was emperor of Mars?"
```

Result:

- `Refused: True`
- Citations: `None`
- The system states that it does not have enough grounded evidence.

### Comparison

The supported case produces a grounded response because the corpus contains matching evidence. The unsupported case produces a refusal because the corpus does not contain sufficient evidence. This demonstrates the intended difference between answering from retrieved context and refusing to hallucinate.

## Final verification

The final test command was:

```powershell
python -m pytest
```

Final result:

```text
9 passed in 0.32s
```

All available tests passed successfully.
