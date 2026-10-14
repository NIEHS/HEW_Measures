# Automate tagging HEW Measures from EnVar/Amadeus metadata

Oct 12, 2026 · @Someone

HEW Measures can tag catalog datasets automatically, from the variable descriptions Amadeus and others already produce, once a handful of technical issues in the vocabulary are fixed.

## The opportunity

The HEW catalog model already distinguishes two useful layers, and HEW Measures is the bridge between them.

- **Themes** (`themes` on a resource) answer *"what is this dataset about?"* — Ozone, Drought, Housing. These are the values people search and filter on, and this is the job HEW Measures does.
- **Variables** (`environmental_variables[].measured_property`) answer *"what exactly does this column measure?"* — an ontology identifier such as ChEBI's term for ozone. This is the level EnVar describes, and Amadeus plans to emit EnVar records for every dataset it produces.

Today a person has to tag themes by hand. But each HEW Measures term already carries ontology mappings, and those mappings are the same kind of identifier a variable description uses. **If the mappings are reliable, the catalog can derive a dataset's themes from its variables automatically.**

Worked example:

| Step | What it holds |
| --- | --- |
| 1. Amadeus emits a variable description | `measured_property: CHEBI:25812` (ozone) |
| 2. HEW Measures says | Term **Ozone (O3)** maps to `CHEBI:25812` |
| 3. The catalog entry gets | Theme **Ozone (O3)**, with no manual tagging |

Ozone is the easy case, because the variable and the theme happen to be the same thing. Usually they are not. A variable names something narrow and precise, and a theme names a broad topic people search for. The link can be many to one, one to many, or only approximate:

| Variables in the dataset | Theme it should land under | How the mapping table gets there |
| --- | --- | --- |
| Daily maximum air temperature, heat index | **Heat** | Neither variable *is* heat. Both terms are mapped to Heat as *related*, so Heat is offered to a curator as a suggestion. |
| Nitrogen dioxide, sulfur dioxide, carbon monoxide | **Trace Gases** | Three variables, one theme. Each gas is mapped to Trace Gases as *broader*. |
| Ozone | **Ozone (O3)**, and its parent theme | One variable, two themes: the exact match, plus whatever sits above it in the HEW Measures hierarchy. |

This is why step 2 below records how strong each mapping is: exact and close matches can tag automatically, and the looser ones become suggestions.

The same works for publications and surveys tagged with HEW Measures: anything that carries a variable-level identifier can land under the right facet. Nobody needs to adopt a new schema for this. It needs one shared convention: **both sides use the same ontology identifiers, and every HEW Measures mapping states whether it is an exact, close, broader or merely related match.**

## How we would realise it

Four steps. The first two are fixes inside the HEW Measures repository; the last two are where the shared identifier agreement and downstream derivation happen.

1. **Fix the plumbing** so every mapping resolves to the correct ontology term and every HEW Measures term has a permanent identifier. These are the technical issues **below**; most are a few lines each.
2. **Record each mapping with its strength.** Keep the mappings in their own table, one row per mapping, stating whether the match is exact, close, broader or only related. The [SSSOM format](https://mapping-commons.github.io/sssom/dev/spec-intro/), a standard for this, does exactly that, and many LinkML tools read it. Jennifer's first-pass mapping moves in largely as it is; curation then tightens it over time.
3. **Agree which identifiers variables use.** For common environmental quantities (PM2.5, ozone, temperature, precipitation…), HEW's `measured_property` and EnVar's `standard_name` should point at the same term. That is a short shared list, not a new standard; one useful mechanism here is [LinkML value sets](https://linkml.io/valuesets/). (Example of an enum specifically for air pollutants, ours would be broader: [AirPollutantEnum](https://linkml.io/valuesets/elements/AirPollutantEnum/).)
4. **Derive themes automatically.** When a dataset enters the catalog with variable descriptions, look up each variable's identifier in the mapping table. Exact and close matches become themes; broader or related matches can be offered as suggestions for a curator to accept. Missing mappings can be sent to a curator review queue or an LLM-assisted suggestion workflow.

## What needs fixing first

After checking the repository as of 12 October 2026: the spreadsheet, the conversion script, the generated JSON-LD and the GitHub Action. The pipeline itself (spreadsheet → CSV → LinkML → JSON-LD on commit) is a good design. Five issues stop the output being usable for tagging yet.

| # | What happens now | Why it matters | Suggested fix |
| --- | --- | --- | --- |
| 1 | Every ontology mapping turns into a broken web address. The prefixes are declared as `http://obolibrary.org_` (and MeSH as `http://nih.gov`), so `CHEBI:25812` becomes `http://obolibrary.org_25812`. | No tool can follow the mapping. Worse, ChEBI 25812 and UBERON 25812 become the *same* address, so different terms collide. | Use the standard prefixes, e.g. `CHEBI: http://purl.obolibrary.org/obo/CHEBI_` and `MESH: http://id.nlm.nih.gov/mesh/`. Use a single CURIE management layer such as [curies](https://pypi.org/project/curies/) rather than ad hoc prefix strings. |
| 2 | Each term's identifier is built from its label: "Ozone (O3)" becomes `OzoneO3`. | When a label is corrected or two duplicates are merged, as Jennifer plans, the identifier changes. Anything already tagged with it silently breaks. | Give each term a permanent identifier (for example `HEWM:0000123`) that never changes, and keep the label as a separate field. This is the safest pattern for long-lived catalog tags. |
| 3 | The term addresses (`https://NIEHS.github.io/HEW_Measures/dist/...`) return "page not found". | People who follow a tag from the catalog land nowhere. | Point the prefix to a stable permanent address such as a w3id.org redirect or a persistent public PURL. Never bind terms to ephemeral GitHub Pages URLs if they are expected to persist. |
| 4 | Terms are modelled as LinkML *classes*, arranged in an `is_a` hierarchy. | A class describes a kind of record, not a tag. The generated JSON-LD is therefore a schema document, not a list of concepts other systems can tag with. | Model the terms as a LinkML enumeration or value set, each with a stable `meaning` and a canonical identifier. |
| 5 | Every mapping is recorded as an *exact* match, and some get lost. | Automatic tagging needs to know when a match is only approximate. A curator also needs to see where the gaps are. | Record mapping strength (step 2 above) and preserve dropped or ambiguous mappings in the output, rather than silently overwriting them. |

Examples behind row 5, from the current file:

- **The same ontology term is used for different measures.** Vegetation Cover, Vegetation Type and Vegetation Structure all point to `ENVO:01000355`. Land Cover and Vegetation Greenness share one term, as do Solar Radiation and Sunlight, and Immigration and Living Conditions.
- **Some mappings point at the wrong kind of thing.** Temperature maps to a PATO *quality* term. Proximity to Hazards is mapped to `proximally_connected_to`, which is a relationship name, not a term. `ENVO:1000745` (Drought) has one digit too few.
- **45 of 227 terms have no mapping yet.** Examples: PM2.5, PM10, Heat and Trace Gases.
- **Terms get dropped silently.** When two rows produce the same identifier, the script keeps the first. Atmospheric Stability is listed under both Weather and Remote Sensing but keeps only one parent; Infectious Disease appears twice.

## Suggested next steps

- Fix the prefixes, permanent identifiers and term addresses (issues 1–3) before anyone tags with the CURIEs. Use [curies](https://pypi.org/project/curies/) for all prefix management.
- Move the mappings into a separate SSSOM table with a match strength per row, starting from Jennifer's first pass.
- Switch the terms from classes to a LinkML value set.
- Agree a short shared list of identifiers for the common environmental variables, so HEW's `measured_property` and EnVar's `standard_name` match.
- Try the automatic theme derivation on one Amadeus dataset, end to end.