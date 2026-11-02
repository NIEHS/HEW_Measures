---
search:
  boost: 10.0
---

# Class: Environment 


_Root domain for Environment_



<div data-search-exclude markdown="1">



URI: [vocab:Environment](https://w3id.org/hew/measures/Environment)





```mermaid
 classDiagram
    class Environment
    click Environment href "../Environment/"
      Category <|-- Environment
        click Category href "../Category/"
      

      Environment <|-- RemoteSensing
        click RemoteSensing href "../RemoteSensing/"
      Environment <|-- Land
        click Land href "../Land/"
      Environment <|-- Water
        click Water href "../Water/"
      Environment <|-- Air
        click Air href "../Air/"
      Environment <|-- Wildfire
        click Wildfire href "../Wildfire/"
      Environment <|-- Weather
        click Weather href "../Weather/"
      

      
```





## Inheritance
* [Category](Category.md)
    * **Environment**
        * [RemoteSensing](RemoteSensing.md)
        * [Land](Land.md)
        * [Water](Water.md)
        * [Air](Air.md)
        * [Wildfire](Wildfire.md)
        * [Weather](Weather.md)


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |















## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/hew/measures/schema




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vocab:Environment |
| native | vocab:Environment |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Environment
description: Root domain for Environment
from_schema: https://w3id.org/hew/measures/schema
is_a: Category

```
</details>

### Induced

<details>
```yaml
name: Environment
description: Root domain for Environment
from_schema: https://w3id.org/hew/measures/schema
is_a: Category

```
</details></div>