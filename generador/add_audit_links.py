# -*- coding: utf-8 -*-
import re,io,json,html,sys
def process(path):
    t=io.open(path,encoding="utf-8").read()
    anchor=t.find("window.PUBMED_DATA")
    if anchor<0: print("  sin PUBMED_DATA:",path); return 0
    s=t.find("[",anchor); i=s; depth=0; instr=False; esc=False
    while i<len(t):
        c=t[i]
        if instr:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': instr=False
        else:
            if c=='"': instr=True
            elif c=='[': depth+=1
            elif c==']':
                depth-=1
                if depth==0: break
        i+=1
    data=json.loads(t[s:i+1])
    by={}
    for a in data:
        title=(a.get("t") or "").strip()
        doi=(a.get("d") or "").strip(); pmid=(a.get("p") or a.get("i") or "").strip()
        link="https://doi.org/"+doi if doi else ("https://pubmed.ncbi.nlm.nih.gov/"+pmid+"/" if pmid else "")
        if title and link: by[title]=link
    cnt=[0]
    def repl(mt):
        inner=mt.group(1)
        if 'class="artlink"' in inner: return mt.group(0)
        m2=re.match(r'(.*?)(<span|$)', inner, re.S)
        lead=m2.group(1); raw=html.unescape(lead).strip()
        link=by.get(raw)
        if not link: return mt.group(0)
        rest=inner[len(lead):]; cnt[0]+=1
        return '<td class="art"><a class="artlink" href="%s" target="_blank" rel="noopener">%s</a>%s%s</td>' % (link, lead.rstrip(), (" " if rest.strip() else ""), rest.lstrip())
    t=re.sub(r'<td class="art">(.*?)</td>', repl, t, flags=re.S)
    if 'a.artlink' not in t:
        t=t.replace('</style>', '.art a.artlink{color:inherit;text-decoration:none;} .art a.artlink:hover{color:#0f9aa0;text-decoration:underline;text-underline-offset:2px;}</style>',1)
    io.open(path,"w",encoding="utf-8").write(t)
    return cnt[0]
if __name__=="__main__":
    for p in sys.argv[1:]:
        print(f"  {process(p):4d} enlaces  ←  {p.split('/')[-1]}")
