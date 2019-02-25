from . import db
from .. import security_manager
from . import tsMixin
from flask_appbuilder import Model
from flask import render_template
from sqlalchemy.ext.declarative import declared_attr


class taskModel(tsMixin, Model):
    __bind_key__ = None
    __tablename__ = "fg_task"
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(150))
    remark = db.Column(db.Text(), nullable=True)

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

    @property
    def taskdetail(self):
        return "<a class='btn btn-default' href='/task/taskdetail/%s/' target_ = 'blank'>Task Detail</a>" % (self.id)

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


class trainModel(tsMixin, Model):
    __tablename__ = "fg_train"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    task = db.relationship(taskModel, backref="trains")
    name = db.Column(db.String(255), nullable=True)
    remark = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return "[trn:%s]task:%s" % (self.name, self.task.taskname)

    @property
    def train_panel(self):
        return render_template("train_panel.html", train=self)


class hyperParam(tsMixin, Model):
    __bind_key__ = None
    __tablename__ = "fg_hyper_param"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150))
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    format_id = db.Column(db.Integer, db.ForeignKey(dataFormat.id))
    val = db.Column(db.String(255), nullable=True)
    remark = db.Column(db.Text(), nullable=True)

    task = db.relationship(taskModel, backref="hyper_params")
    format = db.relationship(dataFormat)

    def __repr__(self):
        return self.slug


class weightModel(tsMixin, Model):
    __bind_key__ = None
    __tablename__ = "fg_weight"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    name = db.Column(db.String(255))
    path = db.Column(db.Text(), nullable=True)
    framewk = db.Column(db.String(50), nullable=True, default="pytorch")
    train_id = db.Column(db.Integer, db.ForeignKey(trainModel.id))
    train = db.relationship(trainModel, foreign_keys=[train_id], backref="weights")
    params_json = db.Column(db.Text())  # a json snapshot of hyperparameters
    remark = db.Column(db.Text(), nullable=True)

    task = db.relationship(taskModel)

    def __repr__(self):
        return self.name


class hyperParamLog(tsMixin, Model):
    __tablename__ = "fg_hp_log"
    id = db.Column(db.Integer, primary_key=True)
    hp_id = db.Column(db.Integer, db.ForeignKey(hyperParam.id))
    hyperparam = db.relationship(hyperParam, foreign_keys=[hp_id], backref="trains")
    train_id = db.Column(db.Integer, db.ForeignKey(trainModel.id))
    train = db.relationship(trainModel, foreign_keys=[train_id], backref="hps")
    valsnap = db.Column(db.String(255), nullable=True)  # snapshot of hyper param value

    def __repr__(self):
        return str(self.train.name) + "|" + str(self.hyperparam.slug)


class mapModel(tsMixin, Model):
    __tablename__ = "fg_map"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    cola = db.Column(db.String(255), nullable=True)
    cola_fid = db.Column(db.Integer, db.ForeignKey(dataFormat.id))
    colb = db.Column(db.String(255), nullable=True)
    colb_fid = db.Column(db.Integer, db.ForeignKey(dataFormat.id))
    kv = db.Column(db.Text)
    remark = db.Column(db.Text(), nullable=True)

    cola_form = db.relationship(dataFormat, foreign_keys=[cola_fid])
    colb_form = db.relationship(dataFormat, foreign_keys=[colb_fid])


class metricModel(tsMixin, Model):
    __tablename__ = "fg_metric"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150))
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    format_id = db.Column(db.Integer, db.ForeignKey(dataFormat.id))
    val = db.Column(db.String(255), nullable=True)
    big_better = db.Column(db.Boolean, default=True)
    bestyet_id = db.Column(db.Integer, db.ForeignKey(weightModel.id), nullable=True)
    remark = db.Column(db.Text(), nullable=True)

    task = db.relationship(taskModel, foreign_keys=[task_id], backref="metrics")
    format = db.relationship(dataFormat)
    bestyet = db.relationship(weightModel, foreign_keys=[bestyet_id])

    def __repr__(self):
        return "%s:%s" % (self.slug, self.val)


class metricLog(tsMixin, Model):
    __tablename__ = "fg_metric_log"
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey(metricModel.id), )
    metric = db.relationship(metricModel, foreign_keys=[metric_id], backref="weights")
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    task = db.relationship(taskModel)
    train_id = db.Column(db.Integer, db.ForeignKey(trainModel.id))
    train = db.relationship(trainModel, foreign_keys=[train_id], backref="metrics")
    valsnap = db.Column(db.String(255), nullable=True)  # snapshot of hyper param value

    def __repr__(self):
        return str(self.train.name) + "|" + str(self.metric.slug)


class keyMetricModel(tsMixin, Model):
    __tablename__ = "fg_key_metric"
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey(metricModel.id), )
    metric = db.relationship(metricModel, foreign_keys=[metric_id], backref="kmetrics")
    best_metric_id = db.Column(db.Integer, db.ForeignKey(metricLog.id))
    best_metric = db.relationship(metricLog, foreign_keys=[best_metric_id], backref="kmetrics")


class logModel(tsMixin, Model):
    __tablename__ = "fg_run_log"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey(taskModel.id))
    task = db.relationship(taskModel, foreign_keys=[task_id], backref="logs")
    train_id = db.Column(db.Integer, db.ForeignKey(trainModel.id))
    train = db.relationship(trainModel, foreign_keys=[train_id], backref="logs")
    path = db.Column(db.Text(), nullable=True)
