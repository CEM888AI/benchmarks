# CEM888.AI — Memory Benchmarks

CEM888 is a local-first state and continuity runtime for AI agents — memory, identity, and project state that live on your machine and persist across Claude, ChatGPT, Codex, and Copilot.

Public, reproducible memory-retrieval results for CEM888's runtime, run as a live agent — not a static embeddings pipeline — against independent third-party benchmark datasets. Every number below links to its full write-up and raw scoring detail in this repo.

> Part of **[CEM888.AI](https://github.com/CEM888AI)** · flagship overview: **[cem888](https://github.com/CEM888AI/cem888)**

## Results

### MemoryAgentBench — Accurate Retrieval (AR)

2,000-question hard split, ICLR 2026 benchmark ([HUST-AI-HYZ/MemoryAgentBench](https://github.com/HUST-AI-HYZ/MemoryAgentBench); dataset on [HuggingFace](https://huggingface.co/datasets/ai-hyz/MemoryAgentBench)). Scored with the benchmark's own `substring_exact_match` metric.

| Agent | AR score | Architecture |
|---|---|---|
| **CEM888 (Vetta / deepseek-v4-pro)** | **99.90% (1,998/2,000)** | Agent-native retrieval, live |
| GPT-4.1-mini | 71.8% | Raw LLM, full context window |
| HippoRAG-v2 | 65.1% | Structure-augmented RAG |
| MIRIX | 63.0% | Agentic memory (GPT-4.1-mini) |
| BM25 | 60.5% | Simple keyword RAG |
| GPT-4o | 58.1% | Raw LLM, full context window |
| MemGPT | 30.6% | Agentic memory |

Full run detail, both misses explained, and a per-entry verification sample: [AR-Results-99.9pct.md](./AR-Results-99.9pct.md)

**Status: TESTED** — run June 15, 2026, live agent, no answer-key access. Mem0, LangMem, and Letta have not published a result on this specific benchmark, so they aren't included as comparison rows here — see [Notes on comparisons](#notes-on-comparisons).

### BEAM — memory at 10M tokens

200-question benchmark across 10 memory categories at up to 10M tokens of context (BEAM, Tavakoli et al., ICLR 2026) — the hardest published long-context memory test in general use, and the one most funded competitors quote. See [benchmarks.hindsight.vectorize.io](https://benchmarks.hindsight.vectorize.io/) for the wider public leaderboard.

| System | BEAM-10M | Method | Source |
|---|---|---|---|
| **CEM888 (Vetta / deepseek-v4-pro)** | **77.2%** | Honest retrieval, no answer keys | [Vetta-BEAM-Honest-77.2pct.md](./Vetta-BEAM-Honest-77.2pct.md) |
| CEM888 (CEM engine) | 78.2% *(experimental)* | Honest retrieval, no answer keys | [CEM-BEAM-Honest-78.2pct.md](./CEM-BEAM-Honest-78.2pct.md) |
| Exabase M-1 | 68.0% | Honest retrieval, smaller/cheaper model | [exabase.io, Jul 2026](https://exabase.io/blog/exabase-m1-achieves-state-of-the-art-on-beam-benchmark) |
| Hindsight | 64.1% | Honest retrieval | [benchmarks.hindsight.vectorize.io](https://benchmarks.hindsight.vectorize.io/) |

**Status:** Vetta's 77.2% is **TESTED** (published June 16, 2026). The CEM engine's 78.2% is **EXPERIMENTAL** — the run is documented and the methodology is honest (its write-up shows the full score-progression across four attempts, including a 100% run that was rejected for crossing into answer-key leakage), but it hasn't been reproduced enough times yet to stand as the settled number. Until it is, 77.2% is the number CEM888 is held to publicly.

Mem0 has not published a BEAM-10M score as of this writing — their public research covers LongMemEval and LoCoMo, not BEAM. See [mem0.ai/research](https://mem0.ai/research) for their current published numbers.

### LoCoMo

199-question long-term conversational memory benchmark, 9-month simulated relationship, 19 sessions ([LoCoMo, Maharana et al., ACL 2024](https://github.com/snap-research/locomo)), scored via the [context-bench](https://github.com/npow/context-bench) framework.

| Category | F1 | Questions |
|---|---|---|
| Single-hop | 92.7% | 32 |
| Adversarial | 89.4% | 47 |
| Open-domain | 88.2% | 13 |
| Multi-hop | 79.0% | 70 |
| Temporal reasoning | 62.8% | 37 |
| **Overall** | **85.8%** | 199 |

Full detail: [locomo-results.md](./locomo-results.md). **Status: TESTED**, run June 7 2026, reverified June 23 2026. Presented standalone: the LoCoMo leaderboard moves fast and other systems have published higher overall scores since this run — this is not presented as a claim of leading the category.

## Notes on comparisons

Different memory benchmarks test different things and are not interchangeable. A 99.9% on MemoryAgentBench AR and a published ~93–94% on Mem0's LongMemEval are not the same measurement, and this repo does not present them as if they were. Where a competitor hasn't published on the exact benchmark CEM888 is scored on, that competitor is left out of the row rather than swapped in from a different test. Where scores exist at different context scales (e.g. BEAM at 1M vs. 10M), the scale is stated next to the number, and every competitor number above links to its primary source.

## Methodology

**Honest retrieval only.** Every run above is a live agent answering questions through its normal retrieval and reasoning path — no pre-computed embeddings of the test corpus, no answer-key access, no rubric-echo scoring. Where a run's methodology allows a legitimate borderline technique (natural phrasing that happens to resemble, but doesn't copy, the scoring rubric), the write-up says so explicitly and shows the rejected alternative that crossed the line. Full methodology is in each individual result file.

## Raw data

```
git clone https://github.com/CEM888AI/benchmarks.git
```

- `AR-Results-99.9pct.md` — MemoryAgentBench AR, full breakdown + verification sample
- `Vetta-BEAM-Honest-77.2pct.md` — BEAM-10M, Vetta run
- `CEM-BEAM-Honest-78.2pct.md` — BEAM-10M, CEM engine run (experimental), including the full honest-score progression and the rejected 100% run
- `locomo-results.md` — LoCoMo, full category breakdown
- `beam_question_contexts.json` / `beam_score.py` — BEAM test corpus and scorer
- `vetta_beam_v9_results.jsonl`, `vetta_live_results.jsonl` — per-question raw results
- `beam-full-results.html` — interactive results viewer

## Verify the published score

```
git clone https://github.com/CEM888AI/benchmarks.git
cd benchmarks
python beam_score.py --check vetta_beam_v9_results.jsonl
```

Recomputes the published Vetta BEAM-10M score from the shipped scorecard. The
`score` column carries fractional per-question credit (e.g. 12/20 rubric items
matched = 0.6), and 77.2% is the unweighted mean across all 200 questions:
142 full-credit + 34 partial (12.4 combined) = 154.4/200.

Expected output: `Overall: 77.2% (154.4/200)`

To score raw answers against the corpus yourself, pass an answers JSONL
(`{qid, answer}` per line) plus the rubric file:

```
python beam_score.py answers.jsonl beam_question_contexts.json
```

## What's being tested

These scores are produced by CEM888's memory runtime, not a standalone retrieval library — a tree-structured memory store (session / episodic / semantic / procedural / vault layers) that a live agent queries as part of normal execution. The implementation is proprietary; what's public here is the methodology, the raw results, and enough of the architecture (in [runtime-case-studies](https://github.com/CEM888AI/runtime-case-studies)) to evaluate whether the results are credible.

## Contact

Built by Chandler Morone. Questions on methodology or raw data: creator@cem888.ai · [cem888.ai](https://cem888.ai)
