# AutoQuizSolver

A Flask-based automated quiz solver for the LLM Data Sourcing & Analysis Challenge.

## Setup
```bash
pip install -r requirements.txt
playwright install --with-deps
export QUIZ_EMAIL="your@email"
export QUIZ_SECRET="your-secret"
python app.py
```

## Test
```bash
curl -X POST https://<your-cloudrun-endpoint>/receive \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","secret":"your-secret","url":"https://tds-llm-analysis.s-anand.net/demo"}'
```

## Deployment
Use Google Cloud Run (HTTPS ready). Dockerfile included.

## License
MIT
