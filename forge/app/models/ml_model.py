from . import db
from .. import security_manager
from . import tsMixin
from flask_appbuilder import Model
from sqlalchemy.ext.declarative import declared_attr

class taskModel(tsMixin,Model):
    __bind_key__ = None
    __tablename__ = "fg_task"
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(150))
    remark = db.Column(db.Text(),nullable = True)

    @declared_attr
    def owner_id(self):
        return db.Column(db.Integer, db.ForeignKey("ab_user.id"),
                         default=self.get_user_id, nullable=True)

    @classmethod
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception as e:
            return None

    owner = db.relationship(security_manager.user_model)

    def __repr__(self):
        return self.taskname

class dataFormat(Model):
    __bind_key__ = None
    __tablename__ = "fg_data_format"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    remark = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return self.name

class hyperParam(tsMixin,Model):
    __bind_key__ = None
    __tablename__ = "fg_hyper_param"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150))
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    format_id = db.Column(db.Integer, db.ForeignKey(dataFormat.id))
    val = db.Column(db.String(255), nullable=True)
    remark = db.Column(db.Text(), nullable=True)

    task = db.relationship(taskModel)
    format = db.relationship(dataFormat)
    def __repr__(self):
        return self.slug

class weightModel(tsMixin,Model):
    __bind_key__ = None
    __tablename__ = "fg_weight"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    name = db.Column(db.String(255))
    path = db.Column(db.Text(), nullable=True)
    framewk = db.Column(db.String(50), nullable=True, default = "pytorch")
    params_json = db.Column(db.Text()) # a json snapshot of hyperparameters
    remark = db.Column(db.Text(), nullable=True)

    task = db.relationship(taskModel)

    def __repr__(self):
        return self.name

class hyperParamWeight(tsMixin,Model):
    __tablename__ = "fg_hp_weight"
    id = db.Column(db.Integer, primary_key=True)
    hp_id = db.Column(db.Integer, db.ForeignKey(hyperParam.id))
    hyperparam = db.relationship(hyperParam, foreign_keys = [hp_id], backref="weights")
    weight_id = db.Column(db.Integer, db.ForeignKey(weightModel.id))
    weight = db.relationship(weightModel, foreign_keys = [weight_id], backref = "hyper_params")
    valsnap = db.Column(db.String(255), nullable = True) # snapshot of hyper param value

    def __repr__(self):
        return str(self.weight.name)+"|"+str(self.hyperparam.slug)

class mapModel(tsMixin,Model):
    __tablename__ = "fg_map"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    cola = db.Column(db.String(255),nullable = True)
    cola_fid = db.Column(db.Integer, db.ForeignKey(dataFormat.id))
    colb = db.Column(db.String(255),nullable = True)
    colb_fid = db.Column(db.Integer, db.ForeignKey(dataFormat.id))
    kv = db.Column(db.Text)
    remark = db.Column(db.Text(), nullable=True)

    cola_form = db.relationship(dataFormat, foreign_keys = [cola_fid])
    colb_form = db.relationship(dataFormat, foreign_keys = [colb_fid])


weightModel.involved_hp = db.relationship(hyperParam, secondary = "fg_hp_weight")

class metricModel(tsMixin,Model):
    __tablename__ = "fg_metric"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150))
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    format_id = db.Column(db.Integer, db.ForeignKey(dataFormat.id))
    val = db.Column(db.String(255), nullable=True)
    big_better = db.Column(db.Boolean, default = True)
    bestyet_id = db.Column(db.Integer,db.ForeignKey(weightModel.id))
    remark = db.Column(db.Text(), nullable=True)

    task = db.relationship(taskModel)
    format = db.relationship(dataFormat)
    bestyet = db.relationship(weightModel, foreign_keys = [bestyet_id])

    def __repr__(self):
        return self.slug

class metricWeight(tsMixin,Model):
    __tablename__ = "fg_metric_weight"
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey(metricModel.id))
    metric = db.relationship(metricModel, foreign_keys=[metric_id], backref="weights")
    weight_id = db.Column(db.Integer, db.ForeignKey(weightModel.id))
    weight = db.relationship(weightModel, foreign_keys=[weight_id], backref="metrics")
    valsnap = db.Column(db.String(255), nullable=True)  # snapshot of hyper param value

    def __repr__(self):
        return str(self.weight.name) + "|" + str(self.metric.slug)