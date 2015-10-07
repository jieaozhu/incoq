"""Symbol tables."""


__all__ = [
    'N',
    
    'Symbol',
    'RelationSymbol',
    'MapSymbol',
    'VarSymbol',
    
    'SymbolTable',
]


from collections import OrderedDict
from itertools import count

from incoq.mars.incast import L
import incoq.mars.types as T
from incoq.mars.config import Attribute


class N:
    
    """Namespace for naming scheme helpers."""
    
    @classmethod
    def get_subnames(cls, prefix, num):
        """Return a list of num many fresh variable names that share
        a common prefix.
        """
        return [prefix + '_v' + str(i) for i in range(1, num + 1)]
    
    @classmethod
    def get_auxmap_name(cls, map, mask):
        return '{}_{}'.format(map, mask.m)
    
    @classmethod
    def get_maint_func_name(cls, inv, param, op):
        return '_maint_{}_for_{}_{}'.format(inv, param, op)


class Symbol:
    
    name = Attribute('name', None,
            'Name of the symbol')
    
    def __init__(self, name, **kargs):
        self.update(name=name, **kargs)
    
    def update(self, **kargs):
        for name, value in kargs.items():
            if not isinstance(getattr(self.__class__, name, None), Attribute):
                raise KeyError('Unknown symbol attribute "{}"'.format(name))
            setattr(self, name, value)


class TypedSymbolMixin(Symbol):
    
    # Min/max type can be supplied as INFO inputs, but type
    # should not be.
    
    type = Attribute('type', T.Bottom,
            'Current annotated or inferred type of the symbol')
    
    min_type = Attribute('min_type', T.Bottom,
            'Initial minimum type before type inference; the type '
            'of input values for variables')
    
    max_type = Attribute('max_type', T.Top,
            'Maximum type after type inference; the type of output '
            'values for variables')
    
    def type_helper(self, t):
        return T.eval_typestr(t)
    
    parse_type = type_helper
    parse_min_type = type_helper
    parse_max_type = type_helper
    
    def decl_comment(self):
        return self.name + ' : ' + str(self.type)

TSM = TypedSymbolMixin


class RelationSymbol(TypedSymbolMixin, Symbol):
    
    type = TSM.type._replace(default=T.Set(T.Bottom))
    min_type = TSM.min_type._replace(default=T.Set(T.Bottom))
    max_type = TSM.max_type._replace(default=T.Set(T.Top))
    
    def __str__(self):
        s = 'Relation {}'.format(self.name)
        opts = []
        if self.type is not None:
            opts.append('type: {}'.format(self.type))
        if len(opts) > 0:
            s += ' (' + ', '.join(opts) + ')'
        return s


class MapSymbol(TypedSymbolMixin, Symbol):
    
    min_type = TSM.min_type._replace(default=T.Map(T.Bottom, T.Bottom))
    max_type = TSM.max_type._replace(default=T.Map(T.Top, T.Top))
    
    def __str__(self):
        return 'Map {}'.format(self.name)


class VarSymbol(TypedSymbolMixin, Symbol):
    
    def __str__(self):
        s = 'Var {}'.format(self.name)
        if self.type is not None:
            s += ' (type: {})'.format(self.type)
        return s


symbol_kindmap = {
    'Set': RelationSymbol,
    'Map': MapSymbol,
    'Var': VarSymbol,
}


class SymbolTable:
    
    def __init__(self):
        self.symbols = OrderedDict()
        """Global symbols, in declaration order."""
        self.fresh_vars = ('_v{}'.format(i) for i in count(1))
        """Fresh variable name generator."""
    
    def define_symbol(self, name, kind, **kargs):
        """Define a new symbol of the given kind."""
        symcls = symbol_kindmap[kind]
        if name in self.symbols:
            raise L.ProgramError('Symbol "{}" already defined'.format(name))
        sym = symcls(name, **kargs)
        self.symbols[name] = sym
    
    def define_relation(self, name, **kargs):
        self.define_symbol(name, 'Set', **kargs)
    
    def define_map(self, name, **kargs):
        self.define_symbol(name, 'Map', **kargs)
    
    def define_var(self, name, **kargs):
        self.define_symbol(name, 'Var', **kargs)
    
    def get_symbols(self, kind=None):
        """Return an OrderedDict of symbols of the requested kind.
        If kind is None, all symbols are returned.
        """
        result = OrderedDict(self.symbols)
        if kind is not None:
            symcls = symbol_kindmap[kind]
            for name, sym in self.symbols.items():
                if not isinstance(sym, symcls):
                    result.pop(name)
        return result
    
    def get_relations(self):
        return self.get_symbols('Set')
    
    def get_maps(self):
        return self.get_symbols('Map')
    
    def get_vars(self):
        return self.get_symbols('Var')
    
    def apply_symconfig(self, name, info):
        """Given a symbol name and a key-value dictionary of symbol
        config attribute, apply the attributes.
        """
        if name not in self.symbols:
            raise L.ProgramError('No symbol "{}"'.format(name))
        sym = self.symbols[name]
        # Hook into a parse_*()  method, if one exists for that
        # attr key on the symbol.
        for k, v in info.items():
            parse_method = getattr(sym, 'parse_' + k, None)
            if parse_method is not None:
                v = parse_method(v)
            setattr(sym, k, v)
    
    def dump_symbols(self):
        """Return a string describing the defined global symbols."""
        entries = []
        for sym in self.symbols.values():
            entries.append(str(sym))
        return '\n'.join(entries)
