from .. import models
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder import expose,BaseView,ModelView

class taskView(ModelView):
    route_base = "/task"
    datamodel = SQLAInterface(models.taskModel)

    label_columns = {"taskname":"Task","owner":"Owner","remark":"Remark"}

    list_columns = ["id","taskname","owner","remark","created_at","updated_at"]
    show_columns = ["id","taskname","owner","remark","created_at","updated_at"]
    edit_columns = ["taskname","owner","remark"]
    add_columns = ["taskname","owner","remark"]


class formatView(ModelView):
    route_base = "/format"
    datamodel = SQLAInterface(models.dataFormat)

    label_columns = {"name":"Object Type","remark":"Remark"}
    list_columns = ["id","name","remark"]
    show_columns = ["id", "name", "remark"]

class hyperParamView(ModelView):
    route_base = "/hp"
    datamodel = SQLAInterface(models.hyperParam)

class weightView(ModelView):
    route_base = "/weight"
    datamodel = SQLAInterface(models.weightModel)

    list_columns = ["id","task","name","path","framewk","param_json","remark","created_at","updated_at"]

class hyperParamWeightView(ModelView):
    route_base = "/hpweight"
    datamodel = SQLAInterface(models.hyperParamWeight)