# HEW Measures

HEW Measures is a controlled vocabulary for describing themes and measures
relevant to health and extreme weather research. Its terms are organized using
the categories and subcategories in the source spreadsheet and can be linked to
external ontology concepts with CURIE mappings.

The repository provides a pipeline for converting the spreadsheet data into a
LinkML schema and publishing machine-readable JSON-LD artifacts.

## Repository contents

- `data/MeasuresTermsv4-1.27.25.xlsx` — spreadsheet source.
- `data/MeasuresTermsv4-1.27.25.csv` — CSV input used by the generator.
- `hew_measures/hew_measures_spreadsheet_to_yaml.py` — converts the CSV into
  the LinkML schema at `data/HewMeasures.yaml`.
- `data/HewMeasures.yaml` — generated LinkML schema. The category hierarchy is
  represented by classes; the vocabulary terms are permissible values in the
  `HEWMeasuresTerm` enumeration.
- `dist/hew_measures.jsonld` and `dist/hew_measures_context.jsonld` — generated
  JSON-LD schema and JSON-LD context.
- `.github/workflows/compile-jsonld.yml` — regenerates the JSON-LD artifacts
  when the LinkML schema changes on the configured branches, or when manually
  dispatched.

## Term identifiers

Each vocabulary term receives a CURIE based on its row number in the CSV,
formatted as `HEWM:` followed by seven digits. For example, the first term
currently appears on row 3 (row 1 is the header and row 2 is a structural
spreadsheet row), so its identifier is `HEWM:0000003`.

The CURIE is the enum permissible-value key and its LinkML `meaning`; its
expanded identifier uses the `HEWM` prefix declared in the schema. The term
label and alternate label are retained separately as the title and aliases.
Ontology identifiers in the spreadsheet are retained as mappings, not used as
the HEW Measures identifier.

These identifiers depend on row position. Do not insert, delete, or reorder
term rows after identifiers have been published: doing so can assign different
identifiers to terms. Coordinate any spreadsheet restructuring as an
identifier migration. The current `https://w3id.org/hew/measures/term/` base
also requires the corresponding w3id redirect configuration before the
expanded term URIs resolve publicly.

## Regenerate the LinkML schema

Use Python 3.11 or later. Install the LinkML command-line tools and MkDocs
Material theme:

```sh
python -m pip install linkml mkdocs-material
```

Generate the schema from the CSV:

```sh
python -m hew_measures.hew_measures_spreadsheet_to_yaml \
  --input data/MeasuresTermsv4-1.27.25.csv \
  --output data/HewMeasures.yaml
```

The generator preserves the spreadsheet's category/subcategory hierarchy,
term labels, descriptions, and ontology mappings. Structural or empty
spreadsheet rows are not emitted as terms, but still contribute to subsequent
row numbers.

## Generate JSON-LD and documentation

The GitHub Actions workflow uses the LinkML CLI to generate the JSON-LD
artifacts:

```sh
gen-jsonld data/HewMeasures.yaml > dist/hew_measures.jsonld
gen-jsonld-context data/HewMeasures.yaml > dist/hew_measures_context.jsonld
```

To generate the LinkML reference documentation and build the MkDocs site:

```sh
gen-doc --directory docs_markdown data/HewMeasures.yaml
cd docs_markdown
mkdocs build --site-dir ../docs_html
```

To generate a schemasheet from the YAML schema (currently does not work!):

```shell

pip install schemasheets
linkml2sheets -s ./data/HewMeasures.yaml -o ./data/HewMeasures.sheets.tsv
```

The workflow is configured to run for changes to `data/HewMeasures.yaml` on
`main` and `develop`, for closed pull requests targeting `main`, and via
`workflow_dispatch`. It generates the JSON-LD artifacts and builds the
documentation site. To regenerate the schema and all outputs locally, run the
schema-generation and artifact-generation commands above in sequence.

## Tools

- **Python 3.11+** runs the spreadsheet-to-schema conversion script.
- **PyYAML** is used by the conversion script to write the generated schema.
- **LinkML** provides the schema model and the `gen-jsonld`,
  `gen-jsonld-context`, and `gen-doc` command-line generators.
- **MkDocs Material** builds the generated reference documentation into a
  static site.
- **GitHub Actions** runs the artifact-generation workflow.