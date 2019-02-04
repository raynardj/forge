from .dbcore import session, taskModel, hyperParam, dataFormat
from datetime import datetime

class forgedb(object):
    def __init__(self, task):
        super(forgedb,self).__init__()
        self.s = session
        self.task = self.s.query(taskModel).filter(taskModel.taskname == task).first()
        self.hp2dict()
        print("="*10+"hyper params"+"="*10)
        print(self.confdict)
        self.set_hp_attributes()

    def get_hyperparams(self):
        """
        from task to hyper parameters
        :return: a list of hyper params
        """
        return self.s.query(hyperParam).filter(hyperParam.task_id == self.task.id).all()

    def hp2dict(self):
        hplist = self.get_hyperparams()
        self.confdict = dict((hp.slug, eval(hp.format.name)(hp.val)) for hp in hplist)
        return self.confdict

    def set_hp_attributes(self):
        list(setattr(self,hpslug,hpval) for hpslug,hpval in self.confdict.items())

    def p(self, key, val=None):
        """
        Access to hyper parameter
        :param key: parameter name/slug, avoid space or strange characters, letters and digits only
        :param val:
        * read value, default none to read value
        * if pass a kwarg here, will set the value to sql db
        :return: the parameter value
        """
        if val:
            hp = self.s.query(hyperParam).filter(hyperParam.slug == key, hyperParam.task_id == self.task.id).first()
            if hp:
                hp.val = str(val)
                hp.updated_at = datetime.now()
                self.s.add(hp)
                self.s.commit()
                return eval(hp.format.name)(hp.val)
            else:
                fmt = self.s.query(dataFormat).filter(dataFormat.name == type(val).__name__).first()
                if fmt ==None:
                    assert False, "No such format set yet: %s"%(type(val))
                hp = hyperParam(task_id = self.task.id,
                                slug = key,
                                remark = "Created in task %s"%(self.task.taskname),
                                format_id = fmt.id,
                                created_at = datetime.now(),
                                updated_at = datetime.now(), val = str(val))
                self.s.add(hp)
                self.s.commit()
                return eval(hp.format.name)(hp.val)
        else:
            hp = self.s.query(hyperParam).filter(hyperParam.slug == key, hyperParam.task_id == self.task.id).first()
            if hp:
                return eval(hp.format.name)(hp.val)