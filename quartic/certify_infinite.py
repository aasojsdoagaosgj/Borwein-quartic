"""Exact checks used with the written infinite-product argument."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json


def exp_lower(x, terms):
    term = total = Q(1)
    for k in range(1, terms+1):
        term *= Q(x,k)
        total += term
    return total


def run():
    a=[1]+[0]*300
    for j in range(1,301):
        if j%3:
            for _ in range(4):
                for k in range(300,j-1,-1):a[k]-=a[k-j]
    assert all(v*(1 if k%3!=1 else -1)>0 for k,v in enumerate(a))
    e17=exp_lower(17,60)
    assert e17>20000000
    error_ratio=Q(240000,e17)+Q(600000000000,e17*e17)
    assert error_ratio<Q(1,50)
    checks={
        'finite_all_301_signs':True,
        'bessel_denominator':Q(2)*Q(22,7)*Q(10,7)*Q(11,4)<25,
        'first_error_constant_fourth_power':Q(22,7)**7<Q(4)**4*24,
        'constant_error_bound':6*3**11+54*3**8<10000000,
        'positive_cosine_margin':2*(Q(157,900)-Q(157,900)**3/6)>Q(1,3),
        'main_vs_error_at_300':error_ratio<Q(1,50),
    }
    assert all(checks.values())
    result={'status':'passed','checks':checks,'max_exact_degree':300,
            'error_ratio_upper_at_300':str(error_ratio),
            'error_ratio_upper_decimal':float(error_ratio),
            'coefficient_sha256':hashlib.sha256(str(a).encode()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'Finite signs and rational constants; the uniform estimates are in INFINITE_SIGNS.md.'}
    Path(__file__).with_name('results').joinpath('infinite_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
