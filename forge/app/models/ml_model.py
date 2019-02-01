from . import db
from .. import security_manager
from . import tsMixin
from flask_appbuilder import Model

class taskModel(tsMixin,Model):
    __bind_key__ = None
    __tablename__ = "fg_task"
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(150)),
    owner_id = db.Column(db.Integer(), db.ForeignKey("ab_user.id"), nullable=True)
    remark = db.Column(db.Text(),nullable = True)

    owner = db.relationship(security_manager.user_model, foreign_keys=[owner_id])

class dataFormat(Model):
    __bind_key__ = None
    __tableName__ = "fg_hyper_param"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    remark = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return self.remark

class hyperParam(tsMixin,Model):
    __bind_key__ = None
    __tableName__ = "fg_hyper_param"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150))
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    format_id = db.Column(db.Integer, db.ForeignKey(dataFormat))
    val = db.Column(db.String(255), nullable=True)
    remark = db.Column(db.Text(), nullable=True)

class weightModel(tsMixin,Model):
    __bind_key__ = None
    __tablename__ = "fg_weight"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    name = db.Column(db.String(255))
    path = db.Column(db.Text())
    params = db.Column(db.Text())
    remark = db.Column(db.Text(), nullable=True)