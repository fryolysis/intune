import sympy
from intune.src.utils import pure_intervals

def solve(pitch_pair_weights, interval_weights):
    x = list( sympy.symbols('x:12') )
    x[0] = sympy.S.Zero
    # loss function
    L = sympy.S.Zero
    for i in range(12):
        for j in range(i+1, 12):
            L += pitch_pair_weights[i][j] * interval_weights[j-i] * (x[j]-x[i]-pure_intervals[j-i])**2
    # partial derivatives
    eqns = []
    for i in range(1,12):
        eqns.append( L.diff(x[i]) )
    # solve
    sol = sympy.solve(eqns, x[1:])
    
    # in case of no solution create an empty dict
    if not sol:
        sol = {}

    # if the system is underdetermined, use 12-tet default values
    for i in range(1,12):
        if x[i] not in sol.keys():
            for k in sol.keys():
                sol[k] = sol[k].subs(x[i], i*100)
            sol[x[i]] = sympy.sympify(i*100)
    scale = list(sol.values())
    scale.sort()
    return scale