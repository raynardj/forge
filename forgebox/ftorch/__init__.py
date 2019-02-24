from ..apicore import forgedb
from .callbacks import recorddf
import torch
import os
from datetime import datetime


class FG(forgedb):
    def __init__(self, *args, **kwargs):
        super(FG, self).__init__(*args, **kwargs)

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

    def weights(self, model, name=None):
        """
        A callback function to save weights
        fg = FG(task = "wgan")
        Trianer(...., callbacks = [fg.wegiths(model_G, name='wgan_g'), fg.weights(model_D,name = 'wgan_d')])
        :param model: A pytorch model
        :param name: Name string of the model, no space and strange charactors
        :return: A weigthModel object
        """
        fgobj = self
        name_ = name
        if name_ == None:
            name_ = self.new_model_name()
        else:  # todo: add a regex to validate a consequtive sting
            name_ = "%s_%s" % (self.train.id, name_)

        def f(record, dataset):
            epoch = list(recorddf(record).epoch)[0]
            name_epoch = "%s.e%s" % (name_, epoch)
            path = self.weightdir / ("%s" % (name_epoch if name_epoch[-4:] == ".npy" else "%s.npy" % (name_epoch)))
            if fgobj.verbose: print("[Model Save]:%s" % (path))
            torch.save(model.state_dict(), path)
            return fgobj.save_weights(path, modelname=name_epoch, framewk="pytorch")

        return f
