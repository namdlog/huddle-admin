from app import db

class MaterialMeasurement(dbo.Model):
  temperature = db.Column(db.Numeric, nullable=True)
  humidity = db.Column(db.Numeric, nullable=True)
  sensor_id = db.Column(db.BigInteger, nullable=True)
  time_of_measurement = db.Column(db.DateTime, nullable=True)
