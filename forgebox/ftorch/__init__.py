from ..apicore import forgedb
import torch
import os
from datetime import datetime

class FG(forgedb):
    def __init__(self,*args, **kwargs):
        super(FG,self).__init__(*args,**kwargs)

    def save_weights(self,model, modelname = None):
        weightname = "%s_torch_%s.npy"%(self.modelnow,str(int(datetime.now().timestamp()*100)))
        path = os.path.join(self.taskdir, weightname)
        torch.save(model.state_dict(), path)
        w = self.log_weights(path, framewk="pytorch")
        return w

    def metrics(self,f):
        """
        A decorator saving the metrics
        :param f:
        :return:
        """
        def wraper(*args,**kwargs):
            metric_dict = f(*args,**kwargs)
            self.save_metrics(metrics = metric_dict,) #todo put in weight & small_list parameter
            return metric_dict
        return wraper