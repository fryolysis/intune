import sympy
from intune.src.utils import pure_intervals

def solve(pitch_pair_weights, interval_weights):
    x = list( sympy.symbols(':12') )
    # loss function
    L = sympy.S.Zero
    for i in range(12):
        for j in range(i+1, 12):
            L += pitch_pair_weights[i][j] * interval_weights[j-i] * (x[j]-x[i]-pure_intervals[j-i])**2
    # partial derivatives
    eqns = []
    for i in range(12):
        eqns.append( L.diff(x[i]) )
    # solve
    sol = sympy.solve(eqns, x)
    
    # in case of no solution abort
    assert sol, "No solution, aborting.."
    
    # normally the rank of the matrix must be at most 11 so there shouldn't be a unique solution (loss function is translation invariant). However due to floating point errors we usually have a unique solution.
    # assuming there is always a unique solution
    try:
        # get rid of sympy symbols
        sol = {int(str(k)) : v for k,v in sol.items()} 
    except AssertionError():
        print('solution is not unique!')
    
    return sol