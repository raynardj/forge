from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from ..config import SQLALCHEMY_DATABASE_URI

Base = automap_base()

import os
if os.environ["FORGE_DB_INITIALIZED"] != True:

    # basedir = os.path.abspath(os.path.dirname(__file__))
    # DATADIR = os.path.expanduser("%s/data"%(os.environ["HOME"]))

    print("Initialize forge db")
    from forge.app import db
    db.create_all()
    os.environ["FORGE_DB_INITIALIZED"] = True

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.prepare(engine, reflect=True)

session = Session(engine)

from .ml_base import taskModel, dataFormat, hyperParam, hyperParamLog, weightModel, metricModel, metricLog, trainModel, \
    logModel, keyMetricModel