from datetime import datetime
from dataclasses import dataclass

from models.main import db


@dataclass
class EquipmentMeasurement(db.Model):
    id: int
    rfid: str
    status: str
    name: str
    deck: str
    timeOfMeasurement: datetime

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    rfid = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=True)
    deck = db.Column(db.String, nullable=True)
    timeOfMeasurement = db.Column(db.DateTime, nullable=True)
