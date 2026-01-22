@echo off
echo Starting Superhero App Locally...
echo Open http://localhost:8000 in your browser.
python -m uvicorn app.main:app --reload
pause
