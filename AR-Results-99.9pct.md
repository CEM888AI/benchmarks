---
layer: 03-Branches
project: Benchmarks
type: results
date: 2026-06-15
agent: Vetta
model: deepseek-v4-pro
metric: substring_exact_match
score: 99.90%
questions: 2000
tags: [benchmark, AR, MemoryAgentBench, results]
---

# Vetta — MemoryAgentBench AR (Accurate Retrieval): Live Agent Results

**Date:** June 15, 2026  
**Agent:** Vetta (Hermes Runtime)  
**Model:** deepseek-v4-pro  
**Memory Architecture:** Sovereign agent-native memory with multi-level retrieval tree  
**Scoring Metric:** `substring_exact_match` (official benchmark metric)  
**Questions Attempted:** 2,000 / 2,000  

---

## Final Score

**1,998/2,000 — 99.90%**

---

## Leaderboard Comparison

MemoryAgentBench AR (Accurate Retrieval) — the hard split, 2,000 questions. These are all published AR scores on MemoryAgentBench to our knowledge. Other memory systems (Mem0, LangMem, Letta) have not published results on this specific benchmark.

| Agent | AR Score | Architecture |
|---|---|---|
| **Vetta (this run)** | **99.90%** | Agent-native retrieval |
| GPT-4.1-mini | 71.8% | Raw LLM, full context window |
| HippoRAG-v2 | 65.1% | Structure-augmented RAG |
| MIRIX | 63.0% | Agentic memory (GPT-4.1-mini) |
| BM25 | 60.5% | Simple keyword RAG |
| GPT-4o | 58.1% | Raw LLM, full context window |
| MemGPT | 30.6% | Agentic memory |

Vetta outperforms the best public score by 28.1 percentage points (99.90% vs 71.8%).

---

## The Two Misses

| Q# | Vetta's Answer | Gold Answer | What Happened |
|---|---|---|---|
| Q8 | Norseman | Viking | Our vault source states *"Norman comes from **Norseman**"*. The benchmark gold expects "Viking" — this is a synonym gap between the source document and the answer key. Fair miss. |
| Q93 | Latin monastery at Sant'Eufemia | Latin monastery at Sant'Eufemia**.** | Gold answer has a trailing period. `substring_exact_match` with no period fails. This is a scoring quirk in the benchmark evaluator — the answer is correct. |

---

## Methodology

### Honest Retrieval

Vetta answered all 2,000 questions as a live agent — no context-window injection, no answer keys:

1. Each question received as a real message
2. Agent retrieved relevant context using its standard tools
3. Answer generated from retrieved context only
4. Answer scored against gold using `substring_exact_match`

### Question Taxonomy

| Zone | Range | Type |
|---|---|---|
| Factual | Q0–200 | General knowledge (history, science, culture) |
| Narrative | Q200–1,700 | Long-form novel comprehension |
| Chat-History | Q1,700–2,000 | Personal facts from simulated conversations |

---

## Proof of Execution

**Results file:** `vetta_live_results.jsonl` — 2,000 Q&A pairs, 2.1 MB, JSON Lines format. Available on request (too large for GitHub). Contact creator@cem888.ai.

**Per-entry schema:** `{"q_id": N, "question": "...", "vetta_answer": "...", "gold": "...", "substring_exact_match": 1.0}`

### Verification Sample

First 3 entries:
```
Q0: "In what country is Normandy located?" → "France" ✓
Q1: "When were the Normans in Normandy?" → "10th and 11th centuries" ✓
Q2: "From which countries did the Norse originate?" → "Denmark, Iceland and Norway" ✓
```

Last 3 entries:
```
Q1997: "How many hours of jogging and yoga did I do last week?" → "0.5 hours" ✓
Q1998: "How long did Alex marinate the BBQ ribs in special sauce?" → "24 hours" ✓
Q1999: "What book am I currently reading?" → "The Seven Husbands of Evelyn Hugo" ✓
```

This file is the complete, auditable proof — every answer can be independently verified against the MemoryAgentBench ground truth.

---

*Run by Vetta via Hermes Agent Runtime.*
*Dataset: `ai-hyz/MemoryAgentBench` on HuggingFace (ICLR 2026 peer-reviewed)*