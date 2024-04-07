from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from prometheus_flask_exporter import PrometheusMetrics
from app.config import config
# from app.models import User  # Assuming User model is in models.py

# SQLAlchemy
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_name='default'):
  """Create a Flask application instance."""

  app = Flask(__name__)
  app.config.from_object(config)
  db.init_app(app)

  # Register Prometheus metrics (if applicable)
  metrics = PrometheusMetrics(app)
  metrics.info('app_info', 'Application info', version=app.config['APP_VERSION'])

  # Register User model with SQLAlchemy
  with app.app_context():
    db.create_all()

    # Import and register routes from routes.py
    from app import routes  # Assuming routes are defined in routes.py
    app.register_blueprint(routes.bp)  # Assuming routes are in a blueprint named 'bp'

  return app
