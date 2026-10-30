# Steering — Tech

- Web face: plain HTML, CSS, and JavaScript. No framework, no build step,
  no bundler. Open `index.html` and it runs.
- Python face: Python 3 standard library only. No pip install step.
- Tests: Python unittest, standard library only.
- Data: JSON files under `data/`, each carrying its source and date.
- Comments: every contest code file carries plain-English comments that
  explain what each part does, so a judge can read the code like prose.
- Safety: no network calls from the web app at runtime; the Python
  fetcher and IRC client are opt-in commands, clearly labelled.
