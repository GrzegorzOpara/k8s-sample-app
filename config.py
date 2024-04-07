import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_CONN_STRING")
    APP_VERSION = os.environ.get("APP_VERSION")

class DevConfig(Config):
    PROMETHEUS_EXPORTER = False
    pass

class TestConfig(Config):
    PROMETHEUS_EXPORTER = False
    pass

class ProdConfig(Config):
    PROMETHEUS_EXPORTER = True
    pass

configs = {
  'dev'  : DevConfig,
  'test' : TestConfig,
  'prod' : ProdConfig,
  'default' : ProdConfig
  }