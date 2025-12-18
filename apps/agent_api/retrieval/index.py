import os
from dataclasses import dataclass
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer

@dataclass
class IndexedChunk:
    source_id: str
    chunk_id: str
    text: str

@dataclass
class RetrievalIndex:
    vectorizer: TfidfVectorizer
    matrix: object
    chunks: List[IndexedChunk]

def _read_corpus_files(corpus_dir: str) -> List[Tuple[str, str]]:
    files = []
    for root, _, fnames in os.walk(corpus_dir):
        for f in fnames:
            if f.lower().endswith(".txt"):
                path = os.path.join(root, f)
                rel = os.path.relpath(path, corpus_dir)  # e.g. "htn_screening_demo.txt"
                with open(path, "r", encoding="utf-8") as fp:
                    files.append((rel, fp.read()))
    return files

def _chunk_text(text: str, chunk_size: int = 600, overlap: int = 80) -> List[str]:
    """
    Simple character-based chunking (v1). Deterministic and fast.
    """
    text = " ".join(text.split())
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks

def build_index(corpus_dir: str, chunk_size: int = 600, overlap: int = 80) -> RetrievalIndex:
    docs = _read_corpus_files(corpus_dir)
    chunks: List[IndexedChunk] = []
    for relpath, content in docs:
        parts = _chunk_text(content, chunk_size=chunk_size, overlap=overlap)
        for i, part in enumerate(parts):
            chunks.append(
                IndexedChunk(
                    source_id=relpath,                # e.g. "htn_screening_demo.txt"
                    chunk_id=str(i).zfill(4),         # e.g. "0000"
                    text=part,
                )
            )

    texts = [c.text for c in chunks] if chunks else [""]  # avoid empty fit errors
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=50000)
    matrix = vectorizer.fit_transform(texts)

    return RetrievalIndex(vectorizer=vectorizer, matrix=matrix, chunks=chunks)
