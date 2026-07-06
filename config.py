import os

class Config:
    SECRET_KEY = 'your-secret-key-here-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///restaurant.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False