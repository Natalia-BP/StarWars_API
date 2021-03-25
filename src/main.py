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
from models import db, User, Characters, Planet, Fav_Planet, Fav_Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# GET ONE character
# Aqui deben ir solo los msjs de error o de buena respuesta
@app.route('/character/<int:id>', methods=['GET'])
def get_OneCharacter(id):
    getCharacter = Characters.query.filter_by(id=id).first()
    if not getCharacter:
        return jsonify({"404_Msg": "Not found!\nCheck your ID!"}), 400
    else:
        char = getCharacter.serialize()
        return jsonify(char), 200

# GET ALL characters
@app.route('/characters', methods=['GET'])
def get_AllCharacters():
    get_Characters = Characters.query.all()
    if not get_Characters:
        return jsonify({"404_Msg": "Not found"}), 400
    else:
        all_people = list(map(lambda x: x.serialize(), get_Characters))
        return jsonify(all_people), 200

# GET ONE planet
@app.route('/planet/<int:id>', methods=['GET'])
def get_OnePlanet(id):
    get_Planet = Planet.query.filter_by(id=id).first()
    if not get_Planet:
        return jsonify({"404_Msg": "Not found"}), 400
    else:
        one_planet = get_Planet.serialize()
        return jsonify(one_planet), 200

# GET ALL planets
@app.route('/planets', methods=['GET'])
def get_AllPlanets():
    get_Planets = Planet.query.all()
    if not get_Planets:
        return jsonify({"404_Msg": "Not found"}), 400
    else:
        all_planets = list(map(lambda x: x.serialize(), get_Planets))
        return jsonify(all_planets), 200

# GET user's Favorite
@app.route('/users/<int:uid>/favorites', methods=['GET'])
def get_UserFav(uid):
    get_User = User.query.filter_by(uid=uid).first()
    if not get_User:
        return jsonify({"404_Msg": "Not found"}), 400
    else:
        userFavs = get_User.serialize()
        return jsonify(userFavs), 200

# POST new user favorite
@app.route('/users/<int:uid>/favorites', methods=['POST'])
def post_newUserFav(uid):
    #request.getjson es para captar de un formulario del front-end
    get_User = User.query.filter_by(uid=uid).first()
    if not get_User:
        return jsonify({"404_Msg":"User not found, check ID"}), 404

    data = request.get_json()
    request_idChar = data.get("id_Character")
    
    #request_idPlanet = request.get_json("id_Planets")

    if not request_idChar:
    #and not request_idPlanet:
        return jsonify({"400_Msg":"Bad request\nInput a valid character or planet id"}), 400

    if request_idChar:
        valid_Chars = Characters.query.get(request_idChar)
        if not valid_Chars:
            return jsonify({"404_Msg":"Not found\nCharacter id is invalid"}), 404
        else:
            #new_favp = People_Fav(user_id=user_id, people_id=requestId_people)
            new_favChar = Fav_Character(id_Username=uid, id_Character=request_idChar)
            db.session.add(new_favChar)
            db.session.commit()

    #if request_idPlanet:
     #   valid_Planets = Planet.query.filter_by(request_idPlanet).first()
      #  if not valid_Planets:
       #     return jsonify({"404_Msg":"Not found\nPlanet id is invalid"}), 404
        #else:
         #   new_favPlanet = Fav_Planet()
          #  new_favPlanet.id_Username = get_User
           # new_favPlanet.id_Planets = request_idPlanet
            #db.session.add(new_favPlanet)
            #db.session.commit()

    return jsonify({"All_Good":"New fave was added"}), 200

# GET ALL users
@app.route('/users', methods=['GET'])
def get_AllUsers():
    get_Users = User.query.all()
    if not get_Users:
        return jsonify({"404_Msg": "Not found"}), 400
    else:
        all_users = list(map(lambda x: x.serialize(), get_Users))
        return jsonify(all_users), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
