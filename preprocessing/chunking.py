from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text_with_metadata(document_texts):
    chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    for doc_name, text in document_texts.items():
        split_texts = splitter.split_text(text)

        for idx, chunk in enumerate(split_texts):
            chunks.append({
                "text": chunk,
                "metadata": {
                    "source": doc_name,
                    "chunk_id": idx
                }
            })

    return chunks
