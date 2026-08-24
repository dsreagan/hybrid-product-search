import json
import requests
import os

from dotenv import load_dotenv
from pathlib import Path
from pathlib import Path


EMBEDDING_SERVICE = "https://embed.danielreagan.dev/embed"


def load_products(file_path: Path) -> list:
    with open(file_path, "r", encoding="utf-8") as products_json:
        return json.load(products_json)


def embed_products(products: list) -> list:
    payload = []

    for product in products:
        product_id = product["id"]
        embedding_text = product["embedding_text"]

        if not isinstance(product_id, int):
            raise ValueError(f"Invalid product id: {product_id}")

        if not isinstance(embedding_text, str) or not embedding_text.strip():
            raise ValueError(
                f"Invalid embedding text for product {product_id}"
            )

        payload.append({
            "id": product_id,
            "fields": {
                "embedding_text": embedding_text
            }
        })

    response = requests.post(
        EMBEDDING_SERVICE,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    embedding_results = response.json()

    embeddings_by_id = {}

    for result in embedding_results:
        product_id = int(result["id"])
        embedding = result["embeddings"]["embedding_text"]

        embeddings_by_id[product_id] = embedding

    for product in products:
        product_id = product["id"]

        if product_id not in embeddings_by_id:
            raise ValueError(
                f"No embedding returned for product {product_id}"
            )

        product["embedding"] = embeddings_by_id[product_id]

    return products


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def build_bulk_body(products: list, index_name: str) -> str:
    lines = []

    for product in products:
        product_id = product["id"]

        action = {
            "index": {
                "_index": index_name,
                "_id": product_id
            }
        }

        lines.append(json.dumps(action))
        lines.append(json.dumps(product))

    return "\n".join(lines) + "\n"


class Elastic:
    def __init__(self, endpoint, username=None, password=None):
        self.endpoint = endpoint.rstrip("/")
        self.auth = (
            (username, password)
            if username and password
            else None
        )

    def bulk(self, operations: str):
        full_url = f"{self.endpoint}/_bulk"

        response = requests.post(
            full_url,
            data=operations,
            auth=self.auth,
            headers={
                "Content-Type": "application/x-ndjson"
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    def request(self, method, url, body=None):
        full_url = f"{self.endpoint}/{url.lstrip('/')}"

        response = requests.request(
            method=method,
            url=full_url,
            json=body,
            auth=self.auth,
            timeout=30
        )

        response.raise_for_status()

        if response.content:
            return response.json()

        return None


def main():
    project_root = Path(__file__).resolve().parent.parent

    load_dotenv(project_root / ".env")

    elastic_endpoint = os.getenv("ELASTIC_ENDPOINT")
    elastic_username = os.getenv("ELASTIC_USERNAME")
    elastic_password = os.getenv("ELASTIC_PASSWORD")
    
    if not all([ elastic_endpoint, elastic_username, elastic_password ]):
        raise RuntimeError("Missing Elasticsearch environment variables")

    products_path = project_root / "data" / "products.json"

    if not products_path.is_file():
        raise FileNotFoundError(
            f"Product data JSON file not found: {products_path}"
        )

    products = load_products(products_path)
    print(f"Loaded {len(products)} products")

    products = embed_products(products)
    print(f"Embedded {len(products)} products")
    
    elastic = Elastic(
        elastic_endpoint,
        elastic_username,
        elastic_password
    )

    for batch in chunks(products, 100):
        bulk_body = build_bulk_body(batch, "products")
        result = elastic.bulk(bulk_body)

        if result.get("errors"):
            print("Bulk batch had errors")
        else:
            print(f"Indexed {len(batch)} products")

    result = elastic.bulk(bulk_body)

    if result["errors"]:
        print("Some documents failed to index")

        for item in result["items"]:
            index_result = item["index"]

            if "error" in index_result:
                print(index_result["error"])
    else:
        print("Bulk indexing successful")


if __name__ == "__main__":
    main()
