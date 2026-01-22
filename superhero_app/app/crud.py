from sqlalchemy.orm import Session
from . import models, schemas
import json

def get_superhero(db: Session, superhero_id: int):
    return db.query(models.Superhero).filter(models.Superhero.id == superhero_id).first()

def get_superheroes(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Superhero)
    if search:
        query = query.filter(models.Superhero.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def create_superhero(db: Session, superhero: schemas.SuperheroCreate):
    db_superhero = models.Superhero(**superhero.dict())
    db.add(db_superhero)
    db.commit()
    db.refresh(db_superhero)
    return db_superhero

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.username + "notreallyhashed"
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def add_favorite(db: Session, user_id: int, superhero_id: int):
    db_favorite = models.Favorite(user_id=user_id, superhero_id=superhero_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def get_favorites(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()

def create_team(db: Session, team: schemas.TeamCreate, user_id: int):
    # hero_ids is a list of methods, but we store it as JSON in SQLite for simplicity in this model
    db_team = models.Team(
        name=team.name,
        description=team.description,
        user_id=user_id,
        hero_ids=team.hero_ids
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session, user_id: int):
    return db.query(models.Team).filter(models.Team.user_id == user_id).all()
