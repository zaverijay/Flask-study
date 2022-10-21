from app import db
from flask_login import UserMixin
from app import login_manager

class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20)) #, unique=True, nullable=False)
    password = db.Column(db.String(20)) #, nullable=False)
    email = db.Column(db.String(50))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))