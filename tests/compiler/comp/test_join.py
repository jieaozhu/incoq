"""Unit tests for join.py."""


import unittest

from incoq.compiler.incast import L
from incoq.compiler.symbol import N
from incoq.compiler.comp.clause import RelMemberHandler
from incoq.compiler.comp.join import *


class JoinCase(unittest.TestCase):
    
    def setUp(self):
        self.ct = CoreClauseTools()
    
    def test_match_eq_cond(self):
        cond = L.Cond(L.Parser.pe('x == y'))
        result = match_eq_cond(cond)
        exp_result = ('x', 'y')
        self.assertEqual(result, exp_result)
        
        cond = L.Cond(L.Parser.pe('x == y + 1'))
        result = match_eq_cond(cond)
        self.assertIsNone(result)
    
    def test_make_eq_cond(self):
        cond = make_eq_cond('x', 'y')
        exp_cond = L.Cond(L.Parser.pe('x == y'))
        self.assertEqual(cond, exp_cond)
    
    def test_lhs_vars(self):
        comp = L.Parser.pe('''{(x, y, z) for (x, y) in REL(R)
                                         for (y, z) in REL(S)}''')
        lhs_vars = self.ct.lhs_vars_from_clauses(comp.clauses)
        self.assertSequenceEqual(lhs_vars, ['x', 'y', 'z'])
        
        lhs_vars = self.ct.lhs_vars_from_comp(comp)
        self.assertSequenceEqual(lhs_vars, ['x', 'y', 'z'])
    
    def test_con_lhs_vars_from_comp(self):
        class DummyHandler(RelMemberHandler):
            def constrained_mask(self, cl):
                return [False, True]
        self.ct.handle_RelMember = DummyHandler(self.ct)
        
        comp = L.Parser.pe('''{c for (x, y) in REL(R)
                                 for (y, z) in REL(R)
                                 for (a, z) in REL(R)
                                 if y > b}''')
        uncon = self.ct.con_lhs_vars_from_comp(comp)
        self.assertSequenceEqual(uncon, ['y', 'z'])
        
        # Cyclic case.
        comp = L.Parser.pe('''{None for (x, y) in REL(R)
                                    for (y, x) in REL(R)}''')
        uncon = self.ct.con_lhs_vars_from_comp(comp)
        self.assertSequenceEqual(uncon, ['y'])
    
    def test_rhs_rels_from_comp(self):
        comp = L.Parser.pe('''{(x, y, z) for (x, y) in REL(R)
                                         for (y, z) in REL(S)
                                         for (z, z) in SING(e)}''')
        rels = self.ct.rhs_rels_from_comp(comp)
        self.assertSequenceEqual(rels, ['R', 'S'])
    
    def test_make_join(self):
        comp = L.Parser.pe('''{(x, y, z) for (x, y) in REL(R)
                                         for (y, z) in REL(S)}''')
        comp2 = self.ct.make_join_from_clauses(comp.clauses)
        self.assertEqual(comp2, comp)
        
        comp3 = L.Parser.pe('''{None for (x, y) in REL(R)
                                     for (y, z) in REL(S)}''')
        comp4 = self.ct.make_join_from_comp(comp3)
        self.assertEqual(comp4, comp)
    
    def test_is_join(self):
        comp = L.Parser.pe('''{(x, y, z) for (x, y) in REL(R)
                                         for (y, z) in REL(S)}''')
        self.assertTrue(self.ct.is_join(comp))
        
        # Different order.
        comp = L.Parser.pe('''{(x, z, y) for (x, y) in REL(R)
                                         for (y, z) in REL(S)}''')
        self.assertTrue(self.ct.is_join(comp))
        
        # Different variables.
        comp = L.Parser.pe('''{(x, z, y) for (a, y) in REL(R)
                                         for (y, z) in REL(S)}''')
        self.assertFalse(self.ct.is_join(comp))
        
        # Not a tuple.
        comp = L.Parser.pe('''{x for (x, y) in REL(R)
                                 for (y, z) in REL(S)}''')
        self.assertFalse(self.ct.is_join(comp))
    
    def test_all_vars_determined(self):
        comp = L.Parser.pe('''{(x, y, z) for (x, y) in REL(R)
                                         for (y, z) in REL(S)}''')
        b = self.ct.all_vars_determined(comp.clauses, ['x'])
        self.assertFalse(b)
        b = self.ct.all_vars_determined(comp.clauses, ['x', 'y', 'z'])
        self.assertTrue(b)
    
    def test_rename_lhs_vars(self):
        comp = L.Parser.pe('''{(a, x, y, z) for (x, y) in REL(R)
                                            for (y, z) in REL(S)
                                            if a}''')
        exp_comp = L.Parser.pe('''{(a, _x, _y, _z) for (_x, _y) in REL(R)
                                                   for (_y, _z) in REL(S)
                                                   if a}''')
        exp_clauses = exp_comp.clauses
        
        renamer = lambda x: '_' + x
        clauses = self.ct.clauses_rename_lhs_vars(comp.clauses, renamer)
        comp = self.ct.comp_rename_lhs_vars(comp, renamer)
        
        self.assertSequenceEqual(clauses, exp_clauses)
        self.assertEqual(comp, exp_comp)
    
    def test_rewrite_with_patterns(self):
        orig_comp = L.Parser.pe('''{a for (a, b) in REL(R)
                                      for (b, c) in REL(R) if a == b}''')
        
        # No keepvars.
        comp = self.ct.rewrite_with_patterns(orig_comp, set())
        exp_comp = L.Parser.pe('''{a for (a, a) in REL(R)
                                     for (a, c) in REL(R)}''')
        self.assertEqual(comp, exp_comp)
        
        # Right side in keepvars.
        comp = self.ct.rewrite_with_patterns(orig_comp, {'b'})
        exp_comp = L.Parser.pe('''{b for (b, b) in REL(R)
                                     for (b, c) in REL(R)}''')
        self.assertEqual(comp, exp_comp)
        
        # Both sides in keepvars.
        comp = self.ct.rewrite_with_patterns(orig_comp, {'a', 'b'})
        self.assertEqual(comp, orig_comp)
    
    def test_elim_sameclause_eqs(self):
        comp = L.Parser.pe('{x for (x, x) in REL(R) for (x, y, x) in REL(R)}')
        comp = self.ct.elim_sameclause_eqs(comp)
        exp_comp = L.Parser.pe('''{x for (x, x_2) in REL(R) if x == x_2
                                     for (x, y, x_3) in REL(R) if x == x_3}''')
        self.assertEqual(comp, exp_comp)
        
        comp = L.Parser.pe('{x for (x,) in REL(R) if x < x}')
        exp_comp = comp
        comp = self.ct.elim_sameclause_eqs(comp)
        self.assertEqual(comp, exp_comp)
    
    def test_rewrite_resexp_with_params(self):
        comp = L.Parser.pe('''{(2 * y,) for (x, y) in REL(R)}''')
        comp = self.ct.rewrite_resexp_with_params(comp, ('x',))
        exp_comp = L.Parser.pe('''{(x, 2 * y) for (x, y) in REL(R)}''')
        self.assertEqual(comp, exp_comp)
        
        comp = L.Parser.pe('''{y for (x, y) in REL(R)}''')
        with self.assertRaises(AssertionError):
            self.ct.rewrite_resexp_with_params(comp, ('x',))
    
    def test_filter_clauses(self):
        class DummyHandler(RelMemberHandler):
            def constrained_mask(self, cl):
                return [False, True]
        self.ct.handle_RelMember = DummyHandler(self.ct)
        
        clauses = L.Parser.pe('''{z for (x, y) in REL(R)
                                    if x < y
                                    for (y, z) in REL(S)}''').clauses
        filters = L.Parser.pe('''{z for (x, y) in REL(dR)
                                    if x < y
                                    for (y, z) in REL(dS)}''').clauses
        clauses = self.ct.filter_clauses(clauses, filters, [])
        exp_clauses = L.Parser.pe('''{z for (x, y) in REL(dR)
                                        if x < y
                                        for (y, z) in REL(S)}''').clauses
        self.assertSequenceEqual(clauses, exp_clauses)
    
    def test_get_code_for_clauses(self):
        comp = L.Parser.pe('''{z for (x, y) in REL(R)
                                 for (y, z) in REL(S)}''')
        code = self.ct.get_code_for_clauses(comp.clauses, ['x'], (L.Pass(),))
        exp_code = L.Parser.pc('''
            for y in unwrap(R.imglookup('bu', (x,))):
                for z in unwrap(S.imglookup('bu', (y,))):
                    pass
            ''')
        self.assertEqual(code, exp_code)
    
    def test_get_loop_for_join(self):
        comp = L.Parser.pe('''{(x, y, z) for (x, y) in REL(R)
                                         for (y, z) in REL(S)}''')
        code = self.ct.get_loop_for_join(comp, (L.Pass(),), 'J')
        exp_code = L.Parser.pc('''
            for (x, y, z) in QUERY('J', {(x, y, z) for (x, y) in REL(R)
                                                   for (y, z) in REL(S)}):
                pass
            ''')
        self.assertEqual(code, exp_code)
    
    def test_get_maint_join(self):
        comp = L.Parser.pe('''
            {(w, x, y, z) for (w, x) in REL(R) for (x, y) in REL(S)
                          for (y, z) in REL(R)}''')
        join = self.ct.get_maint_join(comp, 0, L.Name('e'),
                                      selfjoin=SelfJoin.Without)
        exp_join = L.Parser.pe('''
            {(w, x, y, z) for (w, x) in SING(e) for (x, y) in REL(S)
                          for (y, z) in WITHOUT(REL(R), e)}''')
        self.assertEqual(join, exp_join)
    
    def test_get_maint_join_union(self):
        comp = L.Parser.pe('''
            {(w, x, y, z) for (w, x) in REL(R) for (x, y) in REL(S)
                          for (y, z) in REL(R)}''')
        joins = self.ct.get_maint_join_union(comp, 'R', L.Name('e'),
                                             selfjoin=SelfJoin.Without)
        exp_joins = [
            L.Parser.pe('''
                {(w, x, y, z) for (w, x) in SING(e) for (x, y) in REL(S)
                              for (y, z) in WITHOUT(REL(R), e)}'''),
            L.Parser.pe('''
                {(w, x, y, z) for (w, x) in REL(R) for (x, y) in REL(S)
                              for (y, z) in SING(e)}'''),
        ]
        self.assertSequenceEqual(joins, exp_joins)
    
    def test_get_maint_code(self):
        comp = L.Parser.pe('''
            {w + z for (w, x) in REL(R) for (x, y) in REL(S)
                   for (y, z) in REL(R)}''')
        code = self.ct.get_maint_code('_v1',
                                      N.fresh_name_generator('J{}'),
                                      comp, 'Q',
                                      L.RelUpdate('R', L.SetAdd(), 'e'),
                                      counted=True)
        exp_code = L.Parser.pc('''
            for (_v1_w, _v1_x, _v1_y, _v1_z) in \
                    QUERY('J1', {(_v1_w, _v1_x, _v1_y, _v1_z)
                                 for (_v1_w, _v1_x) in SING(e)
                                 for (_v1_x, _v1_y) in REL(S)
                                 for (_v1_y, _v1_z) in WITHOUT(REL(R), e)}):
                _v1_result = (_v1_w + _v1_z)
                if (_v1_result not in Q):
                    Q.reladd(_v1_result)
                else:
                    Q.relinccount(_v1_result)
            for (_v1_w, _v1_x, _v1_y, _v1_z) in \
                    QUERY('J2', {(_v1_w, _v1_x, _v1_y, _v1_z)
                                 for (_v1_w, _v1_x) in REL(R)
                                 for (_v1_x, _v1_y) in REL(S)
                                 for (_v1_y, _v1_z) in SING(e)}):
                _v1_result = (_v1_w + _v1_z)
                if (_v1_result not in Q):
                    Q.reladd(_v1_result)
                else:
                    Q.relinccount(_v1_result)
            ''')
        self.assertEqual(code, exp_code)


if __name__ == '__main__':
    unittest.main()
