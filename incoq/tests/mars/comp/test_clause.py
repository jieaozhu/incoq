"""Unit tests for test_clause.py."""


import unittest

from incoq.mars.incast import L
from incoq.mars.comp.clause import *


class ClauseCase(unittest.TestCase):
    
    def setUp(self):
        self.visitor = CoreClauseVisitor()
    
    def test_handler(self):
        self.assertIsInstance(self.visitor.handle_RelMember,
                              RelMemberHandler)
    
    def test_subtract(self):
        v = self.visitor
        
        cl = L.RelMember(['x', 'y', 'z'], 'R')
        cl2 = v.subtract(cl, L.Name('e'))
        exp_cl2 = L.WithoutMember(cl, L.Name('e'))
        self.assertEqual(cl2, exp_cl2)
        
        cl = L.Cond(L.Parser.pe('True'))
        with self.assertRaises(NotImplementedError):
            v.subtract(cl, L.Name('e'))
    
    def test_relmember(self):
        v = self.visitor
        
        cl = L.RelMember(['x', 'y', 'z'], 'R')
        
        self.assertIs(v.kind(cl), Kind.Member)
        self.assertSequenceEqual(v.lhs_vars(cl), ['x', 'y', 'z'])
        self.assertEqual(v.rhs_rel(cl), 'R')
        
        code = v.get_code(cl, ['a', 'x'], (L.Pass(),))
        exp_code = L.Parser.pc('''
            for (y, z) in R.imglookup('buu', (x,)):
                pass
            ''')
        self.assertEqual(code, exp_code)
        
        cl2 = v.singletonize(cl, L.Name('e'))
        exp_cl2 = L.SingMember(['x', 'y', 'z'], L.Name('e'))
        self.assertEqual(cl2, exp_cl2)
    
    def test_singmember(self):
        v = self.visitor
        
        cl = L.SingMember(['x', 'y', 'z'], L.Name('e'))
        
        self.assertIs(v.kind(cl), Kind.Member)
        self.assertSequenceEqual(v.lhs_vars(cl), ['x', 'y', 'z'])
        self.assertEqual(v.rhs_rel(cl), None)
        
        code = v.get_code(cl, ['a', 'x'], (L.Pass(),))
        exp_code = L.Parser.pc('''
            (_, y, z) = e
            pass
            ''')
        self.assertEqual(code, exp_code)
        
        with self.assertRaises(NotImplementedError):
            v.singletonize(cl, L.Name('f'))
    
    def test_withoutmember(self):
        v = self.visitor
        
        cl = L.WithoutMember(L.RelMember(['x', 'y', 'z'], 'R'),
                             L.Name('e'))
        
        self.assertIs(v.kind(cl), Kind.Member)
        self.assertSequenceEqual(v.lhs_vars(cl), ['x', 'y', 'z'])
        self.assertEqual(v.rhs_rel(cl), 'R')
        
        code = v.get_code(cl, ['a', 'x'], (L.Pass(),))
        exp_code = L.Parser.pc('''
            for (y, z) in R.imglookup('buu', (x,)):
                if ((x, y, z) != e):
                    pass
            ''')
        self.assertEqual(code, exp_code)
        
        cl2 = v.singletonize(cl, L.Name('f'))
        exp_cl2 = L.WithoutMember(L.SingMember(['x', 'y', 'z'], L.Name('f')),
                                  L.Name('e'))
        self.assertEqual(cl2, exp_cl2)
    
    def test_cond(self):
        v = self.visitor
        
        cl = L.Cond(L.Parser.pe('x == y'))
        
        self.assertIs(v.kind(cl), Kind.Cond)
        self.assertSequenceEqual(v.lhs_vars(cl), [])
        self.assertEqual(v.rhs_rel(cl), None)
        
        code = v.get_code(cl, ['a', 'x', 'y'], (L.Pass(),))
        exp_code = L.Parser.pc('''
            if (x == y):
                pass
            ''')
        self.assertEqual(code, exp_code)
        
        with self.assertRaises(NotImplementedError):
            v.singletonize(cl, L.Name('e'))


if __name__ == '__main__':
    unittest.main()
