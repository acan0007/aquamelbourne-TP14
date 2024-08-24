import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://acan0007:R4skr_123@localhost:5432/aquamelbournedb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
