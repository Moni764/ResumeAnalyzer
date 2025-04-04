import os 
from fpdf import FPDF 
from PyPDF2 import PdfReader
from datetime import datetime
from dotenv import load_dotenv 
import google.generativeai as genai
import docx
import PyPDF2
import markdown

## load environment variables from .env file 
load_dotenv()

# Configure the generative AI model with API key
## GOOGLE_API_KEY="AIzaSyAAcGhPdW8CLCEOJpa8lqirCtJamNo0W1I"
## genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
## model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

GOOGLE_API_KEY = "AIzaSyAAcGhPdW8CLCEOJpa8lqirCtJamNo0W1I"
genai.configure(api_key=GOOGLE_API_KEY)  # ✅ Works correctly

model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
# Function to get AI response based on input and prompt
def SendRequest(input_text, pdf_content, prompt):
    response = model.generate_content([input_text, pdf_content, prompt])
    return response.text

## Function to extract text from PDF 
def ExtractPDF(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text 
def ExtractDoc(file):
    doc = docx.Document(file)
    paragraphs = [p.text for p in doc.paragraphs]
    markdown_text = '\n'.join(paragraphs)
    #with open(output_file, 'w', encoding='utf-8') as f:
     #   f.write(markdown_text)
    return (markdown_text)

# Function to create a Optimized resume PDF
def CreatePDF(text, input_filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_margins(10, 10, 10)  # Set narrower margins to 10 mm
    pdf.set_font("Courier", size=10)
    for line in text.split("\n"):
        # Ensure that the line is encoded in latin-1
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), align='L')
    # Generate the timestamped filename with format ddmmyyyyhhmmss
    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    file_name = f"{input_filename}_Optimized_{timestamp}.pdf"
    pdf.output(file_name, 'F')
    return file_name if os.path.exists(file_name) else None