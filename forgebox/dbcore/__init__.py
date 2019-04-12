from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from ..config import SQLALCHEMY_DATABASE_URI

Base = automap_base()
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
except:
    import os
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATADIR = os.path.expanduser("~/data")
    print("Create forge.db sqlite database file")
    from forge.app import db
    db.create_all()

Base.prepare(engine, reflect=True)

session = Session(engine)

from .ml_base import taskModel, dataFormat, hyperParam, hyperParamLog, weightModel, metricModel, metricLog, trainModel, \
    logModel, keyMetricModel
