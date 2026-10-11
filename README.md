# PlantCare Adventure AI 🌿

An open-source outdoor companion for Hacktoberfest 2026 **Touch Grass**: get a short plant/nature mission, put your phone away, then record what you noticed.

## Features
- Ask for outdoor activity, environment, and preferences
- Generate a small mission and list things to look for
- Offline-style checklist for the activity
- Explicit phone-away prompt
- Record a note and optional photo filename
- Save a Plant Adventure Journal entry locally

## Gemma integration
The app includes an isolated adapter for a compatible Gemma inference endpoint. Configure `GEMMA_API_URL` (and optionally `GEMMA_MODEL`) only when you have an endpoint matching the JSON request format in `gemma_client.py`. If no endpoint is configured, the app uses built-in example missions. **The fallback is not model-generated, and this repository does not claim the Gemma endpoint is already live.**

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Journal entries are saved to `data/journal.json` in the working directory.

## Test
```bash
python -m py_compile app.py gemma_client.py
```

## Repository
https://github.com/godGamerz812/Plant-Care-AI
