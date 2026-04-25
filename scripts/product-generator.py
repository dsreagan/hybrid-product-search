from pathlib import Path
import json
import random

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR.parent / "data" / "products.json"

NUM_PRODUCTS = 500

categories = {
    "furniture": ["chair", "table", "sofa", "desk", "bench", "stool", "cabinet", "bookshelf", "nightstand", "dresser"],
    "lighting": ["lamp", "ceiling light", "pendant", "floor lamp", "wall sconce", "table lamp", "chandelier", "task light"],
    "decor": ["vase", "mirror", "rug", "art print", "planter", "throw pillow", "wall art", "candle holder", "clock"],
    "electronics": ["speaker", "headphones", "monitor", "keyboard", "mouse", "webcam", "soundbar", "microphone"]
}

category_attributes = {
    "furniture": {
        "adjectives": [
            "modern", "minimalist", "rustic", "industrial", "sleek", "premium",
            "contemporary", "elegant", "refined", "coastal", "scandinavian",
            "mid-century", "durable", "ergonomic", "handcrafted", "streamlined",
            "luxury", "textured", "bold", "warm", "functional", "architectural",
            "soft", "balanced", "curved", "polished"
        ],
        "materials": [
            "wood", "metal", "glass", "leather", "fabric", "linen", "oak",
            "walnut", "brass", "steel", "marble", "concrete", "rattan",
            "bamboo", "velvet", "wool", "cotton", "bronze", "stone",
            "ash wood", "solid wood", "tempered glass", "faux leather"
        ],
        "brands": [
            "NordicHome", "UrbanCo", "ZenLiving", "Stone & Beam", "HearthModern",
            "Fieldhouse", "Atelier Form", "Crest Supply", "Arc & Oak", "Vertex Living"
        ],
        "colors": [
            "black", "white", "charcoal", "beige", "cream", "brown", "walnut",
            "oak", "gray", "olive", "navy", "terracotta", "sand"
        ],
        "styles": [
            "modern", "industrial", "minimal", "contemporary", "scandinavian",
            "mid-century", "transitional", "rustic", "coastal"
        ],
    },
    "lighting": {
        "adjectives": [
            "modern", "minimalist", "industrial", "sleek", "compact", "premium",
            "contemporary", "elegant", "refined", "architectural", "decorative",
            "warm", "functional", "streamlined", "bold", "balanced", "polished"
        ],
        "materials": [
            "metal", "glass", "ceramic", "brass", "steel", "aluminum",
            "matte black", "bronze", "acrylic", "tempered glass", "marble"
        ],
        "brands": [
            "BrightLine", "LumaWorks", "UrbanCo", "Apex", "HearthModern",
            "Atelier Form", "Arc & Oak", "Crest Supply"
        ],
        "colors": [
            "black", "white", "charcoal", "cream", "gray", "brass",
            "silver", "bronze", "sand"
        ],
        "styles": [
            "modern", "industrial", "minimal", "contemporary", "scandinavian",
            "mid-century", "transitional"
        ],
    },
    "decor": {
        "adjectives": [
            "modern", "minimalist", "rustic", "sleek", "premium", "contemporary",
            "elegant", "refined", "coastal", "scandinavian", "handcrafted",
            "luxury", "textured", "bold", "warm", "decorative", "soft",
            "balanced", "curved", "polished"
        ],
        "materials": [
            "wood", "glass", "fabric", "ceramic", "linen", "oak", "walnut",
            "brass", "marble", "concrete", "rattan", "bamboo", "velvet",
            "wool", "cotton", "bronze", "stone", "acrylic"
        ],
        "brands": [
            "NordicHome", "ZenLiving", "Stone & Beam", "HearthModern",
            "Fieldhouse", "Atelier Form", "Crest Supply", "Arc & Oak"
        ],
        "colors": [
            "black", "white", "charcoal", "beige", "cream", "brown",
            "walnut", "oak", "gray", "olive", "navy", "terracotta", "sand"
        ],
        "styles": [
            "modern", "minimal", "contemporary", "scandinavian",
            "mid-century", "transitional", "rustic", "coastal"
        ],
    },
    "electronics": {
        "adjectives": [
            "modern", "minimalist", "sleek", "compact", "premium", "durable",
            "lightweight", "versatile", "smart", "wireless", "ergonomic",
            "streamlined", "functional", "polished"
        ],
        "materials": [
            "metal", "glass", "aluminum", "steel", "acrylic", "matte black",
            "tempered glass", "plastic"
        ],
        "brands": [
            "Apex", "NovaTech", "BrightLine", "Vertex Living", "LumaWorks"
        ],
        "colors": [
            "black", "white", "charcoal", "gray", "navy", "silver"
        ],
        "styles": [
            "modern", "minimal", "contemporary"
        ],
    },
}

synonyms = {
    "chair": ["seat", "dining chair", "accent chair"],
    "sofa": ["couch", "sectional", "loveseat"],
    "desk": ["workstation", "writing desk", "office desk"],
    "bench": ["seat bench", "entry bench"],
    "stool": ["bar stool", "counter stool"],
    "cabinet": ["storage cabinet", "console"],
    "bookshelf": ["bookcase", "shelving unit"],
    "nightstand": ["bedside table", "side table"],
    "dresser": ["chest", "storage dresser"],

    "lamp": ["light", "table light"],
    "ceiling light": ["overhead light", "flush mount"],
    "pendant": ["pendant light", "hanging light"],
    "floor lamp": ["standing lamp", "floor light"],
    "wall sconce": ["wall light", "sconce"],
    "table lamp": ["desk lamp", "accent lamp"],
    "chandelier": ["ceiling fixture", "statement light"],
    "task light": ["work light", "desk light"],

    "vase": ["decorative vase", "vessel"],
    "mirror": ["wall mirror", "accent mirror"],
    "rug": ["area rug", "floor rug"],
    "art print": ["print", "wall print"],
    "planter": ["plant pot", "indoor planter"],
    "throw pillow": ["accent pillow", "decor pillow"],
    "wall art": ["art piece", "decor art"],
    "candle holder": ["candle stand", "decor holder"],
    "clock": ["wall clock", "decor clock"],

    "speaker": ["bluetooth speaker", "audio speaker"],
    "headphones": ["headset", "wireless headphones"],
    "monitor": ["display", "screen"],
    "keyboard": ["mechanical keyboard", "wireless keyboard"],
    "mouse": ["wireless mouse", "computer mouse"],
    "webcam": ["camera", "video camera"],
    "soundbar": ["audio bar", "tv speaker"],
    "microphone": ["mic", "usb microphone"],
}

rooms = ["living room", "bedroom", "office", "dining room", "entryway", "studio", "workspace"]

category_description_templates = {
    "furniture": [
        "A {adj} {material} {item} built for the {room}, with a {style} look and a {color} finish.",
        "This {item} pairs {material} construction with a {adj} profile, making it a strong fit for {style} interiors.",
        "Designed for everyday use, this {adj} {item} brings comfort, structure, and a clean {style} presence to any {room}.",
    ],
    "lighting": [
        "A {adj} {item} with {material} detailing, designed to add layered light and a {style} feel to the {room}.",
        "This lighting piece combines a {color} finish with {material} accents for a balanced, {adj} look.",
        "Made to brighten modern spaces, this {item} delivers practical illumination with a distinctive {style} silhouette.",
    ],
    "decor": [
        "A {adj} decorative accent crafted with {material} elements, ideal for adding texture and personality to the {room}.",
        "This {item} features a {style} design language with a {color} tone that works well in curated interiors.",
        "Designed to complement shelves, consoles, and tabletops, this {adj} {item} adds visual warmth and finish to a space.",
    ],
    "electronics": [
        "A {adj} {item} engineered for daily performance, with {material} details and a clean {style} design.",
        "This tech essential blends functionality and form, offering reliable use in a {room} or focused workspace.",
        "Built with a {color} exterior and a {adj} profile, this {item} fits seamlessly into modern desks and media setups.",
    ],
}

price_ranges = {
    "furniture": (80, 1800),
    "lighting": (40, 900),
    "decor": (15, 400),
    "electronics": (30, 1200),
}

def pick_from_category(category: str, key: str) -> str:
    return random.choice(category_attributes[category][key])

def pick_synonym(item: str) -> str:
    return random.choice([item] + synonyms.get(item, []))

def generate_title(adj: str, material: str, color: str, item: str) -> str:
    patterns = [
        f"{adj.capitalize()} {material.capitalize()} {item.capitalize()}",
        f"{color.capitalize()} {adj.capitalize()} {item.capitalize()}",
        f"{adj.capitalize()} {color.capitalize()} {material.capitalize()} {item.capitalize()}",
        f"{material.capitalize()} {item.capitalize()}",
    ]
    return random.choice(patterns)

def generate_description(category: str, adj: str, material: str, item: str, color: str, style: str, room: str) -> str:
    return random.choice(category_description_templates[category]).format(
        adj=adj,
        material=material,
        item=item,
        color=color,
        style=style,
        room=room,
    )

def build_tags(category: str, item: str, adj: str, material: str, color: str, style: str) -> list[str]:
    tag_candidates = [category, item, adj, material, color, style]
    tag_candidates.extend(synonyms.get(item, [])[:2])
    return sorted(set(tag_candidates))

products = []

for i in range(1, NUM_PRODUCTS + 1):
    category = random.choice(list(categories.keys()))
    base_item = random.choice(categories[category])
    item_variant = pick_synonym(base_item)

    adj = pick_from_category(category, "adjectives")
    material = pick_from_category(category, "materials")
    brand = pick_from_category(category, "brands")
    color = pick_from_category(category, "colors")
    style = pick_from_category(category, "styles")
    room = random.choice(rooms)

    title = generate_title(adj, material, color, item_variant)
    description = generate_description(category, adj, material, item_variant, color, style, room)

    min_price, max_price = price_ranges[category]

    product = {
        "id": i,
        "sku": f"SKU-{i:05d}",
        "title": title,
        "description": description,
        "category": category,
        "subcategory": base_item,
        "brand": brand,
        "color": color,
        "material": material,
        "style": style,
        "price": round(random.uniform(min_price, max_price), 2),
        "currency": "USD",
        "tags": build_tags(category, base_item, adj, material, color, style),
        "popularity": random.randint(1, 100),
        "rating": round(random.uniform(3.2, 5.0), 1),
        "in_stock": random.choice([True, True, True, False]),
    }

    product["search_text"] = " ".join([
        product["title"],
        product["description"],
        product["category"],
        product["subcategory"],
        product["brand"],
        product["color"],
        product["material"],
        product["style"],
        " ".join(product["tags"]),
    ])

    products.append(product)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f"Generated {NUM_PRODUCTS} products -> {OUTPUT_FILE}")