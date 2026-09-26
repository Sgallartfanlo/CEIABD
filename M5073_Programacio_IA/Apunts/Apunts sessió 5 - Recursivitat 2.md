# Sessió 5: Recursivitat Avançada i Estructures Arborescents

Quan treballem amb **estructures de dades anidades** (com diccionaris que contenen altres diccionaris o llistes), el nombre de nivells no és fix. En aquests casos, els bucles tradicionals no funcionen i la **recursivitat** és la millor eina.

---

## 1. Model de Dades: Sistema de Fitxers Anidat

Imaginem un diccionari que representa directoris i arxius:

```python
filesystem = {
    "home": {
        "user": {
            "documents": {
                "projects": {
                    "python": {
                        "readme.txt": "Exemple de recursivitat",
                        "main.py": "print('Hola!')"
                    }
                },
                "notes.txt": "Repassar recursivitat"
            }
        }
    }
}
```

---

## 2. Cerca en Profunditat (Depth-First Search - DFS)

L'objectiu és trobar el camí (*path*) cap a un element objectiu dins d'un diccionari anidat.

```python
def cerca_profunditat(data, objectiu, path=None) -> list:
    if path is None:
        path = []

    # Cas 1: L'element és un diccionari
    if isinstance(data, dict):
        for clau, valor in data.items():
            nou_cami = path + [clau]

            if clau == objectiu:
                return nou_cami

            resultat_parcial = cerca_profunditat(valor, objectiu, nou_cami)
            if resultat_parcial is not None:
                return resultat_parcial

    # Cas 2: L'element és una llista
    if isinstance(data, list):
        for item in data:
            if item == objectiu:
                return path + [item]

    return None
```

---

## 3. Obtenir Contingut d'un Node Recursivament

Aquesta funció busca una clau en qualsevol nivell de la jerarquia i retorna el seu valor:

```python
def obtenir_contingut(diccionari, objectiu):
    if isinstance(diccionari, dict):
        for clau, valor in diccionari.items():
            if clau == objectiu:
                return valor

            # Crida recursiva cap als sub-nivells
            res = obtenir_contingut(valor, objectiu)
            if res is not None:
                return res

    return None
```