"""Question-led reading sections drawn from the Lesson 1 content master."""

# Key, relevant source subsection, visible idea, and optional reading sections.
# A None marker starts at the beginning of that source subsection.
READING = {
    'average': ('1.1', 'From positions to a slope',
        r'Two times determine a secant slope. Compare several slopes before deciding what they suggest about $t=2$.',
        [(None, 'Calculate three average velocities', 'example'),
         ('**Think first.**', 'Which times belong to the model?', 'condition')]),
    'data': ('2.1', 'One input, one assigned output',
        r'The declared target is the codomain. The range is the part of that target reached by the assignment.',
        [(None, 'Write the range as a set', 'definition'),
         ('**Check your reasoning.**', 'Test the relation y² = x', 'condition')]),
    'representations': ('2.2', 'Read the input first',
        r'A vertical line fixes one input. Count its intersections with the plotted relation.',
        [(None, 'Why does the vertical-line test work?', 'reasoning'),
         ('A function can also be described', 'How much does a finite table determine?', 'example')]),
    'restrictions': ('2.3', 'Find the domain by intersecting conditions',
        r'Write one condition for each operation. Check the boundary values in the original expression.',
        [(None, 'Read the three real-domain rules', 'definition'),
         ('**Worked example.**', 'Check the included endpoint and the excluded pole', 'example')]),
    'equality': ('2.4', 'What cancellation gives',
        r'Factoring shows agreement for $x\ne1$. To add the missing input, specify the value of a new function there.',
        [(None, 'Follow the cancellation and compare domains', 'reasoning'),
         ('Thus $r$ is the **restriction**', 'Compare extensions that assign different values', 'example')]),
    'compose': ('3.1', 'Check the handoff between functions',
        r'The outer function must accept the inner output. Reversing the order changes which calculation comes first.',
        [(None, 'Justify the domain formula', 'definition'),
         ('**Worked comparison.**', 'Trace both orders through the square root', 'example')]),
    'outer': ('3.2', 'Two boundary values to compare',
        r'At $x=2$ the common inner value is $0$. At $x=\sqrt3$ it is $1$. What reaches the final operation in each case?',
        [(None, 'Derive all three domains', 'reasoning'),
         ('**Endpoint question.**', 'Explain the endpoint choices', 'condition')]),
    'inverse': ('3.3', 'Existence and uniqueness',
        r'Surjectivity supplies an input. Injectivity makes that input unique. The proof uses both facts to define the inverse.',
        [(None, 'Prove the inverse-function statement', 'reasoning'),
         ('3.4', 'Choose a branch and prove strict monotonicity is sufficient', 'example')]),
    'atlas': ('4.1', 'The exponent determines allowable inputs',
        r'A negative exponent excludes zero. For a root, the parity of its index determines whether negative inputs are allowed.',
        [(None, 'Compare the definitions and real domains', 'definition'),
         ('**Accepted result about real powers.**', 'Check the assumptions behind exponent laws', 'condition')]),
    'increments': ('4.2', 'Compare a difference and a factor',
        r'An affine function adds the same amount for a fixed step. An exponential multiplies by the same factor for that step.',
        [(None, 'Derive the change for each family', 'reasoning'),
         ('**Check the claim.**', 'Test a claim about which function is larger', 'condition')]),
    'exponent-log': ('4.3', 'Recover the exponent',
        r'When the base is admissible, the positive output determines exactly one real exponent. The logarithm names that exponent.',
        [(None, 'Find the input of an exponential model', 'example'),
         ('The inverse identities, with their domains', 'Check both inverse identities', 'condition')]),
    'log-laws': ('4.4', 'The inverse reads off the exponent',
        r'Multiplying, dividing, or taking a power changes the exponent. Applying the logarithm gives that changed exponent.',
        [('**Product law.**', 'Derive the product, quotient, and power laws', 'reasoning'),
         ('**Change of base.**', 'Derive the change-of-base formula', 'example')]),
    'identity-domains': ('4.4', 'Check existence before comparing outputs',
        r'If one side is undefined, examine the domain. If both exist, unequal outputs give a counterexample.',
        [('**Worked domain check.**', 'Apply the power law to a positive input', 'reasoning'),
         ('**Reasoning check.**', 'Separate a domain failure from a counterexample', 'condition')]),
    'circle': ('5.1', 'Angles are the inputs',
        r'On the unit circle, signed arc length equals the angle in radians. The point’s coordinates give the two function values.',
        [(None, 'Connect arc length, reflection, and periodicity', 'definition'),
         ('A few exact values', 'Derive the special-angle values from triangles', 'example'),
         ('The tangent function is', 'Explain the excluded tangent angles', 'condition')]),
    'addition': ('5.2', 'One length, two coordinate expressions',
        r'Rotation preserves the chord length and places one endpoint at $(1,0)$. This is the step that makes the two distance formulas useful.',
        [(None, 'Expand the squared distances', 'reasoning'),
         ('Replacing $v$ with $-v$ and using', 'Recover the cosine sum and the sine formulas', 'example')]),
    'derived': ('5.3', 'Start from the addition formulas',
        r'Use equal angles for double angles, then rearrange to reduce powers. A square root in a half-angle formula also requires a sign check.',
        [(None, 'Derive double angles, power reduction, and sums', 'reasoning'),
         ('**Misconception check.**', 'Choose the sign in a half-angle formula', 'condition')]),
    'waves': ('5.4', 'Convert an angle period into a time period',
        r'Divide one full turn by the angle change per unit time. For a constant wave, every positive time shift preserves the output.',
        [(None, 'Find the cycle length and range of the height model', 'example'),
         ('**Parameter connection.**', 'Separate the full wave from the observation interval', 'condition')]),
    'count': ('6.1', 'Count choices of factors',
        r'Each factor contributes either $U$ or $V$. Choosing the $k$ factors that supply $V$ determines a term of the same form.',
        [(None, 'Why is the coefficient a binomial coefficient?', 'reasoning'),
         ('**Small example.**', 'Count the choices in a cubic expansion', 'example')]),
    'coefficient': ('6.2', 'Select the exponent before the coefficient',
        r'Solve the exponent equation first. Only a whole number of available factors can give the requested term.',
        [(None, 'Reveal the worked coefficient and transfer solution', 'example')]),
    'increment': ('6.3', 'Identify the term with one factor of h',
        r'After subtracting the constant term and dividing by $h$, the term linear in $h$ becomes the constant term of the quotient.',
        [(None, 'Expand and divide for any positive integer power', 'reasoning'),
         ('**A deliberate misconception to challenge.**', 'Explain why the quotient still excludes zero', 'condition')]),
    'local': ('7', 'Compare the quotient with its nearby value',
        r'The exact velocity difference from $4$ is $h$ whenever the quotient exists. This difference gives us a concrete quantity to control in the next lesson.',
        [(None, 'Calculate the exact error at two step sizes', 'example'),
         ('**Closing explanation.**', 'Connect the motion model to the next lesson', 'reasoning')]),
}


# Supporting derivations can be opened within a reading panel.
SUPPORTING_STEPS = {
    ('inverse', 0): [('**Reason.**', 'Construct the inverse and check both directions')],
    ('inverse', 1): [('**Derivation.**', 'Why does the principal root give an absolute value?'),
                     ('**A useful sufficient condition.**', 'Prove that strict monotonicity gives injectivity')],
    ('circle', 0): [('A positive number $T$', 'Prove that the period is fundamental'),
                    ('The circle equation gives', 'Derive the identities from circle geometry')],
    ('derived', 0): [('Adding the sine addition', 'Derive the sum-to-product identities')],
    ('coefficient', 0): [('**Transfer question.**', 'Could the x⁻³ term occur?')],
}

def build_reading(key, parts, render):
    reference, title, lead, divisions = READING[key]
    source = parts[reference][1]
    if key == 'inverse':
        source = source.replace(
            r'$$f^{-1}(f(x))=x\quad(x\in D),' + '\n' + r'\qquad f(f^{-1}(y))=y\quad(y\in B).$$',
            r'$$\begin{gathered} f^{-1}(f(x))=x\quad(x\in D), \\ f(f^{-1}(y))=y\quad(y\in B). \end{gathered}$$',
        )
    if key == 'log-laws':
        source = source.split('**Worked domain check.**', 1)[0]
        statement_start = source.index('For another base')
        statement_end = source.index('**Product law.**', statement_start)
        statement = source[statement_start:statement_end]
        # Keep the statement and its hypotheses with the change-of-base proof.
        source = source.replace('**Change of base.**', '**Change of base.**\n\n' + statement)
    starts = []
    for marker, _, _ in divisions:
        if marker is None:
            starts.append(0)
        elif marker == '3.4':
            starts.append(len(source))
            source += parts[marker][1]
        else:
            starts.append(source.index(marker))
    panels = []
    for index, ((_, question, tone), start, stop) in enumerate(zip(divisions, starts, starts[1:] + [len(source)])):
        block = source[start:stop].strip().removesuffix('---').strip()
        if not block:
            raise ValueError(f'Empty explanation for {key}: {question}')
        steps = SUPPORTING_STEPS.get((key, index), [])
        boundaries = [block.index(marker) for marker, _ in steps]
        main = block[:boundaries[0]] if steps else block
        panel = {'title': question, 'tone': tone, 'html': render(main.strip())}
        if steps:
            panel['more'] = [
                {'title': step, 'html': render(block[begin:end].strip())}
                for (_, step), begin, end in zip(steps, boundaries, boundaries[1:] + [len(block)])
            ]
        panels.append(panel)
    return {'title': title, 'lead': render(lead), 'panels': panels}
