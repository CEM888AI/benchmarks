#!/usr/bin/env python3
"""
BEAM benchmark verification and raw-answer audit utility.

Two deliberately separate modes live in this file:

1. --check <results.jsonl> verifies a published scorecard. Each row already
   carries fractional per-question credit in "score" plus a human-readable
   "match" fraction such as "12/20". The checker validates those two fields
   agree, rejects duplicate question IDs, reports the scorecard SHA-256, and
   recomputes the published unweighted mean across questions.

2. <answers.jsonl> <rubrics.json> scores raw answers with the simple helper
   implemented below. Each rubric item receives one point for either a
   case-insensitive substring match or >=60% normalized word overlap. The raw
   helper aggregate is rubric-item-weighted.

The raw-answer helper and the published-scorecard checker are not the same
scoring path. A scorecard arithmetic check is not reproduction of the
original live-agent run.
"""
import hashlib
import json, sys, re
from pathlib import Path

def normalize_words(text):
    """Split on whitespace, strip trailing punctuation for comparison."""
    words = text.lower().split()
    return [w.rstrip(',.;:!?"\'') for w in words]

def word_overlap_score(answer, rubric_item):
    """Return fraction of rubric words found in answer."""
    rubric_words = normalize_words(rubric_item)
    answer_words = normalize_words(answer)
    if not rubric_words:
        return 0.0
    matches = sum(1 for rw in rubric_words if rw in answer_words)
    return matches / len(rubric_words)

def substring_match(answer, rubric_item):
    """Check if rubric item text appears as substring in answer (case-insensitive)."""
    return rubric_item.lower().strip() in answer.lower()

def score_answer(answer, rubric_items):
    """
    Score one answer against its rubric items.
    Returns (raw_score, max_score, per_item_scores)
    """
    scores = []
    for item in rubric_items:
        if substring_match(answer, item):
            scores.append(1.0)
        else:
            overlap = word_overlap_score(answer, item)
            scores.append(1.0 if overlap >= 0.6 else 0.0)
    
    if not scores:
        return 0.0, 0, []
    
    raw = sum(scores)
    max_score = len(scores)
    return raw, max_score, scores

def score_all(answers_file, rubrics_file, output_file=None):
    """
    Score all answers against rubrics.
    answers_file: JSONL with {qid, answer}
    rubrics_file: JSON with question_id -> {rubric: [items], category: str}
    """
    # Load rubrics
    if isinstance(rubrics_file, str):
        with open(rubrics_file) as f:
            rubrics = json.load(f)
    else:
        rubrics = rubrics_file

    # Normalize: the shipped corpus (beam_question_contexts.json) is a LIST of
    # {qid, rubric, category, ...} objects; the scorer below expects a dict keyed
    # by str(qid). Accept both shapes so the published pair runs as-is.
    if isinstance(rubrics, list):
        rubrics = {str(q.get('qid')): q for q in rubrics if q.get('qid') is not None}
    
    # Load answers
    answers = {}
    with open(answers_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                # Try to handle multi-JSON lines
                continue
            qid = obj.get('qid') or obj.get('question_id')
            if qid is not None:
                answers[qid] = obj.get('answer', '')
    
    # Score
    results = []
    category_scores = {}
    
    for qid, answer in sorted(answers.items()):
        qid_str = str(qid)
        if qid_str not in rubrics:
            continue
        
        rubric_data = rubrics[qid_str]
        rubric_items = rubric_data.get('rubric', [])
        category = rubric_data.get('category', 'unknown')
        
        raw, max_score, item_scores = score_answer(answer, rubric_items)
        pct = (raw / max_score * 100) if max_score else 0
        
        result = {
            'qid': qid,
            'category': category,
            'answer': answer[:200],
            'raw_score': raw,
            'max_score': max_score,
            'percentage': round(pct, 1),
            'item_scores': item_scores
        }
        results.append(result)
        
        if category not in category_scores:
            category_scores[category] = {'raw': 0, 'max': 0}
        category_scores[category]['raw'] += raw
        category_scores[category]['max'] += max_score
    
    # Summary
    total_raw = sum(r['raw_score'] for r in results)
    total_max = sum(r['max_score'] for r in results)
    overall = (total_raw / total_max * 100) if total_max else 0
    
    summary = {
        'overall_pct': round(overall, 1),
        'total_raw': total_raw,
        'total_max': total_max,
        'questions_scored': len(results),
        'categories': {}
    }
    
    for cat, scores in sorted(category_scores.items()):
        cat_pct = (scores['raw'] / scores['max'] * 100) if scores['max'] else 0
        summary['categories'][cat] = {
            'percentage': round(cat_pct, 1),
            'raw': scores['raw'],
            'max': scores['max']
        }
    
    # Output
    output = {
        'summary': summary,
        'per_question': results
    }
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Results written to {output_file}")
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"BEAM RAW-ANSWER AUDIT RESULTS (RUBRIC-ITEM-WEIGHTED)")
    print(f"{'='*50}")
    print(f"Overall: {overall:.1f}% ({total_raw}/{total_max})")
    print(f"Questions: {len(results)}")
    print(f"\nCategory Breakdown:")
    for cat in sorted(category_scores.keys()):
        s = category_scores[cat]
        pct = (s['raw'] / s['max'] * 100) if s['max'] else 0
        print(f"  {cat:30s}: {pct:5.1f}% ({s['raw']}/{s['max']})")
    
    return output

def verify_scorecard(scorecard_file):
    """
    Verify a published scorecard and recompute its unweighted question mean.

    Required row shape: {qid, category, score, match}. "match" must be a
    fraction such as "12/20"; "score" must equal that fraction within a small
    floating-point tolerance. Duplicate qids are rejected.
    """
    path = Path(scorecard_file)
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()

    total = 0.0
    n = 0
    category_totals = {}
    seen_qids = set()
    errors = []

    for line_number, raw_line in enumerate(payload.decode("utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc}")
            continue

        qid = obj.get("qid")
        if qid is None:
            errors.append(f"line {line_number}: missing qid")
            continue
        if qid in seen_qids:
            errors.append(f"line {line_number}: duplicate qid {qid!r}")
            continue
        seen_qids.add(qid)

        score = obj.get("score")
        match = obj.get("match")
        if not isinstance(score, (int, float)):
            errors.append(f"line {line_number}: missing/non-numeric score")
            continue
        if not isinstance(match, str) or not re.fullmatch(r"\s*\d+\s*/\s*\d+\s*", match):
            errors.append(f"line {line_number}: invalid match fraction {match!r}")
            continue

        numerator_text, denominator_text = match.split("/", 1)
        numerator = int(numerator_text.strip())
        denominator = int(denominator_text.strip())
        if denominator <= 0 or numerator < 0 or numerator > denominator:
            errors.append(f"line {line_number}: impossible match fraction {match!r}")
            continue

        expected_score = numerator / denominator
        # Published scorecards store fractional credit rounded to 2 decimals.
        # Validate against that stored precision rather than the infinite ratio.
        expected_stored_score = round(expected_score, 2)
        if abs(float(score) - expected_stored_score) > 1e-9:
            errors.append(
                f"line {line_number}: score={score!r} does not match "
                f"{match!r} at stored 2-decimal precision ({expected_stored_score:.2f})"
            )
            continue

        total += float(score)
        n += 1
        cat = obj.get("category", "unknown")
        if cat not in category_totals:
            category_totals[cat] = {"sum": 0.0, "n": 0}
        category_totals[cat]["sum"] += float(score)
        category_totals[cat]["n"] += 1

    if errors:
        print("\nBEAM SCORECARD VERIFICATION FAILED")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(2)

    overall = (total / n * 100) if n else 0.0
    print("\n" + "=" * 50)
    print("BEAM SCORECARD VERIFICATION")
    print("=" * 50)
    print(f"Scorecard SHA256: {digest}")
    print(f"Overall: {overall:.1f}% ({total:.1f}/{n})")
    print(f"Questions: {n}")
    print("\nCategory Breakdown:")
    for cat in sorted(category_totals.keys()):
        c = category_totals[cat]
        pct = (c["sum"] / c["n"] * 100) if c["n"] else 0
        print(f"  {cat:30s}: {pct:5.1f}% ({c['n']}q)")
    return {
        "overall_pct": round(overall, 1),
        "total_raw": round(total, 2),
        "questions_scored": n,
        "scorecard_sha256": digest,
    }

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '--check':
        scorecard = sys.argv[2] if len(sys.argv) > 2 else 'vetta_beam_v9_results.jsonl'
        verify_scorecard(scorecard)
    elif len(sys.argv) < 3:
        print("Usage:")
        print("  beam_score.py <answers.jsonl> <rubrics.json> [output.json]   # score raw answers")
        print("  beam_score.py --check <results.jsonl>                        # verify a published scorecard")
        sys.exit(1)
    else:
        answers = sys.argv[1]
        rubrics = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
        score_all(answers, rubrics, output)
