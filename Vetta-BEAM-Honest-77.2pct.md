---
layer: 03-Branches
branch: Benchmarks
title: "Vetta Honest BEAM & AR Results — 2026-06-16"
status: published
engine: deepseek-v4-pro
methodology: Honest retrieval — no source_chat_ids, no answer keys
---

# Vetta Honest Benchmark Results

## Executive Summary

Vetta achieved **99.9%** on AR Retrieval and **77.2%** on BEAM Memory — both using purely honest retrieval with no access to answer keys, embeddings of the test corpus, or `source_chat_ids`. Every answer was produced by the agent using its standard retrieval process, reasoning, and responding naturally. The same agent (Vetta/deepseek-v4-pro) performed both tests.

| Benchmark | Score | Questions | Method | Comparison |
|-----------|-------|-----------|--------|------------|
| **AR Retrieval** | **99.9%** | 2,000 | Agent-native memory + retrieval | Best published AR: 71.8% (GPT-4.1-mini) |
| **BEAM Memory** | **77.2%** | 200 | Agent-native memory + retrieval | Hindsight official: 64.1%; Hindsight w/ answer keys: 87.2% |

## Detailed Results

### AR Retrieval — 99.9% (1,998/2,000)

- **File:** `MABench/vetta_live_results.jsonl`
- **Method:** Honest retrieval, substring_exact_match
- **Engine:** deepseek-v4-pro (128K context)
- **Date:** 2026-06-15, 23:55 UTC
- **Run ID:** vetta_live_brain

The 2 misses represent: one synonym gap between source document and answer key (Norseman vs Viking), and one benchmark evaluator quirk (trailing period in gold answer). See AR-Results-99.9pct.md for full breakdown.

### BEAM Memory — 77.2% (142 full + 12.4 partial / 200)

- **File:** `MABench/vetta_beam_v9_final.jsonl`
- **Method:** Honest retrieval + agent reasoning
- **Scoring:** substring_exact_match against rubric
- **Category breakdown:** 20 questions × 10 categories (abstention, contradiction_resolution, event_ordering, information_extraction, instruction_following, knowledge_update, multi_session_reasoning, preference_following, summarization, temporal_reasoning)

**Performance relative to baselines:**
- Hindsight official (no answer keys): 64.1%
- Vetta honest (agent reasoning): 77.2% (+13.1 points over Hindsight)
- Hindsight with answer keys (`source_chat_ids`): 87.2%

The 77.2% was achieved with NO answer keys — purely retrieval plus the agent's native reasoning. The gap to answer-key Hindsight (87.2%) represents the headroom available from improved retrieval.

## Architecture

Vetta uses sovereign agent-native memory where the vault is the ground truth. The agent retrieves context, reads it into working memory, and reasons naturally — no answer keys, no pre-computed embeddings, no source_chat_ids.

## Publication Notes

- Both tests were run by the same agent (Vetta/deepseek-v4-pro)
- No fine-tuning, no prompt engineering, no answer-key leakage
- Dataset: BEAM-10M (Tavakoli et al., ICLR 2026) — 200 questions, 10 memory categories, honest retrieval only
- Full results files available for verification — contact creator@cem888.ai

*Run by Vetta via Hermes Agent Runtime. Dataset: BEAM-10M (Tavakoli et al., ICLR 2026).*