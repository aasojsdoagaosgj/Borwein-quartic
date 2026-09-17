# The modulus-3 fourth-power conjecture for sufficiently large n

17 September 2026. Anonymous hobby research manuscript.
Mathematical derivation, source checking, manuscript, and verification
code were produced by OpenAI Codex. This is a conventional proof draft,
with a same-agent audit; it is not independently reviewed or formalized.
No external contact or publication has been made.

## The result

Let

```math
P_n(q)=\prod_{j=1}^{n}(1-q^{3j-2})(1-q^{3j-1}),\qquad
P_n(q)^4=\sum_{j=0}^{12n^2}c_j(n)q^j.
```

**Theorem.** There exists an integer $N_0$ such that, for every
$n\ge N_0$, there is an integer $k_n$ with

```math
c_{3k+2}(n)\begin{cases}
\ge0,&0\le k\le k_n,\\
<0,&k_n<k\le4n^2-1.
\end{cases}                                                    (T1)
```

There is at most one zero in this residue class; if present it is at the
transition. Moreover $c_{3k}(n)\ge0$ for **every** $n\ge1$ and
$0\le k\le4n^2$. The remaining residue class is determined by
$c_j(n)=c_{12n^2-j}(n)$.

In particular, this proves the qualitative sign-pattern and convergence
assertions, for sufficiently large $n$, in
[Berkovich--Dhar, Conjecture 2.1, power 4](https://arxiv.org/html/2407.13788v3#S2),
with the following limiting transition location. It corrects the printed
decimal $0.750\ldots$ in that conjecture's table:

```math
\frac{k_n}{n^2}\longrightarrow\alpha_*,\qquad
\alpha_*=-4R'(\tau_*),
```

```math
R(z)=\int_0^1\log(1+e^{-zu}+e^{-2zu})\,du,\qquad
\tau_*=-\log\left(\frac{2\tan(\pi/24)}{\sqrt3-\tan(\pi/24)}\right).
                                                                    (T2)
```

Indeed $k_n=\alpha_*n^2+\beta_*n+O(1)$, where $\beta_*$ is
given by (C9) of COMPACT_PROOF.md. The limit has a rational interval
certificate; the linear correction is evaluated numerically:

```math
\alpha_*=0.7490800947885107244\ldots,\qquad
\beta_*=0.0881422570523141372\ldots.
```

**The threshold $N_0$ is not numerically evaluated in this manuscript.**
The proof establishes its existence through uniform bounds. It does not
establish the conjecture for every positive $n$. The exact expressions
(T2) define the limit; `certify_limit.py` rigorously encloses it between
0.74908009478851072443256 and 0.74908009478851072443257.

## Proof and the coverage of all coefficients

The second Borwein theorem of Wang--Krattenthaler
([Theorem 10.3](https://arxiv.org/html/2201.12415#S10)) gives

```math
P_n(q)^2=A_n(q^3)-qB_n(q^3)-q^2C_n(q^3),
```

where $A_n,B_n,C_n$ have nonnegative coefficients. Squaring, the
residue-0 component is $A_n(Q)^2+2Q B_n(Q)C_n(Q)$. This proves
the residue-0 assertion for all $n$. This step only uses their proved
second-power theorem, not any cubic conjecture.

There are an even number of reciprocal factors and their total degree
is $12n^2$; hence $F_n(q)=q^{12n^2}F_n(1/q)$. It suffices to
control residues 1 and 2 in the lower half $0\le j\le6n^2$.

1. **Initial degrees.** INFINITE_SIGNS.md proves that the infinite
   fourth power has strict signs $+,-,+$. The finite coefficients
   agree with it through degree $3n$.

2. **Endpoint saddle.** ENDPOINT_PROOF.md proves the same strict signs
   for every $3n\le j\le j_e(n)=-3nL_n'(6)$, once $n$ is
   sufficiently large. Its expansion is uniform even when the saddle
   tends to infinity: its large parameter is $N=n/\tau>\sqrt{n/5}$.

3. **Compact saddle.** COMPACT_PROOF.md covers all
   $3n^2\alpha(7)\le j\le6n^2$, where $\alpha=-4R'$.
   The residue-1 coefficients are strictly negative throughout.
   In residue 2, the leading amplitude has one simple zero, and
   the normalized adjacent-coefficient difference is strictly negative
   throughout a fixed neighborhood of it. Thus there is exactly one
   sign transition, with at most one zero; signs away from that
   neighborhood follow from a uniform nonzero main-term margin.

4. **Overlap.** The endpoint upper boundary satisfies
   $j_e(n)/(3n^2)=\alpha(6)+O(n^{-2})>\alpha(7)$.
   Thus the initial, endpoint, and compact ranges overlap for every
   sufficiently large $n$. They leave no lower-half degree uncovered.

All sufficiently-large conditions above are uniform and finite in
number, so a single integer $N_0$ satisfies them. In the lower half,
residue 1 is always negative, while residue 2 starts positive and ends
negative with one transition. In the upper half, residue 2 is the
reflection of the lower-half residue 1, so remains negative. This gives
(T1) for the entire polynomial. Compact expansion (C9) proves (T2) and
the linear correction. This completes the proof.

## How the numerical findings relate to the theorem

`diagnostic.py` checks every required lower-half sign and transition for
$1\le n\le65$ with exact integers. Reciprocity covers the upper half.
For $n=65$ it gives $k_{65}=3170$, matching the example in
Berkovich--Dhar. Its ratio is $3170/4225=0.7502958579\ldots$,
whereas (T2) is the limiting ratio. The positive linear correction
explains why that finite ratio is higher. These finite checks do not
supply the eventual threshold and are not used to extrapolate the theorem.

`certify_infinite.py` checks the initial 301 infinite coefficients and
the elementary rational margins needed to use an explicit published
infinite-product error estimate. Its role in the proof is precisely
specified in INFINITE_SIGNS.md.

The substantial new argument in this draft is the use of the compact
expansion through an $O(n^{-3})$ remainder to control an actual
lattice sign transition. Pointwise saddle signs and finite numerical
samples alone would not imply that assertion. No claim of priority or
independent verification is made.
