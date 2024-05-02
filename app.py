import os
from flask import Flask,request,jsonify
from models import db, User
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
    print(request.get_json())
    email = request.json.get('email')
    if email is not None:
        user= User.query.filter_by(email=email).first()
        if user is not None:
            access_token= create_access_token(identity=email)
            return jsonify({
                    "user":user.serialize(),
                    "access_token": access_token,
                    "msg":"user login google"
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
            return jsonify({
                "msg":"user created"
            })

    else:
        return jsonify({
            "msg": "email doesnt exist"
        }),400

@app.route('/user/login',methods=['POST'])
def user_loguin():
    print(request.get_json())
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


@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users= User.query.all()
    users= list(map(lambda user:user.serialize(),users))

    return jsonify(users),200


        


if __name__  == '__main__':
    app.run(host='localhost',port=5000,debug=True)