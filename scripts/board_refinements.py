"""Visible reasoning, optional investigations, and links for Lesson 1."""

import re

TRANSITIONS = {
    'average': ('Our first decision was which times the model allows. What else must we specify to define a function?', '#/functions/data', 'Specify a function'),
    'equality': ('The quotient loses its input at 1 because a step of the calculation is undefined there. A composition can lose inputs for the same reason.', '#/composition/compose', 'Trace a composition'),
    'inverse': ('Compare how different function families behave. For exponentials, the same test for unique recovery explains why a logarithm can undo the assignment.', '#/families/exponent-log', 'Recover an exponent'),
    'identity-domains': ('A rotation gives another way to build functions. We can use circle geometry to predict how their values respond to an angle change.', '#/trigonometry/circle', 'Read the circle coordinates'),
    'waves': ('Addition formulas describe a change in angle. For a power such as (x + h)ⁿ, expansion will tell us exactly how the increment enters.', '#/binomial/count', 'Count terms in an expansion'),
    'increment': ('Use the case n = 2 to separate the exact change in position from its linear prediction.', '#/return/local', 'Return to the motion model'),
}

CONNECTIONS = {
    'equality': ('Limits and continuity', 'Nearby values and the value at the missing input are separate questions.'),
    'compose': ('Chain rule', 'Track which intermediate value is passed to the outer function before studying the rate at each stage.'),
    'inverse': ('Inverse-function differentiation', 'Unique recovery gives a well-defined inverse. Later we will need additional hypotheses to differentiate it.'),
    'log-laws': ('Logarithmic differentiation', 'Products become sums and powers become constant factors when the logarithm laws apply.'),
    'addition': ('Trigonometric limits and derivatives', 'The addition formula rewrites a change from x to x + h using trigonometric values at h.'),
    'derived': ('Trigonometric integration', 'Power reduction replaces squared trigonometric terms with expressions in the doubled angle.'),
    'increment': ('Power rule and approximation', 'The term with one factor of h supplies the coefficient that will appear in the derivative.'),
}


def refine_boards(boards, render, term):
    by_key = {board['key']: board for group in boards.values() for board in group}
    for key, board in by_key.items():
        if key in TRANSITIONS:
            board['transition'] = TRANSITIONS[key]
        if key in CONNECTIONS:
            board['connection'] = CONNECTIONS[key]
    def revise(key, title=None, text=None, prompt=None):
        board = by_key[key]
        if title:
            board['title'] = title
        if text:
            board['argument'] = render(text)
        if prompt:
            board['prompt'] = prompt

    def extend(key, text):
        by_key[key]['argument'] += render(text)

    revise('data', 'What information defines a function?')
    extend('data', r"""
The codomain declares the target. The range is computed from the inputs:
$$f(D)=\{f(x): x\in D\}\subseteq B.$$
For the square function on $\mathbb R$, every $y\ge0$ is reached at $x=\sqrt y$, and every square is nonnegative. That establishes the range in both directions.
""")
    revise('representations', 'What can a graph or table tell us?')
    extend('representations', r"""
A vertical line fixes $x$, so its intersections count the outputs assigned to that input. For instance, $x=0$ on the full circle gives both $y=1$ and $y=-1$. The upper semicircle retains only $y=1$.
""")
    revise('restrictions', 'Which inputs make the original expression meaningful?')
    extend('restrictions', r"""
Apply each condition to its own subexpression. Here $x+1\ge0$ and $x-2\ne0$ must **both** hold, so we intersect the two allowed sets.
""")
    revise('atlas', 'How do formulas determine a function’s type and domain?')
    extend('atlas', r"""
Compare $\sqrt{-8}$ and $\sqrt[3]{-8}$. No real square equals $-8$, while $(-2)^3=-8$. The real domain of a root therefore depends on its index.
""")
    revise('exponent-log', 'How does a logarithm recover the exponent?')
    extend('exponent-log', r"""
The graphs reflect across $y=x$ because $b^x=y$ and $\log_b y=x$ give ordered pairs with their coordinates reversed. For $b=2$, this sends $(1,2)$ to $(2,1)$.
""")
    revise('circle', 'How does an angle determine two coordinates?')
    extend('circle', r"""
At radius $1$, the circle equation gives $\cos^2\theta+\sin^2\theta=1$. Reflecting across the horizontal axis keeps the horizontal coordinate and negates the vertical one. Adding $2\pi$ returns to the same point.
""")
    revise('derived', 'How do the addition formulas produce new identities?')
    revise('count', 'Why do the binomial coefficients count choices?')
    extend('count', r"""
The order in which we list the chosen factors does not affect their contribution. The coefficient counts the distinct $k$-element subsets. At $k=1$ there are exactly $n$ choices, which will give the term linear in an increment.
""")

    revise('average', 'Can shorter intervals tell us the velocity at t = 2?', r"""
For motion along a line, let $s(t)=t^2$ for $t\ge0$. Here $t$ is measured in seconds and $s(t)$ in metres.

Between $t=2$ and $t=2+h$, the **average velocity** is the slope of the secant:
$$\frac{s(2+h)-s(2)}{h},\qquad h>0.$$

Predict how the slope changes as $h$ shrinks. At $h=0$ the quotient is undefined. A """ + term('limit') + r""" will give us a precise way to describe its nearby values.
""", 'Start with one second, then compare a tenth and a hundredth of a second.')

    revise('equality', 'When do two formulas define the same function?', r"""
$$\begin{aligned} r(x)&=\frac{x^2-1}{x-1} &&(x\ne1),\\ \ell(x)&=x+1 &&(x\in\mathbb R). \end{aligned}$$

The denominator requires $x\ne1$. On those inputs, $x^2-1=(x-1)(x+1)$ lets us cancel the nonzero factor $x-1$, giving $r(x)=\ell(x)$.

With the same codomain, **equality requires the same domain and the same value at every input**. The quotient is a """ + term('restriction') + r""" of the line. Assigning any value at $1$ gives an """ + term('extension') + r""". Which choice agrees with the line?
""", 'Predict what happens at x = 1 before selecting Simplified. Then compare extensions.')

    revise('compose', 'How does composition affect the domain?', r"""
A """ + term('composition') + r""" can be evaluated at $x$ exactly when the inner function accepts $x$ and the outer function accepts the result:
$$\operatorname{dom}(f\circ g)=\{x\in\operatorname{dom}g:g(x)\in\operatorname{dom}f\}.$$

With $f(u)=\sqrt u$ and $g(x)=1-x^2$:

| Order | Condition from the original operations | Result |
|---|---|---|
| $f\circ g$ | $1-x^2\ge0$ | $\sqrt{1-x^2}$ on $[-1,1]$ |
| $g\circ f$ | $x\ge0$ | $1-x$ on $[0,\infty)$ |

In the second row, $\sqrt x$ must exist before we can square it. As with the cancelled quotient at $x=1$, the simpler formula still has to respect the original input condition.
""", 'Try x = −1 in both orders. Identify the stage that accepts or rejects the input.')

    revise('outer', 'Why does the same inner expression give different domains?', r"""
Let $u=4-x^2$. The admissible values of $u$ depend on the next operation.

| Expression | Condition on $u$ | Domain in $x$ |
|---|---|---|
| $\sqrt u$ | $u\ge0$ | $[-2,2]$ |
| $\ln u$ | $u>0$ | $(-2,2)$ |
| $\sqrt{\ln u}$ | $u>0$ and $\ln u\ge0$ | $[-\sqrt3,\sqrt3]$ |

The last row reduces to $u\ge1$ because $\ln$ is increasing and $\ln1=0$. At $x=\pm\sqrt3$ the outer root receives $0$.
""", 'Trace the stages at an exact boundary or check the inequality that defines the whole domain.')

    revise('inverse', 'When can we recover an input uniquely?', r"""
For a function $f:D\to B$, an inverse $f^{-1}:B\to D$ exists **if and only if** $f$ is """ + term('bijective') + r""".

- """ + term('surjective', 'Surjectivity') + r""" gives at least one preimage for every $y\in B$.
- """ + term('injective', 'Injectivity') + r""" gives at most one, so assigning that preimage defines a function.

A restriction changes which inputs participate in the assignment. For the square, choosing a branch removes one of the two competing inputs for each positive output. Extending the earlier quotient added an input.

The resulting maps satisfy $f^{-1}(f(x))=x$ for $x\in D$ and $f(f^{-1}(y))=y$ for $y\in B$. Conversely, these identities give uniqueness and existence, respectively.

**Example.** Solving $x^2=4$ gives two inputs on $\mathbb R$. On $[0,\infty)$ the inverse is $\sqrt y$, and on $(-\infty,0]$ it is $-\sqrt y$, in both cases for $y\ge0$.
""", 'Predict the preimages of 4 in each domain. Then test 0: what can that one output establish?')

    revise('atlas', prompt='Compare √x and ∛x at negative inputs. Which restriction comes from the exponent?')
    revise('increments', 'What stays fixed when the input moves by h?', r"""
Write $\Delta_h f(x)=f(x+h)-f(x)$ for the output difference. Hold $h$ fixed while varying $x$.

| Function | Exact change for a step $h$ |
|---|---|
| $L(x)=3x+2$ | $\Delta_h L(x)=3h$ |
| $P(x)=x^2$ | $\Delta_h P(x)=2xh+h^2$ |
| $E(x)=2^x$ | $E(x+h)=2^hE(x)$ |

In an affine function $mx+b$, subtracting cancels $b$ and the starting contribution $mx$, leaving $mh$. For $L(x)=x$, this is just $h$.

For the square, the cross term $2xh$ makes the **additive change depend on the starting input** whenever $h\ne0$. For the exponential, adding $h$ to the exponent multiplies the positive output by the **same factor** $2^h$, even though the output difference $2^x(2^h-1)$ depends on $x$ for $h\ne0$.

These rules describe changes over finite steps. The opening motion question asks what happens to change per unit step as the step shrinks.
""", 'Fix h and move x. Compare the output difference and ratio, then test h = 0.')
    revise('exponent-log', prompt='Predict which direction each curve moves after changing the base from 2 to ½.')
    revise('log-laws', 'Why does the logarithm turn products into sums?', r"""
For $u,v>0$, $b>0$ with $b\ne1$, and $r\in\mathbb R$:

| Operation | Result |
|---|---|
| Product | $\log_b(uv)=\log_b u+\log_b v$ |
| Quotient | $\log_b(u/v)=\log_b u-\log_b v$ |
| Power | $\log_b(u^r)=r\log_b u$ |

Write positive inputs as powers of the same base. **Multiplying the inputs adds their exponents.** Applying the inverse logarithm reads off that sum. The derivation uses the real-exponent laws as background.
""", 'Follow the product derivation. Which exponent law would you use for the quotient?')

    revise('identity-domains', 'Can both sides of the identity be evaluated?', r"""
**Check existence first.** As with the cancelled quotient, keep track of where each expression is defined. At $x<0$, $\ln(x^2)$ exists but $2\ln x$ is undefined. On $x\ne0$, rewrite $x^2=|x|^2$ so the power law applies to the positive input $|x|$:
$$\ln(x^2)=2\ln|x|.$$

**Then compare values.** For $x=-2$, both $\sqrt{x^2}$ and $x$ exist. Their values are $2$ and $-2$. In general, the principal root gives $\sqrt{x^2}=|x|$.

Can you find positive inputs that disprove a proposed logarithm sum law?
""", 'Try a negative input, zero, and a positive input. Classify the result before comparing numbers.')

    revise('circle', prompt='At a non-axis angle, predict which coordinate changes sign under reflection. Then select π/2 and inspect tangent.')
    revise('addition', 'How does one chord give the cosine addition formulas?', r"""
Take unit-circle points $P=(\cos u,\sin u)$ and $Q=(\cos v,\sin v)$. Expanding their squared distance in coordinates gives
$$|P-Q|^2=2-2(\cos u\cos v+\sin u\sin v).$$

**Rotate both points by $-v$.** Their distance is preserved and $Q$ moves to $(1,0)$. The squared distance is now $2-2\cos(u-v)$. Equating the two expressions gives
$$\cos(u-v)=\cos u\cos v+\sin u\sin v.$$

Replace $v$ with $-v$ and use the evenness of cosine and oddness of sine to obtain the sum formula.
""", 'What changes when both angles are shifted by −v? Compare coordinates and chord length.')

    revise('waves', 'What sets the period of a wave?', r"""
$$H(t)=m+A\sin(\omega t).$$
Treat $t$ as real and take $\omega>0$.

| Parameter | Meaning |
|---|---|
| $m$ | Middle level |
| $|A|$ | Amplitude |
| $\omega$ | Angle change per unit time |

The example starts with $m=12$, $A=3$, and $\omega=\pi/6$. A step of $T$ hours advances the angle by $\omega T$. Use the graph to compare a full turn at two frequencies.
""", 'Predict how doubling the angular frequency changes the cycle length. Then test the constant case.')

    by_key['waves']['after_visual'] = render(
        r"""**Justification.** When $A\ne0$, a period of $H$ induces a period of sine after scaling by $\omega$. A shift that preserves the sine value $1$ at $\pi/2$ must return to the top of the unit circle. The first positive shift that does this is $2\pi$, which preserves sine at every angle.
$$\omega T=2\pi,\qquad T=\frac{2\pi}{\omega}.$$
For $A=0$, the graph is constant. Every positive shift is a """ + term('period') + r""", so there is no smallest positive one."""
    )

    revise('coefficient', 'Which term can produce the requested power?', r"""
**Course-bank problem · Test 02, Question 1**

Find the coefficient of $x^{-4}$ in $\left(3x^2-x^{-3}\right)^8$, with $x\ne0$.

Let $k$ count factors contributing $-x^{-3}$. The remaining $8-k$ contribute $3x^2$. A term therefore has exponent
$$2(8-k)-3k=16-5k.$$
Choose $k$ by equating this with the target exponent. It must be an integer in $[0,8]$. The coefficient then comes from the factor choices, the copies of $3$, and the sign:
$$\binom{8}{k}3^{8-k}(-1)^k.$$

**Transfer.** Could $x^{-3}$ occur in this expansion?
""", 'Compare two choices of k. What happens to the exponent when one extra factor contributes −x⁻³?')

    revise('increment', 'Which part of a power change survives division by h?', r"""
In $(x+h)^n$, with $x,h\in\mathbb R$ and integer $n\ge1$, the term $x^n$ comes from choosing no factors of $h$. Choosing exactly one gives $nx^{n-1}h$. The remaining terms contain $h^2$ or a higher power.
$$(x+h)^n=x^n+nx^{n-1}h+\sum_{k=2}^{n}\binom nkx^{n-k}h^k.$$

Subtract $x^n$ and divide where $h\ne0$:
$$\frac{(x+h)^n-x^n}{h}=nx^{n-1}+\sum_{k=2}^{n}\binom nk x^{n-k}h^{k-1}.$$

The first term is independent of $h$, and each remaining term contains a positive power of $h$. For $n=1$ the sum is empty. As with the earlier quotient at $x=1$, the polynomial on the right extends the quotient to $0$, with value $nx^{n-1}$. The natural next question concerns the values **near** $0$.
""", 'Select h = 0 to compare the quotient and its polynomial extension.')

    revise('local', 'What does the position model tell us near t = 2?', r"""
$$s(2+h)-s(2)=(2+h)^2-4=4h+h^2,\qquad 2+h\ge0.$$

The model allows both observation times only when $2+h\ge0$. In the binomial expansion the two ways to choose one $h$ give $4h$, and choosing two gives $h^2$.

The linear prediction is $4h$. Its exact error, measured as the actual change minus the prediction, is $h^2$. For $h\ne0$,
$$\frac{s(2+h)-s(2)}{h}=4+h,\qquad 2+h\ge0.$$

The polynomial $4+h$ agrees wherever the quotient exists. As in the missing-point example, the algebra preserves the restriction $h\ne0$. The quotient differs from $4$ by $h$. **Lesson 2 asks how to express “approaches $4$ as $h$ approaches $0$” for all sufficiently small nonzero increments.**
""", 'Compare h = 0.1 and h = −0.1. Which quantity changes sign, and what happens at h = 0?')

    # Emphasise the statements students need while using the investigation.
    for key, label, tone, paragraph in [
        ('inverse', 'Inverse-function theorem', 'definition', 0),
        ('equality', 'Equality criterion', 'condition', -1),
        ('addition', 'Key step in the proof', 'reasoning', 1),
    ]:
        board = by_key[key]
        match = list(re.finditer(r'<p>.*?</p>', board['argument'], re.S))[paragraph]
        callout = f'<div class="core-callout reading-{tone}"><span class="reading-kind">{label}</span>{match.group()}</div>'
        board['argument'] = board['argument'][:match.start()] + callout + board['argument'][match.end():]

    by_key['inverse']['activity'] = {
        'title': 'Reconstruct a proof about injective compositions',
        'prompt': render(r"""
Let $f:A\to B$ and $g:B\to C$ both be injective. Prove that $g\circ f$ is injective. If you know only that $g\circ f$ is injective, which component must be injective?
"""),
        'hint': render(r"""
Start from $g(f(x_1))=g(f(x_2))$. Which function can you cancel first by injectivity? For the converse question, start from $f(x_1)=f(x_2)$.
"""),
        'solution': render(r"""
Injectivity of $g$ gives $f(x_1)=f(x_2)$, then injectivity of $f$ gives $x_1=x_2$. If $g\circ f$ is injective and $f(x_1)=f(x_2)$, apply $g$ to both sides and use injectivity of $g\circ f$ to recover $x_1=x_2$. So $f$ must be injective.

The outer map need only be injective on $f(A)$. For example, take $f:[0,\infty)\to\mathbb R$ to be $f(x)=x$ and $g:\mathbb R\to\mathbb R$ to be $g(y)=y^2$. The composition is injective, while $g(-1)=g(1)$.

**Check your proof:** Identify the domain of each equality and say exactly which injectivity assumption you used at each step.
""")
    }
    by_key['local']['activity'] = {
        'title': 'Recall and transfer',
        'prompt': render(r"""
1. The simplified expression $4+h$ gives a value at $h=0$. Which function has that value, and which function excludes the input?
2. Why does the equation $x^2=4$ fail to define a single inverse value on $\mathbb R$? Give a domain restriction and the resulting inverse rule.
3. Use the binomial theorem at $t=2$ for $s(t)=t^3$, $t\ge0$. What is the linear part of the change, and what remains in the average-velocity quotient?
"""),
        'hint': render(r"""
Check the denominator before cancellation, and the sign of the original input before choosing a root. In the cubic expansion, count choices of one, two, and three factors of $h$.
"""),
        'solution': render(r"""
1. The polynomial extension takes value $4$ at $h=0$. The original quotient excludes $0$ because its denominator is $h$.
2. Both $-2$ and $2$ are preimages. Restricting to $[0,\infty)$ gives $\sqrt y$ for $y\ge0$.
3. The exact change is $12h+6h^2+h^3$ for $2+h\ge0$. The linear part is $12h$ and the quotient is $12+6h+h^2$ for $h\ne0$. This gives the algebra needed to study the nearby values.
""")
    }
