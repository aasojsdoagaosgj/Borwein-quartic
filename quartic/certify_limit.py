"""Rational interval enclosure of the exact limiting transition constant."""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import hashlib
import json


class I:
    def __init__(self,a,b=None):self.a,self.b=Q(a),Q(a if b is None else b)
    @staticmethod
    def of(v):return v if isinstance(v,I) else I(v)
    def __add__(self,o):
        o=I.of(o);return I(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return I(-self.b,-self.a)
    def __sub__(self,o):return self+-I.of(o)
    def __rsub__(self,o):return I.of(o)+-self
    def __mul__(self,o):
        o=I.of(o);v=[self.a*o.a,self.a*o.b,self.b*o.a,self.b*o.b];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=I.of(o);assert o.a*o.b>0;return self*I(1/o.b,1/o.a)
    def __rtruediv__(self,o):return I.of(o)/self
    def __pow__(self,k):
        assert isinstance(k,int) and k>=0
        result=I(1)
        for _ in range(k):result=result*self
        return result


def sqrt_integer(v):
    scale=10**30
    low=isqrt(v*scale*scale)
    assert low*low<=v*scale*scale<(low+1)*(low+1)
    return I(Q(low,scale),Q(low+1,scale))


def atan_inverse(v,terms):
    a=Q(1,v);s=Q(0)
    for k in range(terms):s+=(-1)**k*a**(2*k+1)/(2*k+1)
    next_term=(-1)**terms*a**(2*terms+1)/(2*terms+1)
    return I(min(s,s+next_term),max(s,s+next_term))


def positive_log_from_t(t,terms=110):
    assert 0<=t.a<=t.b<1
    s=I(0);power=t
    square=t*t
    for k in range(terms):
        s+=power/(2*k+1)
        power*=square
    tail=t.b**(2*terms+1)/((2*terms+1)*(1-t.b*t.b))
    return 2*(s+I(0,tail))


def li2(x,terms=60):
    assert 0<x.a<=x.b<1
    s=I(0);power=I(1)
    for k in range(1,terms+1):
        power*=x;s+=power/(k*k)
    tail=x.b**(terms+1)/((terms+1)**2*(1-x.b))
    return s+I(0,tail)


def decimal_out(v,digits,upper=False):
    scale=10**digits
    scaled=v*scale
    k=scaled.numerator//scaled.denominator
    if upper and Q(k)!=scaled:k+=1
    whole,frac=divmod(k,scale)
    return f'{whole}.{frac:0{digits}d}'


def run():
    # Machin's identity and half-angle identity; every operation is rational.
    pi=16*atan_inverse(5,24)-4*atan_inverse(239,8)
    tangent=sqrt_integer(6)+sqrt_integer(2)-sqrt_integer(3)-2
    # tan(pi/24) = sqrt(6)+sqrt(2)-sqrt(3)-2.
    x=2*tangent/(sqrt_integer(3)-tangent)
    tau=positive_log_from_t((1-x)/(1+x))
    delta=1+x+x*x
    log_delta=positive_log_from_t((delta-1)/(delta+1),40)
    numerator=pi*pi/9+li2(x**3)/3-li2(x)
    alpha=4*(numerator-tau*log_delta)/(tau*tau)
    assert Q('0.74908009478851072443')<alpha.a<alpha.b<Q('0.74908009478851072444')
    assert Q(decimal_out(alpha.a,23))<alpha.a
    assert alpha.b<Q(decimal_out(alpha.b,23,True))
    result={'status':'passed','method':'exact rational interval arithmetic',
        'alpha_star_interval':[decimal_out(alpha.a,23),decimal_out(alpha.b,23,True)],
        'tau_star_interval':[decimal_out(tau.a,23),decimal_out(tau.b,23,True)],
        'x_star_interval':[decimal_out(x.a,23),decimal_out(x.b,23,True)],
        'terms':{'atan_1_over_5':24,'atan_1_over_239':8,'log_x':110,'log_delta':40,'dilog':60},
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Encloses the formula in COMPACT_PROOF.md; does not certify its connection to coefficient signs.'}
    Path(__file__).with_name('results').joinpath('limit_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
