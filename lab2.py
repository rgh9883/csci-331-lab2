import sys

class Predicate:
    def __init__(self, name, neg, arg):
        self.name = name
        self.neg = neg
        self.arg = arg

class Function:
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

class Clause:
    def __init__(self, predicates):
        self.predicates = predicates


def parse_file(filename):
    clauses = []
    with open(filename, 'r') as f:
        pred_list = f.readline().split()[1:]
        var_list = f.readline().split()[1:]
        cons_list = f.readline().split()[1:]
        func_list = f.readline().split()[1:]
        f.readline()
        for line in f:
            clauses.append(line.split())
    return pred_list, var_list, cons_list, func_list, clauses

        



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: lab2.py cnf-file")
        sys.exit()
    filename = sys.argv[1]
    items = parse_file(filename)
    for item in items:
        print(item)
