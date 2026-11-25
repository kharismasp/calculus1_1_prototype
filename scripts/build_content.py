from pathlib import Path
import json,re,subprocess,html,shutil

ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'source/content-master.md').read_text()
DIST=ROOT/'dist'

def render(s):
    r=subprocess.run(['pandoc','--from=markdown+tex_math_dollars','--to=html5','--mathml','--wrap=none'],input=s,text=True,capture_output=True,check=True)
    if 'Could not convert' in r.stderr: raise RuntimeError(r.stderr)
    result=re.sub(r'(<math\b[^>]*display="block"[^>]*>.*?</math>)',r'<div class="math-display">\1</div>',r.stdout,flags=re.S)
    return result.replace('in Section 4','in <a href="#/families">Elementary families</a>').replace('in Section 6','in <a href="#/binomial">Binomial structure</a>')

def widget(name):return f'\n\n<div class="lab-mount" data-lab="{name}"></div>\n\n'

inserts={
'## 1.2 Where the course is going':widget('motion')+'## 1.2 Where the course is going',
'The calculation establishes agreement at every input':widget('hole')+'The calculation establishes agreement at every input',
'**Explore.** Follow an input through the two functions, one operation at a time. Then reverse the order. Which inputs survive both stages?':widget('composition'),
'## 3.3 When can a function be reversed?':widget('domains')+'## 3.3 When can a function be reversed?',
'**Connection to later calculus.**':widget('inverse')+'**Connection to later calculus.**',
'## 4.3 Logarithms recover an exponent':widget('families')+'## 4.3 Logarithms recover an exponent',
'**Checkpoint — what carries forward?** Recognizing the operation':widget('identities')+'**Checkpoint — what carries forward?** Recognizing the operation',
'## 5.2 A geometric derivation':widget('circle')+'## 5.2 A geometric derivation',
'**What the derivation used.**':widget('chord')+'**What the derivation used.**',
'**Checkpoint — what carries forward?** The unit circle':widget('waves')+'**Checkpoint — what carries forward?** The unit circle',
'## 6.3 Why this algebra will matter':widget('binomial')+'## 6.3 Why this algebra will matter',
'**Closing explanation.**':widget('return-motion')+'**Closing explanation.**',
}
for old,new in inserts.items():
    if source.count(old)!=1:raise ValueError(f'Expected one content anchor: {old}')
    source=source.replace(old,new)

sections={}
for m in re.finditer(r'^# (\d+)\. (.+)\n',source,re.M):
    nxt=re.search(r'^# \d+\. ',source[m.end():],re.M)
    end=m.end()+nxt.start() if nxt else len(source)
    sections[int(m.group(1))]=(m.group(2),source[m.end():end].strip())

meta=[
('motion',1,'A question of motion','Begin with a question','Position gives us a place to start. Change gives us a reason to look closer.'),
('functions',2,'Functions & domains','Specify the relationship','The allowed inputs are part of the mathematics. Keep them with you as the formula changes.'),
('composition',3,'Compose & reverse','Follow the input','An output becomes a new input. Reversing the journey asks a different question.'),
('families',4,'Recognize the structure','Elementary families','Equal steps can produce equal additions, changing differences, or equal factors.'),
('trigonometry',5,'Circle & waves','Geometry becomes a function','One moving point connects angles, coordinates, graphs, and identities.'),
('binomial',6,'Binomial structure','Choose the term you need','A coefficient counts choices. The same structure will reveal the part linear in a small change.'),
('return',7,'Back to the motion','Connect the ideas','The original question now has a domain, an exact algebraic answer, and a carefully stated next step.'),
('reference',10,'Identity library','Keep useful structure close','Each identity has a reason and a domain. Return here when a problem calls for it.'),
('sources',11,'Sources & foundations','What supports the lesson','Definitions, derivations, accepted results, and the references behind them.'),
]
pages={}
proof_phrases=['Derive the logarithm laws','A geometric derivation','Recover useful identities']
for key,num,title,eyebrow,desc in meta:
    body=sections[num][1]
    chunks=re.split(r'(?=^## )',body,flags=re.M)
    parts=[]
    for chunk in chunks:
        h=re.match(r'^## (?:\d+\.\d+ )?(.+)\n',chunk)
        if h:
            heading=h.group(1)
            inner=render(chunk[h.end():].strip())
            if any(p.lower() in heading.lower() for p in proof_phrases):
                parts.append(f'<details class="derivation"><summary><span>{html.escape(heading)}</span><small>Derivation</small></summary><div class="derivation-body">{inner}</div></details>')
            else:
                sid=re.sub(r'[^a-z0-9]+','-',heading.lower()).strip('-')
                parts.append(f'<section class="text-section" id="{sid}"><h2>{html.escape(heading)}</h2>{inner}</section>')
        else:
            parts.append(render(chunk))
    content=''.join(parts)
    content=re.sub(r'<p><strong>(Definition\.|Theorem\.|Finite binomial theorem\.|Inverse-function statement\.|Equality criterion\.)</strong>',r'<p class="statement"><strong>\1</strong>',content)
    content=content.replace('<table>','<div class="table-scroll" tabindex="0"><table>').replace('</table>','</table></div>')
    content=content.replace('<hr />','')
    pages[key]={'title':title,'eyebrow':eyebrow,'description':desc,'html':content}

practice=sections[8][1]
problems=[]
for m in re.finditer(r'^## ((?:Problem|Further exploration) (\d+)\. (.+))\n',practice,re.M):
    nxt=re.search(r'^## ',practice[m.end():],re.M)
    end=m.end()+nxt.start() if nxt else len(practice)
    body=practice[m.end():end].strip()
    # Each solution can contain several paragraphs and display equations.
    blocks=re.split(r'(?=\*\*(?:Hint 1|Hint 2|Solution|Purpose)\.\*\*)',body)
    prompt=blocks[0].strip();bits={}
    for bit in blocks[1:]:
        k=re.match(r'\*\*(Hint 1|Hint 2|Solution|Purpose)\.\*\*\s*',bit)
        bits[k.group(1)]=render(bit[k.end():].strip())
    if set(bits)!={'Hint 1','Hint 2','Solution','Purpose'}:raise ValueError('Incomplete exercise '+m.group(2))
    n=int(m.group(2))
    topic={1:'Interpretation',2:'Domains',3:'Domains',4:'Domains',5:'Inverses',6:'Models',7:'Domains',8:'Models',9:'Algebra',10:'Algebra',11:'Further exploration',12:'Further exploration'}[n]
    problems.append({'number':n,'title':m.group(3),'topic':topic,'prompt':render(prompt),'hints':[bits['Hint 1'],bits['Hint 2']],'solution':bits['Solution'],'purpose':bits['Purpose']})
assert len(problems)==12
outcomes=re.search(r'### Learning outcomes\n(.*?)\n### How to use',source,re.S).group(1)
pages['overview']={'outcomes':render(outcomes),'roadmap':render(sections[1][1].split('## 1.2 Where the course is going')[1])}
(DIST/'content.json').write_text(json.dumps({'pages':pages,'problems':problems},ensure_ascii=False))
notes=source[:source.index('# 9. Interactive learning')]+source[source.index('# 10. Trigonometric'):source.index('# 12. Final editorial')]
notes=re.sub(r'<div class="lab-mount".*?</div>','',notes)
(DIST/'assets/lesson-notes.md').write_text(notes)
print(f'Generated {len(pages)} chapters and {len(problems)} complete exercises; {len(re.findall(r"<math",json.dumps(pages)))} mathematical expressions.')
