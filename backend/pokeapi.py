import requests

from app import app
from backend.models.pokemon import db, Pokemon


def fetch_and_store_data():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url)
    data = response.json()

    for entry in data['results']:
        pokemon_data = requests.get(entry['url']).json()
        pokemon = Pokemon(
            name=pokemon_data['name'],
            base_experience=pokemon_data['base_experience'],
            height=pokemon_data['height'],
            weight=pokemon_data['weight'],
            image_url=pokemon_data['sprites']['front_default']
        )
        db.session.add(pokemon)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    fetch_and_store_data()
