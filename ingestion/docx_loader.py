import docx

def load_docx(file):
    document = docx.Document(file)
    paragraphs = [para.text for para in document.paragraphs if para.text]
    return "\n".join(paragraphs)
