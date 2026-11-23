from docx import Document

doc = Document("AI_Cyber_Threat_Detection_Project_Documentation.docx")
out = []

# walk paragraphs and tables in the order they appear in the document
from docx.table import Table
from docx.text.paragraph import Paragraph

for child in doc.element.body.iterchildren():
    if child.tag.endswith("}p"):
        p = Paragraph(child, doc)
        text = p.text.strip()
        if not text:
            continue
        style = p.style.name if p.style is not None else ""
        if style.startswith("Heading 1"):
            out.append("# " + text)
        elif style.startswith("Heading 2"):
            out.append("## " + text)
        elif style.startswith("Heading 3"):
            out.append("### " + text)
        else:
            out.append(text)
    elif child.tag.endswith("}tbl"):
        t = Table(child, doc)
        for i, row in enumerate(t.rows):
            cells = [c.text.strip().replace("\n", " ") for c in row.cells]
            out.append("| " + " | ".join(cells) + " |")
            if i == 0:
                out.append("|" + " --- |" * len(cells))
        out.append("")

with open("SPEC.md", "w", encoding="utf-8") as f:
    f.write("\n\n".join(out))
print("SPEC.md created")