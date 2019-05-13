import pandas as pd
import numpy as np
import nltk

tweet_tk =nltk.tokenize.TweetTokenizer()


class DF_Node(object):
    def __init__(self, df, verbose=1):
        super().__init__()
        self.df = df
        self.verbose = verbose
        self.pipenames = list()
        self.pipe = list()

    def __str__(self):
        return "<forge pipeline node>"

    def __or__(self, process_step):
        self.pipe.append(process_step)
        self.pipenames.append(process_step.edge_name)
        return self

    def run(self):
        for pro_i in range(len(self.pipe)):
            if self.verbose > 0: print("[df edge]:%s" % self.pipenames[pro_i])
            pro = self.pipe[pro_i]
            self.df = pro.pro(self.df)
        return self.df


class DF_Chunk_Node(DF_Node):
    def __init__(self, df, verbose=1):
        super().__init__(df, verbose)

    def run(self):
        for df in self.df:
            for pro_i in range(len(self.pipe)):
                if self.verbose > 0: print("[df edge]:%s" % self.pipenames[pro_i])
                pro = self.pipe[pro_i]
                df = pro.pro(df)


class DF_Edge(object):
    def __init__(self, edge_name=None):
        super().__init__()
        if edge_name == None:
            edge_name = "DataFrame_Processing_Edge"
        self.edge_name = edge_name

    def __mul__(self, cols):
        assert 0, "Only Col_Edge support * columns operation"

    def define(self, f):
        def wraper(df):
            return f(df)

        self.pro = wraper
        return wraper


class Col_Edge(object):
    def __init__(self, edge_name=None):
        super().__init__()
        if edge_name == None:
            edge_name = "DataSeries_Processing_Edge"
        self.edge_name = edge_name

    def __mul__(self, cols):
        self.cols = cols
        return self

    def define(self, f):
        def wraper(df):
            for col in self.cols:
                df[col] = f(df[col])
            return df

        self.pro = wraper
        return wraper


nothing = DF_Edge("ept_process")


@nothing.define
def donothing(df):
    return df


class FillNa_Edge(Col_Edge):
    def __init__(self, fill=0.):
        super().__init__("fillna")
        self.fill = fill

    def pro(self, df):
        for c in self.cols:
            df[c] = df[c].fillna(self.fill)
        return df


class EngTok_Edge(Col_Edge):
    def __init__(self, tokenizer = tweet_tk, max_len=None):
        super().__init__("En")
        self.tokenizer = tokenizer
        self.max_len = max_len

    def pro(self, df):
        for c in self.cols:
            df[c] = df[c].apply(lambda x: self.tokenizer.tokenize(x)[:self.max_len])
        return df