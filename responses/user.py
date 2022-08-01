from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    isAdmin = fields.Bool()
    rfid = fields.Str()
    card_type = fields.Str()
    sector = fields.Str()
    extension_number = fields.Str()
