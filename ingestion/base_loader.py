from ingestion.pdf_loader import load_pdf
from ingestion.docx_loader import load_docx
from ingestion.csv_loader import load_csv

def load_document(file):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return load_pdf(file)

    elif filename.endswith(".docx"):
        return load_docx(file)

    elif filename.endswith(".csv"):
        return load_csv(file)

    else:
        raise ValueError("Unsupported file format")
