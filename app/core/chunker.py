from typing import List, Dict, Any

Metadata = Dict[str, Any]


def flatten_metadata(metadata: Metadata, prefix: str = "") -> Metadata:
    flat = {}
    for key, value in metadata.items():
        new_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            flat.update(flatten_metadata(value, new_key))
        elif isinstance(value, list):
            if all(isinstance(item, (str, int, float, bool, type(None))) for item in value):
                flat[new_key] = value
            else:
                flat[new_key] = str(value)
        elif isinstance(value, (str, int, float, bool, type(None))):
            flat[new_key] = value
        else:
            flat[new_key] = str(value)
    
    return flat


def chunk_text(
    text: str,
    doc_id: str,
    doc_meta: Metadata ={},
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[Dict]:
    chunks = []
    start = 0
    text_length = len(text)
    flat_doc_meta = flatten_metadata(doc_meta, "doc_meta")

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk_text = text[start:end]
        chunk_id = f"{doc_id}_chunk_{len(chunks)}"
        chunk_meta = {
            "original_doc_id": doc_id,
            "chunk_index": len(chunks),
            "chunk_size": len(chunk_text),
            "start_char": start,
            "end_char": end,
            **flat_doc_meta,
        }
        
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "metadata": chunk_meta,
        })
        
        if end == text_length:
            break

        start = end - chunk_overlap

    return chunks