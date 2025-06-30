from fpdf import FPDF
from io import BytesIO

def save_as_pdf(agent_outputs: dict) -> BytesIO:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section, content in agent_outputs.items():
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 10, section)
        pdf.set_font("Arial", '', 12)
        
        # Remove markdown that might break FPDF rendering
        clean_content = content.replace("**", "").replace("###", "").replace("##", "").replace("#", "")
        pdf.multi_cell(0, 10, clean_content)
        pdf.ln(5)

    # Write to a BytesIO buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer
