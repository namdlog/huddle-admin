from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
db = SQLAlchemy()

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
    



#@dataclass
#class SensorsMaterial:
#    id: int
#
#    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#    deviceId = db.relationship('Device', backref='sensors_material', lazy=True)
#
#    
#
#@dataclass
#class Device:
#    id: int
#    place: str
#    mac = str
#
#    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
#    place = db.Column(db.String,nullable=True)
#    mac = db.Column(db.String(17),nullable=True)
