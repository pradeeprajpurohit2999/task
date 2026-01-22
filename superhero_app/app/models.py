from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Superhero(Base):
    __tablename__ = "superheroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    powerstats = Column(JSON)  # Store int, str, speed, etc.
    biography = Column(JSON)   # Store full name, alter egos, etc.
    image_url = Column(String)
    
    # Relationships could be added here if needed, e.g. for favorites

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    
    favorites = relationship("Favorite", back_populates="user")
    teams = relationship("Team", back_populates="user")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    superhero_id = Column(Integer, ForeignKey("superheroes.id"))

    user = relationship("User", back_populates="favorites")
    superhero = relationship("Superhero")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String, nullable=True)

    user = relationship("User", back_populates="teams")
    hero_ids = Column(JSON) # Storing list of hero IDs for simplicity
