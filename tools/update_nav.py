from __future__ import annotations
import re,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent
S={".git",".github","_site","_site_test","tools","node_modules","__pycache__"}
M=[("Portfolio home","index.html"),("Secure Software Development","modules/secure-software-development/index.html"),("Object Oriented Programming","modules/object-oriented-programming/index.html"),("Security Risk Management","modules/security-risk-management/index.html"),("Software Engineering Project Management","modules/software-engineering-project-management/index.html"),("Research Methods &amp; Professional Practice","modules/research-methods-and-professional-practice/index.html")]
U={"secure-software-development":[("Unit 1","modules/secure-software-development/unit-1/index.html"),("Unit 2","modules/secure-software-development/unit-2/index.html"),("Unit 3","modules/secure-software-development/unit-3/index.html"),("Unit 4","modules/secure-software-development/unit-4/index.html"),("Unit 5","modules/secure-software-development/unit-5/index.html"),("Unit 6","modules/secure-software-development/unit-6/index.html"),("Unit 7","modules/secure-software-development/unit-7/index.html"),("Unit 8","modules/secure-software-development/unit-8/index.html"),("Unit 9","modules/secure-software-development/unit-9/index.html"),("Unit 10","modules/secure-software-development/unit-10/index.html"),("Unit 11","modules/secure-software-development/unit-11/index.html"),("Unit 12","modules/secure-software-development/unit-12/index.html")],"object-oriented-programming":[],"security-risk-management":[],"software-engineering-project-management":[],"research-methods-and-professional-practice":[]}
UA={}
def lc(x):
 if x=="index.html":return(None,None)
 if x.startswith("modules/"):
  q=x.split("/")
  if len(q)>=4 and q[2].startswith("unit-"):return(q[1],q[2])
  if len(q)>=2:return(q[1],None)
 return(None,None)
A=[("Assessed work",[("Learning outcomes","docs/learning-outcomes.html"),("System overview","docs/system-overview.html"),("Threat model","docs/threat-model.html"),("Risk register","docs/risk-assessment.html"),("Secure design","docs/secure-design.html"),("Implementation","docs/implementation.html"),("Security testing","docs/security-testing.html"),("Critical evaluation","docs/critical-evaluation.html"),("References","docs/references.html")]),("Collaboration",[("Discussion 1","discussions/discussion-summary-1.html"),("Discussion 2","discussions/discussion-summary-2.html")]),("Professional development",[("Reflection","professional-development/reflection.html"),("Meeting notes","professional-development/meeting-notes.html"),("Peer &amp; tutor feedback","professional-development/peer-and-tutor-feedback.html"),("Skills matrix","professional-development/professional-skills-matrix.html"),("Personal development plan","professional-development/personal-development-plan.html")]),("Evidence",[("Evidence index","evidence/README.html"),("Test results","evidence/test-results/index.html")])]
X=[("fastest_path_backend","https://github.com/Paul-Lecomte/fastest_path_backend"),("swiss-pb-map","https://github.com/Paul-Lecomte/swiss-pb-map")]
Z=re.compile(r'<aside class="nav-wrap" id="navWrap">.*?</aside>',re.DOTALL)
def hf():
 o=[]
 for p in R.rglob("*.html"):
  if S.intersection(p.relative_to(R).parts):continue
  o.append(p)
 return sorted(o)
def pfx(d):return"../"*(len(d.relative_to(R).parts)-1)
def nv(d):
 p=pfx(d);h=d.relative_to(R).as_posix();m,u=lc(h)
 L=['<aside class="nav-wrap" id="navWrap">',' <div class="nav-inner">',f' <a href="{p}index.html" class="nav-brand">Secure<span class="accent">SSD</span> Portfolio</a>',' <div class="nav-section-title">Modules</div>',' <ul class="nav-list">']
 for l,t in M:
  hr=t if t.startswith("http")else p+t;a=' class="active"'if t==h else""
  L.append(f'  <li><a href="{hr}"{a}>{l}</a></li>')
 L.append(" </ul>")
 if m and m in U:
  us=U[m]
  L.append(f' <div class="nav-section-title">Units &mdash; {m.replace("-"," ").title()}</div>')
  L.append(' <ul class="nav-list">')
  if us:
   for l,t in us:
    hr=t if t.startswith("http")else p+t;a=' class="active"'if t==h else""
    L.append(f'  <li><a href="{hr}"{a}>{l}</a></li>')
  else:L.append('  <li><span class="badge">No units added yet</span></li>')
  L.append(" </ul>")
 if u:
  up=f"modules/{m}/{u}/index.html";ag=UA.get(up,[])
  L.append(f' <div class="nav-section-title">Assignments &mdash; {u.replace("-"," ").title()}</div>')
  L.append(' <ul class="nav-list">')
  if ag:
   for l,t in ag:
    hr=t if t.startswith("http")else p+t;a=' class="active"'if t==h else""
    L.append(f'  <li><a href="{hr}"{a}>{l}</a></li>')
  else:L.append('  <li><span class="badge">No assignments added yet</span></li>')
  L.append(" </ul>")
 for t,i in A:
  L.append(f' <div class="nav-section-title">{t}</div>')
  L.append(' <ul class="nav-list">')
  for l,t2 in i:
   hr=t2 if t2.startswith("http")else p+t2;a=' class="active"'if t2==h else""
   L.append(f'  <li><a href="{hr}"{a}>{l}</a></li>')
  L.append(" </ul>")
 L.append(' <div class="nav-section-title">Repositories</div>')
 L.append(' <ul class="nav-list">')
 for l,hr in X:L.append(f'  <li><a href="{hr}" target="_blank" rel="noopener">{l}</a></li>')
 L.append(" </ul>")
 L.append(" </div>")
 L.append("</aside>")
 return"\n".join(L)
def main():
 c="--check"in sys.argv[1:];st,ch=[],0
 for d in hf():
  t=d.read_text(encoding="utf-8");z=Z.search(t)
  if not z:
   print(f"  ! no nav in {d.relative_to(R).as_posix()}");st.append(d.relative_to(R).as_posix());continue
  nw=nv(d)
  if z.group(0)==nw:continue
  st.append(d.relative_to(R).as_posix())
  if c:continue
  d.write_text(t[:z.start()]+nw+t[z.end():],encoding="utf-8");ch+=1
 if c:
  if st:
   print(f"{len(st)} page(s) out of date:");
   for r in st:print(f"  - {r}")
   return 1
  print(f"All pages current ({len(hf())} checked).");return 0
 print(f"Rewrote navigation in {ch} page(s).");return 0
if __name__=="__main__":sys.exit(main())