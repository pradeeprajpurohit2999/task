import requests
import os
from sqlalchemy.orm import Session
from . import models, schemas, crud

# Mock data in case API token is missing or fails
MOCK_HEROES = [
    {
        "name": "Batman",
        "powerstats": {"intelligence": 100, "strength": 26, "speed": 27, "durability": 50, "power": 47, "combat": 100},
        "biography": {"full-name": "Bruce Wayne", "alignment": "good", "publisher": "DC Comics"},
        "image": {"url": "https://www.superherodb.com/pictures2/portraits/10/100/639.jpg"}
    },
    {
        "name": "Superman",
        "powerstats": {"intelligence": 94, "strength": 100, "speed": 100, "durability": 100, "power": 100, "combat": 85},
        "biography": {"full-name": "Clark Kent", "alignment": "good", "publisher": "DC Comics"},
        "image": {"url": "https://www.superherodb.com/pictures2/portraits/10/100/791.jpg"}
    },
    {
        "name": "Joker",
        "powerstats": {"intelligence": 100, "strength": 10, "speed": 12, "durability": 60, "power": 43, "combat": 70},
        "biography": {"full-name": "Jack Napier", "alignment": "bad", "publisher": "DC Comics"},
        "image": {"url": "https://www.superherodb.com/pictures2/portraits/10/100/719.jpg"}
    },
    {
        "name": "Deadpool",
        "powerstats": {"intelligence": 69, "strength": 32, "speed": 50, "durability": 100, "power": 100, "combat": 100},
        "biography": {"full-name": "Wade Wilson", "alignment": "neutral", "publisher": "Marvel Comics"},
        "image": {"url": "https://www.superherodb.com/pictures2/portraits/10/100/835.jpg"}
    }
]

def seed_db(db: Session, api_token: str = None):
    # Check if DB is already seeded
    if db.query(models.Superhero).first():
        print("Database already seeded.")
        return

    heroes_data = []

    if api_token:
        print(f"Seeding from API with token: {api_token[:4]}...")
        # Fetch a few heroes. ID 1 to 20 for example.
        for i in range(1, 21):
            try:
                url = f"https://www.superheroapi.com/api.php/{api_token}/{i}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("response") == "success":
                        heroes_data.append(data)
            except Exception as e:
                print(f"Error fetching hero {i}: {e}")
    
    if not heroes_data:
        print("Using mock data for seeding.")
        heroes_data = MOCK_HEROES

    for hero in heroes_data:
        db_hero = models.Superhero(
            name=hero.get("name"),
            powerstats=hero.get("powerstats", {}),
            biography=hero.get("biography", {}),
            image_url=hero.get("image", {}).get("url")
        )
        db.add(db_hero)
    
    # Create a default user
    if not crud.get_user_by_username(db, "admin"):
        crud.create_user(db, schemas.UserCreate(username="admin"))

    db.commit()
    print("Seeding complete.")
