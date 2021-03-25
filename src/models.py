from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabla PLANETAS
class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(250))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.Integer)
    created = db.Column(db.Date)
    edited = db.Column(db.Date)
    photo = db.Column(db.String(250))
    liked_by_users = db.relationship("Fav_Planet", backref="planet")

    def __repr__(self):
        return '<Planet %r - %r>' % (self.id, self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": f"https://3000-peach-spoonbill-64imvwko.ws-us03.gitpod.io/{self.id}",
            "description": self.description,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created,
            "edited": self.edited,
            "photo": self.photo
        }

#Tabla PERSONAJES
class Characters(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.Date)
    gender = db.Column(db.String(250))
    created = db.Column(db.Date)
    edited = db.Column(db.Date)
    photo = db.Column(db.String(250))
    liked_by_users = db.relationship("Fav_Character", backref="characters")

    def __repr__(self):
        return '<Characters %r - %r>' % (self.id, self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": f"https://3000-peach-spoonbill-64imvwko.ws-us03.gitpod.io/{self.id}",
             "description": self.description,
             "height": self.height,
             "mass": self.mass,
             "hair_color": self.hair_color,
             "skin_color": self.skin_color,
             "eye_color": self.eye_color,
             "birth_year": self.birth_year,
             "gender": self.gender,
             "created": self.created,
             "edited": self.edited,
             "photo": self.photo
        }

#Tabla FAVORITOS PLANETAS
class Fav_Planet(db.Model):
    __tablename__ = "fav_planet"
    id_FavPlanets = db.Column(db.Integer, primary_key=True)
    id_Planets = db.Column(db.Integer, db.ForeignKey("planet.id"))
    id_Username = db.Column(db.Integer, db.ForeignKey("user_table.uid"))

    def serialize(self):
        return {
            "id_FavPlanets": self.id_FavPlanets,
            "id_Planets": self.id_Planets,
            "id_Username": self.id_Username
        }

#Tabla FAVORITOS PERSONAJES
class Fav_Character(db.Model):
    __tablename__ = "fav_character"
    id_FavCharacters = db.Column(db.Integer, primary_key=True)
    id_Character = db.Column(db.Integer, db.ForeignKey("characters.id"))
    id_Username = db.Column(db.Integer, db.ForeignKey("user_table.uid"))

    def serialize(self):
        return {
            "id_FavCharacters": self.id_FavCharacters,
            "id_Character": self.id_Character,
            "id_Username": self.id_Username
        }

# Tabla USUARIOS
class User(db.Model):
    __tablename__ = "user_table"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    prophile_photo = db.Column(db.String(250))
    favorite_planet = db.relationship("Fav_Planet", backref="user_liked_planet")
    favorite_character = db.relationship("Fav_Character", backref="user_liked_character")

    def __repr__(self):
        return '<User %r - %r>' % (self.uid, self.name)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
            "prophile_photo": self.prophile_photo,
            "favorite_planet": list(map(lambda fav_planet: fav_planet.serialize(),self.favorite_planet)),
            "favorite_character": list(map(lambda fav_character: fav_character.serialize(),self.favorite_character))
        }