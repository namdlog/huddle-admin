from flask import Flask
from flask_mqtt import Mqtt
import eventlet
import json
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = os.getenv('BROKER_URL')
app.config['MQTT_BROKER_PORT'] = int(os.getenv('BROKER_PORT'))
app.config['MQTT_USERNAME'] = os.getenv('BROKER_USERNAME')
app.config['MQTT_PASSWORD'] = os.getenv('BROKER_PASSWORD')
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BROKER_TOPIC = 'HUDDLE_MATERIAIS'

mqtt = Mqtt(app)
socketio = SocketIO(app)
db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mqtt.subscribe(BROKER_TOPIC)
    print(mqtt.topics)
    app.run(host="0.0.0.0", port=5000)
