from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from ..config import SQLALCHEMY_DATABASE_URI

Base = automap_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base.prepare(engine, reflect=True)

session = Session(engine)

from .ml_base import taskModel, dataFormat, hyperParam, hyperParamLog, weightModel, metricModel, metricLog, trainModel
