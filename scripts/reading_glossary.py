"""First-use glossary reminders for selected passages of the detailed reading."""
import re
from html.parser import HTMLParser

# Locations are (board key, panel index, optional step index).
# Select terms that carry a condition or an idea needed in that passage.
REMINDERS = {
    ('average', 0): [('average-velocity', 'average velocity'), ('limit', 'limits')],
    ('average', 1): [('domain', 'domain')],
    ('data', 0): [('codomain', 'codomain'), ('range', 'range')],
    ('data', 1): [('principal-root', 'principal, nonnegative square root')],
    ('representations', 0): [('domain', 'domain')],
    ('restrictions', 1): [('domain', 'domain')],
    ('equality', 0): [('codomain', 'codomain')],
    ('equality', 1): [('restriction', 'restriction'), ('extension', 'extension')],
    ('compose', 0): [('composition', 'composition')],
    ('compose', 1): [('domain', 'domain')],
    ('outer', 1): [('principal-root', 'square root')],
    ('inverse', 0): [('injective', 'injective'), ('bijective', 'bijective')],
    ('inverse', 0, 0): [('surjective', 'surjectivity'), ('injective', 'injectivity'), ('range', 'range')],
    ('inverse', 1): [('inverse', 'inverse')],
    ('inverse', 1, 0): [('principal-root', 'principal square root')],
    ('inverse', 1, 1): [('strict-monotonicity', 'strictly monotone'), ('injective', 'injective')],
    ('exponent-log', 0): [('bijective', 'bijection')],
    ('log-laws', 0): [('inverse', 'inverse')],
    ('identity-domains', 1): [('domain', 'domain')],
    ('circle', 0): [('radian-measure', 'radian measure'), ('range', 'range')],
    ('circle', 0, 0): [('period', 'fundamental period')],
    ('derived', 0, 0): [('angle-addition', 'sine addition and subtraction formulas')],
    ('waves', 0): [('range', 'range')],
    ('waves', 1): [('period', 'fundamental period')],
    ('increment', 1): [('limit', 'limit')],
    ('local', 0): [('average-velocity', 'average-velocity quotient'), ('limit', 'limit')],
}


class ReadingLinks(HTMLParser):
    """Collect edits in text nodes while preserving the rendered MathML and HTML."""
    protected = {'math', 'a', 'button', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5'}

    def __init__(self, markup, entries, term):
        super().__init__(convert_charrefs=False)
        self.markup = markup
        self.term = term
        self.protected_depth = 0
        self.matches = set()
        self.edits = []
        self.entries = [
            (key, re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE))
            for key, phrase in entries
        ]
        self.line_offsets = [0] + [match.end() for match in re.finditer('\n', markup)]

    def handle_starttag(self, tag, attrs):
        if tag in self.protected:
            self.protected_depth += 1

    def handle_endtag(self, tag):
        if tag in self.protected:
            self.protected_depth -= 1

    def handle_data(self, data):
        if self.protected_depth:
            return
        line, column = self.getpos()
        offset = self.line_offsets[line - 1] + column
        for key, pattern in self.entries:
            if key in self.matches:
                continue
            match = pattern.search(data)
            if match:
                self.matches.add(key)
                self.edits.append((
                    offset + match.start(), offset + match.end(), self.term(key, match.group())
                ))

    def result(self):
        self.feed(self.markup)
        self.close()
        remaining = {key for key, _ in self.entries} - self.matches
        if remaining:
            raise ValueError(f'Glossary terms absent from selected passage: {", ".join(sorted(remaining))}')
        result = self.markup
        for start, end, link in reversed(sorted(self.edits)):
            result = result[:start] + link + result[end:]
        return result


def link_reading(boards, glossary, term):
    by_key = {board['key']: board for group in boards.values() for board in group}
    for (board, panel, *step), entries in REMINDERS.items():
        target = by_key[board]['reading']['panels'][panel]
        if step:
            target = target['more'][step[0]]
        for key, _ in entries:
            if key not in glossary:
                raise ValueError(f'{board}: unknown glossary term {key}')
        try:
            target['html'] = ReadingLinks(target['html'], entries, term).result()
        except ValueError as error:
            raise ValueError(f'{board}, panel {panel}, step {step}: {error}') from error
