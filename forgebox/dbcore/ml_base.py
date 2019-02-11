from . import Base,session
from sqlalchemy import Column,DateTime
from sqlalchemy.orm import relationship

taskModel = Base.classes.fg_task
dataFormat = Base.classes.fg_data_format
hyperParam = Base.classes.fg_hyper_param
weightModel = Base.classes.fg_weight
hyperParamWeight = Base.classes.fg_hp_weight
mapModel = Base.classes.fg_map
metricModel = Base.classes.fg_metric
metricWeight = Base.classes.fg_metric_weight

taskModel.__doc__ = """
Machine Learnin Tasks

from forgebox.dbcore imoprt session, taskModel
from datetime import datetime
task = taskModel(taskname="obj_detection_for_chars", 
            remark = "Object Detection For Characters", 
            created_at =datetime.now(),
            updated_at = datetime.now(),
            )
session.add(task)
session.commit()

id = db.Column(db.Integer, primary_key=True)
taskname = db.Column(db.String(150))
remark = db.Column(db.Text(),nullable = True)
owner_id = db.Column(db.Integer, db.ForeignKey("ab_user.id"),
                         default=self.get_user_id, nullable=True)
columns from tsMixin:
created_at
updated_at
"""
taskModel.__repr__ = lambda self:self.taskname
dataFormat.__repr__ = lambda self:self.name

hyperParam.format = relationship(dataFormat)


def add_metric(self,metric):
    """
    :param metric: A metricModel object
    :return: A metricWeight object, logging the  metric
    """
    metriclog = metricWeight(weight_id = self.id, metric_id = metric.id, valsnap = str(metric.val))
    session.add(metriclog)
    session.flush()
    session.commit()
    return metriclog

weightModel.add_metric = add_metric
