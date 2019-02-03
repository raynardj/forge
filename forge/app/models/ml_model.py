from . import db
from .. import security_manager
from . import tsMixin
from flask_appbuilder import Model

class taskModel(tsMixin,Model):
    __bind_key__ = None
    __tablename__ = "fg_task"
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(150))
    owner_id = db.Column(db.Integer(), db.ForeignKey("ab_user.id"), nullable=True)
    remark = db.Column(db.Text(),nullable = True)

    owner = db.relationship(security_manager.user_model, foreign_keys=[owner_id])

    def __repr__(self):
        return "%s:%s"%(self.taskname, self.owner.username)

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

weightModel.involved_hp = db.relationship(hyperParam, secondary = "fg_hp_weight")
