#solving the given problem with a smt Solver based on cvc5

#1: square * square * circle = 16
#2: triangle * triangle * triangle =27
#3: triangle * square = 6

#square * circle * triangle = ?


import cvc5
from cvc5 import *
from cvc5 import Kind

if __name__ == "__main__":

#configure solver
    solver = cvc5.Solver()

    solver.setOption("produce-models", "true")
    solver.setOption("produce-unsat-cores", "true")

 #set logic
    solver.setLogic("ALL")

#set constraints
    realSort = solver.getRealSort()
    intSort = solver.getIntegerSort()

    square = solver.mkConst(realSort, "x")
    triangle = solver.mkConst(realSort, "y")
    circle = solver.mkConst(realSort, "z")
    a = solver.mkConst(intSort, "a")

#start constants
    zero = solver.mkReal(0)
    one = solver.mkReal(1)

#define constraints.
# They use the operators +, <=, and <.
# In the API, these are denoted by Plus, Leq, and Lt.

    squaresquarecircle = solver.mkTerm(Kind.MULT, square, square, circle)
    trianglecubed = solver.mkTerm(Kind.MULT, triangle, triangle, triangle)
    trianglesquare = solver.mkTerm(Kind.MULT, triangle, square)
    squarecircletriangle = solver.mkTerm(Kind.MULT, square, circle, triangle)

    constraint1 = solver.mkTerm(Kind.EQUAL, squaresquarecircle, 16)
    constraint2 = solver.mkTerm(Kind.EQUAL, trianglecubed, 27)
    constraint3 = solver.mkTerm(Kind.EQUAL, trianglesquare, 6)
    constraint4 = solver.mkTerm(Kind.EQUAL, squarecircletriangle, a)


# Now we assert the constraints to the solver.
    solver.assertFormula(constraint1)
    solver.assertFormula(constraint2)
    solver.assertFormula(constraint3)
    solver.assertFormula(constraint4)

    r1 = solver.checkSat()

    print("expected: sat")
    print("result: ", r1)