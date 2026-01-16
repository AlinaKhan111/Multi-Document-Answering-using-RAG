from llm.gemini_generator import generate_with_gemini
from llm.groq_generator import generate_with_groq


def generate_answer(query, retrieved_chunks, provider="gemini"):
    """
    Build RAG prompt and route to selected LLM.
    """

    # ---- Build context from retrieved chunks ----
    context_blocks = []
    for chunk in retrieved_chunks:
        src = chunk["metadata"]["source"]
        cid = chunk["metadata"]["chunk_id"]
        context_blocks.append(
            f"[Source: {src}, Chunk: {cid}]\n{chunk['text']}"
        )

    context = "\n\n".join(context_blocks)

    # ---- Final RAG Prompt ----
    prompt = f"""
You are a document question answering assistant.

Rules:
- Use ONLY the information provided in the context.
- Do NOT use external knowledge.
- If the answer is not explicitly present, say:
  "Answer not found in the documents."

Context:
{context}

Question:
{query}

Answer:
"""

    # ---- Route to LLM ----
    if provider == "gemini":
        return generate_with_gemini(prompt)

    elif provider == "groq":
        return generate_with_groq(prompt)

    else:
        return "Unknown LLM provider"
