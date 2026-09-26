# Apunts: Tipus Enumerats (`Enum`) en Python

Els **Enumerats (`Enum`)** permeten crear un conjunt de constants amb nom que faciliten la llegibilitat, redueixen els errors en introduir cadenes o valors manuals i milloren el manteniment del codi.

Per utilitzar-los cal importar el mòdul `enum`:
```python
from enum import Enum
```

---

## 1. Definició i Ús Bàsic d'un `Enum`

```python
from enum import Enum

class Color(Enum):
    RED = 0
    BLUE = 1

    def traduccio(self, idioma: str) -> str:
        match self:
            case Color.RED:
                match idioma:
                    case "es": return "Rojo"
                    case "en": return "Red"
            case Color.BLUE:
                match idioma:
                    case "es": return "Azul"
                    case "en": return "Blue"
        return "Sense traducció"
```

---

## 2. Enums amb Mètodes de Llogica de Negoci

Podem afegir mètodes als Enums per calcular valors derivats segons la constant seleccionada:

```python
class TipusRoba(Enum):
    HIVERN = 0
    ESTIU = 1
    ENTRETEMPS = 2

    def marca_temporada((self) -> str:
        match self:
            case TipusRoba.HIVERN:
                return "Aquesta peça és d'hivern"
            case TipusRoba.ESTIU:
                return "Aquesta peça és d'estiu"
            case TipusRoba.ENTRETEMPS:
                return "Val per a tot temps!"

    def multiplicador_preu(self) -> float:
        match self:
            case TipusRoba.HIVERN:
                return 1.5
            case _:
                return 1.0
```

---

## 3. Integració d'Enums en Estructures de Dades i Classes

Podem utilitzar membres d'un `Enum` com a claus de diccionari o com a atributs de classe:

```python
class BodyParts(Enum):
    HEAD = "Pepe"
    BODY = "Manolo"
    LEGS = "Juan"

    def multiplicador(self) -> float:
        match self:
            case BodyParts.HEAD: return 2.0
            case _: return 1.0

class Cowboy:
    def __init__(self, vida: int):
        self.vida = vida
        # Ús de membres Enum com a claus de diccionari
        self.body = {
            BodyParts.HEAD: 10,
            BodyParts.BODY: 15,
            BodyParts.LEGS: 20
        }

# Exemple d'ús:
sergio = Cowboy(4)
dany_aplicat = sergio.body[BodyParts.HEAD] - BodyParts.BODY.multiplicador()
```