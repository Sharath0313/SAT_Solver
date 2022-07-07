from pysat.formula import CNF
import copy
from collections import defaultdict

f1 = CNF(from_file='test5.cnf')

l = list(range(1,f1.nv+1))

def remove_clause(f1,k):
    x=0
    while(x<len(f1)):
        if(k in f1[x]):
            f1.remove(f1[x])
            continue
        x=x+1
    return f1

def remove_literal(f1,k):
    for x in range(len(f1)):
        while(k in f1[x]):
            f1[x].remove(k)
    return f1

def unit_propagate(f1,k):
    remove_clause(f1,k)
    remove_literal(f1,-k)
    return f1

def min_clauses(clauses):
	MinClauses = []
	size = -1

	for clause in clauses:

		clause_size = len(clause)

		if size == -1 or clause_size < size:
			MinClauses = [clause]
			size = clause_size

		elif clause_size == size:
			MinClauses.append(clause)

	return MinClauses

def literal_count(clauses):

	score = defaultdict(int)

	for clause in clauses:
		for l in clause:
			score[l] += 1

	return max(score, key=score.get)

def moms(cnf):

	minc = min_clauses(cnf)

	return literal_count(minc)

def DPLL(f1,l):
    x=0
    while(x<len(f1)):
        if(len(f1[x])==1):
            l[abs(f1[x][0])-1] = f1[x][0]
            unit_propagate(f1,f1[x][0])
            continue
        x=x+1
    if(len(f1)==0):
        print(l)
        quit()
    for x in range(len(f1)):
        if(len(f1[x])==0):
            return False

    k = moms(f1)

    l[abs(k)-1] = k
    f2 = unit_propagate(copy.deepcopy(f1),k)
    bool1 = DPLL(f2,copy.deepcopy(l))
    l[abs(k)-1] = -k
    f3 = unit_propagate(copy.deepcopy(f1),-k)
    bool2 = DPLL(f3,copy.deepcopy(l))
    return bool1 or bool2

DPLL(f1.clauses,copy.deepcopy(l))

print("UNSATISFIABLE")