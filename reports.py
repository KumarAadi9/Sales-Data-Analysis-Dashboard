from fpdf import FPDF

def generate_pdf_report(total_sales, total_orders, total_rows):
    # Initialize the PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(200, 20, txt="Executive Sales Summary", ln=True, align='C')
    
    # Subtitle
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(200, 10, txt="Generated automatically by the AI Sales Dashboard.", ln=True, align='C')
    pdf.ln(15) # Add vertical space
    
    # Header for Metrics
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Key Performance Indicators:", ln=True, align='L')
    pdf.line(10, 65, 200, 65) # Draw a sleek underline
    pdf.ln(10)
    
    # The Metrics
    pdf.set_font("Arial", '', 14)
    pdf.cell(200, 12, txt=f"Total Revenue: ${total_sales:,.2f}", ln=True, align='L')
    pdf.cell(200, 12, txt=f"Total Orders: {total_orders:,}", ln=True, align='L')
    pdf.cell(200, 12, txt=f"Dataset Rows Analyzed: {total_rows:,}", ln=True, align='L')
    
    # Footer
    pdf.ln(30)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="For detailed AI insights and visual charts, please view the live dashboard platform.", ln=True, align='C')
    
    # Output the PDF as a byte string so Streamlit can download it
    return pdf.output(dest='S').encode('latin1')