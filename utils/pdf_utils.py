from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
import io

def _not_empty(x):
    if x is None: return False
    if isinstance(x, str) and x.strip() == "": return False
    if isinstance(x, (list, tuple, set)) and len(x) == 0: return False
    if isinstance(x, dict) and len(x) == 0: return False
    return True

def _flatten(d, parent_key=""):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key} / {k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten(v, new_key))
        else:
            items.append((new_key, v))
    return items

def generate_pdf_bytes(data: dict, title: str = "Bilan Kiné — Synthèse"):
    filtered = {k: v for k, v in data.items() if _not_empty(v)}
    flat = _flatten(filtered)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm
    )
    styles = getSampleStyleSheet()
    story = [Paragraph(f"<b>{title}</b>", styles["Title"]), Spacer(1, 8)]

    for k, v in flat:
        if _not_empty(v):
            story.append(Paragraph(f"<b>{k}:</b> {v}", styles["BodyText"]))
            story.append(Spacer(1, 4))

    if len(story) <= 2:
        story.append(Paragraph("Aucune donnée renseignée.", styles["BodyText"]))

    doc.build(story)
    buf.seek(0)
    return buf
