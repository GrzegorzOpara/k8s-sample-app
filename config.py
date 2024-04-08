import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_VERSION = os.environ.get("APP_VERSION")

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_CONN_STRING")
    PROMETHEUS_EXPORTER = False
    pass

class TestConfig(Config):
    PROMETHEUS_EXPORTER = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    pass

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_CONN_STRING")
    PROMETHEUS_EXPORTER = True
    pass

configs = {
  'dev'  : DevConfig,
  'test' : TestConfig,
  'prod' : ProdConfig,
  'default' : ProdConfig
  }