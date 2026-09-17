"""Cross-check the analytic formulas against exact coefficients and products."""
import hashlib
import json
import sys
from math import factorial, prod
from pathlib import Path
from time import perf_counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.local-deps'))
import mpmath as mp
from diagnostic import multiply


def run():
    start=perf_counter()
    mp.mp.dps=70
    omega=mp.exp(2j*mp.pi/3)
    def R(z):
        x=mp.exp(-z)
        return (mp.pi**2/9+mp.polylog(2,x**3)/3-mp.polylog(2,x))/z
    H=lambda z:4*R(z)
    phi=lambda z:-2*mp.pi/9+mp.mpf(4)/3*mp.atan(mp.sqrt(3)*mp.exp(-z)/(2+mp.exp(-z)))
    psi=lambda z:2*mp.cos(phi(z)+2*mp.pi/3)
    def bfun(z):
        x=mp.exp(-z)
        return -z*(1-x*(1+2*x)/(1+x+x*x))/9
    def S1(f,z):
        g=mp.diff(H,z,2)
        h3,h4=mp.diff(H,z,3),mp.diff(H,z,4)
        return (-mp.diff(f,z,2)/(2*g)+mp.diff(f,z)*h3/(2*g*g)
                +f(z)*(h4/(8*g*g)-5*h3*h3/(24*g**3)))
    def a1(z):return bfun(z)*psi(z)+S1(psi,z)
    def a2(z):
        g=mp.diff(H,z,2)
        hd={k:mp.diff(H,z,k) for k in range(3,7)}
        pd={k:mp.diff(psi,z,k) for k in range(5)}
        value=mp.mpf(0)
        for p in range(5):
            for e3 in range(5):
                for e4 in range(3):
                    for e5 in range(2):
                        for e6 in range(2):
                            if p+e3+2*e4+3*e5+4*e6!=4:continue
                            exps={3:e3,4:e4,5:e5,6:e6}
                            degree=p+sum(k*e for k,e in exps.items())
                            moment=prod(range(1,degree,2))/g**(degree//2)
                            term=(-1)**(degree//2)*pd[p]*moment/factorial(p)
                            for k,e in exps.items():term*=hd[k]**e/(factorial(k)**e*factorial(e))
                            value+=term
        x=mp.exp(-z);delta=1+x+x*x
        d=-2j*mp.sqrt(3)*z*z*x*(1-x*x)/(81*delta*delta)
        amplitude2=bfun(z)**2*psi(z)/2+d*2j*mp.sin(phi(z)+2*mp.pi/3)
        return mp.re(amplitude2+S1(lambda u:bfun(u)*psi(u),z)+value)
    tstar=-mp.log(2*mp.tan(mp.pi/24)/(mp.sqrt(3)-mp.tan(mp.pi/24)))
    astar=-mp.diff(H,tstar)
    beta=mp.diff(H,tstar,2)*a1(tstar)/mp.diff(psi,tstar)
    samples=[]
    for n in (20,40,80,160):
        prediction=astar*n*n+beta*n-mp.mpf(2)/3
        k=int(mp.floor(prediction))-1
        j=3*k+2
        a=[1]+[0]*(j+9)
        for part in range(1,3*n):
            if part%3:
                for _ in range(4):multiply(a,part)
        row={'n':n,'coefficients':[],'crossing_prediction':mp.nstr(prediction,25)}
        for degree in (j,j+3,j+6,j+9):
            alpha=mp.mpf(degree)/(3*n*n)
            tau=mp.findroot(lambda z:-mp.diff(H,z)-alpha,tstar)
            g=mp.diff(H,tau,2)
            B=mp.exp(n*(H(tau)+alpha*tau))/(3*n*mp.sqrt(2*mp.pi*n*g))
            normalized=mp.mpf(a[degree])/B
            residual=normalized-psi(tau)-a1(tau)/n
            row['coefficients'].append({'degree':degree,'normalized':mp.nstr(normalized,25),
                'n2_times_first_order_residual':mp.nstr(n*n*residual,25),
                'n3_times_second_order_residual':mp.nstr(n**3*(residual-a2(tau)/n**2),25)})
        positives=[(degree-2)//3 for degree in (j,j+3,j+6,j+9) if a[degree]>0]
        negatives=[(degree-2)//3 for degree in (j,j+3,j+6,j+9) if a[degree]<0]
        assert positives and negatives and max(positives)<min(negatives)
        row['local_last_positive_index']=max(positives)
        row['local_first_negative_index']=min(negatives)
        row['local_crossing_ratio']=mp.nstr(mp.mpf(max(positives))/n**2,25)
        row['n2_times_normalized_difference']=mp.nstr(n*n*(mp.mpf(row['coefficients'][1]['normalized'])-
                                                                  mp.mpf(row['coefficients'][0]['normalized'])),25)
        samples.append(row)
        print('coefficient diagnostic n=',n,flush=True)
    def Finf(q):
        count=int(mp.ceil(200/(-mp.log(abs(q)))))+1
        return mp.exp(4*mp.fsum(mp.log(1-q**j) for j in range(1,count) if j%3))
    modular=[]
    for w in (mp.mpf('.05'),mp.mpf('.4'),mp.mpc('.2','-.3')):
        t=mp.exp(-4*mp.pi**2/(9*w))
        rhs=mp.exp(4*mp.pi**2/(27*w)-w/3-2j*mp.pi/9)*Finf(omega**2*t)
        err=abs(Finf(omega*mp.exp(-w))/rhs-1)
        assert err<mp.mpf('1e-60')
        modular.append({'w':str(w),'relative_error':mp.nstr(err,20)})
    result={'status':'diagnostic_completed','precision_digits':70,'coefficient_samples':samples,
        'modular_identity':modular,'expected_limit_n2_difference':mp.nstr(-mp.diff(psi,tstar)/mp.diff(H,tstar,2),30),
        'expected_limit_n2_first_order_residual':mp.nstr(a2(tstar),30),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_seconds':perf_counter()-start,
        'caution':'Finite diagnostics only; no interval rounding and no proof of uniform error bounds.'}
    Path(__file__).with_name('results').joinpath('saddle_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
