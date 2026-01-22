# Superhero Web App

A FastAPI-based web application to browse superheroes, view details, and create teams.

## Features
- Browse a list of superheroes (seeded from API or mock data).
- View detailed stats and biography.
- Search for superheroes.
- Add superheroes to favorites.
- Generate balanced teams (simple logic implemented).

## Tech Stack
- **Backend**: Python (FastAPI), SQLAlchemy (SQLite).
- **Frontend**: Jinja2 Templates, Vanilla CSS.
- **Containerization**: Docker, Docker Compose.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed.

### Run with Docker
1. Clone the repository (if applicable) or navigate to the project directory.
2. (Optional) Set your Superhero API token in `.env` or `docker-compose.yml`.
   ```bash
   export SUPERHERO_API_TOKEN=your_token_here
   ```
3. Run the application:
   ```bash
   docker-compose up --build
   ```
4. Access the app at `http://localhost:8000`.

### Run Locally (without Docker)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Access at `http://localhost:8000`.

## Notes
- The database is a local SQLite file `superhero.db`.
- On first run, the database is seeded with mock data if no API token is provided.
- Default admin user is created for handling favorites/teams.
