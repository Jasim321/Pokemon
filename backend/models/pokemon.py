from db import db


class Pokemon(db.Model):
    __tablename__ = "pokemons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    base_experience = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.name}"

    @staticmethod
    def create(name, base_experience, height, weight, image_url):
        pokemon = Pokemon(
            name=name,
            base_experience=base_experience,
            height=height,
            weight=weight,
            image_url=image_url
        )
        db.session.add(pokemon)
        db.session.commit()
        return pokemon
