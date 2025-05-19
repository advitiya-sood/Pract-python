from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt
from models.user_model import User
from schemas import UserSchema



user_bp=Blueprint("Users",__name__)

@user_bp.get('/all')    
@jwt_required()
def get_all_users():

    claims=get_jwt()

    if claims.get('is_admin')==True:

        page =request.args.get('page',default=1,type=int)

        per_page=request.args.get('per_page',default=2,type=int)


        users=User.query.paginate(
            page=page,
            per_page=per_page
        )

        result=UserSchema().dump(users,many=True)

        return jsonify({
            "users":result
        }),200
    
    return jsonify({"Message": "Not an  admin member"})