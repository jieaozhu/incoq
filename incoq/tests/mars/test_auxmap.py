"""Unit tests for auxmap.py."""


import unittest

from incoq.mars.incast import L
from incoq.mars.auxmap import *
from incoq.mars.auxmap import (insert_rel_maint,
                               make_imgadd, make_imgremove,
                               make_auxmap_maint_func,
                               AuxmapFinder, AuxmapTransformer)


class AuxmapCase(unittest.TestCase):
    
    def test_insert_rel_maint(self):
        update_code = L.Parser.pc('R.reladd(x)')
        maint_code = L.Parser.pc('pass')
        code = insert_rel_maint(update_code, maint_code, L.SetAdd())
        exp_code = L.Parser.pc('''
            R.reladd(x)
            pass
            ''')
        self.assertEqual(code, exp_code)
        
        update_code = L.Parser.pc('R.relremove(x)')
        maint_code = L.Parser.pc('pass')
        code = insert_rel_maint(update_code, maint_code, L.SetRemove())
        exp_code = L.Parser.pc('''
            pass
            R.relremove(x)
            ''')
        self.assertEqual(code, exp_code)
    
    def test_make_imgadd(self):
        key = L.Parser.pe('k')
        value = L.Parser.pe('v')
        code = make_imgadd('m', key, value)
        exp_code = L.Parser.pc('''
            if k not in m:
                m[k] = set()
            m[k].add(v)
            ''')
        self.assertEqual(code, exp_code)
    
    def test_make_imgremove(self):
        key = L.Parser.pe('k')
        value = L.Parser.pe('v')
        code = make_imgremove('m', key, value)
        exp_code = L.Parser.pc('''
            m[k].remove(v)
            if len(m[k]) == 0:
                del m[k]
            ''')
        self.assertEqual(code, exp_code)
    
    def test_maint_add(self):
        auxmap = AuxmapInvariant('m', 'R', L.mask('bu'))
        func = make_auxmap_maint_func(auxmap, L.SetAdd())
        exp_func = L.Parser.ps('''
            def _maint_m_for_R_add(_elem):
                (_elem_v1, _elem_v2) = _elem
                if ((_elem_v1,) not in m):
                    m[(_elem_v1,)] = set()
                m[(_elem_v1,)].add((_elem_v2,))
            ''')
        self.assertEqual(func, exp_func)
    
    def test_maint_remove(self):
        auxmap = AuxmapInvariant('m', 'R', L.mask('bu'))
        func = make_auxmap_maint_func(auxmap, L.SetRemove())
        exp_func = L.Parser.ps('''
            def _maint_m_for_R_remove(_elem):
                (_elem_v1, _elem_v2) = _elem
                m[(_elem_v1,)].remove((_elem_v2,))
                if (len(m[(_elem_v1,)]) == 0):
                    del m[(_elem_v1,)]
            ''')
        self.assertEqual(func, exp_func)
    
    def test_imgset_finder(self):
        tree = L.Parser.p('''
            def f():
                R.imgset('bu', (x,))
                R.imgset('bu', (x,))
                R.imgset('ub', (y,))
                S.imgset('bu', (x,))
            ''')
        auxmaps = AuxmapFinder.run(tree)
        exp_auxmaps = [
            AuxmapInvariant('R_bu', 'R', L.mask('bu')),
            AuxmapInvariant('R_ub', 'R', L.mask('ub')),
            AuxmapInvariant('S_bu', 'S', L.mask('bu')),
        ]
        self.assertEqual(auxmaps, exp_auxmaps)
    
    def test_auxmap_transformer(self):
        auxmaps = [
            AuxmapInvariant('R_bu', 'R', L.mask('bu')),
        ]
        tree = L.Parser.p('''
            def f():
                R.reladd((1, 2))
                print(R.imgset('bu', (x,)))
                S.reladd((3, 4))
                print(S.imgset('bu', (x,)))
            ''')
        tree = AuxmapTransformer.run(tree, auxmaps)
        exp_tree = L.Parser.p('''
            def _maint_R_bu_for_R_add(_elem):
                (_elem_v1, _elem_v2) = _elem
                if ((_elem_v1,) not in R_bu):
                    R_bu[(_elem_v1,)] = set()
                R_bu[(_elem_v1,)].add((_elem_v2,))
            
            def _maint_R_bu_for_R_remove(_elem):
                (_elem_v1, _elem_v2) = _elem
                R_bu[(_elem_v1,)].remove((_elem_v2,))
                if (len(R_bu[(_elem_v1,)]) == 0):
                    del R_bu[(_elem_v1,)]
            
            def f():
                R.reladd((1, 2))
                _maint_R_bu_for_R_add((1, 2))
                print(R_bu.get((x,), set()))
                S.reladd((3, 4))
                print(S.imgset('bu', (x,)))
            ''')
        self.assertEqual(tree, exp_tree)


if __name__ == '__main__':
    unittest.main()