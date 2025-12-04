import hashlib

import pymupdf


def extract_text_from_model(file):
    try:
        doc = pymupdf.open(stream=file.read(), filetype='pdf')
        text = ''
        for page in doc:
            text += page.get_text()
            text += '\n'
        return text.strip()
    except:
        return None


def hash_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()