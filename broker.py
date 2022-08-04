import json
import os
from datetime import timedelta
from dateutil import parser
from flask_mqtt import Mqtt
from sqlalchemy.orm import aliased
from models.alert import Alert, AlertMaterial
from models.equipment import EquipmentMeasurement
from models.material import *

BROKER_TOPIC_MATERIAL = 'MATERIALS'
BROKER_TOPIC_EQUIPMENT = 'EQUIPAMENTOS'
MIN_TEMPERATURE = float(os.getenv('MIN_TEMPERATURE', -35))
MAX_TEMPERATURE = float(os.getenv('MAX_TEMPERATURE', 45))
MIN_HUMIDITY = float(os.getenv('MIN_HUMIDITY', -35))
MAX_HUMIDITY = float(os.getenv('MAX_HUMIDITY', 100))
MIN_ELAPSED_TIME = int(os.getenv('MIN_ELAPSED_TIME_IN_SECONDS', 2))
result_material = []
result_equipment = []


def setup_mqtt_broker(app):
    mqtt = Mqtt(app)

    @mqtt.on_message()
    def handle_mqtt(client, userdata, message):
        data = dict(
            topic=message.topic,
            payload=json.loads(message.payload.decode())
        )
        result_material.append(data['payload'])
        obj = data['payload']
        if data["topic"] == BROKER_TOPIC_MATERIAL:
            handle_mqtt_material(app, obj)
        elif data["topic"] == BROKER_TOPIC_EQUIPMENT:
            handle_mqtt_equipment(app, obj)

    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        print(level, buf)

    mqtt.subscribe(BROKER_TOPIC_MATERIAL)
    mqtt.subscribe(BROKER_TOPIC_EQUIPMENT)
    return mqtt


def handle_mqtt_material(app, obj):
    print("--------------------")
    with app.app_context():
        device = Device.query.filter(Device.mac == obj["MACADDRESS"]).first()
        if device is None:
            device = Device(mac=obj["MACADDRESS"])
            db.session.add(device)
            db.session.commit()
        sensor = SensorsMaterial.query.join(Device).filter(SensorsMaterial.id == int(obj["idSensor"])).filter(
            Device.mac == obj["MACADDRESS"]).first()
        if sensor is None:
            sensor = SensorsMaterial(id=int(obj["idSensor"]), device_id=device.id)
            db.session.add(sensor)
            db.session.commit()
        time_measurements = parser.parse(obj['timeOfMessage'])
        material = MaterialMeasurement(temperature=obj['temperature'], humidity=obj['humidity'],
                                       timeOfMeasurements=time_measurements, sensor_id=sensor.id)
        db.session.add(material)
        db.session.commit()
        last_relevant_measure = material.timeOfMeasurements - timedelta(seconds=MIN_ELAPSED_TIME)
        query_material = MaterialMeasurement.query.filter(
            MaterialMeasurement.timeOfMeasurements > last_relevant_measure).all()
        last = query_material[-1]
        temps_bool = [m.temperature > MAX_TEMPERATURE or m.temperature <
                      MIN_TEMPERATURE for m in query_material if m.temperature != None]
        hum_bool = [m.humidity > MAX_HUMIDITY or m.humidity <
                    MIN_HUMIDITY for m in query_material if m.humidity != None]
        if all(temps_bool) or all(hum_bool):
            current_alert = AlertMaterial.query.first()
            begin_measure = aliased(MaterialMeasurement)
            end_measure = aliased(MaterialMeasurement)
            current_alert = AlertMaterial.query.join(begin_measure, 'beginmeasure')\
                .join(end_measure, 'endmeasure').filter(
                begin_measure.timeOfMeasurements < last.timeOfMeasurements).filter(
                end_measure.timeOfMeasurements > last.timeOfMeasurements).first()
            if current_alert is None:
                alert = Alert()
                db.session.add(alert)
                db.session.commit()
                alert_m = AlertMaterial(begin_meassurement_id=last.id, end_meassurement_id=material.id,
                                        alert_id=alert.id)
                db.session.add(alert_m)
                db.session.commit()
            else:
                print("Second")
                current_alert.end_measure = material.id
                db.session.commit()


def handle_mqtt_equipment(app, obj):
    print('handle mqtt equipment')
    with app.app_context():
        device = Device.query.filter(Device.mac == obj["MACADDRESS"]).first()
        if device is None:
            device = Device(mac=obj["MACADDRESS"])
            db.session.add(device)
            db.session.commit()
        
        rfid = obj["equipamentTag"]
        time = obj["timeOfMessage"]
        equipment = EquipmentMeasurement.query.filter(EquipmentMeasurement.rfid==rfid and EquipmentMeasurement.timeOfMeasurement==time).first()
        if equipment is None:
            equipment = EquipmentMeasurement(
                rfid=rfid, status="TODO", timeOfMeasurement=time)
            db.session.add(equipment)
            db.session.commit()
        
