import json
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Person, User, Planet


app = Flask(__name__)
app.url_map.slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)
Migrate(app, db)
CORS(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    people = list(map(lambda person: person.serialize(), people))

    return jsonify(people), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):
 
    person = Person.query.get(id)

    if person is None:
        return jsonify({"msg":"This person doesn't exist"})

    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
 
    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"msg":"This planet doesn't exist"})

    return jsonify(planet.serialize()), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites_people():

    people = User.query.get('people')
    

    if people is None:
        return jsonify({"msg":"Favorite is empty"})

    return jsonify(people.serialize_with_favs()), 200
 

@app.route('/users/favorites/people', methods=['POST'])
def add_person():

    #traigo los datos
    name=request.json.get('name')
    url=request.json.get('url', '')

    #creo el fav
    person = Person()
    person.name = name
    person.url = url
    person.save()

    return jsonify({ "msg": "Favorito agregado" }), 201

@app.route('/users/favorites/planet', methods=['POST'])
def add_planet():

    #traigo los datos
    name=request.json.get('name')
    url=request.json.get('url', '')

    #creo el fav
    planet = Planet()
    planet.name = name
    planet.url = url
    planet.save()

    return jsonify({ "msg": "Favorito agregado" }), 201

@app.route('/users/favorites/people/<int:id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    people = Planet.query.get(people_id)

    people.delete()

    return jsonify({ "msg" : "Favorito Borrado "})

@app.route('/users/favorites/planets/<int:id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    planet = Planet.query.get(planet_id)

    planet.delete()

    return jsonify({ "msg" : "Favorito Borrado "})




if __name__ == '__main__':
    app.run()


