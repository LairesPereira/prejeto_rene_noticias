import textwrap
from fpdf import FPDF

def text_to_pdf(text, filepath):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    
    # separa o texto em um lista de strings a partir de cada quebra de linha
    splitted = text.split('\n')

    for line in splitted:
        
        # retorna uma lista com strings adequadas ao tamanho da página
        # garante que cada linha não irá ultrapassar o tamanho da páginas
        lines = textwrap.wrap(line, width_text) 
        print(lines)
        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filepath, 'F')

# input_filepath = 'texto.txt'
# output_filepath = 'output.pdf'
# file = open(input_filepath)
# text = file.read()
# file.close()
# text_to_pdf(text, output_filepath)