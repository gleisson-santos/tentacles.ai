import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "outputs" / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FILENAME = OUTPUT_DIR / "10_filmes_de_terror_elegante.pdf"

def generate():
    doc = SimpleDocTemplate(
        str(FILENAME),
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
    )

    styles = getSampleStyleSheet()
    
    # Estilos customizados
    title_style = ParagraphStyle(
        "HorrorTitle",
        parent=styles["Title"],
        fontSize=32,
        textColor=colors.HexColor("#8B0000"), # Dark Red
        fontName="Helvetica-Bold",
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    movie_title_style = ParagraphStyle(
        "MovieTitle",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#2F4F4F"), # Dark Slate Gray
        fontName="Helvetica-Bold",
        spaceBefore=15,
        spaceAfter=5
    )
    
    info_style = ParagraphStyle(
        "MovieInfo",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#555555"),
        fontName="Helvetica-Oblique",
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        "MovieBody",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        textColor=colors.black,
        alignment=TA_LEFT
    )

    movies = [
        {
            "title": "1. O Exorcista",
            "year": "1973",
            "dir": "William Friedkin",
            "synopsis": "Um marco do cinema de terror. Quando uma adolescente é possuída por uma entidade misteriosa, sua mãe busca a ajuda de dois padres para salvar sua alma. É amplamente considerado um dos filmes mais aterrorizantes de todos os tempos."
        },
        {
            "title": "2. O Iluminado",
            "year": "1980",
            "dir": "Stanley Kubrick",
            "synopsis": "Jack Torrance torna-se zelador de inverno no isolado Hotel Overlook. Conforme o isolamento aumenta, forças sinistras influenciam Jack, levando sua família a uma luta desesperada pela sobrevivência."
        },
        {
            "title": "3. Hereditário",
            "year": "2018",
            "dir": "Ari Aster",
            "synopsis": "Após a morte da matriarca da família Graham, sua filha e netos começam a desvendar segredos enigmáticos e cada vez mais aterrorizantes sobre sua ancestralidade, tentando superar o destino sinistro que herdaram."
        },
        {
            "title": "4. Invocação do Mal",
            "year": "2013",
            "dir": "James Wan",
            "synopsis": "Baseado em um caso real dos investigadores paranormais Ed e Lorraine Warren. Eles são chamados para ajudar uma família que se mudou para uma fazenda onde fenômenos perturbadores começam a ocorrer."
        },
        {
            "title": "5. Alien, o Oitavo Passageiro",
            "year": "1979",
            "dir": "Ridley Scott",
            "synopsis": "Terror no espaço profundo. A tripulação da nave comercial Nostromo atende a um chamado de socorro e acaba trazendo a bordo uma forma de vida alienígena agressiva que os caça nos corredores escuros da nave."
        },
        {
            "title": "6. O Enigma de Outro Mundo",
            "year": "1982",
            "dir": "John Carpenter",
            "synopsis": "Em uma estação de pesquisa na Antártida, uma equipe é confrontada por um alienígena metamorfo que pode assumir a aparência de qualquer ser vivo. O clima de paranoia atinge níveis extremos."
        },
        {
            "title": "7. Corra!",
            "year": "2017",
            "dir": "Jordan Peele",
            "synopsis": "Um jovem fotógrafo viaja para conhecer os pais de sua namorada. O que começa como uma recepção estranhamente amigável evolui para um pesadelo perturbador que mistura terror e crítica social."
        },
        {
            "title": "8. A Hora do Pesadelo",
            "year": "1984",
            "dir": "Wes Craven",
            "synopsis": "Freddy Krueger, um assassino que ataca nos sonhos, aterroriza um grupo de adolescentes. Se ele te matar no sonho, você morre na vida real. Um ícone do subgênero slasher."
        },
        {
            "title": "9. The Babadook",
            "year": "2014",
            "dir": "Jennifer Kent",
            "synopsis": "Uma mãe solteira atormentada pela morte violenta do marido luta contra o medo de seu filho de um monstro que se esconde na casa, mas logo descobre uma presença sinistra ao seu redor."
        },
        {
            "title": "10. Corrente do Mal",
            "year": "2014",
            "dir": "David Robert Mitchell",
            "synopsis": "Após um encontro sexual aparentemente inocente, uma jovem se vê perseguida por uma entidade sobrenatural que assume formas humanas e caminha lentamente em sua direção até alcançá-la."
        }
    ]

    story = []
    
    # Cabeçalho
    story.append(Paragraph("TOP 10 FILMES DE TERROR", title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#8B0000")))
    story.append(Spacer(1, 1*cm))

    for movie in movies:
        # Título do Filme
        story.append(Paragraph(movie["title"], movie_title_style))
        
        # Info: Diretor e Ano
        info_text = f"<b>Ano:</b> {movie['year']} | <b>Diretor:</b> {movie['dir']}"
        story.append(Paragraph(info_text, info_style))
        
        # Sinopse
        story.append(Paragraph(movie["synopsis"], body_style))
        
        # Linha separadora discreta
        story.append(Spacer(1, 0.5*cm))
        story.append(HRFlowable(width="80%", thickness=0.5, color=colors.lightgrey, hAlign='LEFT'))
        story.append(Spacer(1, 0.5*cm))

    # Rodapé
    story.append(Spacer(1, 2*cm))
    footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    story.append(Paragraph("Gerado automaticamente pelo Tentacles Assistant", footer_style))

    doc.build(story)
    print(f"PDF gerado com sucesso em: {FILENAME}")

if __name__ == "__main__":
    generate()
