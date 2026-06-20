# ⚡ CEM888.AI — Sovereign Memory Benchmarks

**The highest verified memory retrieval scores in open-source AI. Built solo. No funding. No cloud.**

---

## 🏆 Verified Scores

| Benchmark | Score | Competitor Best | Delta |
|-----------|-------|-----------------|-------|
| **AR Memory Retrieval** | **99.9%** (1,998/2,000) | Mem0 LongMemEval: 93.4% | **+6.5%** |
| **Vetta BEAM 10M-token** | **77.2%** | Mem0 BEAM 1M: 70.1% | **+7.1% (at 10x context)** |
| CEM BEAM 10M-token | *Reproducing — target 78%+* | Hindsight (honest): 64.1% | *pending* |

> *Mem0 raised $24M for 93.4% LongMemEval. We built 99.9% AR alone in Florida. No team. No funding.*

---

## 🔬 What We Test

### AR (Accurate Retrieval)
- 2,000 questions across diverse memory types
- `substring_exact_match` — the official benchmark metric
- **1,998/2,000 correct** — real retrieval, no answer-key leakage
- [Full results →](AR-Results-99.9pct.md)

### BEAM (Beyond a Million Tokens)
- 10M-token conversations — the hardest long-context memory test in existence
- 200 questions across 10 categories (abstention, contradiction, event ordering, information extraction, instruction following, preference tracking, summarization, temporal reasoning, multi-session reasoning, knowledge update)
- Honest retrieval only — no `source_chat_ids`, no rubric copying
- [Vetta verified results →](Vetta-BEAM-Honest-77.2pct.md)
- CEM BEAM: reproducing now — target 78%+

---

## 🧠 Architecture

Not a vector DB wrapper. A **5-layer tree-native memory OS**:

```
Layer 1 — Session Memory (active context routing)
Layer 2 — Episodic Memory (timestamped event chains)  
Layer 3 — Semantic Memory (concept trees)
Layer 4 — Procedural Memory (skill execution)
Layer 5 — Sovereign Vault (credential-blind, local-first)
```

- **Runs locally.** No cloud. No vendor lock-in. No API costs.
- **Makes any model smarter.** DeepSeek, Qwen, Claude — our harness amplifies all of them.
- **Built on Hermes Agent** by Nous Research.
- **Gets better the longer it runs.** Tree-native architecture self-organizes.

---

## 📊 Competition

| System | AR Score | BEAM Score | BEAM Context | Funding |
|--------|----------|------------|-------------|---------|
| **CEM888.AI (Vetta)** | **99.9%** | **77.2%** | **10M tokens** | $0 |
| Mem0 | 93.4% | 70.1% | 1M tokens | $24M |
| Hindsight | — | 64.1% | 10M tokens | — |

---

## 📁 Raw Data

```bash
git clone https://github.com/CEM888AI/benchmarks.git
```

- `vetta_beam_v9_results.jsonl` — per-question BEAM breakdown (verified)
- `vetta_live_results.jsonl` — live run log
- `beam_question_contexts.json` — full BEAM test corpus
- `beam-full-results.html` — interactive results viewer

---

## 🔗 Links

- [CEM888.AI](https://cem888.ai)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — our platform
- Email: creator@cem888.ai

---

**Built by Chandler Morone. Ocala, FL. No team. No investors. Just better architecture.**

⭐ **Star this repo. Sovereign AI wins.**
