from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.set_password(password)  # Hash and set the password
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def set_password(self, password):
        # Hash the password and set it
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # Check if the provided password matches the stored hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f"<User {self.email}>"
    
try: 
    with app.app_context():
        db.create_all()
except Exception as e:
    print(str(e))        
