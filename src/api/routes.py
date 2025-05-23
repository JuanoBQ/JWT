"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,  get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)
bcrypt = Bcrypt()

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200



@api.route('/signup', methods=['POST'])
def handle_signup():
    try:
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password") 

        if not email or not password or not name:
            return jsonify({'error': 'email, password and name are required!'}),400
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'Email already exist!'}),409

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(email=email, password=password_hash, name=name, is_active=True)

        db.session.add(new_user)
        db.session.commit()

        response_body = {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        }
        return jsonify({'message':'User created','user':response_body}), 200
    except Exception as e:
        return jsonify({'error':'Error in user creation: '+str(e)}),500



@api.route('/login', methods=['POST'])
def handle_login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'email, password are required!'}),400

        #Importante
        login_user = User.query.filter_by(email=email).one()

        #Verificacion de existencia de email
        if not login_user:
            return jsonify({'error': 'Invalid email'}),404

        #Verificacion del password
        password_from_db = login_user.password
        true_or_false = bcrypt.check_password_hash(password_from_db, password)

        #Si existe, generamos el token
        if true_or_false:
            expires = timedelta(hours=1)

            user_id = login_user.id
            access_token = create_access_token(identity=str(user_id), expires_delta=expires)


            return jsonify({"access_token": access_token})

        else:
            return {"Error":"invalid password"}, 404
    except Exception as e:
        return {"Error":"Email no registrado "+ str(e)}, 500
    

@api.route('/private', methods=['GET'])
@jwt_required()
def private_route():
    current_user_id = get_jwt_identity()
    if current_user_id:
        users = User.query.all()
        user_list = []
        for user in users:
            user_dict = {
                "id":user.id,
                "name":user.name,
                "email": user.email,
                "is_active": user.is_active
            }
            user_list.append(user_dict)
        return jsonify(user_list),200
    else:
        return {"Error":"No hay access token"},401
