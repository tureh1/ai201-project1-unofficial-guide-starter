from pathlib import Path
import re


DOCS_DIR = "docs"
CHUNK_SIZE = 500
OVERLAP_PARAGRAPHS = 1


def load_documents(docs_dir=DOCS_DIR):
    """
    Load all .txt documents from the docs folder.
    """
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"Could not find docs folder: {docs_dir}")

    documents = []

    for file_path in sorted(docs_path.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


def remove_header(text):
    """
    Remove document header lines from the chunk text.

    The source filename is already stored in metadata, so we do not need
    Title, Source Type, Source URL, or Date Collected inside the chunk text.
    """
    if "Content:" in text:
        return text.split("Content:", 1)[1]

    return text


def remove_helper_sections(text):
    """
    Remove helper/planning text that should not be treated as source content.
    """
    stop_phrases = [
        "Suggested content to collect:",
        "Notes:",
        "Potential questions this document can help answer:",
    ]

    lines = text.splitlines()
    cleaned_lines = []
    skip = False

    for line in lines:
        stripped = line.strip()

        if stripped in stop_phrases:
            skip = True
            continue

        if skip:
            # Stop skipping only if a new major section appears.
            if stripped.startswith("FILE NAME:") or stripped.startswith("Title:"):
                skip = False
            else:
                continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def clean_text(text):
    """
    Clean text before chunking.
    """
    text = remove_header(text)
    text = remove_helper_sections(text)

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Fix small spacing issue in one document.
    text = text.replace("dining centermeals", "dining center meals")

    # Remove extra spaces and tabs.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove too many blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_text(text, source, chunk_size=CHUNK_SIZE, overlap_paragraphs=OVERLAP_PARAGRAPHS):
    """
    Split text into paragraph-based chunks.

    Strategy:
    - Around 500 characters per chunk
    - One paragraph of overlap
    - Paragraph-based chunks so the text stays readable
    """
    text = clean_text(text)

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_paragraphs = []
    current_length = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)

        if current_paragraphs and current_length + paragraph_length + 2 > chunk_size:
            chunks.append("\n\n".join(current_paragraphs))

            overlap = current_paragraphs[-overlap_paragraphs:] if overlap_paragraphs > 0 else []
            current_paragraphs = overlap + [paragraph]
            current_length = sum(len(p) for p in current_paragraphs)
        else:
            current_paragraphs.append(paragraph)
            current_length += paragraph_length + 2

    if current_paragraphs:
        chunks.append("\n\n".join(current_paragraphs))

    chunk_dicts = []

    for index, chunk in enumerate(chunks):
        chunk_dicts.append({
            "id": f"{Path(source).stem}_chunk_{index}",
            "text": chunk,
            "metadata": {
                "source": source,
                "chunk_index": index
            }
        })

    return chunk_dicts


def build_chunks(docs_dir=DOCS_DIR):
    """
    Load all documents, clean them, and split them into chunks.
    """
    documents = load_documents(docs_dir)
    all_chunks = []

    for document in documents:
        chunks = chunk_text(
            text=document["text"],
            source=document["source"]
        )
        all_chunks.extend(chunks)

    return all_chunks


def print_sample_chunks(chunks, sample_size=5):
    """
    Print sample chunks so we can inspect whether chunking worked.
    """
    if not chunks:
        print("No chunks were created.")
        return

    print("Sample chunks:")
    print("=" * 80)

    for chunk in chunks[:sample_size]:
        print(f"ID: {chunk['id']}")
        print(f"Source: {chunk['metadata']['source']}")
        print(f"Chunk index: {chunk['metadata']['chunk_index']}")
        print(f"Length: {len(chunk['text'])} characters")
        print("-" * 80)
        print(chunk["text"])
        print("=" * 80)


if __name__ == "__main__":
    documents = load_documents()
    chunks = build_chunks()

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.")
    print()

    print_sample_chunks(chunks, sample_size=5)