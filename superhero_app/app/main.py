from fastapi import FastAPI, Depends, Request, Form, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, seeder
import os

app = FastAPI(title="Superhero App")

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Seed database on startup
@app.on_event("startup")
def on_startup():
    db = database.SessionLocal()
    token = os.getenv("SUPERHERO_API_TOKEN")
    seeder.seed_db(db, token)
    db.close()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, search: str = None, db: Session = Depends(get_db)):
    heroes = crud.get_superheroes(db, search=search)
    return templates.TemplateResponse("index.html", {"request": request, "heroes": heroes, "search": search})

@app.get("/hero/{hero_id}", response_class=HTMLResponse)
async def read_hero(request: Request, hero_id: int, db: Session = Depends(get_db)):
    hero = crud.get_superhero(db, hero_id)
    return templates.TemplateResponse("detail.html", {"request": request, "hero": hero})

@app.post("/favorites/add", response_class=HTMLResponse)
async def add_fav(request: Request, hero_id: int = Form(...), db: Session = Depends(get_db)):
    # Assuming user_id 1 (admin) for simplicity as no auth is implemented
    user = crud.get_user_by_username(db, "admin")
    if user:
        crud.add_favorite(db, user.id, hero_id)
    return RedirectResponse(url=f"/hero/{hero_id}", status_code=303)

@app.get("/favorites", response_class=HTMLResponse)
async def read_favorites(request: Request, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, "admin")
    favorites = crud.get_favorites(db, user.id) if user else []
    return templates.TemplateResponse("favorites.html", {"request": request, "favorites": favorites})

@app.get("/team", response_class=HTMLResponse)
async def read_team(request: Request, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, "admin")
    teams = crud.get_teams(db, user.id) if user else []
    return templates.TemplateResponse("team.html", {"request": request, "teams": teams})

@app.post("/team/create", response_class=HTMLResponse)
async def create_team_route(request: Request, name: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, "admin")
    # For now, just create a random team or empty one. 
    # Logic for "Recommendation" implies backend logic to pick heroes.
    # Let's pick 5 random good/bad mix for "Balanced" recommendation.
    # But for this simple form, we'll just create a placeholder team.
    
    # Recommendation Logic (Simplified)
    heroes = crud.get_superheroes(db, limit=50) # Get a pool
    recommended_ids = [h.id for h in heroes[:5]] # Just take first 5 for now as recommendation

    team_data = schemas.TeamCreate(name=name, description=description, hero_ids=recommended_ids)
    crud.create_team(db, team_data, user.id)
    return RedirectResponse(url="/team", status_code=303)
