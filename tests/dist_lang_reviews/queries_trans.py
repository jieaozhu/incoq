# Q : projects_python, projects_github -> {(projects_python, projects_github, p1_developer) for (projects_python, projects_github) in REL(_U_Q) for (projects_python, p1) in M() for (projects_github, p1) in M() for (p1, p1_developer) in F(developer)} : {({Bottom}, {Bottom}, Top)}
from incoq.runtime import *
# _U_Q : {({Bottom}, {Bottom})}
_U_Q = Set()
# R_Q : {({Bottom}, {Bottom}, Top)}
R_Q = CSet()
# _U_Q_bu : {{Bottom}: {{Bottom}}}
_U_Q_bu = Map()
# _U_Q_ub : {{Bottom}: {{Bottom}}}
_U_Q_ub = Map()
# _M_ub : {Top: {Top}}
_M_ub = Map()
# R_Q_bbu : {({Bottom}, {Bottom}): {Top}}
R_Q_bbu = Map()
def _maint__U_Q_bu_for__U_Q_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v9_key = _elem_v1
    _v9_value = _elem_v2
    if (_v9_key not in _U_Q_bu):
        _v10 = Set()
        _U_Q_bu[_v9_key] = _v10
    _U_Q_bu[_v9_key].add(_v9_value)

def _maint__U_Q_ub_for__U_Q_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v12_key = _elem_v2
    _v12_value = _elem_v1
    if (_v12_key not in _U_Q_ub):
        _v13 = Set()
        _U_Q_ub[_v12_key] = _v13
    _U_Q_ub[_v12_key].add(_v12_value)

def _maint__M_ub_for__M_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v15_key = _elem_v2
    _v15_value = _elem_v1
    if (_v15_key not in _M_ub):
        _v16 = Set()
        _M_ub[_v15_key] = _v16
    _M_ub[_v15_key].add(_v15_value)

def _maint_R_Q_bbu_for_R_Q_add(_elem):
    (_elem_v1, _elem_v2, _elem_v3) = _elem
    _v18_key = (_elem_v1, _elem_v2)
    _v18_value = _elem_v3
    if (_v18_key not in R_Q_bbu):
        _v19 = Set()
        R_Q_bbu[_v18_key] = _v19
    R_Q_bbu[_v18_key].add(_v18_value)

def _maint_R_Q_bbu_for_R_Q_remove(_elem):
    (_elem_v1, _elem_v2, _elem_v3) = _elem
    _v20_key = (_elem_v1, _elem_v2)
    _v20_value = _elem_v3
    R_Q_bbu[_v20_key].remove(_v20_value)
    if (len(R_Q_bbu[_v20_key]) == 0):
        del R_Q_bbu[_v20_key]

def _maint_R_Q_for__U_Q_add(_elem):
    # Cost: O(_v3_projects_python)
    #       O(_v3_projects_python)
    (_v3_projects_python, _v3_projects_github) = _elem
    if isset(_v3_projects_python):
        for _v3_p1 in _v3_projects_python:
            if isset(_v3_projects_github):
                if (_v3_p1 in _v3_projects_github):
                    if hasfield(_v3_p1, 'developer'):
                        _v3_p1_developer = _v3_p1.developer
                        _v3_result = (_v3_projects_python, _v3_projects_github, _v3_p1_developer)
                        if (_v3_result not in R_Q):
                            R_Q.add(_v3_result)
                            _maint_R_Q_bbu_for_R_Q_add(_v3_result)
                        else:
                            R_Q.inccount(_v3_result)

def _maint_R_Q_for__M_add(_elem):
    # Cost: O((_U_Q_bu + _U_Q_ub))
    #       O((_U_Q_bu + _U_Q_ub))
    (_v5_projects_python, _v5_p1) = _elem
    if hasfield(_v5_p1, 'developer'):
        _v5_p1_developer = _v5_p1.developer
        for _v5_projects_github in (_U_Q_bu[_v5_projects_python] if (_v5_projects_python in _U_Q_bu) else ()):
            if isset(_v5_projects_github):
                if (_v5_p1 in _v5_projects_github):
                    if ((_v5_projects_github, _v5_p1) != _elem):
                        _v5_result = (_v5_projects_python, _v5_projects_github, _v5_p1_developer)
                        if (_v5_result not in R_Q):
                            R_Q.add(_v5_result)
                            _maint_R_Q_bbu_for_R_Q_add(_v5_result)
                        else:
                            R_Q.inccount(_v5_result)
    (_v5_projects_github, _v5_p1) = _elem
    if hasfield(_v5_p1, 'developer'):
        _v5_p1_developer = _v5_p1.developer
        for _v5_projects_python in (_U_Q_ub[_v5_projects_github] if (_v5_projects_github in _U_Q_ub) else ()):
            if isset(_v5_projects_python):
                if (_v5_p1 in _v5_projects_python):
                    _v5_result = (_v5_projects_python, _v5_projects_github, _v5_p1_developer)
                    if (_v5_result not in R_Q):
                        R_Q.add(_v5_result)
                        _maint_R_Q_bbu_for_R_Q_add(_v5_result)
                    else:
                        R_Q.inccount(_v5_result)

def _demand_Q(_elem):
    # Cost: O(_v3_projects_python)
    #       O(_v3_projects_python)
    if (_elem not in _U_Q):
        _U_Q.add(_elem)
        _maint__U_Q_bu_for__U_Q_add(_elem)
        _maint__U_Q_ub_for__U_Q_add(_elem)
        _maint_R_Q_for__U_Q_add(_elem)

def strip(x):
    # Cost: O(?)
    #       O(?)
    return x.strip()

def do_query(ps):
    # Cost: O(((? * ps) + (_U_Q_bu * ps) + (_U_Q_ub * ps) + _v3_projects_python))
    #       O(((? * ps) + (_U_Q_bu * ps) + (_U_Q_ub * ps) + _v3_projects_python))
    projects_python = Set()
    projects_github = Set()
    for p in ps:
        if ('python' in map(strip, p.language.lower().split(','))):
            _v1 = (projects_python, p)
            index(_v1, 0).add(index(_v1, 1))
            _maint__M_ub_for__M_add(_v1)
            _maint_R_Q_for__M_add(_v1)
        if ('github' in p.home_page):
            _v2 = (projects_github, p)
            index(_v2, 0).add(index(_v2, 1))
            _maint__M_ub_for__M_add(_v2)
            _maint_R_Q_for__M_add(_v2)
    print(((_demand_Q((projects_python, projects_github)) or True) and (R_Q_bbu[(projects_python, projects_github)] if ((projects_python, projects_github) in R_Q_bbu) else Set())))

