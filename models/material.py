from datetime import datetime
from dataclasses import dataclass

from sqlalchemy import false

from models.main import db





class Device(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    mac = db.Column(db.String(256))
    place = db.Column(db.String(256))
    sensors = db.relationship('SensorsMaterial', backref='device', lazy=False)


class SensorsMaterial(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    place = db.Column(db.String(256))
    measurements = db.relationship('MaterialMeasurement', backref='sensor', lazy=False)
    device_id = db.Column(db.BigInteger, db.ForeignKey('device.id'),
        nullable=True)


class MaterialMeasurement(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    temperature = db.Column(db.Numeric, nullable=True)
    humidity = db.Column(db.Numeric, nullable=True)
    sensor_id = db.Column(db.BigInteger, db.ForeignKey('sensors_material.id'),
        nullable=True)
    timeOfMeasurements = db.Column(db.DateTime, nullable=True)
    begin_alert = db.relationship('AlertMaterial', backref='beginmeasure', lazy=False, foreign_keys="AlertMaterial.begin_meassurement_id")
    end_alert = db.relationship('AlertMaterial', backref='endmeasure', lazy=False, foreign_keys="AlertMaterial.end_meassurement_id")
