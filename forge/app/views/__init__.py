from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from .. import appbuilder, db

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

from .post_view import PostView
from .ml_view import taskView,formatView,hyperParamView,weightView,hyperParamWeightView

web_cate = {"category":"Web", "category_icon":"fa-dashboard"}
appbuilder.add_view(PostView, "posts", icon="fa-book", **web_cate )

ml_cate = {"category":"ML", "category_icon":"fa-magic"}
appbuilder.add_view(taskView, "Tasks", icon="fa-tasks", **ml_cate )
appbuilder.add_view(formatView, "Config Formats", icon="fa-star-half-o", **ml_cate )
appbuilder.add_view(hyperParamView, "Hyper Parameters", icon="fa-flask", **ml_cate )
appbuilder.add_view(weightView, "Model Weights", icon="fa-cubes", **ml_cate )

db.create_all()


