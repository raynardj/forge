# The pytorch core for mananging AI tasks

## This module should run independently from forge web UI


## Change the default db usage
* In [config.py](config.py) setting the following:
```python
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATADIR, 'forge.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////mnt/disk1/forge.db')
```
TODO move ray to here