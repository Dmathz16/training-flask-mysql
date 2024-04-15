# import io
# import os
from datetime import datetime

# import bcrypt
# import face_recognition
# import flask
# import flask_login
# import numpy as np
# import PIL
# from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.types import DateTime, Integer, TIMESTAMP, LargeBinary, String

# from extensions import db, login_manager

from application import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(191), unique=True, nullable=False)
    password = db.Column(String(255), nullable=False)

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(Integer, primary_key=True)
    author_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    created = db.Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    title = db.Column(String(255), nullable=False)
    body = db.Column(String, nullable=False)
    author = db.relationship('User', backref='posts')