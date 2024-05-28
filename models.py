from flask_sqlalchemy import SQLAlchemy;
from dataclasses import dataclass;

db= SQLAlchemy()

@dataclass
class User(db.Model):
    __tablename__= 'user'
    id:int = db.Column(db.Integer, primary_key=True)
    email:str = db.Column(db.String(120), unique=True)
    password:str = db.Column(db.String(80), nullable=False)
    firstname:str = db.Column(db.String(80), nullable=False)
    lastname:str = db.Column(db.String(80),nullable=False)
    username:str = db.Column(db.String(80),  nullable=False)
    wishes = db.relationship('Wishlist', backref='user')
    products= db.relationship('Product', backref='user')
    
    

@dataclass
class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id:int = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id:int = db.Column(db.Integer, db.ForeignKey('product.id'))


@dataclass
class Product(db.Model):
    __tablename__= 'product'
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
 

@dataclass
class Offer(db.Model):
    __tablename__= 'offer'
    id = db.Column(db.Integer, primary_key=True)
    user_id:int = db.Column(db.Integer, nullable=False)
    amount:int = db.Column(db.Integer, nullable=False)
    user_interested:int = db.Column(db.Integer, nullable=False)
    product_id:int = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_offered:int = db.Column(db.Integer, nullable=False)

