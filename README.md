# The modulus-3 fourth-power Borwein-type conjecture for sufficiently large $n$

**Status:** proof draft with reproducible computational certificates; not peer-reviewed or formally verified.

This repository studies the fourth-power case of Berkovich–Dhar's modulus-3 Borwein-type conjecture. Let

```math
P_n(q)=\prod_{j=1}^{n}(1-q^{3j-2})(1-q^{3j-1}),
\qquad
P_n(q)^4=\sum_{j=0}^{12n^2} c_j(n)q^j.
```

The main result proved in this draft is an **eventual (large-$n$) version** of the conjectured sign pattern, together with an asymptotic formula for the unique transition point.

## Main result

There exists an integer $N_0$ such that for every $n\ge N_0$, there is an integer $k_n$ satisfying

```math
c_{3k+2}(n)\begin{cases}
\ge 0,&0\le k\le k_n,\\
<0,&k_n<k\le 4n^2-1.
\end{cases}
```

There is at most one zero in this residue class, and if it occurs, it occurs at the transition.

In addition,

```math
c_{3k}(n)\ge 0
```

for every $n\ge1$, and the remaining residue class is determined by the palindromic symmetry

```math
c_j(n)=c_{12n^2-j}(n).
```

Thus the quartic case of Berkovich–Dhar, Conjecture 2.1, is proved here for all sufficiently large $n$.

The transition location satisfies the sharper asymptotic

```math
k_n=\alpha_*n^2+\beta_*n+O(1),
```

where

```math
\alpha_*=-4R'(\tau_*),
\qquad
R(z)=\int_0^1\log(1+e^{-zu}+e^{-2zu})\,du,
```

and

```math
\tau_*=-\log\left(\frac{2\tan(\pi/24)}{\sqrt3-\tan(\pi/24)}\right).
```

A rigorous rational interval certificate gives

```math
0.74908009478851072443256
<\alpha_*<
0.74908009478851072443257.
```

Numerically,

```math
\beta_*\approx0.0881422570523141372.
```

The concrete threshold $N_0$ is **not evaluated** in this repository. The theorem is an existence statement for sufficiently large $n$, not a proof for every positive integer $n$.

## What is new here

Berkovich and Dhar introduced this fourth-power sign-pattern problem as part of Conjecture 2.1. Their published conjecture was based on computation and predicted a limiting transition ratio near $0.75$.

This draft provides:

- an eventual proof of the quartic sign pattern;
- uniqueness of the sign transition in the $3k+2$ residue class;
- the exact analytic definition of the limiting transition constant;
- the rigorous value
```math
  \alpha_*=0.7490800947885107244\ldots;
```
- the refined expansion $k_n=\alpha_*n^2+\beta_*n+O(1)$.

A preliminary literature search did not locate an earlier proof of this large-$n$ quartic result or the constant above. This is **not a formal priority claim**; readers are encouraged to point out related or prior work.

## Proof architecture

The proof divides the coefficient range into three overlapping regimes.

### 1. Initial coefficients

[`quartic/INFINITE_SIGNS.md`](quartic/INFINITE_SIGNS.md) proves the required signs for the corresponding infinite product. The finite and infinite products agree through degree $3n$.

The argument combines a published explicit error estimate with an exact check of the first 301 coefficients.

### 2. Endpoint saddle regime

[`quartic/ENDPOINT_PROOF.md`](quartic/ENDPOINT_PROOF.md) treats the range in which the saddle parameter grows with $n$. The estimates are uniform in the effective large parameter $N=n/\tau$, rather than relying on a fixed-saddle approximation.

### 3. Compact saddle regime and the actual transition

[`quartic/COMPACT_PROOF.md`](quartic/COMPACT_PROOF.md) derives a uniform expansion through an $O(n^{-3})$ remainder.

The key point is that near the zero of the leading amplitude, a pointwise sign approximation is insufficient. After normalization, adjacent coefficients in the same residue class satisfy

```math
u_{n,j+3}-u_{n,j}
=-\frac{c(\tau)}{n^2}+O(n^{-3}),
\qquad c(\tau)>0,
```

uniformly in a fixed neighborhood of the transition. This gives strict monotonicity across the lattice transition and rules out repeated sign changes.

### 4. Global gluing

[`quartic/LARGE_N_RESULT.md`](quartic/LARGE_N_RESULT.md) shows that the initial, endpoint, and compact ranges overlap for all sufficiently large $n$, and uses reciprocity to cover the upper half of the polynomial.

## Repository guide

| File | Purpose |
|---|---|
| [`quartic/LARGE_N_RESULT.md`](quartic/LARGE_N_RESULT.md) | Main theorem and global assembly |
| [`quartic/COMPACT_PROOF.md`](quartic/COMPACT_PROOF.md) | Uniform compact-saddle expansion and unique transition |
| [`quartic/ENDPOINT_PROOF.md`](quartic/ENDPOINT_PROOF.md) | Growing-saddle endpoint analysis |
| [`quartic/INFINITE_SIGNS.md`](quartic/INFINITE_SIGNS.md) | Infinite-product signs and finite-product connection |
| [`quartic/AUDIT.md`](quartic/AUDIT.md) | Internal proof audit |
| [`INDEPENDENT_AUDIT.md`](INDEPENDENT_AUDIT.md) | Subsequent independent audit report |
| [`quartic/verify.py`](quartic/verify.py) | Reproducibility entry point |
| [`quartic/results/`](quartic/results/) | Stored certificates and diagnostics |

## Reproducibility

Python 3.10 or later is recommended.

First verify that the bundled files match their recorded SHA-256 hashes:

```bash
python verify_bundle.py
```

Install the numerical dependency used by the diagnostics:

```bash
python -m pip install -r requirements-audit.txt
```

Then replay all supplied calculations:

```bash
python -B quartic/verify.py --replay
```

On the public bundle used to prepare this README, the replay completed successfully for:

- `certify_infinite.py`;
- `certify_endpoint_constants.py`;
- `certify_limit.py`;
- `diagnostic.py`;
- `saddle_diagnostic.py`.

The finite diagnostic checks all required lower-half signs and transitions for $1\le n\le65$ using exact integer arithmetic. These computations are **diagnostics and certificates for specific dependencies**, not a substitute for the asymptotic proof.

## Current limitations

This repository does **not** currently provide:

- a numerical value of the eventual threshold $N_0$;
- a proof of the quartic conjecture for every positive $n$;
- a formal proof in Lean, Coq, Isabelle, or another proof assistant;
- peer review or journal refereeing;
- a definitive claim of publication priority.

## AI-use disclosure

The mathematical derivation, manuscript drafting, source checking, and verification code in the original research bundle were produced with OpenAI Codex. A subsequent independent audit in ChatGPT rechecked the main logical dependencies, literature citations, and supplied computations and did not identify a fatal gap in the stated large-$n$ theorem.

This repository should therefore be read as an **AI-assisted mathematical proof draft with reproducible supporting computations**, not as independently certified mathematics.

## References

1. A. Berkovich and A. Dhar, *New Borwein-Type Conjectures*, Experimental Mathematics 35 (2026), 349–352. arXiv:2407.13788.
2. C. Krattenthaler and C. Wang, *An asymptotic approach to Borwein-type sign pattern theorems*, arXiv:2201.12415.
3. L. Wang, *Sign Changes of Coefficients of Powers of the Infinite Borwein Product*, arXiv:2108.03932.

## Feedback

Corrections, counterexamples, references to prior work, and independent checks are welcome.
