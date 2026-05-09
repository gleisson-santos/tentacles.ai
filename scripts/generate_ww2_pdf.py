
import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "outputs" / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FILENAME = OUTPUT_DIR / "ww2_vibrant_history.pdf"

# Cores Vibrantes / Modernas
COLOR_BG = colors.HexColor("#121212")  # Fundo Escuro (Charcoal)
COLOR_TITLE = colors.HexColor("#E63946") # Vermelho Vibrante
COLOR_TEXT = colors.HexColor("#F1FAEE")  # Branco Suave
COLOR_ACCENT = colors.HexColor("#A8DADC") # Azul Pastel / Ciano
COLOR_GOLD = colors.HexColor("#FFD700")  # Dourado para destaques

def draw_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(COLOR_BG)
    canvas.rect(0, 0, A4[0], A4[1], fill=1)
    canvas.restoreState()

def generate_ww2_pdf():
    doc = SimpleDocTemplate(
        str(FILENAME),
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    
    # Estilos customizados
    title_style = ParagraphStyle(
        "WW2Title",
        parent=styles["Title"],
        fontSize=34,
        textColor=COLOR_TITLE,
        fontName="Helvetica-Bold",
        spaceAfter=30,
        alignment=TA_CENTER,
        leading=40
    )
    
    event_title_style = ParagraphStyle(
        "EventTitle",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=COLOR_GOLD,
        fontName="Helvetica-Bold",
        spaceBefore=12,
        spaceAfter=4,
        alignment=TA_LEFT
    )
    
    body_style = ParagraphStyle(
        "EventBody",
        parent=styles["Normal"],
        fontSize=12,
        leading=16,
        textColor=COLOR_TEXT,
        alignment=TA_LEFT,
        fontName="Helvetica"
    )

    events = [
        ("1. Invasão da Polônia (Set 1939)", "A Alemanha nazista invade a Polônia, marcando o início oficial do maior conflito da história humana."),
        ("2. Queda da França (Maio 1940)", "A estratégia Blitzkrieg alemã domina a Europa Ocidental, levando à ocupação de Paris em tempo recorde."),
        ("3. Batalha da Grã-Bretanha (Verão 1940)", "A RAF defende o Reino Unido contra os ataques aéreos massivos da Luftwaffe, impedindo a invasão terrestre."),
        ("4. Operação Barbarossa (Jun 1941)", "As potências do Eixo lançam uma invasão massiva contra a União Soviética, abrindo a sangrenta Frente Oriental."),
        ("5. Ataque a Pearl Harbor (Dez 1941)", "O Japão ataca a base naval dos EUA no Havaí, forçando a entrada definitiva dos Estados Unidos na guerra."),
        ("6. Batalha de Stalingrado (1942-1943)", "O ponto de virada decisivo na Frente Oriental, onde a vitória soviética marcou o início do recuo alemão."),
        ("7. Dia D - Normandia (Jun 1944)", "A maior operação anfíbia da história inicia a libertação da Europa Ocidental ocupada pelos nazistas."),
        ("8. Batalha de Berlim (Abr-Maio 1945)", "O cerco final soviético à capital alemã culmina no suicídio de Hitler e na rendição incondicional da Alemanha."),
        ("9. Bombas Atômicas (Ago 1945)", "O uso de armas nucleares em Hiroshima e Nagasaki precipita o fim imediato das hostilidades no Pacífico."),
        ("10. Rendição do Japão (Set 1945)", "A assinatura oficial da rendição a bordo do USS Missouri encerra formalmente os seis anos de conflito global.")
    ]

    story = []
    
    # Título Principal
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("SEGUNDA GUERRA MUNDIAL", title_style))
    story.append(HRFlowable(width="100%", thickness=3, color=COLOR_ACCENT, spaceAfter=20))
    story.append(Paragraph("<font color='#A8DADC' size='14'>CRONOLOGIA DOS PRINCIPAIS EVENTOS</font>", 
                           ParagraphStyle("Sub", parent=title_style, fontSize=14, spaceAfter=30)))

    for title, description in events:
        story.append(Paragraph(title, event_title_style))
        story.append(Paragraph(description, body_style))
        story.append(Spacer(1, 0.4*cm))

    # Rodapé Decorativo
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_ACCENT, spaceBefore=20))
    footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontSize=9, textColor=COLOR_ACCENT, alignment=TA_CENTER)
    story.append(Paragraph("Gerado por Tentacles Files Assistant • 2026", footer_style))

    # Construção do documento com o fundo
    doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)
    print(f"PDF VIBRANTE gerado com sucesso em: {FILENAME}")

if __name__ == "__main__":
    generate_ww2_pdf()
