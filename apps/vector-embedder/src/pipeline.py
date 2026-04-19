"""
Flatten structured items into text batches, embed them, and rebuild the
result keyed by item id and field name.
"""

from .model import embed_texts


def embed_items(items):
    work = []

    for item in items:
        item_id = item.get("id")
        fields = item.get("fields")

        if item_id is None or not isinstance(fields, dict):
            continue

        for field_name, text in fields.items():
            if not isinstance(text, str) or not text.strip():
                continue
            work.append((item_id, field_name, text))

    texts = [text for _, _, text in work]
    vectors = embed_texts(texts)

    by_id = {}

    for (item_id, field_name, _), vector in zip(work, vectors):
        if item_id not in by_id:
            by_id[item_id] = {
                "id": item_id, 
                "embeddings": {}
            }
        by_id[item_id]["embeddings"][field_name] = vector

    return list(by_id.values())