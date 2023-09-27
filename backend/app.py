from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from blueprints.pokemons import pokemons_bp
from db import db

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/pokemon'

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(pokemons_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
