from flask import Flask, jsonify
from config import Config
from blueprints.auth import auth_bp
from blueprints.users import user_bp
from blueprints.tasks import task_bp
from models.user_model import User
from extensions import db, jwt
from flask_cors import CORS

# def create_app(config_class=Config):
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt.init_app(app)

CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(task_bp, url_prefix='/api')

# JWT additional claims
@jwt.additional_claims_loader
def make_additional_claims(identity):
    return {"is_admin": identity == "Test User6"}

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "token has expired", "error": "token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "signature verification failed", "error": "invalid_token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "Does not contain a valid token", "error": "authorization_error"}), 401

    # return app



if __name__=="__main__":
    app.run(debug=True)





















































# @app.route('/',methods=['GET','POST'])
# def index():
#     if request.method=="GET":
#         tasks=Todo.query.order_by(Todo.time_created).all()
#         return render_template('index.html',tasks=tasks)

#     else:
#         content_entered=request.form['content']
#         new_task= Todo(content=content_entered)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')

#         except:
#             return "There was an issue"



# @app.route('/delete/<int:task_id>')
# def delete(task_id):
#     task_to_delete= Todo.query.get_or_404(task_id)
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
    
#     except:
#         return "there was an error "
    


# @app.route('/update/<int:task_id>',methods=['GET','POST'])
# def update(task_id):
#     task_to_update= Todo.query.get_or_404(task_id)

#     if request.method=="GET":
#         return render_template('update.html',task=task_to_update)
#     else:
#         task_to_update.content=request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "some error occured updating"



