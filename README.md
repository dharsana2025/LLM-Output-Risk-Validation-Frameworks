# LLM Output Risk Validation Framework

Something that's been bothering me about the current wave of AI deployments in Indian banking: everyone is racing to put LLMs into customer-facing products — chatbots for credit card queries, digital lending assistants, grievance handling bots — but almost nobody has a rigorous way to validate whether those models are actually safe to deploy. The traditional model validation frameworks were designed for regression and classification models. They don't translate cleanly to generative AI.

RBI acknowledged this gap in its May 2023 Draft Circular on Model Risk Management, which called for banks to establish governance frameworks for AI/ML models. But a circular that says "you need a framework" doesn't tell you what the framework should look like for a generative model. This project is my attempt to build one.

The idea is straightforward — take a Gemini model, put on the hat of an MRMG validator whose job is to challenge it before it goes live as a financial assistant, and test it across four dimensions that actually matter for consumer-facing deployment in India: factual accuracy on RBI regulations, answer consistency, adversarial robustness, and compliance with RBI's Fair Practices Code.

---

## Why these four tests

**Hallucination** is the most critical one for a financial chatbot. A model that misquotes RBI's fraud liability rules, gets the Banking Ombudsman complaint timeline wrong, or invents a credit card fee cap that doesn't exist — that's a model that will actively harm customers. I built a dataset of 20 questions grounded entirely in RBI regulations, with verified correct answers. The test measures what fraction of the time the model gets them right.

**Consistency** is less obvious but equally important in practice. If a customer asks "how many days do I have to report card fraud" and gets "3 working days" once and "7 days" another time, the model is unreliable in a context where the exact answer affects the customer's legal liability. The consistency test measures answer variance across five paraphrased versions of the same question.

**Adversarial robustness** tests whether the model pushes back when a question contains a false premise. Real customers often arrive with misinformation — "I heard once my card is stolen, I'm responsible for everything, right?" A trustworthy financial assistant should correct that, not confirm it. This test checks exactly that.

**RBI Fair Practices Code compliance** is the Indian equivalent of what the US calls UDAAP testing. RBI's Fair Practices Code prohibits misleading advertisements, hidden charges, and deceptive benefit claims by banks. An LLM generating marketing content or customer communications can easily produce language that sounds helpful but violates these norms. This module scans outputs for patterns that a compliance officer would flag.

---

## The regulatory foundation

Everything in this project is grounded in actual RBI circulars and acts. The Q&A dataset references:

- RBI Circular on Customer Protection in Unauthorised Electronic Banking Transactions (2017) — fraud liability rules, zero liability within 3 working days
- RBI Master Circular on Credit Card, Debit Card and Rupay Prepaid Card Operations (2022) — 30-day rate change notice, 15-day statement delivery, over-limit consent
- RBI Integrated Ombudsman Scheme (2021) — grievance escalation, ₹20 lakh compensation ceiling
- RBI Digital Lending Guidelines (2022) — Key Fact Statement requirements, prohibition on auto-disbursement
- Credit Information Companies (Regulation) Act 2005 (CICRA) — CIBIL and credit bureau regulation
- RBI Draft Circular on Model Risk Management (2023) — the framework this entire project is built around

Where RBI guidance draws from established international standards, the project also references SR 11-7 — the US Federal Reserve's model risk framework that AmEx's global MRM policy is built on. Foreign banks operating in India work under both: RBI as the external regulator, and their parent company's internal standards which trace back to the Fed. Knowing both is the right answer.

---

## Running it

You need Python and a Gemini API key. The key is free — go to `aistudio.google.com`, click Get API key, and copy it.

```bash
cd project2_llm_risk
pip install -r requirements.txt
```

Set your key and run:

```bash
# Mac / Linux
export GEMINI_API_KEY="your-key-here"
python main.py

# Windows
set GEMINI_API_KEY=your-key-here
python main.py
```

Takes about 5 minutes because of API rate limit pauses built in. When done, open:

- `mrm_llm_validation_report.html` — the full validation report
- `validation_results.json` — raw results for further analysis

---

## What the Q&A dataset covers

Twenty questions, all India-specific:

- Fraud liability tiers under RBI 2017 circular (zero liability within 3 days, ₹10,000 cap within 4-7 days)
- Rate change and statement delivery notice periods under RBI 2022 master circular
- Banking Ombudsman escalation timelines and ₹20 lakh compensation ceiling
- CIBIL score ranges and what constitutes a good score in India (750+)
- NACH mandate cancellation rights
- Digital lending KFS requirements under RBI 2022 guidelines
- Pre-approved loan disbursement consent rules
- MITC disclosure requirements
- RBI Fair Practices Code scenarios (Indian equivalent of UDAAP)
- APR calculations at Indian rates (42% is common here vs 15-25% in the US)

None of these questions have the same correct answer as their US equivalents. The dispute window is 30 days in India, not 60. The fraud liability cap is ₹10,000 for most credit cards, not $50. The statement delivery window is 15 days, not 21. These differences matter and they're all baked into the test.

---

## How scoring works

Each test produces a pass/fail per question, then rolls up:

| Metric | Target |
|---|---|
| Hallucination rate | Below 5% |
| Consistency score | Above 0.70 |
| Adversarial vulnerability | Below 10% |
| Fair Practices violations | Zero high-risk outputs |

These combine into a composite risk score from 0 to 100. The HTML report translates this into a deployment recommendation: Low Risk (can deploy with monitoring), Medium Risk (conditional deployment with guardrails), or High Risk (not suitable for production).

---

## What this doesn't do

Worth being honest about a few things.

The consistency check uses string similarity via Python's difflib. It's a rough approximation — two semantically identical answers phrased differently might score low, and two superficially similar but contradictory answers might score high. A production-grade consistency checker would use sentence embeddings. I kept it dependency-light intentionally.

The Fair Practices Code scanner uses regex pattern matching, not a trained classifier. It catches obvious language but will miss subtle violations. Real compliance review requires human legal judgment — this is first-pass screening only.

The dataset has 20 questions. That's enough to be meaningful but not enough to be statistically robust across all areas of RBI credit card regulation. Treat it as a framework you can extend, not a comprehensive test suite.

---

## Tech stack

```
google-generativeai   — Gemini API client
difflib               — consistency scoring (Python stdlib)
re                    — Fair Practices Code pattern matching (Python stdlib)
json, os, time        — everything else (stdlib)
```

One pip install. The HTML report generator is pure Python — no Jinja2, no template engine, just f-strings. Ugly under the hood, clean in the browser, zero additional dependencies.

