import os
from flask import Flask,request,jsonify
from models import db, User, Product
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager,create_access_token,get_jwt_identity, jwt_required)

BASEDIR= os.path.abspath(os.path.dirname(__file__))

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///" +os.path.join(BASEDIR,"blog.db")
app.config['JWT_SECRET_KEY']= 'secret-code-01'
db.init_app(app)
Migrate(app,db)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/')
def home():
    return 'hello'
    
@app.route('/user/register', methods=['POST'])
def user_register():
     email= request.json.get('email')
     if email is not None:
        useremail = User.query.filter_by(email=email).first()
        if useremail is not None:
            return jsonify({
                "msg":"Este usuario ya existe"
                }),400      
        else:
            user=User()
            username= request.json.get('username')
            firstname= request.json.get('firstname')
            lastname= request.json.get('lastname')
            password= request.json.get('password')
            
            password_hash= bcrypt.generate_password_hash(password)

            user.password =password_hash
            user.email= email
            user.firstname= firstname
            user.lastname= lastname
            user.username= username
        

            db.session.add(user)
            db.session.commit()

            return jsonify({
                "msg":"user created"
            }), 200

     else:
        return jsonify({
            "msg": "email is required"
        }),400

@app.route('/user/logingoogle',methods=['POST'])
def user_login_google():
    email = request.json.get('email')
    if email is not None:
        user= User.query.filter_by(email=email).first()
        if user is not None:
            access_token= create_access_token(identity=email)
            return jsonify({
                    "user":user.serialize(),
                    "access_token": access_token,
                    "msg":"user login google",
                    "user_id": user.id,
                }),200
        else: 
            user=User()
           
            username= request.json.get('given_name')
            firstname= request.json.get('name')
            lastname= request.json.get('family_name')
            password= request.json.get('exp')
            
            
            password_hash= bcrypt.generate_password_hash(str(password))
            
            user.password =password_hash
            user.email= email
            user.firstname= firstname
            user.lastname= lastname
            user.username= username
        
            db.session.add(user)
            db.session.commit()
            access_token= create_access_token(identity=email)
            return jsonify({
                "msg":"user created",
                "access_token": access_token,
                "user_id": user.id,
            }),200

    else:
        return jsonify({
            "msg": "email needed"
        }),400

@app.route('/products/user/<int:user>',methods=['GET'])
def get_user_products(user):
    products= Product.query.filter_by(user_id=user).all()
    return jsonify(products)


@app.route('/products',methods=['GET'])
def get_allProducts():
    products= Product.query.all()   

    return jsonify(products) ,200

@app.route('/category/products/<int:id>',methods=['GET'])
def get_Products_by_category(id):
    products= Product.query.filter_by(category_id=id).all()

    return jsonify(products) ,200


@app.route('/user/login',methods=['POST'])
def user_loguin():
    print(request.get_json())
    user=User()
    email = request.json.get('email')
    password = request.json.get('password')
    if email is not None:
        user= User.query.filter_by(email=email).first()
        if user is not None:
            is_valid= bcrypt.check_password_hash(user.password,password)
            if is_valid:
                access_token= create_access_token(identity=email)
                return jsonify({
                    "user":user.serialize(),
                    "access_token": access_token,
                    "user_id": user.id,
                    "msg":"user login"
                }),200
            else:
                return jsonify({
                    "msg":"credentials are not valid"
                }),400
        else: 
            return jsonify({
                "msg":"user not found"
            }),400

    else:   
        return jsonify({
            "msg": "email doesnt exist"
        }),400

@app.route('/products/upload', methods=['POST'])
def productUpload():
    product= Product()
    product_category= request.json.get('category_id')
    product_userid= request.json.get('user_id')
    product.state=True
    product_name = request.json.get('name')
    product_price= request.json.get('price')
    product_photo_url= request.json.get('photo')
    product_info= request.json.get('product_info')
    product_brand= request.json.get('brand')
    
    if product_name and product_brand and product_price and product_info and product_photo_url is not None:
        product.name= product_name
        product.price= product_price
        product.photo= product_photo_url
        product.product_info= product_info
        product.brand= product_brand
        product.user_id= product_userid
        product.category_id= product_category
         
        db.session.add(product)
        db.session.commit()
        return jsonify({"msg": "product uploaded"
        }),200

    else:
        return jsonify({
            "msg":"field missing"
        })

    


   


        
@app.route('/users', methods=['GET'])
@jwt_required()
def protected_view():
    response="user logged in    "

    return jsonify(response),200





if __name__  == '__main__': 
    app.run(host='localhost',port=5000,debug=True)