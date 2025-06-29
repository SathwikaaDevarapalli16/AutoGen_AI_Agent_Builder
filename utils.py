def save_as_pdf(agent_outputs, filename="startup_summary.pdf"):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for section, content in agent_outputs.items():
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=section, ln=True)
        pdf.set_font("Arial", size=12)
        for line in content.split('\n'):
            pdf.multi_cell(0, 10, txt=line)
        pdf.ln()

    pdf.output(filename)
    return filename  # <<< This line is critical!


