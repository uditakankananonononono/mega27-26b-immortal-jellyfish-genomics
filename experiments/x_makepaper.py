"""Build the 26b expansion paper DOCX + verify the 50+ page TEXT-body rule.

Sections live in paper_x/sections/*.txt ('# ' = heading, else paragraphs).
Body-text page count: body prose only (no headings/refs/appendix/captions),
typeset 12pt Times New Roman, 1.5 spacing, 1in margins, rendered to PDF via
LibreOffice, pages counted with pdfinfo. Diagrams never count.
"""
import glob, json, os, re, subprocess, sys

SECTIONS = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "paper_x", "sections", "*.txt")))
OUT = os.path.join(os.path.dirname(__file__), "..", "paper", "MEGA27-26b-EXPANSION.docx")
BODY = "/tmp/xpaper_body.docx"

def parse_section(path):
    lines = open(path).read().splitlines()
    title, paras, cur = None, [], []
    for ln in lines:
        if ln.startswith("# "):
            title = ln[2:].strip()
        elif ln.strip() == "":
            if cur: paras.append(" ".join(cur)); cur = []
        else:
            cur.append(ln.strip())
    if cur: paras.append(" ".join(cur))
    return title, paras

def base_doc():
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_LINE_SPACING
    doc = Document()
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1)
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"; st.font.size = Pt(12)
    st.paragraph_format.line_spacing = 1.5
    return doc

def build_full():
    doc = base_doc()
    nwords = 0
    for sp in SECTIONS:
        title, paras = parse_section(sp)
        doc.add_heading(title, level=1)
        for p in paras:
            doc.add_paragraph(p)
            nwords += len(p.split())
    # references + appendix placeholder files appended by caller sections
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc.save(OUT)
    return nwords

def build_body_only():
    doc = base_doc()
    nwords = 0
    for sp in SECTIONS:
        base = os.path.basename(sp)
        if base.startswith(("98_", "99_")):  # references/appendix excluded
            continue
        _, paras = parse_section(sp)
        for p in paras:
            doc.add_paragraph(p)
            nwords += len(p.split())
    doc.save(BODY)
    return nwords

def pdf_pages(docx_path):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    "--outdir", "/tmp", docx_path],
                   check=True, capture_output=True, timeout=600)
    pdf = "/tmp/" + os.path.basename(docx_path).replace(".docx", ".pdf")
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1)), pdf

if __name__ == "__main__":
    full_words = build_full()
    body_words = build_body_only()
    pages, pdf = pdf_pages(BODY)
    rep = {"body_words": body_words, "full_words": full_words,
           "body_pages_rendered": pages,
           "rule": ">=50 pages of body text; headings/references/appendix/diagrams excluded; diagrams never count",
           "pass": pages >= 50}
    print(json.dumps(rep, indent=1))
    json.dump(rep, open("results/x-papercount.json", "w"), indent=1)
