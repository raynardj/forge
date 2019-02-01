import os
DATADIR = os.path.expanduser("~/data")
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATADIR, 'forge.db')