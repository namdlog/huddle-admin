import imp
from marshmallow import Schema, fields
from responses.material import *

class AlertMaterial(Schema):
    alert_id = fields.Method("get_alert_id")
    temperatures = fields.List(fields.Nested(MaterialSchema, only=["temperature","macaddress", "timeOfMeasurements" ]))
    humidities = fields.List(fields.Nested(MaterialSchema, only=["humidity","macaddress", "timeOfMeasurements" ]))
    def get_alert_id(self,obj):
        return obj.id


class Alert(Schema):
    materials= fields.Nested(AlertMaterial)
    equipaments = fields.Constant([])
