import os
from flask_migrate import Migrate
from flask import Flask
from models.main import db


def set_environments_var(app):
    app.config['MQTT_BROKER_URL'] = os.getenv('BROKER_URL')
    app.config['MQTT_BROKER_PORT'] = int(os.getenv('BROKER_PORT'))
    app.config['MQTT_USERNAME'] = os.getenv('BROKER_USERNAME')
    app.config['MQTT_PASSWORD'] = os.getenv('BROKER_PASSWORD')
    app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
    app.config['sqlalchemy.url'] = os.getenv('DB_URL')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def setup_flask_app():
    app = Flask(__name__)
    set_environments_var(app)
    run_db_migration(app)
    return app


def run_db_migration(app):
    print("==============================")
    print(app.config['sqlalchemy.url'])
    print(app.config['MQTT_BROKER_URL'])
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    with app.app_context():
        from flask_migrate import upgrade as _upgrade
        from flask_migrate import migrate as _migrate
        from flask_migrate import stamp as _stamp

        _stamp()
        _migrate()
        _upgrade()
