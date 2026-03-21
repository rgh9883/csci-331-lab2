import sys
 
class Clause:
    def __int__(self, literals):
        self.literals = literals
    
    def __repr__(self):
        return '{' + ', '.join(map(repr, self.literals)) + '}'
    
    def __eq__(self, other):
        if not isinstance(other, Clause): return False
        return frozenset(self.literals) == frozenset(other.literals)
    
    def __hash__(self):
        return hash(frozenset(self.literals))
    
    def is_empty(self):
        return len(self.literals) == 0

class Literal:
    def __init__(self, name, args, negated=False):
        self.name = name
        self.args = args
        self.negated = negated
    
    def __repr__(self):
        prefix = '!' if self.negated else ''
        return f"{prefix}{self.name}({', '.join(map(repr, self.args))})"
    
    def __eq__(self, other):
        return (isinstance(other, Literal) and
                self.name == other.name and
                self.args == other.args and
                self.negated == other.negated)
    
    def __hash__(self):
        return hash((self.name, self.negated, tuple(self.args)))
    
    def complement(self):
        return Literal(self.name, self.args, not self.negated)
    
class Term:
    VAR, CONST, FUNC = 'const', 'var', 'func'

    def __init__(self, type, name, args=None):
        self.type = type
        self.name = name
        self.args = args or []
    
    def is_var(self): return self.type == Term.VAR
    def is_const(self): return self.type == Term.CONST
    def is_func(self): return self.type == Term.FUNC

    def __repr__(self):
        if self.is_func():
            return f"{self.name}({','.join(map(repr, self.args))})"
        return self.name
    
    def __eq__(self, other):
        return (isinstance(other, Term) and
                self.type == other.type and
                self.name == other.name and
                self.args == other.args)
    
    def __hash__(self):
        return hash((self.type, self.name, tuple(self.args)))
    
    