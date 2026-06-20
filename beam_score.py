#!/usr/bin/env python3
"""
BEAM Benchmark Scorer — Substring + Word-Overlap scoring.
Reproduced from the original /tmp/beam_score.py that was lost to /tmp wipe.

Scoring rules:
1. Substring match: rubric item appears in answer → 1 point
2. Fallback word overlap: ≥60% word overlap → 1 point  
3. Multi-rubric items: ≥80% items match → full credit, ≥40% → half credit
4. Punctuation-insensitive word comparison
"""
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
    print(f"BEAM SCORING RESULTS")
    print(f"{'='*50}")
    print(f"Overall: {overall:.1f}% ({total_raw}/{total_max})")
    print(f"Questions: {len(results)}")
    print(f"\nCategory Breakdown:")
    for cat in sorted(category_scores.keys()):
        s = category_scores[cat]
        pct = (s['raw'] / s['max'] * 100) if s['max'] else 0
        print(f"  {cat:30s}: {pct:5.1f}% ({s['raw']}/{s['max']})")
    
    return output

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: beam_score.py <answers.jsonl> <rubrics.json> [output.json]")
        sys.exit(1)
    
    answers = sys.argv[1]
    rubrics = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None
    score_all(answers, rubrics, output)
