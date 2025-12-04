import pymupdf

def extract_text(filepath):
    doc = pymupdf.open(filepath)
    text = ''
    for page in doc:
        text +=page.get_text()
        text +='\n'
    return text.strip()