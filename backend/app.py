import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from blueprints.pokemons import pokemons_bp
from db import db

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ALEMBIC_CONFIG"] = os.path.join(app.root_path, "migrations/alembic.ini")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/jasim/PycharmProjects/Pokeman/backend/poke.db'

# Initialize and associate SQLAlchemy with the Flask app
db.init_app(app)

# Import Migrate after initializing db
migrate = Migrate(app, db)

app.register_blueprint(pokemons_bp)

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()

    app.run(debug=True)
