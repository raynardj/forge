from ..apicore import forgedb
from .callbacks import recorddf
import torch
import os
from datetime import datetime


class FG(forgedb):
    def __init__(self, *args, **kwargs):
        super(FG, self).__init__(*args, **kwargs)

    def save_weights(self, model, modelname=None):
        weightname = "%s_torch_%s.npy" % (self.modelnow, str(int(datetime.now().timestamp() * 100)))
        path = os.path.join(self.taskdir, weightname)
        torch.save(model.state_dict(), path)
        w = self.log_weights(path, framewk="pytorch")
        return w

    # callbacks
    def metrics(self, adapt=["mean"], ):
        """
        return a function to save metrics
        :param adapt: list, default ["mean"], possible values:"mean","min","max","std","20%","50%","70%"
        """

        def func(record, dataset):
            df = recorddf(record)
            des = df.describe().loc[adapt, :]
            metric_dict = dict()
            for col in des.columns:
                des.apply(lambda x: metric_dict.update({"%s_%s" % (x.name, col): x[col]}), axis=1)
            if self.verbose:
                print(metric_dict, flush=True)
            self.save_metrics(metrics=metric_dict)
            return metric_dict

        return func
