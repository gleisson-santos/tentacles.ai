"""Ferramentas PDF: criar contratos, currículos e documentos personalizados."""
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

OUTPUT_DIR = Path(__file__).parent.parent.parent / "outputs" / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _doc(filename: str):
    path = OUTPUT_DIR / filename
    return SimpleDocTemplate(
        str(path), pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
    ), path


def create_pdf(title: str, sections: list[dict], filename: str = None) -> str:
    """
    Cria PDF genérico com seções.
    sections = [{"heading": "Título", "body": "Texto..."}, ...]
    """
    fname = filename or f"{title.lower().replace(' ', '_')}.pdf"
    doc, path = _doc(fname)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title2", parent=styles["Title"], fontSize=20, spaceAfter=12)
    heading_style = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, spaceAfter=6)
    body_style = ParagraphStyle("Body2", parent=styles["Normal"], fontSize=11, leading=16)

    story = [Paragraph(title, title_style), HRFlowable(width="100%"), Spacer(1, 0.4*cm)]
    for sec in sections:
        if sec.get("heading"):
            story.append(Paragraph(sec["heading"], heading_style))
        if sec.get("body"):
            for para in sec["body"].split("\n\n"):
                story.append(Paragraph(para.replace("\n", "<br/>"), body_style))
                story.append(Spacer(1, 0.2*cm))
        story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    return str(path)


def create_contract(
    title: str,
    party_a: str,
    party_b: str,
    clauses: list[str],
    date: str,
    filename: str = None,
) -> str:
    """Cria contrato profissional com cláusulas numeradas e área de assinatura."""
    fname = filename or f"contrato_{party_a.split()[0].lower()}_{party_b.split()[0].lower()}.pdf"
    doc, path = _doc(fname)
    styles = getSampleStyleSheet()
    bold = ParagraphStyle("Bold", parent=styles["Normal"], fontSize=11, fontName="Helvetica-Bold")
    normal = ParagraphStyle("N", parent=styles["Normal"], fontSize=11, leading=16)
    title_s = ParagraphStyle("T", parent=styles["Title"], fontSize=16, spaceAfter=10)

    story = [
        Paragraph(title.upper(), title_s),
        HRFlowable(width="100%", thickness=2),
        Spacer(1, 0.5*cm),
        Paragraph(f"<b>CONTRATANTE:</b> {party_a}", normal),
        Paragraph(f"<b>CONTRATADO:</b>  {party_b}", normal),
        Spacer(1, 0.5*cm),
    ]
    for i, clause in enumerate(clauses, 1):
        story.append(Paragraph(f"<b>Cláusula {i}ª</b>", bold))
        story.append(Paragraph(clause, normal))
        story.append(Spacer(1, 0.3*cm))

    story += [
        Spacer(1, 1*cm),
        Paragraph(f"Data: {date}", normal),
        Spacer(1, 1.5*cm),
        Table(
            [["_" * 35, "", "_" * 35]],
            colWidths=[7*cm, 2*cm, 7*cm],
        ),
        Table(
            [[party_a, "", party_b]],
            colWidths=[7*cm, 2*cm, 7*cm],
            style=TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]),
        ),
    ]
    doc.build(story)
    return str(path)


def create_resume(
    name: str,
    contact: dict,
    summary: str,
    experience: list[dict],
    education: list[dict],
    skills: list[str],
    filename: str = None,
) -> str:
    """
    Cria currículo profissional.
    contact = {"email": "", "phone": "", "linkedin": "", "city": ""}
    experience = [{"company": "", "role": "", "period": "", "description": ""}]
    education = [{"institution": "", "degree": "", "period": ""}]
    """
    fname = filename or f"curriculo_{name.split()[0].lower()}.pdf"
    doc, path = _doc(fname)
    styles = getSampleStyleSheet()
    name_s = ParagraphStyle("Name", parent=styles["Title"], fontSize=22, textColor=colors.HexColor("#0077B5"))
    section_s = ParagraphStyle("Sec", parent=styles["Heading2"], fontSize=12,
                                textColor=colors.HexColor("#0077B5"), spaceAfter=4)
    normal = ParagraphStyle("N", parent=styles["Normal"], fontSize=10, leading=14)
    bold = ParagraphStyle("B", parent=styles["Normal"], fontSize=10, fontName="Helvetica-Bold")
    small = ParagraphStyle("S", parent=styles["Normal"], fontSize=9, textColor=colors.grey)

    story = [
        Paragraph(name, name_s),
        Paragraph(
            f"{contact.get('city', '')} | {contact.get('email', '')} | {contact.get('phone', '')} | {contact.get('linkedin', '')}",
            small
        ),
        HRFlowable(width="100%", color=colors.HexColor("#0077B5"), thickness=1.5),
        Spacer(1, 0.3*cm),
        Paragraph("RESUMO PROFISSIONAL", section_s),
        Paragraph(summary, normal),
        Spacer(1, 0.4*cm),
        Paragraph("EXPERIÊNCIA", section_s),
        HRFlowable(width="100%", thickness=0.5),
    ]
    for exp in experience:
        story += [
            Spacer(1, 0.2*cm),
            Paragraph(f"<b>{exp['role']}</b> — {exp['company']}", bold),
            Paragraph(exp["period"], small),
            Paragraph(exp.get("description", ""), normal),
        ]

    story += [Spacer(1, 0.4*cm), Paragraph("EDUCAÇÃO", section_s), HRFlowable(width="100%", thickness=0.5)]
    for edu in education:
        story += [
            Spacer(1, 0.2*cm),
            Paragraph(f"<b>{edu['degree']}</b> — {edu['institution']}", bold),
            Paragraph(edu["period"], small),
        ]

    story += [
        Spacer(1, 0.4*cm),
        Paragraph("HABILIDADES", section_s),
        HRFlowable(width="100%", thickness=0.5),
        Spacer(1, 0.2*cm),
        Paragraph(" • ".join(skills), normal),
    ]
    doc.build(story)
    return str(path)
