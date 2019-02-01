from .. import models
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder import expose,BaseView,ModelView


class PostView(ModelView):
    route_base = "/post"
    datamodel = SQLAInterface(models.postModel)
    label_columns = {
        "user":"User","head_big":"Title","head_small":"SubTitle","content":"Content",
        "content.brief_ctt":"Brief Content","created_at":"Created","updated_at":"Updated",
                     }
    list_columns = ["user","head_big","content.brief_ctt","created_at","updated_at"]
    show_columns = ["user","head_big","head_small","content","created_at","updated_at"]
    edit_columns = ["head_big","head_small","content"]
    add_columns = ["head_big","head_small","content"]

