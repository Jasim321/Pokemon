from flask_marshmallow import Marshmallow


ma = Marshmallow()


class PokemonSchema(ma.Schema):

    class Meta:
        fields = (
            "id",
            "name",
            "base_experience",
            "height",
            "weight",
            "image_url"
        )
