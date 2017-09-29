from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
from flask_login import LoginManager
from flask_openid import OpenID 
from config import basedir

print "initializing flask objec in __init__.py"	

app=Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login' #View function name which handles user login

oid=OpenID(app,os.path.join(basedir,'tmp'))

from app import views,models
