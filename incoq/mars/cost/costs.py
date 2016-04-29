"""Definition of asymptotic cost terms and basic helpers."""


__all__ = [
    'Cost',
    'UnknownCost',
    'UnitCost',
    'NameCost',
    'IndefImagesetCost',
    'DefImagesetCost',
    'ProductCost',
    'SumCost',
    'MinCost',
    
    'eval_coststr',
    'CostVisitor',
    'CostTransformer',
    'PrettyPrinter',
]


from itertools import groupby
from simplestruct import Struct, TypedField

from incoq.mars.incast import L


class Cost(Struct):
    
    """Base of the cost term hierarchy."""


class UnknownCost(Cost):
    
    """Unknown cost."""
    
    def __str__(self):
        return '?'


class UnitCost(Cost):
    
    """Constant cost."""
    
    def __str__(self):
        return '1'


class NameCost(Cost):
    
    """Atomic cost, e.g. a domain size or a relation size."""
    
    name = TypedField(str)
    
    def __str__(self):
        return self.name


class IndefImagesetCost(Cost):
    
    """Indefinite image set, i.e., the size of the largest image set
    under any key for a given relation and mask.
    """
    
    rel = TypedField(str)
    mask = TypedField(L.mask)
    
    def __str__(self):
        return '{}_{}'.format(self.rel, self.mask)


class DefImagesetCost(Cost):
    
    """Definite image set, i.e., the size of a particular image set
    under a given sequence of key variables, for the given relation and
    mask.
    """
    
    rel = TypedField(str)
    mask = TypedField(L.mask)
    key = TypedField(str, seq=True)
    
    def __str__(self):
        return '{}_{}[{}]'.format(self.rel, self.mask,
                                  ', '.join(self.key))
    
    def to_indef(self):
        """Return the indefinite image set cost that generalizes this
        cost.
        """
        return IndefImagesetCost(self.rel, self.mask)


class ProductCost(Cost):
    
    """Product of a sequence of costs."""
    
    terms = TypedField(Cost, seq=True)
    
    def __str__(self):
        return '(' + ' * '.join(str(t) for t in self.terms) + ')'


class SumCost(Cost):
    
    """Sum of a sequence of costs."""
    
    terms = TypedField(Cost, seq=True)
    
    def __str__(self):
        return '(' + ' + '.join(str(t) for t in self.terms) + ')'


class MinCost(Cost):
    
    """Minimum of a sequence of costs."""
    
    terms = TypedField(Cost, seq=True)
    
    def __str__(self):
        return 'min(' + ', '.join(str(t) for t in self.terms) + ')'


def eval_coststr(s):
    """eval() a string representing a cost expression."""
    ns = {k: v for k, v in globals().items()
               if isinstance(v, type) and issubclass(v, Cost)}
    return eval(s, ns)


class BaseCostVisitor:
    
    """Visitor for costs, analogous to NodeVisitor."""
    
    # We don't use a generic_visit() method because there are only
    # a few types of Cost nodes, and that would require a common
    # list of subterms a la '_fields' for AST nodes. Instead we give
    # visit_ handlers for each kind of cost.
    #
    # To avoid an accidental inconsistency if a new cost type is added
    # but a new handler is not defined, we separate BaseCostVisitor
    # from CostVisitor so that CostTransformer is forced to explicitly
    # provide its own handlers.
    
    @classmethod
    def run(cls, tree, *args, **kargs):
        visitor = cls(*args, **kargs)
        result = visitor.process(tree)
        return result
    
    def process(self, tree):
        result = self.visit(tree)
        return result
    
    def visit(self, cost):
        assert isinstance(cost, Cost)
        method = 'visit_' + cost.__class__.__name__
        visitor = getattr(self, method)
        result = visitor(cost)
        return result


class CostVisitor(BaseCostVisitor):
    
    """Visitor for cost terms."""
    
    def do_nothing(self, cost):
        return
    
    visit_UnknownCost = do_nothing
    visit_UnitCost = do_nothing
    visit_NameCost = do_nothing
    visit_IndefImgsetCost = do_nothing
    visit_DefImgsetCost = do_nothing
    
    def do_termlist(self, cost):
        for c in cost.terms:
            self.visit(c)
    
    visit_ProductCost = do_termlist
    visit_SumCost = do_termlist
    visit_MinCost = do_termlist


class CostTransformer(BaseCostVisitor):
    
    """Transformer for costs. Like NodeTransformer, use None to indicate
    no change, and in a sequence return () to indicate removal of this
    term.
    """
    
    def visit(self, cost):
        result = super().visit(cost)
        if result is None:
            result = cost
        return result
    
    def do_nothing(self, cost):
        return cost
    
    visit_UnknownCost = do_nothing
    visit_UnitCost = do_nothing
    visit_NameCost = do_nothing
    visit_IndefImgsetCost = do_nothing
    visit_DefImgsetCost = do_nothing
    
    def do_termlist(self, cost):
        changed = False
        new_terms = []
        
        for c in cost.terms:
            result = self.visit(c)
            if result is not c:
                changed = True
            if isinstance(result, (tuple, list)):
                new_terms.extend(result)
            else:
                new_terms.append(result)
        
        if changed:
            return cost._replace(terms=new_terms)
        else:
            return cost
    
    visit_ProductCost = do_termlist
    visit_SumCost = do_termlist
    visit_MinCost = do_termlist


class PrettyPrinter(CostVisitor):
    
    """Print out costs in a way that displays multiple occurrences of
    the same factor as powers.
    """
    
    def helper(self, cost):
        return str(cost)
    
    visit_UnknownCost = helper
    visit_UnitCost = helper
    visit_NameCost = helper
    visit_IndefImgsetCost = helper
    visit_DefImgsetCost = helper
    
    def visit_ProductCost(self, cost):
        termstrs = []
        
        # Sort terms by string representation first, then group.
        # Each repetition of the same term is coalesced into a power.
        terms = list(cost.terms)
        terms.sort(key=lambda t: str(t).lower())
        for key, group in groupby(terms):
            n = len(list(group))
            s = self.visit(key)
            if n == 1:
                termstrs.append(s)
            else:
                termstrs.append(s + '^' + str(n))
        
        return '(' + ' * '.join(termstrs) + ')'
    
    def visit_SumCost(self, cost):
        return '(' + ' + '.join(self.visit(t) for t in cost.terms) + ')'
    
    def visit_MinCost(self, cost):
        return 'min(' + ', '.join(self.visit(t) for t in cost.terms) + ')'
