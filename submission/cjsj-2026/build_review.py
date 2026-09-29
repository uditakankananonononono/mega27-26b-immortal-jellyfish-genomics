from pathlib import Path
from docx import Document
from docx.shared import Inches,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
root=Path(__file__).resolve().parent
segments=(root/'manuscript.txt').read_text().strip().split('\n\n')
d=Document('/tmp/cjsj-template/research.docx')
body=d._element.body
for el in list(body):
 if not el.tag.endswith('sectPr'): body.remove(el)
sec=d.sections[0];sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Inches(.75)
normal=d.styles['Normal'];normal.font.name='Times New Roman';normal.font.size=Pt(10);normal.font.bold=False;normal.paragraph_format.line_spacing=.95;normal.paragraph_format.space_after=Pt(4)

def add_run(p,text,bold=False,size=10):
 r=p.add_run(text);r.bold=bold;r.font.name='Times New Roman';r.font.size=Pt(size);return r
for chunk in segments:
 key,text=chunk.split(': ',1) if ': ' in chunk else ('',chunk)
 if key=='TITLE':
  p=d.add_paragraph(style='Normal');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  add_run(p,text,bold=True,size=13)
 elif key=='AUTHOR LINE':
  p=d.add_paragraph(style='Normal');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  add_run(p,text,size=10)
 elif key=='REFERENCES':
  p=d.add_paragraph(style='Normal');add_run(p,'References',bold=True)
  for line in text.split('\n'):
   p=d.add_paragraph(style='Normal');p.paragraph_format.space_after=Pt(2);add_run(p,line,size=8)
 else:
  p=d.add_paragraph(style='Normal')
  add_run(p,key.title()+' - ',bold=True)
  add_run(p,text)
for p in d.paragraphs:p.paragraph_format.keep_together=False
# The journal template is retained (two columns/section properties); no unsupported layout mutations.
out=root/'PhookanUdita_paper_REVIEW.docx';d.save(out);print(out)
