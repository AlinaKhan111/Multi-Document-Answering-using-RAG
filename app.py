import streamlit as st

from ingestion.base_loader import load_document
from preprocessing.chunking import chunk_text_with_metadata
from embeddings.embedder import load_embedding_model, build_faiss_index
from retrieval.retriever import filter_chunks_by_document, retrieve_top_k
from llm.router import generate_answer 


# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Multi-Document RAG QA", layout="wide")
st.title("📄 Multi-Document Question Answering System")


# -------------------------------
# File Upload
# -------------------------------
uploaded_files = st.file_uploader(
    "Upload documents (PDF, DOCX, CSV)",
    type=["pdf", "docx", "csv"],
    accept_multiple_files=True
)


if uploaded_files:
    # -------------------------------
    # Document Ingestion
    # -------------------------------
    document_texts = {}
    for file in uploaded_files:
        document_texts[file.name] = load_document(file)

    # -------------------------------
    # Chunking
    # -------------------------------
    chunks = chunk_text_with_metadata(document_texts)

    # -------------------------------
    # Sidebar Controls
    # -------------------------------
    st.sidebar.header("⚙️ Retrieval Settings")

    selected_doc = st.sidebar.selectbox(
        "📂 Select document",
        ["All Documents"] + list(document_texts.keys())
    )

    top_k = st.sidebar.slider(
        "🔎 Top-K chunks",
        min_value=1,
        max_value=10,
        value=3
    )

    st.sidebar.header("🧠 LLM Settings")

    llm_provider_ui = st.sidebar.selectbox(
        "Choose LLM Provider",
        ["Groq (LLaMA-3)", "Gemini"]
    )

    provider_map = {
        "Gemini": "gemini",
        "Groq (LLaMA-3)": "groq"
    }

    llm_provider = provider_map[llm_provider_ui]

    use_llm = st.sidebar.checkbox(
        "Use LLM",
        value=True,
        help="Disable to run in retrieval-only demo mode"
    )

    # -------------------------------
    # Filter Chunks
    # -------------------------------
    search_chunks = filter_chunks_by_document(chunks, selected_doc)

    # -------------------------------
    # Embeddings + FAISS
    # -------------------------------
    embed_model = load_embedding_model()
    faiss_index = build_faiss_index(search_chunks, embed_model)

    # -------------------------------
    # Query Input
    # -------------------------------
    st.subheader("🤖 Ask a Question")
    query = st.text_input("Enter your question")

    if query:
        retrieved_chunks = retrieve_top_k(
            query,
            search_chunks,
            faiss_index,
            embed_model,
            top_k
        )

        # -------------------------------
        # Answer Generation
        # -------------------------------
        if use_llm:
            answer = generate_answer(
                query=query,
                retrieved_chunks=retrieved_chunks,
                provider=llm_provider
            )
        else:
            answer = (
                "🔧 **LLM disabled (demo mode)**\n\n"
                "Showing retrieved context instead:\n\n"
                + retrieved_chunks[0]["text"][:800]
            )

        # -------------------------------
        # Output
        # -------------------------------
        st.subheader("📌 Answer")
        st.write(answer)

        st.subheader("📚 Sources")
        for chunk in retrieved_chunks:
            with st.expander(
                f"{chunk['metadata']['source']} "
                f"(Chunk {chunk['metadata']['chunk_id']})"
            ):
                st.write(chunk["text"])
