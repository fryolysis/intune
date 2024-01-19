import sympy
from intune.src.params import *

def _align(sol):
    '''
    - In the sequence C,C#,D... the first pitch class which appears in the solution is chosen as pivot and all the solution is rotated so that pivot class gets its default value.
     
     Default values:
     C:     0 cents
     C#:    100 cents
     D:     200 cents
     ...
    '''
    
    # iterates over C, C#, D.. until it finds one that's in the solution
    akey = 0
    while akey not in sol.keys():
        akey += 1
    # shift all notes so that the picked note gets its default 12-tet value
    sol = {k : (v-sol[akey]+(akey//K)*100)%1200 for k,v in sol.items()}
    return sol

def solve(score, pitch_pair_weights):
    varcount = pitch_pair_weights.shape[0]
    x = list( sympy.symbols(f':{varcount}') )
    # loss function
    L = sympy.S.Zero
    for i in range(varcount):
        for j in range(i+1, varcount):
            icls, jcls = i//K, j//K
            big,smol,clsdiff = (i,j,icls-jcls) if icls > jcls else (j,i,jcls-icls)
            L += pitch_pair_weights[i][j] * interval_weight[clsdiff] * (x[big]-x[smol]-pure_intervals[clsdiff])**2
    # partial derivatives
    eqns = []
    for i in range(varcount):
        eqns.append( L.diff(x[i]) )
    # solve
    sol = sympy.solve(eqns, x)
    # get rid of sympy symbols
    sol = {int(str(k)):v for k,v in sol.items()}
    
    score.solution = _align(sol)