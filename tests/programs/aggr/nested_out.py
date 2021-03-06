# Q1 : x -> {(x, w) for (x, w) in REL(S)} : {(Number, Number)}
# Q2 : x -> min(unwrap(R_Q1.imglookup('bu', (x,))), (x,), R__QU_Q2) : Top
# Q3 : x -> {(x, z) for (x, y) in REL(S) for (y, z) in REL(S) for (x, _v10) in SETFROMMAP(SA_Q2, A_Q2, 'bu') if (y <= index(_v10, 1))} : {(Number, Number)}
# _QU_Q2 : {(_v2x,) for (_v2x, _v2y) in REL(S) for (_v2y, _v2z) in REL(S)} : {(Number)}
from incoq.runtime import *
# R__QU_Q2 : {(Number)}
R__QU_Q2 = CSet()
# R_Q3 : {(Number, Number)}
R_Q3 = CSet()
# A_Q2 : {(Number): (Number, Number)}
A_Q2 = Map()
# S_bu : {Number: {Number}}
S_bu = Map()
# S_ub : {Number: {Number}}
S_ub = Map()
# R_Q1_bu : {Number: {(Number)}}
R_Q1_bu = Map()
# R_Q3_bu : {Number: {(Number)}}
R_Q3_bu = Map()
def _maint_S_bu_for_S_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v17_key = _elem_v1
    _v17_value = _elem_v2
    if (_v17_key not in S_bu):
        _v18 = Set()
        S_bu[_v17_key] = _v18
    S_bu[_v17_key].add(_v17_value)

def _maint_S_ub_for_S_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v20_key = _elem_v2
    _v20_value = _elem_v1
    if (_v20_key not in S_ub):
        _v21 = Set()
        S_ub[_v20_key] = _v21
    S_ub[_v20_key].add(_v20_value)

def _maint_R_Q1_bu_for_R_Q1_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v23_key = _elem_v1
    _v23_value = (_elem_v2,)
    if (_v23_key not in R_Q1_bu):
        _v24 = Set()
        R_Q1_bu[_v23_key] = _v24
    R_Q1_bu[_v23_key].add(_v23_value)

def _maint_R_Q1_bu_for_R_Q1_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v25_key = _elem_v1
    _v25_value = (_elem_v2,)
    R_Q1_bu[_v25_key].remove(_v25_value)
    if (len(R_Q1_bu[_v25_key]) == 0):
        del R_Q1_bu[_v25_key]

def _maint_R_Q3_bu_for_R_Q3_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v26_key = _elem_v1
    _v26_value = (_elem_v2,)
    if (_v26_key not in R_Q3_bu):
        _v27 = Set()
        R_Q3_bu[_v26_key] = _v27
    R_Q3_bu[_v26_key].add(_v26_value)

def _maint_R_Q3_bu_for_R_Q3_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v28_key = _elem_v1
    _v28_value = (_elem_v2,)
    R_Q3_bu[_v28_key].remove(_v28_value)
    if (len(R_Q3_bu[_v28_key]) == 0):
        del R_Q3_bu[_v28_key]

def _maint_R_Q3_for_S_add(_elem):
    (_v13_x, _v13_y) = _elem
    if ((_v13_x,) in A_Q2):
        _v13__v10 = A_Q2[(_v13_x,)]
        if (_v13_y <= index(_v13__v10, 1)):
            for _v13_z in (S_bu[_v13_y] if (_v13_y in S_bu) else ()):
                if ((_v13_y, _v13_z) != _elem):
                    _v13_result = (_v13_x, _v13_z)
                    if (_v13_result not in R_Q3):
                        R_Q3.add(_v13_result)
                        _maint_R_Q3_bu_for_R_Q3_add(_v13_result)
                    else:
                        R_Q3.inccount(_v13_result)
    (_v13_y, _v13_z) = _elem
    for _v13_x in (S_ub[_v13_y] if (_v13_y in S_ub) else ()):
        if ((_v13_x,) in A_Q2):
            _v13__v10 = A_Q2[(_v13_x,)]
            if (_v13_y <= index(_v13__v10, 1)):
                _v13_result = (_v13_x, _v13_z)
                if (_v13_result not in R_Q3):
                    R_Q3.add(_v13_result)
                    _maint_R_Q3_bu_for_R_Q3_add(_v13_result)
                else:
                    R_Q3.inccount(_v13_result)

def _maint_R_Q3_for_SA_Q2_add(_elem):
    (_v15_x, _v15__v10) = _elem
    for _v15_y in (S_bu[_v15_x] if (_v15_x in S_bu) else ()):
        if (_v15_y <= index(_v15__v10, 1)):
            for _v15_z in (S_bu[_v15_y] if (_v15_y in S_bu) else ()):
                _v15_result = (_v15_x, _v15_z)
                if (_v15_result not in R_Q3):
                    R_Q3.add(_v15_result)
                    _maint_R_Q3_bu_for_R_Q3_add(_v15_result)
                else:
                    R_Q3.inccount(_v15_result)

def _maint_R_Q3_for_SA_Q2_remove(_elem):
    (_v16_x, _v16__v10) = _elem
    for _v16_y in (S_bu[_v16_x] if (_v16_x in S_bu) else ()):
        if (_v16_y <= index(_v16__v10, 1)):
            for _v16_z in (S_bu[_v16_y] if (_v16_y in S_bu) else ()):
                _v16_result = (_v16_x, _v16_z)
                if (R_Q3.getcount(_v16_result) == 1):
                    _maint_R_Q3_bu_for_R_Q3_remove(_v16_result)
                    R_Q3.remove(_v16_result)
                else:
                    R_Q3.deccount(_v16_result)

def _maint_SA_Q2_for_A_Q2_assign(_key, _val):
    (_key_v1,) = _key
    _v11_elem = (_key_v1, _val)
    _maint_R_Q3_for_SA_Q2_add(_v11_elem)

def _maint_SA_Q2_for_A_Q2_delete(_key):
    _val = A_Q2[_key]
    (_key_v1,) = _key
    _v12_elem = (_key_v1, _val)
    _maint_R_Q3_for_SA_Q2_remove(_v12_elem)

def _maint_A_Q2_for_R_Q1_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v7_key = (_elem_v1,)
    _v7_value = _elem_v2
    if (_v7_key in R__QU_Q2):
        _v7_state = A_Q2[_v7_key]
        (_v7tree, _) = _v7_state
        _v7tree[_v7_value] = None
        _v7_state = (_v7tree, _v7tree.__min__())
        _maint_SA_Q2_for_A_Q2_delete(_v7_key)
        del A_Q2[_v7_key]
        A_Q2[_v7_key] = _v7_state
        _maint_SA_Q2_for_A_Q2_assign(_v7_key, _v7_state)

def _maint_A_Q2_for_R_Q1_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v8_key = (_elem_v1,)
    _v8_value = _elem_v2
    if (_v8_key in R__QU_Q2):
        _v8_state = A_Q2[_v8_key]
        (_v8tree, _) = _v8_state
        del _v8tree[_v8_value]
        _v8_state = (_v8tree, _v8tree.__min__())
        _maint_SA_Q2_for_A_Q2_delete(_v8_key)
        del A_Q2[_v8_key]
        A_Q2[_v8_key] = _v8_state
        _maint_SA_Q2_for_A_Q2_assign(_v8_key, _v8_state)

def _maint_A_Q2_for_R__QU_Q2_add(_key):
    _v9_state = (Tree(), None)
    (_key_v1,) = _key
    for (_v9_value,) in (R_Q1_bu[_key_v1] if (_key_v1 in R_Q1_bu) else Set()):
        (_v9tree, _) = _v9_state
        _v9tree[_v9_value] = None
        _v9_state = (_v9tree, _v9tree.__min__())
    A_Q2[_key] = _v9_state
    _maint_SA_Q2_for_A_Q2_assign(_key, _v9_state)

def _maint_A_Q2_for_R__QU_Q2_remove(_key):
    _maint_SA_Q2_for_A_Q2_delete(_key)
    del A_Q2[_key]

def _maint_R__QU_Q2_for_S_add(_elem):
    (_v5__v2x, _v5__v2y) = _elem
    for _v5__v2z in (S_bu[_v5__v2y] if (_v5__v2y in S_bu) else ()):
        if ((_v5__v2y, _v5__v2z) != _elem):
            _v5_result = (_v5__v2x,)
            if (_v5_result not in R__QU_Q2):
                R__QU_Q2.add(_v5_result)
                _maint_A_Q2_for_R__QU_Q2_add(_v5_result)
            else:
                R__QU_Q2.inccount(_v5_result)
    (_v5__v2y, _v5__v2z) = _elem
    for _v5__v2x in (S_ub[_v5__v2y] if (_v5__v2y in S_ub) else ()):
        _v5_result = (_v5__v2x,)
        if (_v5_result not in R__QU_Q2):
            R__QU_Q2.add(_v5_result)
            _maint_A_Q2_for_R__QU_Q2_add(_v5_result)
        else:
            R__QU_Q2.inccount(_v5_result)

def _maint_R_Q1_for_S_add(_elem):
    (_v3_x, _v3_w) = _elem
    _v3_result = (_v3_x, _v3_w)
    _maint_R_Q1_bu_for_R_Q1_add(_v3_result)
    _maint_A_Q2_for_R_Q1_add(_v3_result)

def main():
    for (a, b) in [(1, 2), (2, 3), (2, 4), (1, 3), (3, 5)]:
        _v1 = (a, b)
        _maint_S_bu_for_S_add(_v1)
        _maint_S_ub_for_S_add(_v1)
        _maint_R_Q3_for_S_add(_v1)
        _maint_R__QU_Q2_for_S_add(_v1)
        _maint_R_Q1_for_S_add(_v1)
    x = 1
    print(sorted((R_Q3_bu[x] if (x in R_Q3_bu) else Set())))

if (__name__ == '__main__'):
    main()
