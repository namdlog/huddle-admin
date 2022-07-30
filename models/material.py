from datetime import datetime
from dataclasses import dataclass

from models.main import db


@dataclass
class MaterialMeasurement(db.Model):
    id: int
    temperature: float
    humidity: float
    timeOfMeasurements: datetime

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    temperature = db.Column(db.Numeric, nullable=True)
    humidity = db.Column(db.Numeric, nullable=True)
    #sensorId = db.relationship('SensorsMaterial', backref='material_measurement', lazy=True)
    timeOfMeasurements = db.Column(db.DateTime, nullable=True)
