import csv
import re
import yaml
import logging
import argparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PREFIXES = {
    "HEWM": "https://w3id.org/hew/measures/term/",
    "mesh": "http://id.nlm.nih.gov/mesh/",
    "uberon": "http://purl.obolibrary.org/obo/UBERON_",
    "mondo": "http://purl.obolibrary.org/obo/MONDO_",
    "chebi": "http://purl.obolibrary.org/obo/CHEBI_",
    "ncit": "http://purl.obolibrary.org/obo/NCIT_",
    "hp": "http://purl.obolibrary.org/obo/HP_",
    "ecto": "http://purl.obolibrary.org/obo/ECTO_",
    "vo": "http://purl.obolibrary.org/obo/VO_",
    "scdo": "http://purl.obolibrary.org/obo/SCDO_",
    "pato": "http://purl.obolibrary.org/obo/PATO_",
    "envo": "http://purl.obolibrary.org/obo/ENVO_",
    "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
    "gsso": "http://purl.obolibrary.org/obo/GSSO_",
    "ppo": "http://purl.obolibrary.org/obo/PPO_",
    "vocab": "https://w3id.org/hew/measures/",
}


def clean_id(text):
    """Converts a row string into a valid CamelCase identifier for LinkML."""
    if not text:
        return None
    # Remove special characters except spaces, dashes, and slashes
    text = re.sub(r'[^a-zA-Z0-9\s/_\-]', '', text)
    # Standardize word separators
    words = text.replace('/', ' ').replace('_', ' ').replace('-', ' ').split()
    return "".join(w.capitalize() for w in words)


def parse_ontology_ids(row):
    """Extracts ontology IDs from the row, handling multi-term entries."""
    mappings = []

    def normalize_curie(value):
        prefix, separator, identifier = value.partition(":")
        if separator and prefix.lower() in PREFIXES:
            return f"{prefix.lower()}:{identifier}"
        return value

    # Primary ontology ID column check
    primary_id = row.get('ontology ID', '').strip()
    if primary_id and ":" in primary_id and "not found" not in primary_id.lower() and "not in" not in primary_id.lower():
        mappings.append(normalize_curie(primary_id))

    # Check for secondary ontology IDs in trailing columns (e.g., for AIDS/HIV)
    # This safely scans all values in the row dictionary for pattern matches
    for value in row.values():
        if value and isinstance(value, str):
            matches = re.findall(r'\b[A-Z]+:\d+\b', value)
            for match in matches:
                normalized_match = normalize_curie(match)
                if normalized_match not in mappings:
                    mappings.append(normalized_match)
    return mappings


def csv_to_linkml_yaml(csv_filepath, yaml_outputpath):
    # Initialize the base LinkML structure
    linkml_dict = {
        "id": "https://w3id.org/hew/measures/schema",
        "name": "hew_measures_vocabulary",
        "version": "1.0.0",
        "prefixes": PREFIXES,
        "default_prefix": "vocab",
        "default_range": "string",
        "classes": {
            "Category": {
                "abstract": True,
                "description": "Root abstraction for all vocabulary domains."
            }
        },
        "enums": {
            "HEWMeasuresTerm": {
                "enum_uri": "vocab:HEWMeasuresTerm",
                "permissible_values": {}
            }
        },
    }

    classes = linkml_dict["classes"]
    permissible_values = linkml_dict["enums"]["HEWMeasuresTerm"]["permissible_values"]

    with open(csv_filepath, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row_number, row in enumerate(reader, start=2):
            # Skip empty rows, section header headers, or column definition re-declarations
            if not row.get('Category') or row['Category'].startswith(',') or "Category" in row['Category']:
                continue

            # Read and clean our taxonomy levels
            cat_raw = row['Category'].strip()
            sub1_raw = row['SubCategory 1'].strip()
            sub2_raw = row.get('SubCategory 2', '').strip() or sub1_raw  # Default to sub1 if missing
            term_raw = row['Term'].strip()

            cat_id = clean_id(cat_raw)
            sub1_id = clean_id(sub1_raw)
            sub2_id = clean_id(sub2_raw)
            assigned_curie = f"HEWM:{row_number:07d}"

            # 1. Establish Top Level Category (e.g., Health, Environment)
            if cat_id not in classes:
                classes[cat_id] = {
                    "is_a": "Category",
                    "description": f"Root domain for {cat_raw}"
                }

            # 2. Establish Level 2 SubCategory
            if sub1_id not in classes:
                classes[sub1_id] = {
                    "is_a": cat_id,
                    "description": f"Subcategory: {sub1_raw}"
                }

            # 3. Establish Level 3 SubCategory (If distinct from Level 2)
            current_parent = sub1_id
            if sub2_id != sub1_id:
                if sub2_id not in classes:
                    classes[sub2_id] = {
                        "is_a": sub1_id,
                        "description": f"Nested Subcategory: {sub2_raw}"
                    }
                current_parent = sub2_id

            # 4. Create a stable enum value for the spreadsheet term.
            aliases = [term_raw]
            if row.get('ontology term'):
                aliases.append(row['ontology term'].strip())
            permissible_value = {
                "meaning": assigned_curie,
                "title": term_raw,
                "aliases": aliases
            }

            # Add human-focused descriptions if documented.
            if row.get('ontology term'):
                permissible_value["description"] = row['ontology term'].strip()
            else:
                permissible_value["description"] = f"Local concept term for {term_raw}"

            permissible_value["annotations"] = {
                "category": cat_raw,
                "subcategory_1": sub1_raw,
                "subcategory_2": sub2_raw,
                "taxonomy_parent": current_parent,
            }

            # Preserve ontology mappings as mappings, not as term identifiers.
            mappings = parse_ontology_ids(row)
            if mappings:
                permissible_value["exact_mappings"] = mappings

            permissible_values[assigned_curie] = permissible_value

    # Output the structured Python dictionary straight into pristine YAML format
    with open(yaml_outputpath, 'w', encoding='utf-8') as yf:
        yaml.dump(linkml_dict, yf, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Successfully compiled LinkML model schema map to: {yaml_outputpath}")

# To execute the script:
# csv_to_linkml_yaml('my_vocabulary.csv', 'nexus_schema.yaml')

def main():
    logger.info("startup")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input csv file", required=True)
    parser.add_argument("--output", help="output yaml file", required=True)
    args = parser.parse_args()

    logger.info("retrieve  props")
    input_file = args.input
    output_file = args.output

    logger.debug("input:%s" % input_file)
    logger.debug("output:%s" % output_file)


    csv_to_linkml_yaml(input_file, output_file)

if __name__ == "__main__":
    main()
