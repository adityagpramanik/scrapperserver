from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from .textutil import cleanText
from io import BytesIO
import PyPDF2

def extract_urls(pdf_file):
    hyperlinks = []
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        for annot in page["/Annots"]:
            uri = annot.get_object()["/A"]["/URI"]
            hyperlinks.append(uri)

    return ", ".join(hyperlinks)

def extractTextFromPDFFile(file):
    resume = file.read()
    laparams = LAParams(
        char_margin=2.0,
        line_margin=0.5,
        word_margin=0.1,
        boxes_flow=0.5,
    )
    text = extract_text(pdf_file=BytesIO(resume), laparams=laparams)
    text = cleanText(text)
    text += "  links: " + extract_urls(file)
    return text