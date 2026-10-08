import csv
import re
import yaml
import logging
import argparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



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
    # Primary ontology ID column check
    primary_id = row.get('ontology ID', '').strip()
    if primary_id and ":" in primary_id and "not found" not in primary_id.lower() and "not in" not in primary_id.lower():
        mappings.append(primary_id)

    # Check for secondary ontology IDs in trailing columns (e.g., for AIDS/HIV)
    # This safely scans all values in the row dictionary for pattern matches
    for value in row.values():
        if value and isinstance(value, str):
            matches = re.findall(r'\b[A-Z]+:\d+\b', value)
            for match in matches:
                if match not in mappings:
                    mappings.append(match)
    return mappings


def csv_to_linkml_yaml(csv_filepath, yaml_outputpath):
    # Initialize the base LinkML structure
    linkml_dict = {
        "id": "http://niehs.nih.org/hew",
        "name": "hew_measures_vocabulary",
        "version": "1.0.0",
        "prefixes": {
            "mesh": "http://nih.gov",
            "uberon": "http://obolibrary.org_",
            "mondo": "http://obolibrary.org_",
            "chebi": "http://obolibrary.org_",
            "ncit": "http://obolibrary.org_",
            "hp": "http://obolibrary.org_",
            "ecto": "http://obolibrary.org_",
            "vo": "http://obolibrary.org_",
            "scdo": "http://obolibrary.org_",
            "pato": "http://obolibrary.org_",
            "envo": "http://obolibrary.org_",
            "snomed": "http://snomed.info",
            "vocab": "http://example.org"
        },
        "default_prefix": "vocab",
        "default_range": "string",
        "classes": {
            "Category": {
                "abstract": True,
                "description": "Root abstraction for all vocabulary domains."
            }
        }
    }

    classes = linkml_dict["classes"]

    with open(csv_filepath, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
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
            term_id = clean_id(term_raw)

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

            # 4. Create Concrete Leaf Term, add ontology term as an alias
            if term_id not in classes:
                aliases = [term_raw]
                if row.get('ontology term'):
                    aliases.append(row['ontology term'].strip())
                class_entry = {
                    "is_a": current_parent,
                    "aliases": aliases
                }

                # Add human-focused descriptions if documented
                if row.get('ontology term'):
                    class_entry["description"] = row['ontology term'].strip()
                else:
                    class_entry["description"] = f"Local concept term for {term_raw}"

                # Parse out mappings cleanly
                mappings = parse_ontology_ids(row)
                if mappings:
                    class_entry["exact_mappings"] = mappings

                classes[term_id] = class_entry

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


