from api import api
from flask import Blueprint

from controllers.pokemons import PokemonsController

api.add_resource(PokemonsController, "/pokemons")

pokemons_bp = Blueprint("pokemons", __name__)
api.init_app(pokemons_bp)
