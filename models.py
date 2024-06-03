from flask_sqlalchemy import SQLAlchemy;
from dataclasses import dataclass;

db= SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), nullable=False)
    firstname= db.Column(db.String(80), nullable=False)
    lastname= db.Column(db.String(80),nullable=False)
    username= db.Column(db.String(80),  nullable=False)
    wishes = db.relationship('Wishlist', backref='user')
    products= db.relationship('Product', backref='user')
    
    def __repr__(self):
        return f'<User {self.email}>'
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

class Publication(db.Model):
    __tablename__= 'publication'
    id = db.Column(db.Integer, primary_key=True)
    value= db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    state = db.Column(db.Boolean, nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    wishes = db.relationship('Wishlist', backref='publication') 

@dataclass
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name:str = db.Column(db.String(200), nullable=False)
    photo:str = db.Column(db.String(200),nullable=False)
    product_info:str = db.Column(db.String(400),nullable=False )
    brand:str = db.Column(db.String(200),nullable=False)
    state:bool = db.Column(db.Boolean, nullable=False)
    category_id:int= db.Column(db.Integer, nullable=False)
    price:int =db.Column(db.Integer, nullable=False)
    user_id:int = db.Column(db.Integer, db.ForeignKey('user.id'))
    offers= db.relationship('Offer', backref='product')
    publications=db.relationship('Publication', backref='product')


class Offer(db.Model):
    __tablename__= 'offer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Boolean, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    


