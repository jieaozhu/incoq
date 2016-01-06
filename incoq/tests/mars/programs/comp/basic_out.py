from incoq.mars.runtime import *
# S : {(Number, Number)}
S = Set()
# R_Q : {Number}
R_Q = Set()
def _maint_R_Q_for_S_add(_elem):
    (_v2_a, _v2_b) = _elem
    for (_v2_b2, _v2_c) in S:
        if ((_v2_b2, _v2_c) != _elem):
            if (_v2_b == _v2_b2):
                _v2_result = (_v2_c,)
                if (_v2_result not in R_Q):
                    R_Q.add(_v2_result)
                else:
                    R_Q.inccount(_v2_result)
    for (_v2_a, _v2_b) in S:
        (_v2_b2, _v2_c) = _elem
        if (_v2_b == _v2_b2):
            _v2_result = (_v2_c,)
            if (_v2_result not in R_Q):
                R_Q.add(_v2_result)
            else:
                R_Q.inccount(_v2_result)

def _maint_R_Q_for_S_remove(_elem):
    (_v3_a, _v3_b) = _elem
    for (_v3_b2, _v3_c) in S:
        if ((_v3_b2, _v3_c) != _elem):
            if (_v3_b == _v3_b2):
                _v3_result = (_v3_c,)
                if (R_Q.getcount(_v3_result) == 1):
                    R_Q.remove(_v3_result)
                else:
                    R_Q.deccount(_v3_result)
    for (_v3_a, _v3_b) in S:
        (_v3_b2, _v3_c) = _elem
        if (_v3_b == _v3_b2):
            _v3_result = (_v3_c,)
            if (R_Q.getcount(_v3_result) == 1):
                R_Q.remove(_v3_result)
            else:
                R_Q.deccount(_v3_result)

def main():
    for (x, y) in [(1, 2), (1, 3), (2, 3), (2, 4)]:
        _v1 = (x, y)
        S.add(_v1)
        _maint_R_Q_for_S_add(_v1)
    print(R_Q.unwrap())

if (__name__ == '__main__'):
    main()
