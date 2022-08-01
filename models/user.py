from models.main import db

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)
    rfid = db.Column(db.String(256), nullable=True)
    card_type = db.Column(db.String(45), nullable=False)
    sector = db.Column(db.String(256), nullable=True)
    extension_number = db.Column(db.String(15), nullable=True)


