# The pytorch core for mananging AI tasks

## This module should run independently from forge web UI


## Change the default db usage
* In [config.py](config.py) setting the following:
```python
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATADIR, 'forge.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////mnt/disk1/forge.db')
```

## Task Management

You can add a task at the Web UI ```http://[host]:[port]/task/add```

## Set/ Read Hyper Params

```python
from forgebox.apicore import forgedb
fg = forgedb("nlp_binary_classification")
p = fg.p
```

Read the hyper param from database
```python
hs1 = p("hidden_size1")
```

Set a new hyper param, like, 3 epochs for training
```python
epochs = p("nb_epochs",3)
```
## PyTorch Intergration
For pytorch users, Forge is intergrated into the training framework:


### Preprocessor
forgebox contains data pre-processing module for pytorch.

It returns pytorch dataset
```python
from forgebox.ftorch.prepro import DF_Dataset,fuse
train_ds_x = DF_Dataset(train_df, # pandas dataframe for training
                        prepro=x_prepro, # x_prepro is the function: input a chunk of dataframe, return same len of data in numpy array
                        bs=64, # batch_size
                        shuffle=False)
# train_ds_x will be a pytorch dataset
train_ds_y = DF_Dataset(train_df,prepro=y_prepro,bs=64,shuffle=False)
```
fuse combines 2 datasets together,
```python
train_ds = fuse(train_ds_x,train_ds_y)
```
we can use it like ```x,y = next(iter(train_ds))```

### Trainer
```python
from forgebox.ftorch.train import Trainer
from forgebox.ftorch.metrics import accuracy,recall,precision

trainer=Trainer(train_ds, val_dataset = valid_ds ,batch_size=1,print_on=2)
```

#### A training step
we use the step_train decorator to define a training step
```python
@trainer.step_train
def action(*args,**kwargs):
    x,y = args[0]
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
    return {"loss":loss.item(),"acc":acc,"rec":rec,"prec":prec,"f1":f1}
```
The above is only an example, you can define the training step as you like.

Even if you have 3 models, updated by 2 optimizers, as long as you can decribe them in a single training step, it can be done easily.

#### A validation step
Very similar to the train step, minus any code relate to updating weights

```python
@trainer.step_val # step_val decorator
def val_action(*args,**kwargs)
    x,y = args[0]
    x = x.squeeze(0)
    y = y.float()
    y_ = model(x)
    ...
```
