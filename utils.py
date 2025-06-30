
from fpdf import FPDF
from io import BytesIO

def save_as_pdf(agent_outputs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for section, content in agent_outputs.items():
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 10, txt=section)
        pdf.ln()
        pdf.set_font("Arial", size=12)
        for line in content.split('\n'):
            pdf.multi_cell(0, 10, txt=line)
        pdf.ln()

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    return buffer


