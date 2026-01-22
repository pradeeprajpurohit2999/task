from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class SuperheroBase(BaseModel):
    name: str
    powerstats: Dict[str, Any]
    biography: Dict[str, Any]
    image_url: str

class SuperheroCreate(SuperheroBase):
    pass

class Superhero(SuperheroBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    favorites: List["Favorite"] = []
    teams: List["Team"] = []

    class Config:
        from_attributes = True

class FavoriteBase(BaseModel):
    superhero_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int
    user_id: int
    superhero: Superhero

    class Config:
        from_attributes = True

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    hero_ids: List[int]

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
