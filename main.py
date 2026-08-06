"""
============================================================
  LLM Output Risk Validation Framework
  Model: Gemini 3.1 Flash-Lite · Domain: Financial Services (India)
  MRMG Validation Framework · RBI Model Risk Circular Aligned

  Usage:
    export GEMINI_API_KEY="your-key-here"
    python main.py

  Output:
    mrm_llm_validation_report.md — open in any Markdown viewer,
    or push straight to GitHub for a rendered report.
============================================================
"""

import os
import json
from datetime import datetime
from validators import run_all_validators, MODEL_NAME
from report_generator import generate_markdown_report


def main():
    print(f"\n{'='*60}")
    print(f"  LLM OUTPUT RISK VALIDATION FRAMEWORK")
    print(f"  Model: {MODEL_NAME} | {datetime.now():%Y-%m-%d %H:%M}")
    print(f"{'='*60}")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n❌ GEMINI_API_KEY not set.")
        print("   export GEMINI_API_KEY='your-key'   (get one free at aistudio.google.com)\n")
        return

    qa_path = os.path.join(os.path.dirname(__file__), "financial_qa.json")
    with open(qa_path, encoding="utf-8") as f:
        qa_data = json.load(f)

    print(f"\n📋 Loaded {len(qa_data)} financial QA test cases")
    print("⏳ Running validation suite — takes 5-8 minutes on the free tier…\n")

    results = run_all_validators(api_key, qa_data)
    h, co, ad, ud = (results["hallucination"], results["consistency"],
                      results["adversarial"], results["udaap"])

    print(f"\n{'─'*60}")
    print(f"  Hallucination  : {h['passed']}/{h['total']} passed  | rate {h['hallucination_rate']:.1%}")
    print(f"  Consistency    : {co['passed']}/{co['total']} passed | avg score {co['avg_consistency']:.3f}")
    print(f"  Adversarial    : {ad['passed']}/{ad['total']} robust | vuln rate {ad['vulnerability_rate']:.1%}")
    print(f"  Fair Practices : {ud['passed']} clean, {ud['warned']} warn, {ud['failed']} fail")
    print(f"{'─'*60}")
    print(f"  OVERALL: {results['overall_rating']}")
    print(f"  SCORE  : {results['overall_risk_score']:.1f} / 100")
    print(f"{'─'*60}\n")

    report_path = "mrm_llm_validation_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(generate_markdown_report(results, MODEL_NAME))

    print(f"📄 Report saved → {report_path}")
    print(f"   Open in any Markdown viewer, or push it straight to GitHub.\n")


if __name__ == "__main__":
    main()
