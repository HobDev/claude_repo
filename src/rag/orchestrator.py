import argparse
from pathlib import Path
from typing import Callable, cast

from chunking.manual_chunking import (
    chunk_by_char,
    chunk_by_section,
    chunk_by_sentence,
)
from embeddings import generate_embedding
from vector_index import VectorIndex


ChunkerFunction = Callable[[str], list[str]]


# Map the chunking function name to the concrete callable.
AVAILABLE_CHUNKERS: dict[str, ChunkerFunction] = {
    "chunk_by_section": lambda text: chunk_by_section(text),
    "chunk_by_char": lambda text: chunk_by_char(text),
    "chunk_by_sentence": lambda text: chunk_by_sentence(text),
}


# Read and validate the input file path.
def read_input_file(file_path: str) -> tuple[Path, str]:
    input_path = Path(file_path).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not input_path.is_file():
        raise FileNotFoundError(f"Input path is not a file: {input_path}")

    return input_path, input_path.read_text(encoding="utf-8")


# Split the input document into chunks and return them.
def chunk_document(file_path: str, function_name: str) -> list[str]:
    if function_name not in AVAILABLE_CHUNKERS:
        valid_names = ", ".join(AVAILABLE_CHUNKERS.keys())
        raise ValueError(
            f"Unsupported function_name '{function_name}'. Use one of: {valid_names}"
        )

    _, input_text = read_input_file(file_path)
    chunking_fn = AVAILABLE_CHUNKERS[function_name]
    return chunking_fn(input_text)


# Create embeddings for chunks and store both chunk text and vector in the vector index.
def build_vector_store(chunks: list[str]) -> VectorIndex:
    if not chunks:
        raise ValueError("No chunks were generated from the input file.")

    raw_embeddings = generate_embedding(chunks, input_type="document")
    if not isinstance(raw_embeddings, list) or len(raw_embeddings) != len(chunks):
        raise ValueError("Embedding generation did not return one embedding per chunk.")
    if raw_embeddings and not isinstance(raw_embeddings[0], list):
        raise ValueError("Expected a list of embedding vectors for chunk input.")

    embeddings = cast(list[list[float]], raw_embeddings)

    vector_store = VectorIndex(distance_metric="cosine")
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):
        document = {
            "content": chunk,
            "chunk_id": idx,
        }
        vector_store.add_vector(vector=[float(value) for value in embedding], document=document)

    return vector_store


# Full orchestration: chunk file, embed chunks, and index them in vector store.
def orchestrate(file_path: str, function_name: str) -> tuple[list[str], VectorIndex]:
    chunks = chunk_document(file_path=file_path, function_name=function_name)
    vector_store = build_vector_store(chunks)
    return chunks, vector_store


# CLI entrypoint for invoking orchestration from terminal.
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chunk a file, embed the chunks, and store them in vector index."
    )
    parser.add_argument("file_path", help="Path to the input text/markdown file")
    parser.add_argument(
        "function_name",
        choices=sorted(AVAILABLE_CHUNKERS.keys()),
        help="Chunking function to use",
    )
    args = parser.parse_args()

    chunks, vector_store = orchestrate(args.file_path, args.function_name)

    print(f"Generated {len(chunks)} chunks from input file.")
    print(f"Stored {len(vector_store)} chunk embeddings in vector index.")


if __name__ == "__main__":
    main()
