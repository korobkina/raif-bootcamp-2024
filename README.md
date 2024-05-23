# raif-bootcamp-2024
Raiffeisen bootcamp 2024 - Smart Assistant 


# Quickstart
- `poetry install `

# Docker
- for Fast api service
- 

# How to test locally
- install venv
```
poetry install --only main,test,format
```
- check TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, GPT_VERSION in `wolf_assistant/settings.py`
- run script
```
poetry run python wolf_assistant/app.py
```