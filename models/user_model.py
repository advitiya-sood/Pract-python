from uuid import uuid4
from flask_bcrypt import Bcrypt
from extensions import db


bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text())
 
    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self,password):
        self.password=bcrypt.generate_password_hash(password).decode('utf-8')

    
    def check_password(self,password):
        return  bcrypt.check_password_hash(self.password, password)   # self.password is hashed password and password is the password to be checked
    




    @classmethod                                            # more research to be done on this
    def get_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
