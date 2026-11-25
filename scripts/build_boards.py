from pathlib import Path
import json,re,subprocess,html,sys

sys.dont_write_bytecode = True
from board_refinements import refine_boards
from reading_sections import build_reading
from reading_glossary import link_reading
ROOT=Path(__file__).resolve().parents[1]
master=(ROOT/'source/content-master.md').read_text()

def render(text):
    r=subprocess.run(['pandoc','-f','markdown+tex_math_dollars','-t','html5','--mathml','--wrap=none'],input=text,text=True,capture_output=True,check=True)
    if 'Could not convert' in r.stderr:raise RuntimeError(r.stderr)
    s=re.sub(r"""(<math\b[^>]*display="block"[^>]*>.*?</math>)""",r"""<div class="math-display">\1</div>""",r.stdout,flags=re.S)
    return s.replace('<table>','<div class="table-scroll"><table>').replace('</table>','</table></div>')

def term(key,label=None):return f'<button class="term-link" data-concept="{key}" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="concept-popup">{label or key}</button>'
def card(label,text,tone='definition'):
    return f'<div class="argument-card {tone}"><span class="card-label">{html.escape(label)}</span>{render(text)}</div>'
def note(text):return render(text)
def table(text):return render(text)
def proofsteps(items):return '<ol class="proof-steps">'+''.join('<li>'+render(x)+'</li>' for x in items)+'</ol>'
parts={}
for m in re.finditer(r"""^## (\d+\.\d+) (.+)\n""",master,re.M):
    end=re.search(r"""^#{1,2} """,master[m.end():],re.M)
    body=master[m.end():m.end()+end.start() if end else len(master)]
    parts[m.group(1)]=(m.group(2),body)
start=master.index('# 7. Return to the opening motion');end=master.index('# 8. Practice:')
parts['7']=('Return to the opening motion',master[start:end].split('\n',1)[1])

boards={}
def add(page,key,title,arg,visual,prompt=''):
    reading = build_reading(key, parts, render)
    boards.setdefault(page, []).append({
        'key': key, 'title': title, 'argument': arg, 'visual': visual,
        'reading': reading, 'prompt': prompt
    })

add('motion','average','Position and average velocity',
 card('Model',r"""$$s(t)=t^2,\qquad t\ge0.$$
Time is measured in seconds; position in metres.""")+
 card('Average velocity',r"""$$\frac{s(2+h)-s(2)}h,\qquad h>0.$$
**Shorten the interval.** Compare the change in position with the interval length.""",'result')+
 note('At $h=0$, the original quotient is **undefined**. A '+term('limit')+' will describe its nearby behaviour.'),
 'motion','What can average velocities tell us about velocity at t = 2?')

add('functions','data','Domain, codomain, range',
 card('Definition','A '+term('function')+' $f:D\\to B$ assigns **exactly one output** $f(x)\\in B$ to each $x\\in D$.')+
 table('| Information | Meaning |\n|---|---|\n| '+term('domain','Domain $D$')+' | Allowed inputs |\n| '+term('codomain','Codomain $B$')+' | Declared target |\n| '+term('range','Range $f(D)$')+' | Outputs actually reached |')+
 card('Example',r"""For $f:\mathbb R\to\mathbb R$, $f(x)=x^2$:
$$f(\mathbb R)=[0,\infty).$$
The range can be smaller than the codomain.""",'example'),
 'mapping','Select an input. Which target values are reached?')

add('functions','representations','Graphs and recorded values',
 card('Graph test','A graph represents a function of $x$ when **each allowed input has one output**.')+
 table('| Relation | Output at a typical input |\n|---|---|\n| $x^2+y^2=1$ | Usually two $y$-values |\n| $y=\\sqrt{1-x^2}$ | One nonnegative value |')+
 card('Data and models','A finite table specifies only its listed inputs. **Matching the table does not prove a formula between them.**','caution'),
 'representations','Compare a relation with a function, then compare two models matching the same table.')

add('functions','restrictions','Real-domain conditions',
 table('| Operation | Required condition |\n|---|---|\n| $1/u$ | $u\\ne0$ |\n| $\\sqrt u$ | $u\\ge0$ |\n| $\\ln u$ | $u>0$ |')+
 card('Worked example',r"""$$F(x)=\frac{\sqrt{x+1}}{x-2}.$$
Both $x\ge-1$ and $x\ne2$ must hold.""",'example')+
 card('Domain',r"""$$[-1,2)\cup(2,\infty).$$
Include $-1$: $\sqrt0$ exists. Exclude $2$: the denominator vanishes.""",'result'),
 'restrictions','Check each operation, intersect its conditions, then inspect the endpoints.')

add('functions','equality','Equality, restriction, extension',
 card('Two functions',r"""$$r(x)=\frac{x^2-1}{x-1},\quad x\ne1,$$
$$\ell(x)=x+1,\quad x\in\mathbb R.$$""")+
 card('What cancellation proves',r"""$$r(x)=\ell(x)\quad\text{for }x\ne1.$$
**The original input restriction remains.**""",'result')+
 note('The quotient is a '+term('restriction')+' of the line. Assigning a new value at $1$ defines an '+term('extension')+'.')+
 card('Equality criterion','With the same codomain: **same domain + same value at every input**.','caution'),
 'hole','Cancel the factor. Then inspect the missing input.')

add('composition','compose','Composition and its domain',
 card('Composition','Apply the **inner function first**:\n\n$$(f\\circ g)(x)=f(g(x)).$$')+
 card('Domain condition',r"""$$x\in\operatorname{dom}g,$$
$$g(x)\in\operatorname{dom}f.$$""",'result')+
 table('| Order | Formula | Domain |\n|---|---|---|\n| $f\\circ g$ | $\\sqrt{1-x^2}$ | $[-1,1]$ |\n| $g\\circ f$ | $1-x$ | $[0,\\infty)$ |')+
 note('Here $f(u)=\\sqrt u$ and $g(x)=1-x^2$. **Simplification does not enlarge the original domain.**'),
 'composition','Reverse the order and trace the input through both operations.')

add('composition','outer','One inner expression, different domains',
 table('| Function | Condition | Domain |\n|---|---|---|\n| $\\sqrt{4-x^2}$ | $4-x^2\\ge0$ | $[-2,2]$ |\n| $\\ln(4-x^2)$ | $4-x^2>0$ | $(-2,2)$ |')+
 card('A nested condition',r"""$$\sqrt{\ln(4-x^2)}$$
needs $\ln(4-x^2)\ge0$, hence $4-x^2\ge1$.
$$\operatorname{dom}=[-\sqrt3,\sqrt3].$$""",'example')+
 note('The '+term('principal-root','principal square root')+' accepts zero. The logarithm requires a **strictly positive input**.'),
 'domains','Choose the restriction before choosing the interval.')

add('composition','inverse','Inverse functions and branches',
 card('Inverse on the range','An '+term('injective')+' function can be reversed on its '+term('range')+'. An inverse on its entire codomain requires '+term('bijective','bijectivity')+'.')+
 card('Two inverse identities',r"""For a bijection $f:D\to B$:
$$f^{-1}(f(x))=x\quad(x\in D),$$
$$f(f^{-1}(y))=y\quad(y\in B).$$""",'result')+
 table('| Domain for $x^2$ | Inverse on $[0,\\infty)$ |\n|---|---|\n| $[0,\\infty)$ | $\\sqrt y$ |\n| $(-\\infty,0]$ | $-\\sqrt y$ |')+
 note('For arbitrary real $x$, **$\\sqrt{x^2}=|x|$**. A '+term('strict-monotonicity','strictly monotone')+' function is injective.'),
 'inverse','Which domain permits unique recovery of every input?')

add('families','atlas','Polynomial, rational, and power functions',
 table('| Family | Structure |\n|---|---|\n| Polynomial | Finite sum of nonnegative integer powers |\n| Rational | $P(x)/Q(x)$, where $Q(x)\\ne0$ |\n| Power | $x^\\alpha$ with a fixed exponent |')+
 card('Classification',r"""$$x+x^{-2}=\frac{x^3+1}{x^2},\quad x\ne0.$$
This is **rational, not polynomial**.""",'example')+
 card('Real powers','The exponent affects the domain. Even roots, odd roots, and negative powers require different checks. General real exponents use $x>0$ unless an extension is specified.','caution'),
 'atlas','Compare the graphs with their exact domain conditions.')

add('families','increments','Equal increments: addition or multiplication?',
 table('| Function | What a step $h$ does |\n|---|---|\n| $L(x)=3x+2$ | $L(x+h)-L(x)=3h$ |\n| $P(x)=x^2$ | $P(x+h)-P(x)=2xh+h^2$ |\n| $E(x)=2^x$ | $E(x+h)=2^hE(x)$ |')+
 card('Distinction','An affine function has a **fixed additive change** for a fixed input step. An exponential has a **fixed multiplicative factor**.','result')+
 note('For a power function, the change generally depends on the **starting input**.'),
 'families','Move the starting input while keeping the step length fixed.')

add('families','exponent-log','Exponential and logarithmic functions',
 card('Inverse relationship',r"""For $b>0$, $b\ne1$:
$$\log_b y=x\iff b^x=y.$$""")+
 table('| Function | Domain | Range |\n|---|---|---|\n| $b^x$ | $\\mathbb R$ | $(0,\\infty)$ |\n| $\\log_b x$ | $(0,\\infty)$ | $\\mathbb R$ |')+
 card('Identities with their domains',r"""$$\log_b(b^x)=x,\quad x\in\mathbb R,$$
$$b^{\log_b y}=y,\quad y>0.$$""",'result')+
 note('The '+term('inverse','inverse graph')+' interchanges input and output. Here $\\ln=\\log_e$.'),
 'explog','Observe the reflected point, then switch the base.')

add('families','log-laws','Why logarithm laws hold',
 card('Assumptions',r"""$$u,v>0,\quad b>0,\quad b\ne1,\quad r\in\mathbb R.$$""")+
 table('| Operation | Logarithm law |\n|---|---|\n| Product | $\\log_b(uv)=\\log_bu+\\log_bv$ |\n| Quotient | $\\log_b(u/v)=\\log_bu-\\log_bv$ |\n| Power | $\\log_b(u^r)=r\\log_bu$ |')+
 card('Use later','Products become sums; powers become factors. This is the structure used in **logarithmic differentiation**.','connection'),
 'log-proof','The product law follows from exponent addition and the inverse relationship.')

add('families','identity-domains','An identity includes its domain',
 table('| Claim | Required correction |\n|---|---|\n| $\\sqrt{x^2}=x$ | Valid for $x\\ge0$; generally $|x|$ |\n| $\\ln(x^2)=2\\ln x$ | Both sides exist for $x>0$ |\n| $\\ln(x^2)=2\\ln|x|$ | Valid for $x\\ne0$ |')+
 card('Counterexamples','To disprove an equality numerically, use an input where **both sides exist**. An undefined side instead identifies a domain failure.','caution')+
 note('There is no general logarithm sum law: at $u=v=1$, $\\ln(u+v)=\\ln2\\ne0=\\ln u+\\ln v$.'),
 'identities','Distinguish an unequal pair of values from an undefined expression.')

add('trigonometry','circle','Radians and coordinates',
 card('Radian measure',r"""$$\theta=\frac{s}{r},\qquad r>0.$$
On the unit circle, the signed arc length is $s=\theta$.""")+
 card('Coordinate functions',r"""$$P(\theta)=(\cos\theta,\sin\theta).$$
$$\cos^2\theta+\sin^2\theta=1.$$""",'result')+
 table('| Reflection | Consequence |\n|---|---|\n| $\\theta\\mapsto-\\theta$ | Cosine unchanged; sine changes sign |\n| $\\theta\\mapsto\\theta+2\\pi$ | Both coordinates repeat |')+
 note('**$\\tan\\theta$ is undefined when $\\cos\\theta=0$.** Its domain excludes $\\pi/2+k\\pi$, $k\\in\\mathbb Z$.'),
 'circle','Move the point or choose an exact angle. Reflect it across the horizontal axis.')

add('trigonometry','addition','Derive the addition formulas',
 card('Two points',r"""$$P=(\cos u,\sin u),$$
$$Q=(\cos v,\sin v).$$""")+
 proofsteps([r"""Calculate $|P-Q|^2$ using coordinates.""",r"""Rotate both points by $-v$. **Distance is preserved.**""",r"""Equate the two expressions for the squared distance."""])+
 card('Result',r"""$$\cos(u-v)=\cos u\cos v+\sin u\sin v.$$""",'result'),
 'chord','Rotate the pair of points while preserving the chord.')

add('trigonometry','derived','Derive related identities',
 card('Starting point','Use the '+term('angle-addition','addition formulas')+' and $\\sin^2x+\\cos^2x=1$.')+
 table('| Choice | Algebraic consequence |\n|---|---|\n| Set $v=u$ | Double-angle identities |\n| Rearrange $\\cos2u$ | Power-reduction identities |\n| Add sine formulas | Sum-to-product identities |')+
 card('Half-angle sign',r"""$$\left|\sin\frac\theta2\right|=\sqrt{\frac{1-\cos\theta}{2}}.$$
Removing the absolute value requires a **sign check**.""",'caution'),
 'identity-proof','Select an identity and follow its derivation. The full reference remains available.')

add('trigonometry','waves','Periodic models',
 card('Model',r"""$$H(t)=m+A\sin(\omega t),\quad \omega>0.$$""")+
 table('| Parameter | Meaning |\n|---|---|\n| $m$ | Middle level |\n| $|A|$ | Amplitude |\n| $\\omega$ | Rate of change of the input angle |')+
 card('Fundamental period',r"""For $A\ne0$:
$$\omega T=2\pi\implies T=\frac{2\pi}{\omega}.$$""",'result')+
 note('If $A=0$, the function is constant: it has **no smallest positive period**. '+term('period','Period reminder')+'.'),
 'waves','Change one parameter and inspect what is preserved.')

add('binomial','count','Why binomial coefficients count choices',
 card('Finite binomial theorem',r"""For an integer $n\ge0$:
$$(U+V)^n=\sum_{k=0}^{n}\binom nkU^{n-k}V^k.$$""")+
 proofsteps(['Each factor contributes **one** of $U,V$.','Choose the $k$ factors that contribute $V$.',r"""There are $\binom nk=\frac{n!}{k!(n-k)!}$ choices."""])+
 note('The visual uses **$n=4$**. Distinct choices can produce the same algebraic term.'),
 'choices','Select factors and compare all choices with the same number of V terms.')

add('binomial','coefficient','Find one coefficient',
 card('Course-bank problem',r"""Find the coefficient of $x^{-4}$ in
$$\left(3x^2-x^{-3}\right)^8.$$""",'example')+
 table('| Track | General term |\n|---|---|\n| Exponent | $2(8-k)-3k=16-5k$ |\n| Coefficient | $\\binom8k3^{8-k}(-1)^k$ |')+
 card('Select the index',r"""$$16-5k=-4\implies k=4.$$
Then $\binom{8}{4}3^4=5670$.""",'result')+
 note('An admissible index must be an **integer from $0$ to $8$**.'),
 'binomial','Select the exponent before calculating the coefficient.')

add('binomial','increment','The term linear in a small change',
 card('Separate by powers of h',r"""For an integer $n\ge1$:
$$(x+h)^n=x^n+nx^{n-1}h+\text{higher powers of }h.$$""")+
 proofsteps([r"""Subtract $x^n$.""",r"""Divide by $h$, retaining **$h\ne0$**.""",r"""The constant term of the resulting polynomial in $h$ is $nx^{n-1}$."""])+
 card('What is established','This is **exact algebra**. A limit and the derivative definition will justify the limiting step later.','caution'),
 'increments','Compare the quotient with its polynomial extension at the excluded input.')

add('return','local','Exact change and linear approximation',
 card('Return to the motion model',r"""$$s(2+h)-s(2)=4h+h^2.$$""")+
 table('| Quantity | Exact expression |\n|---|---|\n| Linear prediction | $4h$ |\n| Remaining error | $h^2$ |\n| Average velocity | $4+h$, for $h\\ne0$ |')+
 card('Domain still matters',r"""The times must satisfy $2+h\ge0$. The original average-velocity quotient excludes **$h=0$**.""",'caution')+
 note('**Question for Lesson 2:** Why does $4$ describe the quotient’s behaviour near $h=0$?'),
 'return-motion','Inspect the exact error while the interval becomes shorter.')

glossary={
'angle-addition':('Angle addition',r"""On the unit circle, $\cos(u+v)=\cos u\cos v-\sin u\sin v$ and $\sin(u+v)=\sin u\cos v+\cos u\sin v$. The cosine difference formula follows by comparing the same chord before and after a rotation.""",'trigonometry','addition'),
'average-velocity':('Average velocity',r"""For position $s$ at two distinct times $t_1,t_2$, the average velocity is $\bigl(s(t_2)-s(t_1)\bigr)/(t_2-t_1)$. This is the slope of the secant through the two position points.""",'motion','average'),
'radian-measure':('Radian measure',r"""On a circle of radius $r>0$, the angle in radians is the signed arc length divided by $r$. One full counterclockwise turn is $2\pi$ radians.""",'trigonometry','circle'),
'function':('Function',r"""A map $f:D\to B$ assigns exactly one output in $B$ to each input in $D$. Different inputs may share an output.""",'functions','data'),
'domain':('Domain',r"""The set of inputs for which the function is declared. For $\sqrt x$, the natural real domain is $[0,\infty)$.""",'functions','restrictions'),
'codomain':('Codomain',r"""The declared target set $B$ in $f:D\to B$. A function need not reach every element of $B$.""",'functions','data'),
'range':('Range',r"""The set of outputs actually reached: $f(D)=\{f(x):x\in D\}$. It is a subset of the codomain.""",'functions','data'),
'restriction':('Restriction',r"""Keep a function’s existing values but allow a smaller input set. The quotient $(x^2-1)/(x-1)$ is the line $x+1$ restricted to $x\ne1$.""",'functions','equality'),
'extension':('Extension',r"""Enlarge the domain while preserving every original output. Assigning a value at a missing input is an additional definition.""",'functions','equality'),
'composition':('Composition',r"""$(f\circ g)(x)=f(g(x))$. The inner output must exist and belong to the outer function’s domain.""",'composition','compose'),
'injective':('Injective / one-to-one',r"""$f(x_1)=f(x_2)$ implies $x_1=x_2$. Equivalently, distinct allowed inputs produce distinct outputs.""",'composition','inverse'),
'surjective':('Surjective',r"""Every element of the declared codomain is reached. This property depends on the chosen codomain.""",'composition','inverse'),
'bijective':('Bijective',r"""Both injective and surjective. Each element of the codomain then has exactly one preimage.""",'composition','inverse'),
'inverse':('Inverse function',r"""$f^{-1}(y)=x$ means $f(x)=y$, with unique recovery on the specified sets. Its graph reflects the original across $y=x$.""",'composition','inverse'),
'principal-root':('Principal square root',r"""For $u\ge0$, $\sqrt u$ is the nonnegative number whose square is $u$. Thus $\sqrt{x^2}=|x|$.""",'composition','inverse'),
'strict-monotonicity':('Strict monotonicity',r"""If $x_1<x_2$, a strictly increasing function satisfies $f(x_1)<f(x_2)$. A strictly decreasing function reverses that inequality. Both are injective.""",'composition','inverse'),
'period':('Period and fundamental period',r"""A positive $T$ is a period if $f(x+T)=f(x)$ for every input of the function on $\mathbb R$. A fundamental period is the smallest such positive $T$, if one exists.""",'trigonometry','waves'),
'limit':('Limit: the next lesson',r"""A limit describes nearby values as the input approaches a point. The function’s value at that point is a separate question. Lesson 2 gives the precise definition.""",'return','local'),
}
g={k:{'title':v[0],'html':render(v[1]),'page':v[2],'topic':v[3]} for k,v in glossary.items()}
refine_boards(boards, render, term)
link_reading(boards, glossary, term)
(ROOT/'dist/boards.json').write_text(json.dumps({'boards': boards, 'glossary': g}, ensure_ascii=False))
print('Built',sum(len(x) for x in boards.values()),'topic boards and',len(g),'definition reminders.')
