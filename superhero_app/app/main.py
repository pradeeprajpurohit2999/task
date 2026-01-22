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
async def create_team_route(
    request: Request, 
    name: str = Form(...), 
    description: str = Form(None), 
    strategy: str = Form("random"),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, "admin")
    heroes = crud.get_superheroes(db, limit=200) # Fetch a larger pool

    recommended_ids = []
    
    if strategy == "balanced":
        # Strategy: Mix of Good (2), Bad (2), Neutral/Other (1)
        good = [h for h in heroes if h.biography.get('alignment') == 'good']
        bad = [h for h in heroes if h.biography.get('alignment') == 'bad']
        others = [h for h in heroes if h.biography.get('alignment') not in ['good', 'bad']]
        
        import random
        team_heroes = []
        if len(good) >= 2: team_heroes.extend(random.sample(good, 2))
        else: team_heroes.extend(good)
        
        if len(bad) >= 2: team_heroes.extend(random.sample(bad, 2))
        else: team_heroes.extend(bad)
        
        remaining_needed = 5 - len(team_heroes)
        pool = others + good + bad # Fallback to anyone
        # Remove already selected
        pool = [h for h in pool if h not in team_heroes]
        
        if len(pool) >= remaining_needed:
            team_heroes.extend(random.sample(pool, remaining_needed))
        
        recommended_ids = [h.id for h in team_heroes]

    elif strategy == "power":
        # Strategy: Top 5 by total power stats
        def get_total_power(hero):
            stats = hero.powerstats
            total = 0
            for k, v in stats.items():
                if v and str(v).isdigit():
                    total += int(v)
            return total

        top_heroes = sorted(heroes, key=get_total_power, reverse=True)[:5]
        recommended_ids = [h.id for h in top_heroes]

    else: # Random
        import random
        if len(heroes) >= 5:
            recommended_ids = [h.id for h in random.sample(heroes, 5)]
        else:
            recommended_ids = [h.id for h in heroes]

    team_data = schemas.TeamCreate(name=name, description=description, hero_ids=recommended_ids)
    crud.create_team(db, team_data, user.id)
    return RedirectResponse(url="/team", status_code=303)

@app.get("/hero/{hero_id}/edit", response_class=HTMLResponse)
async def edit_hero_form(request: Request, hero_id: int, db: Session = Depends(get_db)):
    hero = crud.get_superhero(db, hero_id)
    return templates.TemplateResponse("edit.html", {"request": request, "hero": hero})

@app.post("/hero/{hero_id}/edit", response_class=HTMLResponse)
async def update_hero(
    request: Request,
    hero_id: int,
    name: str = Form(...),
    full_name: str = Form(None),
    publisher: str = Form(None),
    alignment: str = Form(None),
    intelligence: int = Form(0),
    strength: int = Form(0),
    speed: int = Form(0),
    durability: int = Form(0),
    power: int = Form(0),
    combat: int = Form(0),
    db: Session = Depends(get_db)
):
    # Construct update data
    # Note: Flattened forms need to be reconstructed into the nested JSON structure expected by the model
    # Powerstats
    powerstats = {
        "intelligence": intelligence,
        "strength": strength,
        "speed": speed,
        "durability": durability,
        "power": power,
        "combat": combat
    }
    
    # Biography updates (partial)
    # Fetch existing to preserve other fields if needed, or just update what we have
    current_hero = crud.get_superhero(db, hero_id)
    biography = current_hero.biography.copy() if current_hero.biography else {}
    biography.update({
        "full-name": full_name,
        "publisher": publisher,
        "alignment": alignment
    })

    update_data = schemas.SuperheroUpdate(
        name=name,
        powerstats=powerstats,
        biography=biography,
        image_url=current_hero.image_url # Keep existing image
    )
    
    crud.update_superhero(db, hero_id, update_data)
    return RedirectResponse(url=f"/hero/{hero_id}", status_code=303)
