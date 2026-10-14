---
search:
  boost: 10.0
---

# Class: Category 


_Root abstraction for all vocabulary domains._



<div data-search-exclude markdown="1">


* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [vocab:Category](https://w3id.org/hew/measures/Category)





```mermaid
 classDiagram
    class Category
    click Category href "../Category/"
      Category <|-- Health
        click Health href "../Health/"
      Category <|-- Environment
        click Environment href "../Environment/"
      Category <|-- Social
        click Social href "../Social/"
      Category <|-- Exposures
        click Exposures href "../Exposures/"
      
      
```





## Inheritance
* **Category**
    * [Health](Health.md)
    * [Environment](Environment.md)
    * [Social](Social.md)
    * [Exposures](Exposures.md)


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |















## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/hew/measures/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vocab:Category |
| native | vocab:Category |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Category
description: Root abstraction for all vocabulary domains.
from_schema: https://w3id.org/hew/measures/schema
abstract: true

```
</details>

### Induced

<details>
```yaml
name: Category
description: Root abstraction for all vocabulary domains.
from_schema: https://w3id.org/hew/measures/schema
abstract: true

```
</details></div>