import os
from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve


MODEL_NAME = "llama-3.3-70b-versatile"


def build_context(retrieved_chunks):
    """
    Format retrieved chunks into context for the LLM.
    """
    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk["metadata"]["source"]
        chunk_index = chunk["metadata"]["chunk_index"]
        text = chunk["text"]

        context_parts.append(
            f"[Source {i}: {source}, chunk {chunk_index}]\n{text}"
        )

    return "\n\n---\n\n".join(context_parts)


def get_unique_sources(retrieved_chunks):
    """
    Return a clean list of unique source filenames.
    """
    sources = []

    for chunk in retrieved_chunks:
        source = chunk["metadata"]["source"]
        if source not in sources:
            sources.append(source)

    return sources


def ask(question, top_k=5):
    """
    Retrieve relevant chunks and generate a grounded answer.
    """
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Missing GROQ_API_KEY. Put your Groq key in a .env file."
        )

    retrieved_chunks = retrieve(question, top_k=top_k)
    context = build_context(retrieved_chunks)
    sources = get_unique_sources(retrieved_chunks)

    client = Groq(api_key=api_key)

    system_prompt = """
You are an assistant for a RAG system called The Unofficial Guide.

You must answer using ONLY the provided retrieved document context.
Do not use outside knowledge.
Do not make up facts.

If the retrieved context does not contain enough information to answer the question, say exactly:
"I don't have enough information in the collected documents to answer that."

Write in a clear, helpful style for a college student.
Include specific names, places, food spots, dining halls, or meal plan names when the context provides them.

Do NOT write a Sources section. The program will add source filenames separately.
"""

    user_prompt = f"""
Question:
{question}

Retrieved context:
{context}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content.strip()

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


def print_answer(result):
    """
    Print the generated answer and sources.
    """
    print()
    print("=" * 100)
    print(f"QUESTION: {result['question']}")
    print("=" * 100)
    print(result["answer"])

    print()
    print("Sources:")
    for source in result["sources"]:
        print(f"- {source}")


if __name__ == "__main__":
    test_questions = [
        "What do students say is the best food on campus?",
        "Are ISU meal plans worth it?",
        "What restaurants near campus do students recommend?",
        "What do students say about parking on campus?",
    ]

    for question in test_questions:
        result = ask(question)
        print_answer(result)