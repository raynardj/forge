from ..models import taskModel,dataFormat,hyperParam,hyperParamWeight,weightModel,metricModel,metricWeight
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder import expose,BaseView,ModelView

tscol = ["created_at","updated_at"]

class taskView(ModelView):
    route_base = "/task"
    datamodel = SQLAInterface(taskModel)

    label_columns = {"taskname":"Task","owner":"Owner","remark":"Remark","created_at":"Create","updated_at":"Update"}
    list_title = "Machine Learning Tasks"
    show_title = "Machine Learning Task"
    edit_title = "Machine Learning Task"
    add_title = "Machine Learning Task"
    list_columns = ["id","taskname","owner","remark", *tscol]
    show_columns = ["id","taskname","owner","remark", *tscol]
    edit_columns = ["taskname","owner","remark"]
    add_columns = ["taskname","owner","remark"]

class formatView(ModelView):
    route_base = "/format"
    datamodel = SQLAInterface(dataFormat)

    label_columns = {"name":"Object Type","remark":"Remark"}
    list_columns = ["id","name","remark"]
    show_columns = ["id", "name", "remark"]

class hyperParamView(ModelView):
    route_base = "/hp"
    datamodel = SQLAInterface(hyperParam)

    list_title = "Hyper Parameters"
    show_title = "Hyper Parameter"
    edit_title = "Hyper Parameter"
    add_title = "Hyper Parameter"
    label_columns = {"slug":"Name","val":"Value","format":"Type","created_at":"Create","updated_at":"Update"}
    add_columns = ["task", "format", "slug", "val", "remark"]
    edit_columns = ["task","format","slug","val","remark"]
    list_columns = ["task","format","slug","val","remark", *tscol]

class weightView(ModelView):
    route_base = "/weight"
    datamodel = SQLAInterface(weightModel)

    label_columns = {"name":"Model Name","framewk":"Framework","path":"path_saved","created_at":"Create","updated_at":"Update"}

    list_title = "Model Weights"
    add_title = "Model Weights"
    edit_title = "Model Weights"
    show_title = "Model Weights"
    add_columns = ["task","name","path","framewk","params_json","remark"]
    edit_columns = ["task","name","path","framewk","params_json","remark"]
    list_columns = ["id","task","name","path","framewk","params_json","remark", *tscol]
    show_columns = ["id","task","name","path","framewk","params_json","remark", *tscol]

class hyperParamWeightView(ModelView):
    route_base = "/hpweight"
    datamodel = SQLAInterface(hyperParamWeight)

    list_title = "H Param for Model Weights"
    add_title = "H Param for Model Weights"
    edit_title = "H Param for Model Weights"
    show_title = "H Param for Model Weights"
    add_columns = ["hyperparam","weight"]
    list_columns = ["hyperparam","weight","valsnap", *tscol]
    show_columns = ["id","hyperparam","weight","valsnap", *tscol]

class metricView(ModelView):
    route_base = "/metric"
    datamodel = SQLAInterface(metricModel)

    add_title = "Metrics"
    edit_title = "Metrics"
    list_title = "Metrics"
    show_columns = "Metrics"

    label_columns = {"bestyet":"Best so far", "val":"Value"}

    add_columns = ["slug", "task", "format", "val", "big_better", "remark", "weights", "bestyet"]
    edit_columns = ["slug", "task", "format", "val", "big_better", "remark", "weights", "bestyet"]
    show_columns = ["slug", "task", "format", "val", "big_better", "remark", "weights", "bestyet", *tscol]
    list_columns = ["slug", "task", "format", "val", "big_better", "remark", "weights", "bestyet", *tscol]

class metricWeightView(ModelView):
    route_base = "/metricweight"
    datamodel = SQLAInterface(metricWeight)

    label_columns = {"valsnap":"Value Snapshot"}

    add_title = "Metrics Log"
    edit_title = "Metrics Log"
    show_title = "Metrics Log"
    list_title = "Metrics Log"

    add_columns = ["metric","weight","valsnap"]
    edit_columns = ["metric","weight","valsnap"]
    show_columns = ["metric","weight","valsnap", *tscol]
    list_columns = ["metric","weight","valsnap", *tscol]