#!/usr/bin/env python3
"""Grade customer-voice agent eval outputs against assertions."""
import json, re, os

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
ITER = os.path.join(WORKSPACE, "iteration-1")

EVALS = [
    {"name": "eval-streaks", "id": 0},
    {"name": "eval-amp-connect", "id": 1},
    {"name": "eval-workout-together", "id": 2},
]

ASSERTIONS = [
    {
        "text": "All 6 personas present",
        "check": lambda t: all(p in t for p in [
            "Power Tracker", "Busy Optimizer", "Guided Explorer",
            "Tech-Savvy Engager", "Self-Directed Builder", "Recovery Seeker"
        ])
    },
    {
        "text": "Correct weight ordering (42% before 20% before 17% before 11% before 6% before 4%)",
        "check": lambda t: bool(re.search(r"42%[\s\S]*20%[\s\S]*17%[\s\S]*11%[\s\S]*6%[\s\S]*4%", t))
    },
    {
        "text": "Weighted verdict present (Positive weight, Blocked weight, Decision)",
        "check": lambda t: all(k.lower() in t.lower() for k in ["Positive weight", "Blocked weight", "Decision"])
    },
    {
        "text": "All 7 rule checks present",
        "check": lambda t: all(r in t for r in [
            "Silent Persona", "Peloton Parity", "NPS Detractor",
            "Onboarding Tax", "Quote or Flag", "Cannibalization", "Mid-Workout Disruption"
        ])
    },
    {
        "text": "Feature type classification (Engagement/Retention/Growth)",
        "check": lambda t: any(f in t for f in ["Engagement", "Retention", "Growth"])
    },
    {
        "text": "Impact Assessment header present",
        "check": lambda t: all(k in t for k in ["Impact Assessment", "Personas served", "Weighted coverage", "Primary beneficiary"])
    },
    {
        "text": "Impact labels present (BLOCKER/STRONG POSITIVE/NEUTRAL/MILD CONCERN)",
        "check": lambda t: any(l in t for l in ["BLOCKER", "STRONG POSITIVE", "NEUTRAL", "MILD CONCERN"])
    },
]

def grade_file(filepath, assertions):
    if not os.path.exists(filepath):
        return [{"text": a["text"], "passed": False, "evidence": "File not found"} for a in assertions]

    with open(filepath) as f:
        content = f.read()

    results = []
    for a in assertions:
        passed = a["check"](content)
        results.append({
            "text": a["text"],
            "passed": passed,
            "evidence": "Found in output" if passed else "NOT found in output"
        })
    return results

for ev in EVALS:
    for variant in ["with_skill", "without_skill"]:
        filepath = os.path.join(ITER, ev["name"], variant, "outputs", "review.md")
        results = grade_file(filepath, ASSERTIONS)

        passed = sum(1 for r in results if r["passed"])
        total = len(results)

        grading = {
            "eval_id": ev["id"],
            "eval_name": ev["name"],
            "variant": variant,
            "pass_rate": passed / total,
            "passed": passed,
            "total": total,
            "expectations": results
        }

        out_dir = os.path.join(ITER, ev["name"], variant)
        with open(os.path.join(out_dir, "grading.json"), "w") as f:
            json.dump(grading, f, indent=2)

        print(f"{ev['name']}/{variant}: {passed}/{total} ({passed/total*100:.0f}%)")

# Aggregate into benchmark.json
print("\n--- Benchmark Summary ---")
benchmark = {"evals": [], "summary": {}}
with_scores = []
without_scores = []

for ev in EVALS:
    eval_data = {"name": ev["name"], "with_skill": {}, "without_skill": {}}
    for variant in ["with_skill", "without_skill"]:
        gpath = os.path.join(ITER, ev["name"], variant, "grading.json")
        with open(gpath) as f:
            g = json.load(f)
        eval_data[variant] = {
            "pass_rate": g["pass_rate"],
            "passed": g["passed"],
            "total": g["total"],
        }
        tpath = os.path.join(ITER, ev["name"], variant, "timing.json")
        if os.path.exists(tpath):
            with open(tpath) as f:
                t = json.load(f)
            eval_data[variant]["tokens"] = t["total_tokens"]
            eval_data[variant]["duration_s"] = t["total_duration_seconds"]

        if variant == "with_skill":
            with_scores.append(g["pass_rate"])
        else:
            without_scores.append(g["pass_rate"])

    benchmark["evals"].append(eval_data)

benchmark["summary"] = {
    "with_skill_avg_pass_rate": sum(with_scores) / len(with_scores),
    "without_skill_avg_pass_rate": sum(without_scores) / len(without_scores),
    "delta": sum(with_scores) / len(with_scores) - sum(without_scores) / len(without_scores),
}

with open(os.path.join(ITER, "benchmark.json"), "w") as f:
    json.dump(benchmark, f, indent=2)

print(f"With agent:    {benchmark['summary']['with_skill_avg_pass_rate']*100:.0f}% avg pass rate")
print(f"Without agent: {benchmark['summary']['without_skill_avg_pass_rate']*100:.0f}% avg pass rate")
print(f"Delta:         +{benchmark['summary']['delta']*100:.0f}pp")
