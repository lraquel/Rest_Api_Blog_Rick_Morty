"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Favoritos_Personajes
#from models import Person

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rickmorty.db'
db.init_app(app)

MIGRATE = Migrate(app, db)

# generating all your endpoints
@app.route('/')
def home():
    return "Base Datos Rick and Morty"


#Create new User
@app.route('/users', methods=['POST'])
def new_user():
    user = User()
    user.name = request.json.get('name')
    user.lastname = request.json.get('lastname')
    user.username = request.json.get('username')
    user.email = request.json.get('email')
    user.password = request.json.get('password')

    db.session.add(user)
    db.session.commit()

    return "user created"

#Create new Character
@app.route('/character', methods=['POST'])
def new_character():
    character = Character()
    character.name = request.json.get('name')
    character.status = request.json.get('status')
    character.gender = request.json.get('gender')
    character.species = request.json.get('species')
    character.origin = request.json.get('origin')
    character.image = request.json.get('image')

    db.session.add(character)
    db.session.commit()

    return "character create"

#Create new Favorite
@app.route('/favorite', methods=['POST'])
def new_favorite():
    favorite = Favoritos_Personajes()
    favorite.user_id= request.json.get('user_id')
    favorite.personaje_id = request.json.get('personaje_id')

    db.session.add(favorite)
    db.session.commit()

    return "saved favorite"


#Read Users
@app.route('/users/list', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.serialize())
    return jsonify(result), 200
    
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is not None:
        return jsonify(user.serialize())
    else:
        return jsonify("not found"), 404

#Read Characters
@app.route('/character/list', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    result = []
    for character in characters:
        result.append(character.serialize())
    return jsonify(result), 200
    
@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get(id)
    if character is not None:
        return jsonify(character.serialize())
    else:
        return jsonify("not found"), 404

#Read Favorite
@app.route('/favorites/list', methods=['GET'])
def get_favorites():
    favorites = Favoritos_Personajes.query.all()
    result = []
    for favorite in favorites:
        result.append(favorite.serialize())
    return jsonify(result), 200
    
@app.route('/favorite/<int:id>', methods=['GET'])
def get_favorite(id):
    favorite = Favoritos_Personajes.query.get(id)
    if favorite is not None:
        return jsonify(favorite.serialize())
    else:
        return jsonify("not found"), 404    

#update/delete Users
@app.route('/users/<int:id>', methods=['PUT', 'DELETE'])
def update_user(id):
    user = User.query.get(id)
    if user is not None:
        if request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()

            return jsonify(" "), 204
        else:
            user.name = request.json.get('name')
            user.lastname = request.json.get('lastname')
            user.username = request.json.get('username')
            user.email = request.json.get('email')
            user.password = request.json.get('password')
            db.session.commit()

            return jsonify("updated user"), 200
        
    return jsonify("not found"), 404    

#update/delete Characters
@app.route('/character/<int:id>', methods=['PUT', 'DELETE'])
def update_character(id):
    character = Character.query.get(id)
    if character is not None:
        if request.method == "DELETE":
            db.session.delete(character)
            db.session.commit()

            return jsonify(" "), 204
        else:
            character.name = request.json.get('name')
            character.status = request.json.get('status')
            character.gender = request.json.get('gender')
            character.species = request.json.get('species')
            character.origin = request.json.get('origin')
            character.image = request.json.get('image')
            db.session.commit()

            return jsonify("updated character"), 200
        
    return jsonify("not found"), 404  

#update/delete Favorites
@app.route('/favorite/<int:id>', methods=['PUT', 'DELETE'])
def update_favorite(id):
    favorite = Favoritos_Personajes.query.get(id)
    if favorite is not None:
        if request.method == "DELETE":
            db.session.delete(favorite)
            db.session.commit()

            return jsonify(" "), 204
        else:
            favorite.user_id = request.json.get('user_id')
            favorite.personaje_id = request.json.get('personaje_id')

            db.session.commit()

            return jsonify("updated favorite"), 200
        
    return jsonify("not found"), 404  








#@app.route('/user', methods=['GET'])
#def handle_hello():

 #   response_body = {
  #      "msg": "Hello, this is your GET /user response "
   # }

    #return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
