# CEM888 — Benchmark Evidence

> **Supporting evidence for [CEM888](https://github.com/CEM888AI/cem888).**
>
> CEM888 is a local-first state and control runtime for AI agents. This repository publishes benchmark artifacts, scoring detail, and explicit limitations. It is an evidence archive, not the production runtime.

## Canonical published results

| Benchmark | Published result | Date | Evidence status |
|---|---:|---|---|
| MemoryAgentBench — Accurate Retrieval (AR) | **99.90% (1,998/2,000)** | 2026-06-15 | TESTED |
| BEAM-10M | **77.2%** | 2026-06-16 | TESTED / scorecard arithmetic independently checkable |
| LoCoMo | **85.8% F1** | 2026-06-07 | TESTED; reverified 2026-06-23 |

These are separate benchmarks and should not be compared as if they measure the same capability.

## BEAM-10M — canonical public score: 77.2%

The **only canonical public CEM888 BEAM-10M score is 77.2%**, produced by Vetta using deepseek-v4-pro on the 200-question BEAM-10M benchmark.

**Method:** live-agent retrieval and answering through the normal CEM888 memory path, with no answer-key access or `source_chat_ids` supplied to the agent.

**Public artifact:** [Vetta-BEAM-Honest-77.2pct.md](./Vetta-BEAM-Honest-77.2pct.md)

**Scorecard check:**

```bash
git clone https://github.com/CEM888AI/benchmarks.git
cd benchmarks
python beam_score.py --check vetta_beam_v9_results.jsonl
```

Expected output:

```text
Overall: 77.2% (154.4/200)
```

### What the public check proves

The shipped scorecard is internally consistent and the reported aggregate follows from the published per-question results.

### What it does not prove

This repository does **not** fully recreate the original live-agent generation environment, model/runtime configuration, or retrieval state. Those conditions are documented in the run write-up but are not independently reconstructed by `--check`.

Future BEAM numbers do **not** replace 77.2% publicly unless they ship with a complete per-question artifact, frozen methodology, scorer, date, model/runtime identity, and enough evidence to support the stronger claim.

## MemoryAgentBench — Accurate Retrieval

2,000-question hard split from MemoryAgentBench (ICLR 2026), scored with the benchmark's `substring_exact_match` metric.

**CEM888 result: 99.90% (1,998/2,000).**

Run detail and verification sample: [AR-Results-99.9pct.md](./AR-Results-99.9pct.md)

**Limit:** this is a benchmark-specific retrieval result. It is not a claim that every CEM888 task, memory operation, or runtime behavior is 99.9% accurate.

## LoCoMo

199-question conversational-memory evaluation spanning single-hop, multi-hop, temporal, adversarial, and open-domain questions.

**Overall: 85.8% F1.**

Full detail: [locomo-results.md](./locomo-results.md)

This result is presented standalone. It is not claimed as a current category-leading score.

## Raw/public artifacts

- `AR-Results-99.9pct.md` — MemoryAgentBench AR result and verification sample
- `Vetta-BEAM-Honest-77.2pct.md` — canonical BEAM-10M result
- `vetta_beam_v9_results.jsonl` — published BEAM per-question scorecard
- `vetta_live_results.jsonl` — retained live-result artifact
- `beam_question_contexts.json` / `beam_score.py` — BEAM corpus/scoring utilities
- `beam-full-results.html` — result viewer
- `locomo-results.md` — LoCoMo result breakdown

## Evidence policy

Public benchmark claims must state:

- the benchmark and version/split where known;
- run date;
- model/provider identity;
- scoring method;
- the artifact supporting the number;
- what can and cannot be independently reproduced.

Experimental or exploratory runs may inform engineering, but they do not become public headline numbers until they satisfy the evidence requirements above.

---

**CEM888** — local-first state & control runtime underneath AI agents.

[⭐ CEM888](https://github.com/CEM888AI/cem888) · [cem888.ai](https://cem888.ai) · [Engineering case studies](https://github.com/CEM888AI/runtime-case-studies) · creator@cem888.ai
