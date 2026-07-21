---
name: regex-llm-hybrid
description: Use when parsing structured, repetitive text (quizzes, forms, invoices) and deciding between regex and LLM extraction. Covers the regex-first pipeline with confidence scoring and cheap-LLM fallback, with production cost/accuracy numbers.
---

# Regex-LLM Hybrid Extraction

For text where >90% of items follow a repeating pattern, regex extraction plus a cheap-LLM fallback for the low-confidence remainder beats sending everything to an LLM. If the text is free-form and highly variable, skip regex and use an LLM directly.

Pipeline: regex parse -> heuristic confidence score per item -> items below threshold (e.g. 0.95) go to the cheapest available LLM for correction; the rest pass through untouched.

## Production Metrics

Quiz-parsing pipeline, 410 items:

| Metric | Value |
|--------|-------|
| Regex success rate | 98.0% |
| Low-confidence items | 8 (2.0%) |
| LLM calls needed | ~5 |
| Cost savings vs all-LLM | ~95% |

## Sketch

```python
import re
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Item:
    id: str
    text: str
    choices: tuple[str, ...]
    answer: str

PATTERN = re.compile(
    r"(?P<id>\d+)\.\s*(?P<text>.+?)\n"
    r"(?P<choices>(?:[A-D]\..+?\n)+)"
    r"Answer:\s*(?P<answer>[A-D])",
    re.MULTILINE | re.DOTALL,
)

def parse(content: str) -> list[Item]:
    return [
        Item(
            id=m.group("id"),
            text=m.group("text").strip(),
            choices=tuple(re.findall(r"[A-D]\.\s*(.+)", m.group("choices"))),
            answer=m.group("answer"),
        )
        for m in PATTERN.finditer(content)
    ]

def confidence(item: Item) -> float:
    score = 1.0
    if len(item.choices) < 3: score -= 0.3   # truncated choice block
    if not item.answer:       score -= 0.5   # missing answer line
    if len(item.text) < 10:   score -= 0.2   # suspiciously short question
    return max(0.0, score)

def process(content: str, llm_client=None, threshold: float = 0.95) -> list[Item]:
    items = parse(content)
    return [
        fix_with_llm(it, content, llm_client)
        if llm_client and confidence(it) < threshold else it
        for it in items
    ]

def fix_with_llm(item: Item, source: str, client) -> Item:
    resp = client.messages.create(
        model="claude-haiku-4-5",  # cheapest model is sufficient for correction
        max_tokens=500,
        messages=[{"role": "user", "content":
            f"Extract question, choices, answer from:\n{source}\n\n"
            f"Current extraction: {item}\n"
            f"Return corrected JSON, or 'CORRECT' if accurate."}],
    )
    return item if resp_says_correct(resp) else item_from_json(resp)
```

## Notes

- Confidence heuristics are structural (missing fields, wrong counts, short text), not probabilistic -- cheap to compute and easy to tune against a labeled sample.
- Keep parsed items immutable; cleaning and LLM correction return new instances, which keeps the fallback path testable.
- Log regex success rate and LLM call count per run; a dropping regex rate signals the source format drifted.
- Test the parser against known-good patterns first, then malformed input, missing fields, and encoding artifacts.
