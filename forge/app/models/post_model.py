from . import db
from .. import security_manager
from . import tsMixin
from flask_appbuilder import Model

class postModel(tsMixin,Model):
    __bind_key__ = None
    __tablename__ = "fg_post"
    id = db.Column(db.Integer, primary_key=True)
    head_big = db.Column(db.String(150), )
    head_small = db.Column(db.String(150), nullable=True)
    content = db.Column(db.Text)

    @declared_attr
    def user_id(self):
        return db.Column(db.Integer, db.ForeignKey("ab_user.id"),
                      default=self.get_user_id, nullable=True)
    @classmethod
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception as e:
            return None
    @property
    def brief_ctt(self):
        return self.content[:30]
    user = db.relationship(security_manager.user_model)