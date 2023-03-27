from reportlab.lib.units import mm
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
import json

# Función para dividir el texto en varias líneas
def split_text(text, width):
    text = Paragraph(text)
    lines = []
    text_width, text_height = text.wrap(width, 10000)
    for l in text.breakLines(width).lines:
        lines.append(" ".join(l[1]))
    return lines

# Cargar los términos desde el archivo JSON
with open('terminos.json', encoding="utf8") as f:
    terminos = json.load(f)

# Configuración de la ficha
max_width, max_height = landscape(A4)
border = 3*mm
width, height = max_width/2 - border*2, max_height/2 - border*2
pdfmetrics.registerFont(TTFont('Tahoma', 'Tahoma.ttf'))
pdfmetrics.registerFont(TTFont('TahomaBd', 'TahomaBd.ttf'))
#pdfmetrics.registerFont(TTFont('TahomaIt', 'TahomaIt.ttf'))
#pdfmetrics.registerFont(TTFont('TahomaBI', 'TahomaBI.ttf'))
term_font_size = 20
desc_font_size = 12
tabu_height = 5*mm
tabu_spacing = 1*mm
tabu_font_size = 9

# Configuración del documento PDF
pdf = canvas.Canvas('fichas.pdf', pagesize=landscape(A4))

# Bucle para crear las fichas
for i, termino in enumerate(terminos):
    # Calcular las coordenadas de la ficha
    i_prime = i % 4
    x = (i_prime % 2) * (width + border) + border
    y = ((i_prime // 2) + 1)
    
    if y == 1:
        y = 2
    else:
        y = 1
        
    y = y*(height + border) + border
    
    y -= 5*mm

    # Agregar el término al centro de la ficha
    pdf.setFont("TahomaBd", term_font_size)
    if not termino.get("acronimo",None):
        pdf.drawCentredString(x + width/2, y, termino['termino'].title())
        y -= 8*mm
        pdf.setFont("Tahoma", term_font_size)
        pdf.drawCentredString(x + width/2, y, " ")
    else:
        pdf.drawCentredString(x + width/2, y, termino['termino'])
        y -= 8*mm
        pdf.setFont("Tahoma", term_font_size)
        pdf.drawCentredString(x + width/2, y, " ("+ termino['acronimo']+")")
        

    y -= 7*mm
    # Agregar la descripción debajo del término
    pdf.setFont("Tahoma", desc_font_size)
    pdf.drawCentredString(x + width/2, y, "Tema " + str(termino["tema"])) # +": " + termino["tipo"].capitalize())


    # Agregar descripción
    tabu_x = x + border
    tabu_y = y - 8*mm 
    pdf.setFont("TahomaBd", tabu_font_size)
    pdf.drawString(tabu_x, tabu_y - tabu_height/2, "Descripción:")
    pdf.setFont("Tahoma", tabu_font_size)
    lineas = split_text(termino["descripcion"], width - border)
    tabu_y -= (tabu_height + 2*mm)
    for linea in lineas:
        pdf.drawString(tabu_x, tabu_y - tabu_height/2, linea)
        tabu_y -= (tabu_height - 1*mm)

    # Agregar los espacios en blanco para escribir las palabras tabú
    """
    tabu_x = x + border
    tabu_y = y - 8*mm 
    pdf.setFont("TahomaBd", tabu_font_size)
    pdf.drawString(tabu_x, tabu_y - tabu_height/2, "Palabras Tabú:")
    for j, tabu in enumerate(termino['tabu']):
        if j % 4 == 0:
            tabu_y = tabu_y - tabu_height - 2*mm
            tabu_x = x + border
        # pdf.rect(tabu_x, tabu_y, 22*mm, tabu_height)
        pdf.setFont("Tahoma", tabu_font_size)
        pdf.drawCentredString(tabu_x + jump_x/2, tabu_y - tabu_height/2, tabu)
        tabu_x += jump_x
    """
    
    # Agregar los espacios en blanco para escribir las palabras tabú
    jump_x = width/4 - border
    tabu_x = x + border
    words_height = 8*mm
    tabu_y = tabu_y - 2*mm        
    pdf.setFont("TahomaBd", tabu_font_size)
    pdf.drawString(tabu_x, tabu_y - words_height/2, "Palabras seleccionadas:")
    tabu_y = tabu_y - words_height/2     
    for j in range(8):
        if j % 4 == 0:
            tabu_y = tabu_y - words_height - 2*mm       
            tabu_x = x + border
        pdf.rect(tabu_x, tabu_y, jump_x - border, words_height)
        #pdf.setFontSize(tabu_font_size)
        #pdf.drawCentredString(tabu_x + width/8, tabu_y - tabu_height/2, "")
        tabu_x += jump_x

    tabu_y = tabu_y - 4*mm
    tabu_x = x + border
    pdf.setFont("TahomaBd", tabu_font_size)
    pdf.drawString(tabu_x, tabu_y - tabu_height/2, "Reglas:")
    reglamento = "No puede usar ninguna palabra del término y a lo sumo dos palabras de la descripción. Se consideran la misma palabra si está en diferente idioma o si tienen la misma raíz (es decir, son derivaciones de la misma)"
    pdf.setFont("Tahoma", tabu_font_size)
    lineas = split_text(reglamento, width - border)
    tabu_y -= (tabu_height + 2*mm)
    for linea in lineas:
        pdf.drawString(tabu_x, tabu_y - tabu_height/2, linea)
        tabu_y -= (tabu_height - 1*mm)

    # Salto de página después de cada 4 fichas
    if (i + 1) % 4 == 0:
        pdf.showPage()

    
# Guardar el documento PDF
pdf.save()