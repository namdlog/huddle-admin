from models.main import db


class Alert(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    material_alert = db.relationship('AlertMaterial', backref='alerts_material', lazy=False)
    


class AlertMaterial(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    alert_id = db.Column(db.BigInteger, db.ForeignKey('alert.id'),
        nullable=True)
    begin_meassurement_id = db.Column(db.BigInteger, db.ForeignKey('material_measurement.id'),
        nullable=True)
    end_meassurement_id = db.Column(db.BigInteger, db.ForeignKey('material_measurement.id'),
        nullable=True)