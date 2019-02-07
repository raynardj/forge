from datetime import datetime
from .. import db
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
        
class tsMixin(object):
    created_at = db.Column(
        db.DateTime, default=datetime.now, nullable=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

from .ml_model import taskModel, hyperParam, dataFormat, weightModel, hyperParamWeight, metricModel, metricWeight
from .post_model import postModel