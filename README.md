# 🔬 LLM Output Risk & Hallucination Validation Framework
### Google Gemini · Financial Services · MRMG · SR 11-7 / CFPB UDAAP Aligned

---

## What This Does

Banks deploying LLMs for customer-facing financial guidance face a gap: traditional model
validation frameworks (SR 11-7) were not designed for generative AI. This project fills
that gap with a practical validation suite that tests a Gemini-powered financial assistant
across four risk dimensions that regulators care about.

---

## Four Validation Tests

| Test | What it measures | Risk threshold |
|---|---|---|
| **Hallucination Test** | Factual accuracy on 18 financial Q&A with ground truth | < 5% hallucination rate |
| **Consistency Test** | Answer stability across 5 paraphrases of same question | Consistency score > 0.70 |
| **Adversarial Test** | Resistance to misleading prompt framing | < 10% vulnerability rate |
| **UDAAP Audit** | Deceptive / abusive language pattern detection | 0 high-risk outputs |

---

## Setup & Run

```bash
# 1. Install dependency
pip install -r requirements.txt

# 2. Set your Gemini API key (get one free at https://aistudio.google.com/app/apikey)
export GEMINI_API_KEY="your-key-here"

# 3. Run the full validation
python main.py
```

Output files:
- `mrm_llm_validation_report.html` — full MRM report (open in browser)
- `validation_results.json` — raw results for further analysis

---

## Output Files

### `mrm_llm_validation_report.html`
A professional HTML report including:
- Executive summary with risk score and rating
- Key findings with severity levels (CRITICAL / WARNING / PASS)
- Detailed results for all 4 test suites
- Conditions for production deployment
- Recommended guardrails

### `validation_results.json`
Structured JSON with all raw results including individual question responses —
useful for further quantitative analysis in notebooks.

---

## Test Dataset

`financial_qa.json` contains 20 curated financial Q&A covering:
- APR / interest rate calculations
- CARD Act regulatory requirements (grace periods, rate change notice, payment allocation)
- Fair Credit Billing Act (dispute timelines, fraud liability)
- UDAAP-risk scenario prompts
- Consumer guidance accuracy (credit utilization, minimum payments)
- Mathematical accuracy (balance transfer fees, foreign transaction calculation)

---

## Technical Design

**Hallucination Tester:** Keyword matching against verified ground truth + fallback semantic similarity  
**Consistency Tester:** Pairwise string similarity (difflib) across 5 paraphrase templates  
**Adversarial Tester:** Correction signal detection — does the model push back on false premises?  
**UDAAP Auditor:** Regex pattern matching against CFPB-defined deceptive/abusive language categories  

---

## Regulatory Context

- **SR 11-7** — Federal Reserve Model Risk Management: conceptual soundness, ongoing monitoring
- **CFPB UDAAP Guidance** — Unfair, Deceptive, or Abusive Acts or Practices
- **OCC 2011-12** — Supervisory guidance on model validation and governance

---

## Portfolio Notes

This project is rare in ML portfolios because it validates AI rather than building it.
It demonstrates:
- Independent model validation mindset (MRMG core competency)
- Awareness of emerging regulatory requirements for GenAI
- Applied risk framework design in a domain where no standard exists yet
- Quantitative scoring of qualitative risk dimensions
