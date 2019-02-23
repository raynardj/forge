import os
from datetime import datetime
import __main__ as main
from torch.utils.data import DataLoader
from tqdm import trange
from functools import reduce
import pandas as pd
try:
    JUPYTER = True if main.get_ipython else False
except:
    JUPYTER = False

if JUPYTER:from tqdm import tqdm_notebook as tn

class Trainer:
    def __init__(self, dataset, val_dataset=None, batch_size=16, fg = None,
                 print_on=20, fields=None, is_log=True, shuffle=True,
                 conn=None, modelName="model", tryName="try", callbacks = [], val_callbacks = []):
        """
        Pytorch trainer
        fields: the fields you choose to print out
        is_log: writing a log？

        Training:

        write action function for a step of training,
        assuming a generator will spit out tuple x,y,z in each:

        def action(*args,**kwargs):
            x,y,z = args[0]
            x,y,z = x.cuda(),y.cuda(),z.cuda()

            #optimizer is a global variable, or many different optimizers if you like
            sgd.zero_grad()
            adam.zero_grad()

            # model is a global variable, or many models if you like
            y_ = model(x)
            y2_ = model_2(z)

            ...... more param updating details here

            return {"loss":loss.data[0],"acc":accuracy.data[0]}
            ...

        then pass the function to object
        trainer=Trainer(...)
        trainer.action=action
        trainer.train(epochs = 30)

        same work for validation:trainer.val_action = val_action

        conn: a sql table connection, (sqlalchemy). if assigned value, save the record in the designated sql database;
        """
        self.batch_size = batch_size
        self.dataset = dataset
        self.conn = conn
        self.fg = fg
        self.modelName = modelName
        self.tryName = tryName
        self.train_data = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=shuffle)
        self.train_len = len(self.train_data)
        self.val_dataset = val_dataset
        self.print_on = print_on

        self.callbacks = callbacks
        self.val_callbacks = val_callbacks

        if self.val_dataset:
            self.val_dataset = val_dataset
            self.val_data = DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=shuffle)
            self.val_len = len(self.val_data)
            self.val_track = dict()

        self.track = dict()
        self.fields = fields
        self.is_log = is_log

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def train(self, epochs, name=None, log_addr=None):
        """
        Train the model for some epochs
        """
        if name == None:
            name = "torch_train_" + datetime.now().strftime("%y%m%d_%H%M%S")
        if log_addr == None:
            log_addr = ".log_%s" % (name)

        if log_addr[-1] != "/": log_addr += "/"

        for epoch in range(epochs):
            self.track[epoch] = list()
            self.run(epoch)
        if self.is_log:
            os.system("mkdir -p %s" % (log_addr))
            trn_track = pd.DataFrame(reduce((lambda x, y: x + y), list(self.track.values())))
            trn_track = trn_track.to_csv(log_addr + "trn_" + datetime.now().strftime("%y_%m_%d__%H_%M_%S") + ".csv",
                                         index=False)

            if self.val_dataset:
                val_track = pd.DataFrame(reduce((lambda x, y: x + y), list(self.val_track.values())))
                val_track.to_csv(log_addr + "val_" + datetime.now().strftime("%y_%m_%d__%H_%M_%S") + ".csv",
                                 index=False)

        if self.fg:
            return self.fg.new_train()

    def run(self, epoch):
        """
        run for a single epoch
        :param epoch: the epoch index
        :return:
        """
        if JUPYTER:
            t = tn(range(self.train_len))
        else:
            t = trange(self.train_len)
        self.train_gen = iter(self.train_data)

        for i in t:
            ret = self.action(next(self.train_gen), epoch=epoch, ite=i)
            ret.update({"epoch": epoch,
                        "iter": i,
                        "ts": self.get_time()})
            self.track[epoch].append(ret)

            if i % self.print_on == self.print_on - 1:
                self.update_descrition(epoch, i, t)
        for cb_func in self.callbacks:
            cb_func(record = self.track[epoch],dataset = self.dataset, )

        if self.val_dataset:

            self.val_track[epoch] = list()
            self.val_gen = iter(self.val_data)
            if JUPYTER:
                val_t = tn(range(self.val_len))
            else:
                val_t = trange(self.val_len)

            for i in val_t:
                ret = self.val_action(next(self.val_gen), epoch=epoch, ite=i)
                ret.update({"epoch": epoch,
                            "iter": i,
                            "ts": self.get_time()})
                self.val_track[epoch].append(ret)
                self.update_descrition_val(epoch, i, val_t)

            for v_cb_func in self.val_callbacks:
                v_cb_func(record = self.val_track[epoch],dataset = self.val_dataset, )

    def update_descrition(self, epoch, i, t):
        window_df = pd.DataFrame(self.track[epoch][max(i - self.print_on, 0):i])

        if self.conn:  # if saving to a SQL database
            window_df["split_"] = "train"
            window_df["tryName"] = self.tryName + "_train"
            window_df.to_sql("track_%s" % (self.modelName), con=self.conn, if_exists="append", index=False)
        window_dict = dict(window_df.mean())
        del window_dict["epoch"]
        del window_dict["iter"]

        desc = "⭐[ep_%s_i_%s]" % (epoch, i)
        if JUPYTER:
            t.set_postfix(window_dict)
        else:
            if self.fields != None:
                desc += "✨".join(list("\t%s\t%.3f" % (k, v) for k, v in window_dict.items() if k in self.fields))
            else:
                desc += "✨".join(list("\t%s\t%.3f" % (k, v) for k, v in window_dict.items()))
        t.set_description(desc)

    def update_descrition_val(self, epoch, i, t):
        if self.conn:  # if saving to a SQL database
            window_df = pd.DataFrame(self.val_track[epoch][max(i - self.print_on, 0):i])
            window_df["split_"] = "valid"
            window_df["tryName"] = self.tryName + "_valid"
            window_df.to_sql("track_%s" % (self.modelName), con=self.conn, if_exists="append", index=False)
        window_dict = dict(pd.DataFrame(self.val_track[epoch]).mean())
        # print(pd.DataFrame(self.val_track[epoch]))
        del window_dict["epoch"]
        del window_dict["iter"]

        desc = "😎[val_ep_%s_i_%s]" % (epoch, i)
        if JUPYTER:
            t.set_postfix(window_dict)
        else:
            if self.fields != None:
                desc += "😂".join(list("\t%s\t%.3f" % (k, v) for k, v in window_dict.items() if k in self.fields))
            else:
                desc += "😂".join(list("\t%s\t%.3f" % (k, v) for k, v in window_dict.items()))
        t.set_description(desc)

    def todataframe(self, dict_):
        """return a dataframe on the train log dictionary"""
        tracks = []
        for i in range(len(dict_)):
            tracks += dict_[i]

        return pd.DataFrame(tracks)

    def save_track(self, filepath, val_filepath=None): # todo: move this to a callback
        """
        Save the track to csv files in a path you designated,
        :param filepath: a file path ended with .csv
        :return: None
        """
        self.todataframe(self.track).to_csv(filepath, index=False)
        if val_filepath:
            self.todataframe(self.val_track).to_csv(val_filepath, index=False)

    def step_train(self,f):
        def wraper(*args,**kwargs):
            return f(*args,**kwargs)
        self.action = wraper
        return wraper

    def step_val(self,f):
        def wraper(*args,**kwargs):
            return f(*args,**kwargs)
        self.val_action = wraper
        return wraper