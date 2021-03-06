"""Unit tests for trans.py."""


import unittest

from incoq.compiler.incast import L
from incoq.compiler.symbol import S
from incoq.compiler.comp import CoreClauseTools
from incoq.compiler.obj import ObjClauseVisitor
from incoq.compiler.demand.trans import *


class ClauseTools(CoreClauseTools, ObjClauseVisitor):
    pass


class TransCase(unittest.TestCase):
    
    def test_transform_comp_query_with_filtering(self):
        symtab = S.SymbolTable()
        symtab.clausetools = ClauseTools()
        symtab.config = S.Config()
        comp = L.Parser.pe('''
            {(z,) for (w, x) in REL(U) for (x, y) in M() for (y, z) in M()}
            ''')
        query = symtab.define_query('Q', node=comp)
        tree = L.Parser.p('''
            def main():
                print(QUERY('Q', {(z,) for (w, x) in REL(U) for (x, y) in M()
                                       for (y, z) in M()}))
            ''')
        tree = transform_comp_query_with_filtering(tree, symtab, query)
        
        func = {d.name: d for d in tree.body}['_maint_R_Q_for__M_add']
        exp_func = L.Parser.ps('''
            def _maint_R_Q_for__M_add(_elem):
                (_v3_x, _v3_y) = _elem
                if ((_v3_x, _v3_y) in R_Q_d_M_1):
                    for _v3_w in unwrap(U.imglookup('ub', (_v3_x,))):
                        if isset(_v3_y):
                            for _v3_z in _v3_y:
                                if ((_v3_y, _v3_z) != _elem):
                                    _v3_result = (_v3_z,)
                                    if (_v3_result not in R_Q):
                                        R_Q.reladd(_v3_result)
                                    else:
                                        R_Q.relinccount(_v3_result)
                (_v3_y, _v3_z) = _elem
                if ((_v3_y, _v3_z) in R_Q_d_M_2):
                    for _v3_x in unwrap(R_Q_d_M_1.imglookup('ub', (_v3_y,))):
                        for _v3_w in unwrap(U.imglookup('ub', (_v3_x,))):
                            _v3_result = (_v3_z,)
                            if (_v3_result not in R_Q):
                                R_Q.reladd(_v3_result)
                            else:
                                R_Q.relinccount(_v3_result)
            ''')
        self.assertEqual(func, exp_func)
        
        func = {d.name: d for d in tree.body} \
                ['_maint_R_Q_d_M_2_for_R_Q_T_y_add']
        exp_func = L.Parser.ps('''
            def _maint_R_Q_d_M_2_for_R_Q_T_y_add(_elem):
                (_v13_y,) = _elem
                if isset(_v13_y):
                    for _v13_z in _v13_y:
                        _v13_result = (_v13_y, _v13_z)
                        R_Q_d_M_2.reladd(_v13_result)
            ''')
        self.assertEqual(func, exp_func)


if __name__ == '__main__':
    unittest.main()
