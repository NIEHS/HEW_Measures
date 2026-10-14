---
search:
  boost: 10.0
---

# Class: Land 


_Subcategory: Land_



<div data-search-exclude markdown="1">



URI: [vocab:Land](https://w3id.org/hew/measures/Land)





```mermaid
 classDiagram
    class Land
    click Land href "../Land/"
      Environment <|-- Land
        click Environment href "../Environment/"
      

      Land <|-- Vegetation
        click Vegetation href "../Vegetation/"
      Land <|-- LandSurface
        click LandSurface href "../LandSurface/"
      

      
```





## Inheritance
* [Category](Category.md)
    * [Environment](Environment.md)
        * **Land**
            * [Vegetation](Vegetation.md)
            * [LandSurface](LandSurface.md)


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |















## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/hew/measures/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vocab:Land |
| native | vocab:Land |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Land
description: 'Subcategory: Land'
from_schema: https://w3id.org/hew/measures/schema
is_a: Environment

```
</details>

### Induced

<details>
```yaml
name: Land
description: 'Subcategory: Land'
from_schema: https://w3id.org/hew/measures/schema
is_a: Environment

```
</details></div>