import logging
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder
from .security import MySecurityManager as SecurityManager
from .utils import create_dir

"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
create_dir(app.config.get("DATADIR"))
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, security_manager_class=SecurityManager)
security_manager = appbuilder.sm

if "sqlite:///" in app.config.get("SQLALCHEMY_DATABASE_URI"):
    # Only include this for SQLLite constraints
    from sqlalchemy.engine import Engine
    from sqlalchemy import event

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        # Will force sqllite contraint foreign keys
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

from . import views

