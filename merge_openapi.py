# -*- coding: utf-8 -*-
import json
from pathlib import Path

# Paths to your original OpenAPI files
ATHENA_FILE = Path("mintlify-docs/openapi.json")
ARTEMIS_FILE = Path("mintlify-docs/openapi_2.json")
OUTPUT_FILE = Path("mintlify-docs/merged_openapi.json")

def load_json(path):
    with open(str(path), "r") as f:
        return json.load(f)

def tag_paths(paths, tag_name):
    for path, methods in paths.items():
        for method in methods.values():
            if "tags" not in method:
                method["tags"] = []
            if tag_name not in method["tags"]:
                method["tags"].append(tag_name)
    return paths

def main():
    athena = load_json(ATHENA_FILE)
    artemis = load_json(ARTEMIS_FILE)

    merged = {
        "openapi": "3.0.0",
        "info": {
            "title": "Merged Athena & Artemis API",
            "version": "1.0.0"
        },
        "paths": {},
        "tags": []
    }

    # Merge tags
    existing_tags = set()

    for spec, tag_name in [(athena, "Athena"), (artemis, "Artemis")]:
        spec_paths = tag_paths(spec["paths"], tag_name)
        merged["paths"].update(spec_paths)

        for tag in spec.get("tags", []):
            if tag["name"] != tag_name:
                tag["name"] = tag_name  # override if inconsistent
            if tag_name not in existing_tags:
                merged["tags"].append(tag)
                existing_tags.add(tag_name)

        # Add fallback tag if tags block is missing
        if tag_name not in existing_tags:
            merged["tags"].append({
                "name": tag_name,
                "description": "{} endpoints".format(tag_name)
            })
            existing_tags.add(tag_name)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(merged, f, indent=2)
    # print(f"✅ Merged OpenAPI written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
