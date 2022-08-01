from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    responsable_id = fields.Int()
    status = fields.Str()
    date_to_complete = fields.DateTime()
    alert_id = fields.Int()
