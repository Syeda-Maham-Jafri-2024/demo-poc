# # from fpdf import FPDF

# # def save_report_to_pdf(report_text, file_name="endoscopy_report.pdf"):
# #     """
# #     Save the generated report to a PDF file with improved formatting.
# #     """
# #     pdf = FPDF()
# #     pdf.set_auto_page_break(auto=True, margin=15)
# #     pdf.add_page()

# #     # Set title and font
# #     pdf.set_font("Arial", 'B', 16)  # Larger title font
# #     pdf.cell(200, 10, txt="Endoscopy Report", ln=True, align='C')
    
# #     # Add space between title and report content
# #     pdf.ln(10)

# #     # Add Procedure Summary section
# #     pdf.set_font("Arial", 'B', 9)
# #     pdf.cell(0, 10, 'Procedure Summary', ln=True)
# #     pdf.set_font("Arial", size=9)
# #     pdf.multi_cell(0, 10, txt=report_text.split('Procedure Summary')[1].split('Procedure Details')[0].strip())
    
# #     # Add Procedure Details section
# #     pdf.set_font("Arial", 'B', 9)
# #     pdf.cell(0, 10, 'Procedure Details', ln=True)
# #     pdf.set_font("Arial", size=9)
# #     pdf.multi_cell(0, 10, txt=report_text.split('Procedure Details')[1].split('Post-Procedure Findings')[0].strip())
    
# #     # Add Post-Procedure Findings section
# #     pdf.set_font("Arial", 'B', 9)
# #     pdf.cell(0, 10, 'Post-Procedure Findings', ln=True)
# #     pdf.set_font("Arial", size=9)
# #     pdf.multi_cell(0, 10, txt=report_text.split('Post-Procedure Findings')[1].split('Follow-Up Plan')[0].strip())
    
# #     # Add Follow-Up Plan section
# #     pdf.set_font("Arial", 'B', 9)
# #     pdf.cell(0, 10, 'Follow-Up Plan', ln=True)
# #     pdf.set_font("Arial", size=9)
# #     pdf.multi_cell(0, 10, txt=report_text.split('Follow-Up Plan')[1].split('Additonal Comments')[0].strip())

# #      # Add Additional Comments section
# #     pdf.set_font("Arial", 'B', 9)
# #     pdf.cell(0, 10, 'Additional Comments', ln=True)
# #     pdf.set_font("Arial", size=9)
# #     pdf.multi_cell(0, 10, txt=report_text.split('Additional Comments')[1].strip())
    
# #     # Save the PDF file
# #     pdf.output(file_name)
# #     print(f"Report saved as {file_name}")

# from fpdf import FPDF
# import io

# def save_report_to_pdf(report_text):
#     """
#     Save the generated report to a PDF file with improved formatting and return the PDF file in memory.
#     """
#     # Create PDF instance
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     # Set title and font
#     pdf.set_font("Arial", 'B', 16)  # Larger title font
#     pdf.cell(200, 10, txt="Endoscopy Report", ln=True, align='C')
    
#     # Add space between title and report content
#     pdf.ln(10)

#     # Add Procedure Summary section
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, 'Procedure Summary', ln=True)
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, txt=report_text.split('Procedure Summary')[1].split('Procedure Details')[0].strip())
    
#     # Add Procedure Details section
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, 'Procedure Details', ln=True)
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, txt=report_text.split('Procedure Details')[1].split('Post-Procedure Findings')[0].strip())
    
#     # Add Post-Procedure Findings section
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, 'Post-Procedure Findings', ln=True)
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, txt=report_text.split('Post-Procedure Findings')[1].split('Follow-Up Plan')[0].strip())
    
#     # Add Follow-Up Plan section
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, 'Follow-Up Plan', ln=True)
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, txt=report_text.split('Follow-Up Plan')[1].strip())
    
#     # Save the PDF to a byte stream
#     pdf_output = io.BytesIO()
#     pdf.output(pdf_output)
    
#     # Return the byte stream containing the PDF content
#     pdf_output.seek(0)
#     return pdf_output.getvalue(), len(report_text)

from fpdf import FPDF

def save_report_to_pdf(report_text):
    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set font for the report
    pdf.set_font("Arial", size=12)
    
    # Add the report text to the PDF
    pdf.multi_cell(0, 10, report_text)
    
    # Save the PDF to a file
    output_file = "generated_report.pdf"
    pdf.output(output_file)
    
    # Return the file path for download
    return output_file
