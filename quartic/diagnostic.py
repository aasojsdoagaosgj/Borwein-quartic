"""Exact finite signs and numerical saddle diagnostics, not a proof of asymptotics."""
import hashlib
import json
import sys
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.local-deps'))
import mpmath as mp


def multiply(a, j):
    for k in range(len(a)-1, j-1, -1):
        a[k] -= a[k-j]


def run(max_n=65):
    start = perf_counter()
    mp.mp.dps = 60
    omega = mp.exp(2j*mp.pi/3)
    R = lambda z: mp.quad(lambda u: mp.log(1+mp.exp(-z*u)+mp.exp(-2*z*u)), [0, 1])
    phi = lambda z: -2*mp.pi/9+mp.mpf(4)/3*mp.atan(mp.sqrt(3)*mp.exp(-z)/(2+mp.exp(-z)))
    psi = lambda z, a: 2*mp.cos(phi(z)-2*mp.pi*a/3)
    xstar = 2*mp.tan(mp.pi/24)/(mp.sqrt(3)-mp.tan(mp.pi/24))
    tstar = -mp.log(xstar)
    astar = -4*mp.diff(R, tstar)
    # The coefficient degree is 3*alpha*n^2; alpha is the dissection scale.
    g = 4*mp.diff(R, tstar, 2)
    H3 = 4*mp.diff(R, tstar, 3)
    p1, p2 = mp.diff(lambda z: psi(z, 2), tstar), mp.diff(lambda z: psi(z, 2), tstar, 2)
    correction_at_zero = -p2/(2*g)+p1*H3/(2*g*g)
    linear_shift = g*correction_at_zero/p1
    cap = 6*max_n*max_n
    finite = [1]+[0]*cap
    rows = []
    for n in range(1, max_n+1):
        for j in (3*n-2, 3*n-1):
            for _ in range(4):
                multiply(finite, j)
        half = 6*n*n
        assert all(finite[j] >= 0 for j in range(0,half+1,3))
        assert all(finite[j] <= 0 for j in range(1,half+1,3))
        seen_negative = False
        last_positive, first_negative, zeros = None, None, []
        for j in range(2,half+1,3):
            v = finite[j]
            if v > 0:
                assert not seen_negative, (n,j,'return to positive')
                last_positive = (j-2)//3
            elif v < 0:
                if not seen_negative:
                    first_negative = (j-2)//3
                seen_negative = True
            else:
                zeros.append((j-2)//3)
        assert last_positive is not None and first_negative is not None
        rows.append({'n':n,'last_positive_index':last_positive,'first_negative_index':first_negative,
                     'zeros_lower_half':zeros,'last_positive_over_n2':last_positive/n**2,
                     'continuous_prediction':float(astar*n*n+linear_shift*n-mp.mpf(2)/3)})
    infinite = [1]+[0]*300
    for j in range(1,301):
        if j%3:
            for _ in range(4):multiply(infinite,j)
    assert all(v*(1 if j%3!=1 else -1)>0 for j,v in enumerate(infinite))
    em = []
    for n in (10,40,160):
        for z in (mp.mpf('.5'),tstar,mp.mpf('4'),mp.mpc('1.8','.1')):
            f1 = lambda u: mp.log(1-omega*mp.exp(-z*u))
            f2 = lambda u: mp.log(1-omega**2*mp.exp(-z*u))
            h = mp.mpf(2)/3*(f2(1)-f2(0)-f1(1)+f1(0))
            finite_log = 4*mp.fsum(mp.log(1-omega**a*mp.exp(-z*(3*j+a)/(3*n)))
                                  for j in range(n) for a in (1,2))
            delta=1+mp.exp(-z)+mp.exp(-2*z)
            u1=mp.exp(-z)*(1+2*mp.exp(-z))/delta
            beta=-z*(1-u1)/9
            err=abs(mp.exp(finite_log-4*n*R(z)-h-beta/n)-1)
            em.append({'n':n,'z':str(z),'relative_error_after_first_correction':mp.nstr(err,20)})
    result={'status':'passed','kind':'finite exact checks and nonrigorous numerical diagnostics',
            'max_n':max_n,'infinite_exact_check_max_degree':300,
            'x_star':mp.nstr(xstar,50),'tau_star':mp.nstr(tstar,50),'alpha_star':mp.nstr(astar,50),
            'profile_derivative_at_root':mp.nstr(p1,40),'linear_index_shift':mp.nstr(linear_shift,40),
            'rows':rows,'em_diagnostics':em,'infinite_first_30':infinite[:30],
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'elapsed_seconds':perf_counter()-start}
    target=ROOT/'quartic/results/diagnostic.json'
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','em_diagnostics')},indent=2))
    print('Last rows:',json.dumps(rows[-5:],indent=2))


if __name__=='__main__':run()
