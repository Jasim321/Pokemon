import csv

from decorators.pagination import paginate
from flask import jsonify
from flask_restful import Resource
from models import Pokemon
from schemas import PokemonSchema


class PokemonsController(Resource):
    def post(self):
        csv_path = "backend/pokemons.csv"

        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                name = row['Name']
                base_experience = row['BaseExperience']
                height = int(row['Height'])
                weight = int(row['Weight'])
                image_url = row['ImageURL']
                pokemon = Pokemon.create(
                    name=name,
                    base_experience=base_experience,
                    height=height,
                    weight=weight,
                    image_url=image_url
                )
            if pokemon:
                return jsonify(message="Successfully Created")

    @paginate(model=Pokemon, schema_class=PokemonSchema,
              sortable_fields=['name', 'base_experience', 'height', 'weight'])
    def get(self, pagination_result):
        return jsonify(pagination_result)
