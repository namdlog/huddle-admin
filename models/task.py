from models.main import db

class Task(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=True)
    responsable_id = db.Column(db.BigInteger, nullable=True)
    status = db.Column(db.String(256), nullable=True)
    date_to_complete = db.Column(db.DateTime, nullable=True)
    alert_id = db.Column(db.BigInteger, nullable=True)

