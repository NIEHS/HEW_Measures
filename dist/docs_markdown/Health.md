---
search:
  boost: 10.0
---

# Class: Health 


_Root domain for Health_



<div data-search-exclude markdown="1">



URI: [vocab:Health](https://w3id.org/hew/measures/Health)





```mermaid
 classDiagram
    class Health
    click Health href "../Health/"
      Category <|-- Health
        click Category href "../Category/"
      

      Health <|-- HealthData
        click HealthData href "../HealthData/"
      Health <|-- HealthPopulation
        click HealthPopulation href "../HealthPopulation/"
      Health <|-- HealthSystem
        click HealthSystem href "../HealthSystem/"
      Health <|-- HealthCondition
        click HealthCondition href "../HealthCondition/"
      

      
```





## Inheritance
* [Category](Category.md)
    * **Health**
        * [HealthData](HealthData.md)
        * [HealthPopulation](HealthPopulation.md)
        * [HealthSystem](HealthSystem.md)
        * [HealthCondition](HealthCondition.md)


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |















## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/hew/measures/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vocab:Health |
| native | vocab:Health |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Health
description: Root domain for Health
from_schema: https://w3id.org/hew/measures/schema
is_a: Category

```
</details>

### Induced

<details>
```yaml
name: Health
description: Root domain for Health
from_schema: https://w3id.org/hew/measures/schema
is_a: Category

```
</details></div>