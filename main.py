"""
============================================================
  LLM Output Risk & Hallucination Validation Framework
  Model: Google Gemini · Domain: Financial Services
  MRMG Validation Framework · SR 11-7 / CFPB UDAAP Aligned
============================================================

Tests a production LLM deployment across four risk dimensions:
  1. Hallucination Rate         — factual accuracy on known Q&A
  2. Consistency Score          — answer stability across paraphrases
  3. Adversarial Vulnerability  — robustness to misleading prompts
  4. UDAAP Compliance           — regulatory language audit

Usage:
  export GEMINI_API_KEY="your-key-here"
  python main.py

Output:
  - Console summary
  - mrm_llm_validation_report.html (full MRM report)
  - validation_results.json        (raw results for further analysis)
"""

import os
import json
from datetime import datetime
from validators import run_all_validators
from report_generator import generate_html_report


def print_banner():
    print("\n" + "=" * 60)
    print("  LLM OUTPUT RISK VALIDATION FRAMEWORK")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Model Target: gemini-1.5-flash")
    print(f"  Domain: Financial Services (Credit Card)")
    print("=" * 60)


def print_summary(results: dict):
    h  = results["hallucination"]
    co = results["consistency"]
    ad = results["adversarial"]
    ud = results["udaap"]

    print("\n" + "─" * 60)
    print("  VALIDATION SUMMARY")
    print("─" * 60)

    print(f"\n  [1] Hallucination Test")
    print(f"      Pass: {h['passed']}/{h['total']} | "
          f"Hallucination Rate: {h['hallucination_rate']:.1%}")

    print(f"\n  [2] Consistency Test")
    print(f"      Pass: {co['passed']}/{co['total']} | "
          f"Avg Consistency Score: {co['avg_consistency']:.3f}")

    print(f"\n  [3] Adversarial Robustness Test")
    print(f"      Robust: {ad['passed']}/{ad['total']} | "
          f"Vulnerability Rate: {ad['vulnerability_rate']:.1%}")

    print(f"\n  [4] UDAAP Compliance Audit")
    print(f"      Clean: {ud['passed']} | Warn: {ud['warned']} | "
          f"Fail: {ud['failed']} | Avg Risk Score: {ud['avg_risk_score']:.2f}")

    print(f"\n{'─'*60}")
    print(f"  OVERALL COMPOSITE RISK SCORE: {results['overall_risk_score']:.1f} / 100")
    print(f"  RATING: {results['overall_rating']}")
    print("─" * 60 + "\n")


def main():
    print_banner()

    # ── API Key ──────────────────────────────────────────────────
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n❌ ERROR: GEMINI_API_KEY environment variable not set.")
        print("   Run: export GEMINI_API_KEY='your-key-here'")
        print("   Get your key: https://aistudio.google.com/app/apikey\n")
        return

    # ── Load QA Dataset ──────────────────────────────────────────
    qa_path = os.path.join(os.path.dirname(__file__), "financial_qa.json")
    if not os.path.exists(qa_path):
        print(f"\n❌ ERROR: financial_qa.json not found at {qa_path}")
        return

    with open(qa_path, encoding="utf-8") as f:
        qa_data = json.load(f)

    print(f"\n📋 Loaded {len(qa_data)} financial QA test cases")
    print(f"   Categories: {', '.join(set(q['category'] for q in qa_data))}\n")
    print("⏳ Running validation suite (this will take a few minutes due to API rate limits)…")

    # ── Run All Validators ───────────────────────────────────────
    results = run_all_validators(api_key, qa_data)

    # ── Print Summary ────────────────────────────────────────────
    print_summary(results)

    # ── Save Raw JSON ────────────────────────────────────────────
    json_path = "validation_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"📄 Raw results saved → {json_path}")

    # ── Generate HTML Report ─────────────────────────────────────
    report_path = generate_html_report(results, "gemini-1.5-flash")
    print(f"📊 MRM Report saved  → {report_path}")

    print("\n✅ Open mrm_llm_validation_report.html in your browser for the full report.\n")


if __name__ == "__main__":
    main()
