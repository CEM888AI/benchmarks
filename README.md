# ⚡ CEM888.AI — Sovereign Memory Benchmarks

**The highest verified memory retrieval scores in open-source AI. Built solo. No funding. No cloud.**

---

## 🏆 Scores at a Glance

| Benchmark | CEM888.AI | Closest Competitor | Delta |
|-----------|-----------|-------------------|-------|
| **AR Memory Retrieval** | **99.9%** | Mem0 LongMemEval: 93.4% | **+6.5%** |
| **BEAM 10M-token** | **78.2%** | Mem0 BEAM 1M: 70.1% | **+8.1% (at 10x context)** |
| **Vetta BEAM 10M** | **77.2%** | Hindsight (honest): 64.1% | **+13.1%** |

> *Mem0 raised $24M for 93.4%. We built 99.9% alone in Florida.*

---

## 🔬 What We Test

### AR (Accurate Retrieval)
- 2,000 questions across diverse memory types
- `substring_exact_match` — the official benchmark metric
- **1,998/2,000 correct** — real retrieval, no answer-key leakage
- [Full results →](AR-Results-99.9pct.md)

### BEAM (Beyond a Million Tokens)
- 10M-token conversations — the hardest long-context memory test in existence
- 200 questions across 10 categories
- Honest retrieval only — no `source_chat_ids`, no rubric copying
- [CEM results →](CEM-BEAM-Honest-78.2pct.md) | [Vetta results →](Vetta-BEAM-Honest-77.2pct.md)

---

## 🧠 Architecture

This isn't a vector DB with a pretty API. This is a **5-layer tree-native memory OS**:

```
Layer 1 — Session Memory (active context routing)
Layer 2 — Episodic Memory (timestamped event chains)  
Layer 3 — Semantic Memory (concept trees)
Layer 4 — Procedural Memory (skill execution)
Layer 5 — Sovereign Vault (credential-blind, local-first)
```

- **Runs locally.** No cloud. No vendor lock-in. No API costs.
- **Makes any model smarter.** DeepSeek, Qwen, Claude — the harness amplifies all of them.
- **Built on Hermes Agent** by Nous Research.
- **Gets better the longer it runs.** Tree-native architecture self-organizes.

---

## 📊 Competition

| System | AR Score | BEAM Score | BEAM Context | Funding |
|--------|----------|------------|-------------|---------|
| **CEM888.AI** | **99.9%** | **78.2%** | **10M tokens** | $0 |
| Mem0 | 93.4% | 70.1% | 1M tokens | $24M |
| Hindsight | — | 64.1% | 10M tokens | — |
| agentmemory V4 | 96.2%* | — | — | $0 |

*\*LongMemEval score — different benchmark, included for reference*

---

## 🚀 Quick Start

```bash
git clone https://github.com/CEM888AI/benchmarks.git
```

Raw data available:
- `beam_question_contexts.json` — full BEAM test corpus
- `beam-full-results.html` — interactive results viewer
- `vetta_beam_v9_results.jsonl` — per-question breakdown

---

## 🔗 Links

- [CEM888.AI](https://cem888.ai) — main site
- [@CEM888AI](https://github.com/CEM888AI) — GitHub org
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — the platform we're built on

---

**Built by Chandler Morone. Ocala, FL. No team. No investors. Just better architecture.**

⭐ **Star this repo if you believe sovereign AI wins.**
