from .dbcore import session, taskModel, weightModel, hyperParam, hyperParamWeight, dataFormat, metricModel, metricWeight
from datetime import datetime
import json, os
from .utils import create_dir
from .config import DATADIR

# todo decide whether should I need an independent metric object
# class metric(object):
#     def __init__(self, metric_slug, task_id):
#         super(metric,self).__init__()
#         self.s = session
#         self.task = self.s.query(taskModel).filter(taskModel.id == task_id).first()
#         self.metric = self.s.query(metricModel).fitler(metricModel.slug == metric_slug).first()

class forgedb(object):
    def __init__(self, task, remark="created_in_code", framewk="pytorch", verbose = True):
        """
        connect to a task, will create a new task if not already established
        :param task: task name string
        :param remark: Introduction about this task
        """
        super(forgedb, self).__init__()
        self.s = session
        self.task = self.s.query(taskModel).filter(taskModel.taskname == task).first()
        self.verbose = verbose
        if self.task == None:
            if self.verbose:print("[creating task:%s]"%(task))
            taskitem = taskModel(taskname=task, remark=remark)
            self.s.add(taskitem)
            self.s.flush()
            self.s.commit()
            self.task = taskitem
        self.taskdir = os.path.join(DATADIR, self.task.taskname)
        create_dir(self.taskdir)
        self.hp2dict()
        if self.verbose:
            print("=" * 10 + "hyper params" + "=" * 10)
            print(self.confdict)
        self.framewk = framewk
        self.set_hp_attributes()
        self.modelnow = self.new_model_name()

    def __repr__(self):
        return "[forge:%s]" % (self.task.taskname)

    def get_hyperparams(self):
        """
        from task to hyper parameters
        :return: a list of hyper params
        """
        return self.s.query(hyperParam).filter(hyperParam.task_id == self.task.id).all()

    def hp2dict(self, ):
        """

        :return: hplist, hpdict
        """
        hplist = self.get_hyperparams()
        self.confdict = dict((hp.slug, eval(hp.format.name)(hp.val)) for hp in hplist)
        return hplist, self.confdict

    def set_hp_attributes(self):
        list(setattr(self, hpslug, hpval) for hpslug, hpval in self.confdict.items())

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
                fmt = self.get_format(val)
                hp = hyperParam(task_id=self.task.id,
                                slug=key,
                                remark="Created in task %s" % (self.task.taskname),
                                format_id=fmt.id,
                                created_at=datetime.now(),
                                updated_at=datetime.now(), val=str(val))
                self.s.add(hp)
                self.s.commit()
                return eval(hp.format.name)(hp.val)
        else:
            hp = self.s.query(hyperParam).filter(hyperParam.slug == key, hyperParam.task_id == self.task.id).first()
            if hp:
                return eval(hp.format.name)(hp.val)

    def get_format(self,val):
        """
        A sample value to return format object
        :param val: sample value
        :return: format object
        """
        fmt = self.s.query(dataFormat).filter(dataFormat.name == type(val).__name__).first()
        if fmt == None:
            assert False, "No such format set yet: %s" % (type(val))
        else:
            return fmt

    def new_model_name(self, extra_name="model"):
        """
        :param extra_name: optional, default model, describe this in 1 consequtive string, something like model structure
        :return: a model name
        """
        self.modelnow = "%s_%s" % (self.task.taskname, extra_name)
        return self.modelnow

    def log_weights(self, path, modelname=None, framewk=None):
        hplist, hpdict = self.hp2dict()
        if framewk:
            self.framewk = framewk
        mn = modelname if modelname else self.modelnow
        w = weightModel(task_id=self.task.id, name=mn,
                        path=path, framewk=self.framewk,
                        params_json=json.dumps(hpdict),
                        created_at=datetime.now(), updated_at=datetime.now(),
                        )
        self.s.add(w)
        # self.s.flush()
        self.s.commit()
        wlist = (hyperParamWeight(hp_id=hp.id, weight_id=w.id, valsnap=hp.val) for hp in hplist)
        self.s.add_all(wlist)
        self.s.commit()
        return w

    def m(self, key, val, big_better = True,
          remark = None,
          weight = None):
        """
        recording the metrics
        key: metric name
        val: metric value
        weight: weight object, if None, using the latest weight in task
        """
        val = str(val)
        mt = self.s.query(metricModel).filter(metricModel.slug == key, metricModel.task_id == self.task.id).first()
        if remark == None:
            remark = "creating from task:%s"%(self.task.taskname)
        if mt:
            mt.val = val
        else:
            fmt = self.get_format(val)
            mt = metricModel(slug = key,
                             task_id = self.task.id,
                             format_id = fmt.id,
                             val = str(val),
                             big_better = big_better,
                             remark = remark)
        self.s.add(mt)
        self.s.commit()
        if weight:
            mw = metricWeight(metric_id = mt.id, weight_id = weightModel, valsnap = str(val))
            self.s.add(mw)
            self.s.commit()
        return mt

    def save_metrics(self,metrics,small_list = None, weight = None):
        """
        saving a dictionary of metrics
        :param metrics: dictionary
        :return:
        """
        if small_list ==None: small_list = []
        for k, v in metrics.items():
            kwa = dict({"key":k,"val":v,"weight":weight})
            if k in small_list:
                kwa.update({"big_better":False})
            self.m(**kwa)
