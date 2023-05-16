#encoding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sqlite3

global d
global lang_ok
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///prince.db'
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db = SQLAlchemy(app)

from prince import routes
