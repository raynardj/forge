
# Forge ML/DL API Walk Through Tutorial

### With the eg. of titanic dataset (because it's absurdly tiny)

Forge box the the code api for the Forge WebUI, it offers a convenient API when you're coding marchine learning with python.

For now it works seemless with pytorch, I hope api with other frameworks will emerge, like tensorflow/api

If this is the first time you run anything with forge, You'll have to run the command ```forge``` in your terminal first to initialize database.

Without extra configuration, the database will be ``` $HOME/data/forge.db ```. Or you can change it to an assortment of other SQL data base of your choice, like MySQL or PostgreSQL in config.py


```python
import pandas as pd
from forgebox.ftorch import FG
```

    loading configs from /etc/forgebox.cfg
    [Connecting to] sqlite:////Users/salvor/data/forge.db


Set a name for your training task, without space or funny charactors.

A task name will only be marked once, you can run your jupyter notebook or py script repeatatively, it will be considered only one task


```python
fg = FG("titanic2")
p = fg.p
```

    ==========hyper params==========
    {'bench_mark': 0.6, 'dim': 30, 'hidden': 512}


Set the hyper params


```python
BENCH_MARK = p("bench_mark",.6) # bench mark for a prediction to be treated as a positive
DIM = p("dim",30) # latent space for the embedding
HIDDEN = p("hidden",512) # hidden size for neural network
```

```p("hidden")``` will return 512, this is how we can retrieve our hyper-param from the config later

```p("hidden",1024)``` to set hidden size to 1024, meanwhile, the expression will return 1024.

Now we fire up those csv files


```python
train_df = pd.read_csv("/data/titanic/Data/train.csv")
test_df = pd.read_csv("/data/titanic/Data/test.csv")
train_df = train_df.fillna(0)
test_df = test_df.fillna(0)
train_df["AgeZero"] = train_df["Age"].apply(lambda x:(int(x==0))*1)
test_df["AgeZero"] = test_df["Age"].apply(lambda x:(int(x==0))*1)
```


```python
train_df.sample(10)
```


#### Preprocessing tabulated data with forgebox

We have several modules in the forgebox preprocessing package that will speed up the preprocessing on structured data


```python
from forgebox.ftorch.prepro import categorical,minmax,tabulate,categorical_idx
```

```categorical_idx``` can transfer the categorical fields to indices, like 0 for male, 1 for female, 2 for unkown.

The order of indices will be according to the frequency counts, from the most happened situations to the least happened.

The ```build``` function will calculate and record the meta info of this preprocess, based on a pandas data series.

You can specify ```max_``` arguement in the ```build``` function, it will have a max category number, the least happened cases will be summarized as ```other```, the default ```max_``` number is 20


```python
Pclass = categorical_idx("Pclass",)
Pclass.build(train_df.Pclass)

Sex = categorical_idx("Sex")
Sex.build(train_df.Sex)

Embarked = categorical_idx("Embarked")
Embarked.build(train_df.Embarked)

AgeZero = categorical_idx("AgeZero")
AgeZero.build(train_df.AgeZero)
```

       Pclass
    3     491
    1     216
    2     184
            Sex
    male    577
    female  314
       Embarked
    S       644
    C       168
    Q        77
    0         2
       AgeZero
    0      714
    1      177


MinMax is to change the range of the data series, the any data in the column will be capped to max or min, and scale down/up to a machine learning model friendly level.


```python
Age = minmax("Age")
Age.build(train_df.Age)

SibSp = minmax("SibSp")
SibSp.build(train_df.SibSp)

Parch = minmax("Parch")
Parch.build(train_df.Parch)

Fare = minmax("Fare")
Fare.build(train_df.Fare)
```

    min_:0.000 	max_:80.000	 range:80.000
    min_:0.000 	max_:8.000	 range:8.000
    min_:0.000 	max_:6.000	 range:6.000
    min_:0.000 	max_:512.329	 range:512.329


```Tabulate``` is how we combine several column preprocess channels into one.

Notice! the you can use another ```Tabulate``` as a column, and combine it further with other columns


```python
x_pre = tabulate("x_pre")
x_pre.build(Pclass,Sex,Embarked,AgeZero,Age,SibSp,Parch,Fare)
```

Here we preprocess our "Y" data


```python
Survived = minmax("Survived")
Survived.build(train_df["Survived"])
```

    min_:0.000 	max_:1.000	 range:1.000



```python
y_pre = tabulate("y_pre")
y_pre.build(Survived)
```

Now we check our preprocess channel with dataframe.


```python
x_pre.prepro(train_df), y_pre.prepro(train_df)
```




    ((891, 8), (891, 1))



Titanic is a tiny dataset by size, if you are using forgebox for real project, dataframe will be much bigger, you can use ```x_pre.prepro(train_df.head(20))``` instead

#### Build up a pytorch model


```python
import torch
from torch import nn

class ti_mlp(nn.Module):
    def __init__(self):
        super().__init__()
        self.emb_p = nn.Embedding(len(Pclass.cate_list),DIM)
        self.emb_s = nn.Embedding(len(Sex.cate_list),DIM)
        self.emb_e = nn.Embedding(len(Embarked.cate_list),DIM)
        self.emb_a = nn.Embedding(2,DIM)
        self.mlp = nn.Sequential(*[
            nn.Linear(DIM*4+4,HIDDEN,bias=False),
            nn.BatchNorm1d(HIDDEN),
            nn.ReLU(),
            nn.Linear(HIDDEN,HIDDEN,bias=False),
            nn.BatchNorm1d(HIDDEN),
            nn.ReLU(),
            nn.Linear(HIDDEN,1,bias=False),
            nn.Sigmoid(),
        ])
    def forward(self,x):
        p,s,e,a,conti = x[:,:1].long(),x[:,1:2].long(),x[:,2:3].long(),x[:,3:4].long(),x[:,4:].float()
        x_ = torch.cat([self.emb_p(p).squeeze(1),
                        self.emb_s(s).squeeze(1),
                        self.emb_e(e).squeeze(1),
                        self.emb_a(a).squeeze(1),
                        conti],dim=1)
        return self.mlp(x_)
```


```python
from forgebox.ftorch.prepro import DF_Dataset,fuse
from forgebox.ftorch.train import Trainer
from forgebox.ftorch.metrics import accuracy,recall,precision
```

The following is to make pytorch dataset, which a familiar term with pytorch users, it's just another pytorch dataset, can be further put into a pytorh dataloader.

But, forgebox put the batchsize configuration in dataset instead of dataloader.

Reason:since tabulation data usually goes beyond hundreds, if putting the batchsize in dataloader, we'll end up running line by line non-parallel iterations by python, which is sssllooowww, hence every python coders's big-no-no. We use the numpy/pandas slicing to replace the simple "for" loop


```python
train_ds_x = DF_Dataset(train_df,prepro=x_pre.prepro,bs=64,shuffle=False)
train_ds_y = DF_Dataset(train_df,prepro=y_pre.prepro,bs=64,shuffle=False)
train_ds = fuse(train_ds_x,train_ds_y)

valid_ds_x = DF_Dataset(test_df,prepro=x_pre.prepro,bs=64,shuffle=False)
valid_ds_y = DF_Dataset(test_df,prepro=y_pre.prepro,bs=64,shuffle=False)
valid_ds = fuse(valid_ds_x,valid_ds_y)
```


```python
from forgebox.ftorch.callbacks import print_all,recorddf,mars,stat
```


```python
model = ti_mlp()
```


```python
from torch.optim import Adam

opt = Adam(model.parameters())
loss_func = nn.BCELoss()

trainer=Trainer(train_ds, val_dataset=valid_ds, # dataset
                batch_size=1, # batch size in dataloader, it has to be 1 in this case
                fg=fg,
                print_on=2, # print on every 2 steps
                callbacks=[print_all, # print all metrics
                           stat,fg.logs(), # save the training log
                           fg.metrics(), # save the metrics
                           fg.weights(model) # save the model weights
                          ])
```

Define a training step and a validation step

Here we don't embody the optimizer or model into Trainer, that's how we can use several different types of optimizers to update several models in a free style way totally in you dictates.

What you decide is what will happen, within an iteration, given a batch of data.


```python
@trainer.step_train
def action(batch):
    x,y = batch.data
    if batch.i == 0:
        model.train()
    x = x.squeeze(0)
    y = y.float()

    opt.zero_grad()

    y_ = model(x)

    loss = loss_func(y_,y)
    acc = accuracy(y_,y.long())
    rec = recall(y_,y.long())
    prec = precision(y_,y.long().squeeze(0))
    f1 = (rec*prec)/(rec+prec)

    loss.backward()
    opt.step()
    return {"loss":loss.item(),"acc":acc.item(),"rec":rec.item(),"prec":prec.item(),"f1":f1.item()}

@trainer.step_val
def val_action(batch):
    x,y = batch.data
    if batch.i == 0:
        model.eval()
    x = x.squeeze(0)
    y = y.float()
    y_ = model(x)

    loss = loss_func(y_,y)
    acc = accuracy(y_,y.long())
    rec = recall(y_,y.long())
    prec = precision(y_,y.long().squeeze(0))
    f1 = (rec*prec)/(rec+prec)

    return {"loss":loss.item(),"acc":acc.item(),"rec":rec.item(),"prec":prec.item(),"f1":f1.item()}
```

Train the model!


```python
trainer.train(3)
```

