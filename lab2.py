import sys
import re

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

class Clause:
    def __init__(self, literals: list[Literal]):
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

class Term:
    VAR, CONST, FUNC = 'var', 'const', 'func'

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
    

def pl_resolve(c1: Clause, c2: Clause) -> list[Clause]:
    resolvents = []
    for lit1 in c1.literals:
        resolve = []
        comp = lit1.complement()
        for lit2 in c2.literals:
            if comp == lit2:
                resolve = Clause([l for l in c1.literals if l != lit1] +
                            [l for l in c2.literals if l != lit2])
                resolvents.append(resolve)
                break
    return resolvents


def pl_resolution(clauses: list[Clause]):
    known = set(clauses)
    while True:
        new = []
        for ci in clauses:
            for cj in clauses:
                for res in pl_resolve(ci, cj):
                    if res.is_empty():
                        return False # unsatisfiable
                    if res not in known:
                        known.add(res)
                        new.append(res)
        if not new:
            return True # satisfiable
        clauses.extend(new)
                        
    
def parse_term(str, vars):
    func = re.match(r'^(\w+)\((.+)\)$', str)
    if func:
        name = func.group(1)
        arg_strs = func.group(2).split(',')
        args = [parse_term(a.strip(), vars) for a in arg_strs]
        return Term(Term.FUNC, name, args)
    
    if str in vars:
        return Term(Term.VAR, str)
    
    return Term(Term.CONST, str)


def parse_lit(str, vars):
    negated = str.startswith('!')
    if negated:
        str = str[1:]
    
    match = re.match(r'^(\w+)\((.*)\)$', str)
    if match:
        name = match.group(1)
        arg_strs = match.group(2).split(',')
        args = [parse_term(a.strip(), vars) for a in arg_strs]
    else:
        name = str
        args = []

    return Literal(name, args, negated)


def parse_cnf(filepath):
    with open(filepath) as f:
        text = f.read()
    var_reg = re.search(r'Variables:\s*(.*)', text)
    variables = set(var_reg.group(1).split()) if var_reg else set()
    clause_reg = re.search(r'Clauses:\s*(.*)', text, re.DOTALL)

    if not clause_reg:
        return []
    
    clauses = []
    for line in clause_reg.group(1).strip().splitlines():
        line = line.strip()
        if not line:
            continue
        lits = [parse_lit(lit, variables) for lit in line.split()]
        c = Clause(lits)
        clauses.append(c)
    
    return clauses


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit()
    
    clauses = parse_cnf(sys.argv[1])
    print("yes" if pl_resolution(clauses) else "no")
        