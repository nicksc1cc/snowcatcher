# Traveller question audits

`question_bank.py` holds 199 traveller questions with stable IDs, written as templates so the same bank serves every country. Run it to regenerate `question_bank.json`.

Each country has its own folder with:

- `01_inventory.md`: what the page contains now and where each figure comes from
- `score.py`: coverage scores (0 to 4), confidence and evidence for that country's page
- `coverage.csv` and `coverage.json`: the register, one row per question
- `03_gap_report.md`: gaps grouped into page additions, in priority order

Score scale: 0 not answered; 1 passing mention or unsupported; 2 partial; 3 useful, evidenced, with a clear implication; 4 strong comparative answer with trade offs and links. Confidence is recorded separately from score.
