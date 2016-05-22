from incoq.runtime import *
import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask import make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
import random
import sys
import inspect
from sqlalchemy import desc
app = Flask(__name__)
Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://webadmin:webadmin123.@s2.zhujieao.com/dist'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
def sqlSearch():
    sql1 = 'select p1.title from projects p1, projects p2  where p1.developer = p2.developer and p1.title <> p2.title'
    sql2 = 'select p1.title from projects p1, comments c1  where p1.id = c1.pid'
    res = []
    if sql != '':
        results = db.engine.execute(sql)
        if results is not None:
            for row in results:
                res.append(list(row))
    res = json.dumps(res)
