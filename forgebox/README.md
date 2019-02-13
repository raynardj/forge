# The coding add-on for mananging AI tasks

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
## PyTorch Integration
For pytorch users, Forge is intergrated into the training framework. Check [ftorch](forgebox/ftorch) for detail
