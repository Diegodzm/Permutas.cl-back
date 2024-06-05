import os
from flask import Flask,request,jsonify
from models import db, User, Product, Offer, Wishlist
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager,create_access_token,get_jwt_identity, jwt_required, current_user)


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
                    "user":user.firstname,
                    "access_token": access_token,
                    "msg":"user login google",
                    "user_id": user.id,
                    "username":user.username
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

@app.route('/products/user/<int:user>', methods=['GET'])
def get_user_products(user):
    products = Product.query.filter_by(user_id=user).all()

    products_data = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'photo': product.photo,
            'product_info': product.product_info,
            'brand': product.brand,
            'state': product.state,
            'category_id': product.category_id,
            'price': product.price,
            'user_id': product.user_id
        }
        products_data.append(product_data)
    return jsonify(products_data)



@app.route('/offerupload',methods=['POST'])
def offerupload():
    offer=Offer()
    userid= request.json.get('user_id')
    amount_offer= request.json.get('amount')
    product_info= request.json.get('product_info')
    photo= request.json.get('photo')
    brand = request.json.get('brand')
    userinterested= request.json.get('user_interested')
    photointerested= request.json.get('photo_interested')
    brandinterested = request.json.get('brand_interested')
    infointerested = request.json.get('info_interested')

    product_id_search_by_userid_interested= Product.query.filter_by(user_id=userinterested).all()
    product_id_search_by_userid = Product.query.filter_by(user_id=userid).all()
    
    for z in product_id_search_by_userid_interested:
        if brandinterested == z.brand:
            if infointerested== z.product_info:
                if photointerested ==z.photo:
                    offer.product_offered=z.id
                    offer.user_interested=userinterested
                    

    for x in product_id_search_by_userid:
        if brand == x.brand:
            if product_info== x.product_info:
                if photo ==x.photo:
                    product_id= x.id
                    offer.user_id= userid
                    offer.amount= amount_offer
                    offer.product_id= product_id

                    db.session.add(offer)
                    db.session.commit()

                        
                return jsonify({"msg":x,
                "offer id ":offer.id})
                
                    


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
                    "user":user.firstname,
                    "access_token": access_token,
                    "user_id": user.id,
                    "msg":"user login",
                    "username":user.username,
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


@app.route('/products/wishlist/<int:user>',methods=['POST'])
def post_wishlist(user):
    wishlist= Wishlist()
    name= request.json.get('name')
    userid= request.json.get('user_id')
    product_info= request.json.get('product_info')
    photo= request.json.get('photo')
    product_id_search_userid = Product.query.filter_by(user_id=userid).all()
    brand = request.json.get('brand')
    for x in product_id_search_userid:
        if brand == x.brand:
            if name == x.name:
                if product_info== x.product_info:
                    if photo ==x.photo:
                        product_id= x.id
                        wishlist.user_id= user
                        wishlist.product_id= product_id
                        db.session.add(wishlist)
                        db.session.commit()
                        return jsonify({"msg":"agregado a wishlist"})
                    
@app.route('/products/wishlist/<int:wishlist_product_id>/<int:user>', methods=['DELETE'])
def remove_from_wishlist(wishlist_product_id,user):
    wishlist_item = Wishlist.query.filter_by(id = wishlist_product_id).first()
    
   
    db.session.delete(wishlist_item)
    db.session.commit()
    wishlist_return = []
    remain_wishlist = Wishlist.query.filter_by(user_id=user).all()
    for x in remain_wishlist : 
        product_wish_remain = Product.query.filter_by(id = x.product_id).first()
        product_wish = {
            "id": x.id,
            "name": product_wish_remain.name,
            "photo": product_wish_remain.photo,
            "product_info": product_wish_remain.product_info,
            "price": product_wish_remain.price,
            "product_id": product_wish_remain.id
    }
        wishlist_return.append(product_wish)
    return jsonify(wishlist_return), 200



   

    
    




@app.route ('/products/published', methods=['GET'])

def published_products(): 
    published = Product.query.all()
    return jsonify (published)


   
@app.route('/wishlist/<int:user>', methods=['GET'])
def getWishlist(user):
    wished_info= Wishlist.query.filter_by(user_id=user).all()
    wishlist=[]
    for x in wished_info:
        product= Product.query.filter_by(id=x.product_id).first()
        product_wish =  {
            "id": x.id,
            "name": product.name,
            "photo": product.photo,
            "product_info": product.product_info,
            "price": product.price,
            "product_id" : product.id
        }
        wishlist.append(product_wish)
    return wishlist
        
@app.route('/users', methods=['GET'])
@jwt_required()
def protected_view():
    response="user logged in    "

    return jsonify(response),200


@app.route ('/products/oferta', methods = ['POST'])
def create_offer ():
    offer = Offer()

    user_id_offer = request.json.get ('user_id')
    amount_offer = request.json.get ('amount')
    state_offer = True
    product_id_offer = request.json.get ('product_id')

    offer.user_id = user_id_offer
    offer.amount = amount_offer 
    offer.state = state_offer 
    offer.product_id = product_id_offer 

    db.session.add(offer)
    db.session.commit()
@app.route('/Email/<int:user>', methods=['GET'])
def correo(user):
     userof= User.query.filter_by(id=user).first()

     return jsonify({'email':userof.email})


@app.route('/notifications/<int:user>', methods=['GET'])
def notificacion(user):
    offerbyuser= Offer.query.filter_by(user_id=user).all()

    return jsonify(offerbyuser)


@app.route('/offertrade',methods=['POST'])
def getTrade():
    tradeinfo= request.get_json()
    trade=[]

    for x in tradeinfo:
        user= User.query.filter_by(id=x['user_id']).first()
        user_interested= User.query.filter_by(id=x['user_interested']).first()
        product= Product.query.filter_by(id=x['product_id']).first()
        product_offered= Product.query.filter_by(id=x['product_offered']).first()
        tradeobject={
            "user":{
                "email":user.email,
                "firstname":user.firstname,
                "lastname":user.lastname,
                "username":user.username,
            },
           
            "user_interested":{
                "email":user_interested.email,
                "firstname":user_interested.firstname,
                "lastname":user_interested.lastname,
                "username":user_interested.username,

            },
            "product":{
                "product_info":product.product_info,
                "price":product.price,
                "photo":product.photo, 
                "name":product.name,
                "brand":product.brand,
            },
            "product_offered":{
                "product_info":product_offered.product_info,
                "amount":x['amount'],
                "photo":product_offered.photo,
                "name":product_offered.name,
                "brand":product_offered.brand,

            },

        }
  
        trade.append(tradeobject)

      
    return jsonify(
        trade
    )

@app.route('/products/delete/<int:product_id>',methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"msg": "Producto eliminado correctamente"}), 200
    else:
        return jsonify({"msg": "Producto no encontrado"}), 404

   



    

@app.route('/deloffer',methods=['PUT'])
def deloffer():     
    offerinfo= request.get_json()
    offeruserid= Offer.query.filter_by(user_id=offerinfo['user_id']).all()
    for x in offeruserid:
        if offerinfo['user_interested']==x.user_interested:
            if offerinfo['product_id']==x.product_id:
                if offerinfo['product_offered']==x.product_offered:
                    if offerinfo['amount']==x.amount:
                        db.session.delete(x)
                        db.session.commit()
    newoffer= Offer.query.all()
    return jsonify(newoffer)




if __name__  == '__main__':
    app.run(host='localhost',port=5000)
