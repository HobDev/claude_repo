import re

# Chunk by section
def chunk_by_section(document_text: str) -> list[str]:
    pattern = r"\n## "
    return re.split(pattern, document_text)


# Chunk by a set number of characters
def chunk_by_char(text: str, chunk_size: int = 150, chunk_overlap: int = 20) -> list[str]:
    chunks: list[str] = []
    start_idx = 0

    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))

        chunk_text = text[start_idx:end_idx]
        chunks.append(chunk_text)

        start_idx = (
            end_idx - chunk_overlap if end_idx < len(text) else len(text)
        )

    return chunks


# Chunk by sentence
def chunk_by_sentence(
    text: str, max_sentences_per_chunk: int = 5, overlap_sentences: int = 1
) -> list[str]:
    sentences: list[str] = re.split(r"(?<=[.!?])\s+", text)

    chunks: list[str] = []
    start_idx = 0

    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))

        current_chunk = sentences[start_idx:end_idx]
        chunks.append(" ".join(current_chunk))

        start_idx += max_sentences_per_chunk - overlap_sentences

        if start_idx < 0:
            start_idx = 0

    return chunks