from ..models import taskModel, dataFormat, hyperParam, hyperParamLog, weightModel, metricModel, metricLog, trainModel
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder import expose, BaseView, ModelView

tscol = ["created_at", "updated_at"]


class taskView(ModelView):
    route_base = "/task"
    datamodel = SQLAInterface(taskModel)

    label_columns = {"taskname": "Task", "owner": "Owner", "remark": "Remark", "metrics": "Last Metrics",
                     "created_at": "Create", "updated_at": "Update","taskdetail":"Task Detail"}

    list_title = "Machine Learning Tasks"
    show_title = "Machine Learning Task"
    edit_title = "Machine Learning Task"
    add_title = "Machine Learning Task"

    list_columns = ["id", "taskdetail", "taskname", "owner", "remark", *tscol]
    show_columns = ["id", "taskname", "owner", "remark", "metrics", *tscol]
    edit_columns = ["taskname", "owner", "remark"]
    add_columns = ["taskname", "owner", "remark"]

    @expose("/taskdetail/<task_id>/")
    def taskdetail(self, task_id):
        task = self.datamodel.get(task_id)
        intro_dict = {
            "Task ID": task.id,
            "Task Name": task.taskname,
            "Owner": task.owner if task.owner else "No owner yet",
            "Remark": task.remark,
            "Created At": task.created_at.strftime("%Y-%m-%d %H:%M:%S") if task.created_at else "Not Set",
            "Updated At": task.updated_at.strftime("%Y-%m-%d %H:%M:%S") if task.updated_at else "Not Set",
            "Latest H-Params": self.render_template("dict_table.html",
                                                    dict_=dict((hp.slug, hp.val) for hp in list(task.hyper_params))) if len(list(task.hyper_params))>0 else None,
            "Latest Metrics":self.render_template("dict_table.html",
                                                  dict_=dict((mt.slug, mt.val) for mt in list(task.metrics)))if len(list(task.metrics))>0 else None,
        }
        return self.render_template("task_show.html", task=task, intro=intro_dict)

    # todo: A more fancy task show page


class formatView(ModelView):
    route_base = "/format"
    datamodel = SQLAInterface(dataFormat)

    label_columns = {"name": "Object Type", "remark": "Remark"}
    list_columns = ["id", "name", "remark"]
    show_columns = ["id", "name", "remark"]


class trainView(ModelView):
    route_base = "/train"
    datamodel = SQLAInterface(trainModel)

    list_title = "Train Management"
    show_title = list_title
    edit_title = list_title
    add_title = list_title

    add_columns = ["task", "name", "remark"]
    edit_columns = ["task", "name", "remark"]
    show_columns = ["id", "task", "name", "remark", *tscol]
    list_columns = ["id", "task", "name", "remark", *tscol]

    # todo: A more fancy task show page


class hyperParamView(ModelView):
    route_base = "/hp"
    datamodel = SQLAInterface(hyperParam)

    list_title = "Hyper Parameters"
    show_title = "Hyper Parameter"
    edit_title = "Hyper Parameter"
    add_title = "Hyper Parameter"
    label_columns = {"slug": "Name", "val": "Value", "format": "Type", "created_at": "Create", "updated_at": "Update"}
    add_columns = ["task", "format", "slug", "val", "remark"]
    edit_columns = ["task", "format", "slug", "val", "remark"]
    list_columns = ["task", "format", "slug", "val", "remark", *tscol]


class weightView(ModelView):
    route_base = "/weight"
    datamodel = SQLAInterface(weightModel)

    label_columns = {"name": "Model Name", "framewk": "Framework", "path": "path_saved", "created_at": "Create",
                     "updated_at": "Update"}

    list_title = "Model Weights"
    add_title = "Model Weights"
    edit_title = "Model Weights"
    show_title = "Model Weights"
    add_columns = ["task", "name", "path", "framewk", "params_json", "remark"]
    edit_columns = ["task", "name", "path", "framewk", "params_json", "remark"]
    list_columns = ["id", "task", "name", "path", "framewk", "params_json", "remark", *tscol]
    show_columns = ["id", "task", "name", "path", "framewk", "params_json", "remark", *tscol]


class hyperParamLogView(ModelView):
    route_base = "/hplog"
    datamodel = SQLAInterface(hyperParamLog)

    list_title = "H Param for Training"
    add_title = list_title
    edit_title = list_title
    show_title = list_title
    add_columns = ["hyperparam", "train"]
    edit_columns = ["hyperparam", "train"]
    list_columns = ["hyperparam", "train", "valsnap", *tscol]
    show_columns = ["id", "hyperparam", "train", "valsnap", *tscol]


class metricView(ModelView):
    route_base = "/metric"
    datamodel = SQLAInterface(metricModel)

    add_title = "Metrics"
    edit_title = "Metrics"
    list_title = "Metrics"
    show_columns = "Metrics"

    label_columns = {"bestyet": "Best so far", "val": "Value"}

    add_columns = ["slug", "task", "format", "val", "big_better", "remark", "bestyet"]
    edit_columns = ["slug", "task", "format", "val", "big_better", "remark", "bestyet"]
    show_columns = ["slug", "task", "format", "val", "big_better", "remark", "bestyet", *tscol]
    list_columns = ["slug", "task", "format", "val", "big_better", "remark", "bestyet", *tscol]


class metricLogView(ModelView):
    route_base = "/metriclog"
    datamodel = SQLAInterface(metricLog)

    label_columns = {"valsnap": "Value Snapshot"}

    add_title = "Metrics Log"
    edit_title = "Metrics Log"
    show_title = "Metrics Log"
    list_title = "Metrics Log"

    add_columns = ["metric", "train", "valsnap"]
    edit_columns = ["metric", "train", "valsnap"]
    show_columns = ["metric", "train", "valsnap", *tscol]
    list_columns = ["metric", "train", "valsnap", *tscol]
