import os
from PyPDF2 import PdfMerger, PdfFileReader
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

if not os.path.exists('txt-summaries/to-be-concatenated'):
    os.makedirs('txt-summaries/to-be-concatenated')
if not os.path.exists('concatenated-summaries'):
    os.makedirs('concatenated-summaries')

# Function to convert plain text to PDF
def text_to_pdf(text_file_path, pdf_file_path):
    # Define the PDF document
    pdf = SimpleDocTemplate(
        pdf_file_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Initialize list to hold elements to write to the PDF
    elements = []
    
    # Retrieve sample styles from reportlab
    styles = getSampleStyleSheet()
    
    # Open and read the text file
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
    
    # Add each line as a paragraph to the elements list
    for line in lines:
        elements.append(Paragraph(line, styles['Normal']))
    
    # Build the PDF
    pdf.build(elements)

# Function to append PDFs
def append_pdf(input_pdf, output_pdf):
    merger = PdfMerger()
    merger.append(output_pdf)
    merger.append(input_pdf)
    merger.write(output_pdf)
    merger.close()

# Directory with plain text files to be concatenated with their pdf versions
text_dir = 'txt-summaries/to-be-concatenated'

# Directory with PDF files to be concatenated with their text summaries
pdf_dir = 'pdfs-to-summarize'

# Directory to output final concatenated PDFs
output_dir = 'concatenated-summaries'

# Convert each text file to PDF and append to corresponding PDF
for text_file in os.listdir(text_dir):
    if text_file.endswith('.txt'):
        base = os.path.splitext(text_file)[0]
        input_pdf = os.path.join(pdf_dir, base + '.pdf')
        output_pdf = os.path.join(output_dir, base + '.pdf')
        text_to_pdf(os.path.join(text_dir, text_file), output_pdf)
        if os.path.isfile(input_pdf):
            try:
                append_pdf(input_pdf, output_pdf)
            except AssertionError:
                print(f"Failed to append {input_pdf}")

