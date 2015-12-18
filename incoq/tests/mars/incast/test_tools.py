"""Unit tests for tools.py."""

# Note that since the IncAST parser depends on the MacroExpander,
# if the MacroExpander breaks a bunch of unrelated tests will also
# break.


import unittest
import string
from random import shuffle

from incoq.mars.incast import nodes as L
from incoq.mars.incast.tools import *
from incoq.mars.incast import pynodes as P
from incoq.mars.incast.pyconv import Parser, IncLangNodeImporter


class IdentFinderCase(unittest.TestCase):
    
    def test_identfinder(self):
        # Exclude function name main, updated relation R,
        # and query Q.
        tree = Parser.p('''
            def main():
                a = b
                c, d = e
                for f in g:
                    {h for i in j}
                R.reladd(a)
                QUERY('Q', a)
            ''')
        contexts = ['RelUpdate.rel', 'fun.name', 'Query.name']
        vars = sorted(IdentFinder.run(tree, contexts=contexts, invert=True))
        exp_vars = list(string.ascii_lowercase)[:10]
        self.assertEqual(vars, exp_vars)


class TemplaterCase(unittest.TestCase):
    
    def test_name(self):
        # This test eschews the parser in case the parser breaks.
        # a = a + b
        tree = L.Assign('a', L.BinOp(L.Name('a'), L.Add(), L.Name('b')))
        tree = Templater.run(tree, subst={'a': L.Name('c')})
        # a = c + b
        exp_tree = L.Assign('a', L.BinOp(L.Name('c'), L.Add(), L.Name('b')))
        self.assertEqual(tree, exp_tree)
    
    def test_ident(self):
        tree = Parser.pc('''
            def a(a):
                for a in a:
                    a = a
                    a, b = a
                    a.add(a)
                    a.reladd(a)
                    a[a] = a
                    del a[a]
                    a.mapassign(a, a)
                    a.mapdelete(a)
                    a(a.a)
                    a.get(a, a)
                    a.imglookup('bu', (a,))
                    {a for a in a if a}
            ''')
        tree = Templater.run(tree, subst={'a': 'c'})
        exp_tree = Parser.pc('''
            def c(c):
                for c in c:
                    c = c
                    c, b = c
                    c.add(c)
                    c.reladd(c)
                    c[c] = c
                    del c[c]
                    c.mapassign(c, c)
                    c.mapdelete(c)
                    c(c.c)
                    c.get(c, c)
                    c.imglookup('bu', (c,))
                    {c for c in c if c}
            ''')
        self.assertEqual(tree, exp_tree)
    
    def test_code(self):
        tree = Parser.pc('a; C')
        tree = Templater.run(tree, subst={'<c>C':
                                          L.Expr(L.Name('b'))})
        exp_tree = Parser.pc('a; b')
        self.assertEqual(tree, exp_tree)
        
        tree = Parser.pc('a; C')
        tree = Templater.run(tree, subst={'<c>C':
                                          (L.Expr(L.Name('b')),
                                           L.Expr(L.Name('c')))})
        exp_tree = Parser.pc('a; b; c')
        self.assertEqual(tree, exp_tree)


class MacroExpanderCase(unittest.TestCase):
    
    def test_expansion(self):
        # This test uses IncLangNodeImporter while bypassing
        # the overall IncAST parser.
        class A(MacroExpander):
            def handle_ms_plus(self_, func, a, b):
                self.assertEqual(func, 'plus')
                assert isinstance(a, L.Num)
                assert isinstance(b, L.Num)
                return L.Num(a.n + b.n)
        
        tree = P.Parser.ps('(2).plus(3)')
        tree = IncLangNodeImporter.run(tree)
        tree = A.run(tree)
        exp_tree = L.Num(5)
        self.assertEqual(tree, exp_tree)


class TreeCase(unittest.TestCase):
    
    def test_tree_size(self):
        tree = Parser.pe('1 + 2')
        self.assertEqual(tree_size(tree), 4)
        
        tree = Parser.ps('A')
        self.assertEqual(tree_size(tree), 2)
    
    def test_tree_topsort(self):
        # Create some trees.
        pe = Parser.pe
        t1223 = pe('(1 + 2) + (2 + 3)')
        t12 = pe('1 + 2')
        t23 = pe('2 + 3')
        t1 = pe('1')
        t2 = pe('2')
        trees = [t1223, t12, t23, t1, t2]
        # Partial order of containment.
        exp_order = [
            (t1, t12),
            (t1, t1223),
            (t2, t12),
            (t2, t23),
            (t2, t1223),
            (t12, t1223),
            (t23, t1223),
        ]
        
        # Shuffle randomly, topsort, and confirm the partial order.
        # Repeat 10 times.
        for _ in range(10):
            shuffle(trees)
            result = sorted(trees, key=tree_size)
            for tleft, tright in exp_order:
                self.assertTrue(result.index(tleft) < result.index(tright))


if __name__ == '__main__':
    unittest.main()
