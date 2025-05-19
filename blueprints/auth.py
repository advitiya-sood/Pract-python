from flask import Blueprint,jsonify,request
from flask_jwt_extended import create_access_token, create_refresh_token,get_jwt,jwt_required,current_user
from models.user_model import User

auth_bp=Blueprint('auth',__name__)


@auth_bp.post('/register')
def register_user():

    data=request.get_json()

    user=User.get_user_by_username(username=data.get('username'))

    if user is not None:
        return jsonify({"Error":"user already exist"}),403
    

    new_user=User(
        username=data.get('username'),
        email= data.get('email')

    )
    new_user.set_password(password=data.get('password'))
    new_user.save()

    return jsonify({"message":"User created"}),201


@auth_bp.post('/login')
def login_user():

    data=request.get_json()

    user=User.get_user_by_username(username=data.get('username'))

    if user  and (user.check_password(password=data.get('password'))):    # check if password matches form  stored hashed password
        access_token=create_access_token(identity=user.username)
        refresh_token=create_refresh_token(identity=user.username)
        
        
        return jsonify(
            {
                "message":"Loggin Success",
                "tokens":{
                    "access":access_token,
                    "refresh":refresh_token
                }
            }
        ),200
    
    return jsonify({"error":"Invalid username or password"}),400




@auth_bp.get('/getclaim')
@jwt_required()
def get_claim():
    claims=get_jwt()
    return jsonify({"message":"message","user_details":{

            "username":current_user.username,
            "email":current_user.email

    }})




   