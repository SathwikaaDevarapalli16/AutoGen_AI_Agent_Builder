from fpdf import FPDF

def save_as_pdf(agent_outputs, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for section, content in agent_outputs.items():
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 10, f"{section}:", align='L')
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.ln()

    pdf.output(filename)
    return filename  # 🔥 important

