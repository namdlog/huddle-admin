from marshmallow import Schema, fields

class EquipmentSchema(Schema):
    id = fields.Int()
    rfid = fields.Str()
    status = fields.Str()
    timeOfMeasurements = fields.DateTime()
    name = fields.Str()
    deck = fields.Str()
