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
from orm import *
def group(projects):
    # Cost: O(((? * projects) + (lans * projects) + (problems * projects)))
    #       O(((? * projects) + (lans * projects) + (problems * projects)))
    ProjectsGroupByLanguage = Map()
    ProjectsGroupByProblem = Map()
    for p in projects:
        lan_col = p.language.split(',')
        pro_col = p.problem.split(',')
        lans = map(strip, lan_col)
        problems = map(strip, pro_col)
        for lan in lans:
            if (lan != ''):
                if (lan in ProjectsGroupByLanguage):
                    ProjectsGroupByLanguage[lan].add(p)
                else:
                    ProjectsGroupByLanguage[lan] = Set()
                    ProjectsGroupByLanguage[lan].add(p)
        for problem in problems:
            if (problem != ''):
                if (problem in ProjectsGroupByProblem):
                    ProjectsGroupByProblem[problem].add(p)
                else:
                    ProjectsGroupByProblem[problem] = Set()
                    ProjectsGroupByProblem[problem].add(p)
    return (sortByTitle(ProjectsGroupByLanguage), sortByTitle(ProjectsGroupByProblem))

(p_by_language, p_by_problem) = group(db_all_projects)
def index():
    # Cost: O(?)
    #       O(?)
    query = {}
    query['groupBy'] = request.args.get('groupBy', '')
    response = make_response('web')
    if (query['groupBy'] == 'problem'):
        return render('index_groupby_problem.html', p_by_problem)
    else:
        return render('index.html', p_by_language)

app.route('/')(index)
