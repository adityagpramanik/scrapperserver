from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from .textutil import cleanText
from io import BytesIO

def extractTextFromPDFFile(file):
    resume = file.read()
    laparams = LAParams(
        char_margin=2.0,
        line_margin=0.5,
        word_margin=0.1,
        boxes_flow=0.5,
    )
    text = extract_text(pdf_file=BytesIO(resume), laparams=laparams)
    return cleanText(text)