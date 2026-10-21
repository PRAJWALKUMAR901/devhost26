# PondGuard — Aquaculture Early-Warning Prototype

A software-only Streamlit prototype for an explainable pond water-quality alert dashboard.

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `streamlit run app.py`

## What it does
- Takes dissolved oxygen, temperature, and pH readings.
- Accepts a previous reading to show simple trends.
- Produces an illustrative risk score and explains which rules contributed.
- Displays a small history table and trend charts.

## Important limitations
- This is a demo baseline, not a trained ML model.
- Thresholds and scores are illustrative and must not be treated as validated aquaculture advice.
- Validate thresholds with reliable domain references and an aquaculture expert.
- For a real evaluation, use a documented dataset and test on held-out data; report false alarms and missed risky events.
