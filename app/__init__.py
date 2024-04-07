from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from prometheus_flask_exporter import PrometheusMetrics
from config import config

db = SQLAlchemy()

def create_app():
  app_instance = Flask(__name__)
  app_instance.config.from_object(config)

  db.init_app(app_instance)

  # Register Prometheus metrics (if applicable)
  metrics = PrometheusMetrics(app_instance)
  metrics.info('app_info', 'Application info', version=app_instance.config['APP_VERSION'])

  # Register User model with SQLAlchemy
  from . import routes  # Assuming routes are defined in routes.py
  app_instance.register_blueprint(routes.bp)  # Assuming routes are in a blueprint named 'bp'

  with app_instance.app_context():
    from . import models
    db.create_all()

  return app_instance
