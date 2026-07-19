# QueryGenie — Natural Language to Dashboard Query Assistant

## 1. Setup (5 minutes)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"     # Windows: set ANTHROPIC_API_KEY=your-key-here
python setup_data.py                          # creates hr_data.db
```

## 2. Run locally

```bash
streamlit run app.py
```

It opens at `http://localhost:8501`. Click one of the example question buttons, or type your own.

## 3. Deploy so you have a live link for the panel (optional, ~15 min)

1. Push this folder to a new GitHub repo (include `app.py`, `setup_data.py`, `requirements.txt`, and the generated `hr_data.db`).
2. Go to https://share.streamlit.io, sign in with GitHub, click "New app", point it at the repo and `app.py`.
3. In the app's "Secrets" settings, add:
   ```
   ANTHROPIC_API_KEY = "your-key-here"
   ```
4. Deploy. You'll get a public URL you can open on any device.

If deployment gives you trouble the night before, **skip it** — running locally on your laptop during the demo is completely fine and one less point of failure.

## 4. Demo script (~2-3 minutes)

1. **Frame the problem** (20 sec): "Business users wait on analysts for every ad-hoc question. This removes that bottleneck."
2. **Ask a simple question live**: "Show attrition by department" — point out the chart appears automatically.
3. **Ask a comparison question**: "How does overtime affect attrition?" — shows it handles more than one variable.
4. **Open the "Generated SQL" expander**: "It's not a black box — here's exactly what ran." (Builds panel trust fast.)
5. **Close with the value**: "Every one of these would normally be a ticket in an analyst's queue. Now it's instant."

## 5. Backup plan — do this even if you're confident

APIs and venue wifi fail at the worst times. The night before:
- Run through your 4-5 demo questions and **screen-record the working app** (screen recorder, 2 minutes).
- Take screenshots of each question + chart + generated SQL.
- If live demo breaks, say "Let me show you a recording from testing" and play it — panels respect this far more than a frozen screen.

## 6. If you're really short on time — cut in this order

1. Skip deployment. Demo locally.
2. Skip the "explain result" plain-English summary call (one less API call, one less failure point) — the chart alone still tells the story.
3. Reduce to 3 example questions instead of 5, and only rehearse those.
4. Don't build the `recruiter_performance` table/questions — attrition-by-department and attrition-by-overtime alone make a complete demo.

What you should **not** cut: the safety check (`is_safe_select`) and the "Generated SQL" expander — both take two minutes to keep and are exactly what makes a BI panel trust the tool.
