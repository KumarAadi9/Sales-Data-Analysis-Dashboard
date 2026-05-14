from fpdf import FPDF
import tempfile
import os

def generate_pdf_report(total_sales, total_orders, total_rows, fig_trend=None, fig_cat=None):
    # Initialize the PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Title & Subtitle
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(200, 20, txt="Executive Sales Summary", ln=True, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(200, 10, txt="Generated automatically by the AI Sales Dashboard.", ln=True, align='C')
    pdf.ln(10)
    
    # Key Performance Indicators
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Key Performance Indicators:", ln=True, align='L')
    pdf.line(10, 55, 200, 55) 
    pdf.ln(8)
    
    pdf.set_font("Arial", '', 14)
    pdf.cell(200, 10, txt=f"Total Revenue: ${total_sales:,.2f}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Total Orders: {total_orders:,}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Dataset Rows Analyzed: {total_rows:,}", ln=True, align='L')
    pdf.ln(15)

    # --- INJECTING THE CHARTS ---
    # We use tempfile to safely save and delete the images so we don't clutter your hard drive
    temp_files = []
    
    try:
        if fig_trend:
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Monthly Sales Trend", ln=True, align='L')
            
            # Save chart as PNG to a temporary file
            fd, path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            fig_trend.write_image(path, width=800, height=400, scale=2)
            
            # Embed into PDF
            pdf.image(path, x=10, w=190)
            temp_files.append(path)
            pdf.ln(5)

        if fig_cat:
            # Add a new page so the pie chart isn't squished at the bottom
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Sales Distribution by Category", ln=True, align='L')
            
            # Save chart as PNG
            fd, path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            fig_cat.write_image(path, width=800, height=500, scale=2)
            
            # Embed into PDF
            pdf.image(path, x=10, w=190)
            temp_files.append(path)

    finally:
        # Cleanup: Delete the temporary images from your computer
        for file_path in temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)

    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="For detailed AI insights and interactive charts, please view the live dashboard platform.", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin1')