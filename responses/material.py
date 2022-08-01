from marshmallow import Schema, fields




class DeviceInSensorSchmea(Schema):
    place = fields.Str()
    mac = fields.Str()


class SensorInMaterialSchema(Schema):
    place_device = fields.Pluck(DeviceInSensorSchmea, 'place', attribute="place",load_only=False)
    place = fields.Method("get_place")
    macaddress = fields.Method("get_macaddress")

    def get_place(self, obj):
        if( obj.device is None or obj.device.place is None):
            return obj.place
        else:
            return obj.place + " " + obj.device.place
    
    def get_macaddress(self,obj):
        if( obj.device is None):
            return ""
        else:
            return obj.device.mac        



class MaterialSchema(Schema):
    id = fields.Int()
    temperature = fields.Float()
    humidity = fields.Float()
    timeOfMeasurements = fields.DateTime()
    #sensor = fields.Nested(SensorInMaterialSchema)
    place = fields.Pluck(SensorInMaterialSchema, 'place', attribute="sensor")
    macaddress = fields.Method("get_macaddress")
    def get_macaddress(self,obj):
        if( obj.sensor is None or obj.sensor.device is None):
            return ""
        else:
            return obj.sensor.device.mac