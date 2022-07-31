from models.equipment import *
from models.material import *

def seedMaterials(db):
    device = Device(place = "teste 123",mac= "macaddress test")
    db.session.add(device)
    db.session.commit()
    sensor = SensorsMaterial(place = "teste 123",device_id=device.id)
    db.session.add(sensor)
    db.session.commit()
    print("FLAAAAAAAAAAAAg")
    print(sensor.id)
    materials_test = [
        {
            "temperature": 13.0,
            "humidity": 44.3,
            "MACADDRESS": "4458662"
        },
        {
            "temperature": 44.0,
            "humidity": 44.3,
            "MACADDRESS": "4458662"
        },
        {
            "temperature": 13.0,
            "humidity": 44.3,
            "MACADDRESS": "4458662"
        },
        {
            "temperature": 13.0,
            "humidity": 44.3,
            "MACADDRESS": "4458662"
        },
        {
            "temperature": 13.0,
            "humidity": 44.3,
            "MACADDRESS": "4458662"
        },
        {
            "temperature": 13.0,
            "humidity": 44.3,
            "MACADDRESS": "4458662"
        },
        {
            "temperature": 13.0,
            "humidity": 44.3,
            "MACADDRESS": "4458662"
        },
        {
            "temperature": 13.0,
            "humidity": 44.3,
            "MACADDRESS": "4458662"
        },
    ]
    for obj in materials_test:
        material = MaterialMeasurement(temperature=obj['temperature'], humidity=obj['humidity'],
        timeOfMeasurements=datetime.now(),sensor_id= sensor.id)
        db.session.add(material)
        db.session.commit()

