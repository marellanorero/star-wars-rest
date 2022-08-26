from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    people = db.relationship("Person", cascade="all, delete", secondary="people_user")
    planet = db.relationship("Planet", cascade="all, delete", secondary="planets_user")
    
    def __repr__(self):
        return '<User %r>' % self.username


    def serialize(self):
        return{
            "id" : self.id,
            "username": self.username,
            "email" : self.email
        }

    def serialize_with_favs(self):
        return{
            "id" : self.id,
            "username": self.username,
            "people": self.get_fav_people(),
            "planet": self.get_fav_planets()
        }

    def get_fav_people(self):
        return list(map(lambda person: {"id": person.id, "name": person.name}, self.people))
    
    def get_fav_planets(self):
        return list(map(lambda planet: {"id": planet.id, "name": planet.name}, self.planet))
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Person(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    users = db.relationship("User", cascade="all, delete", secondary="people_user")
    
    def __repr__(self):
        return '<Person %r>' % self.name

    def serialize(self):
        return{
            "id" : self.id,
            "name": self.name,
            "url" : self.url
        }

    def serialize_with_users(self):
        return{
            "id" : self.id,
            "name": self.name,
            "url" : self.url,
            "users": self.get_users()
        }    

    def get_users(self):
        return list(map(lambda user: {"id": user.id, "name": user.name}, self.users))
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Planet(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    users = db.relationship("User", cascade="all, delete", secondary="planets_user")
    

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return{
            "id" : self.id,
            "name": self.name,
            "url" : self.url
        }

    def serialize_with_users(self):
        return{
            "id" : self.id,
            "name": self.name,
            "url" : self.url,
            "users": self.get_users()
        }

    def get_users(self):
        return list(map(lambda user: {"id": user.id, "name": user.name}, self.users))
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class PersonUser(db.Model):
    __tablename__ = 'people_user'
    people_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

class PlanetUser(db.Model):
    __tablename__ = 'planets_user'
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)