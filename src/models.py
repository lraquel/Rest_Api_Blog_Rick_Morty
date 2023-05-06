from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()


#favoritos_personajes= db.Table(
 #   "favoritos_personajes",
  #  db.Base.metadata,
   # db.Column("user_id", ForeignKey("user.id")),
    #db.Column("character_id", ForeignKey("character.id")),
#)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    lastname = db.Column(db.String(250))
    username = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorito = db.relationship("Favoritos_Personajes")

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'lastname': self.lastname,
            'username': self.username,
            'email': self.email
             }


class Favoritos_Personajes(db.Model):
     __tablename__ = 'favorito_personaje'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     personaje_id = db.Column(db.Integer, db.ForeignKey('character.id'))
     
     def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'personaje_id': self.personaje_id,
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    status = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    species = db.Column(db.String(250))
    origin =  db.Column(db.String(250))
    image = db.Column(db.String(250))
    favorito = db.relationship("Favoritos_Personajes")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'gender': self.gender,
            'species': self.species,
            'origin' : self.origin,
            'image' : self.image,
        }





    





