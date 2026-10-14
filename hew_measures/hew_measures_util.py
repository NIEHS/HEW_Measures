import csv
import re
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, Prefix


def clean_classname(text):
    # Convert string into valid CamelCase for LinkML Class identifiers
    text = re.sub(r'[^a-zA-Z0-9\s/_\-]', '', text)
    words = text.replace('/', ' ').replace('_', ' ').replace('-', ' ').split()
    return "".join(w.capitalize() for w in words)


def build_schema_from_csv(csv_filepath):
    schema = SchemaDefinition(
        id="https://w3id.org/hew/measures/schema",
        name="hew_measures",
        default_prefix="vocab"
    )

    # Establish ontologies namespaces
    schema.prefixes['vocab'] = Prefix(prefix_prefix='vocab', prefix_reference='https://w3id.org/hew/measures/')
    schema.prefixes['mesh'] = Prefix(prefix_prefix='mesh', prefix_reference='http://id.nlm.nih.gov/mesh/')
    schema.prefixes['envo'] = Prefix(prefix_prefix='envo', prefix_reference='http://purl.obolibrary.org/obo/ENVO_')
    schema.prefixes['chebi'] = Prefix(prefix_prefix='chebi', prefix_reference='http://purl.obolibrary.org/obo/CHEBI_')
    schema.prefixes['uberon'] = Prefix(prefix_prefix='uberon', prefix_reference='http://purl.obolibrary.org/obo/UBERON_')
    schema.prefixes['mondo'] = Prefix(prefix_prefix='mondo', prefix_reference='http://purl.obolibrary.org/obo/MONDO_')
    schema.prefixes['hp'] = Prefix(prefix_prefix='hp', prefix_reference='http://purl.obolibrary.org/obo/HP_')
    schema.prefixes['ecto'] = Prefix(prefix_prefix='ecto', prefix_reference='http://purl.obolibrary.org/obo/ECTO_')

    with open(csv_filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row['Category'] or "Category" in row['Category']:
                continue  # Skip structural sections headers

            cat = clean_classname(row['Category'])
            sub1 = clean_classname(row['SubCategory 1'])
            term_name = clean_classname(row['Term'])
            ontology_id = row.get('ontology ID', '').strip()

            # Ensure Parent Category is initialized
            if cat not in schema.classes:
                schema.classes[cat] = ClassDefinition(name=cat, is_a="Category")

            # Ensure Subcategory is initialized
            if sub1 not in schema.classes:
                schema.classes[sub1] = ClassDefinition(name=sub1, is_a=cat)

            # Create Leaf Node
            if term_name not in schema.classes:
                leaf = ClassDefinition(
                    name=term_name,
                    is_a=sub1,
                    description=row.get('ontology term', f"Local term for {row['Term']}"),
                    aliases=[row['Term']]
                )
                if ontology_id and ":" in ontology_id:
                    leaf.exact_mappings.append(ontology_id.lower())

                schema.classes[term_name] = leaf

    return schema
