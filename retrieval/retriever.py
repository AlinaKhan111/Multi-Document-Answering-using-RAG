def filter_chunks_by_document(chunks, selected_doc):
    if selected_doc == "All Documents":
        return chunks

    return [
        c for c in chunks
        if c["metadata"]["source"] == selected_doc
    ]


def retrieve_top_k(query, chunks, index, model, top_k):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, k=top_k)

    return [chunks[idx] for idx in indices[0]]
