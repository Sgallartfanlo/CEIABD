# Sessió 3: Arrays i Llistes Multidimensionals

En Python, les estructures que anomenem de forma genèrica *arrays* es representen habitualment mitjançant **llistes**. Una llista és una col·lecció ordenada, mutable (modificable) i que permet elements duplicats.

---

## 1. Concepte i Dimensions

* **Unidimensional (1D):** Llista simple d'elements.
  ```python
  fruites = ["Poma", "Pera", "Plàtan", "Kiwi"]
  ```

* **Bidimensional (2D):** Llista de llistes (matriu de files i columnes).
  ```python
  coordenades = [
      [13, 20],
      [19, 3],
      [4, 23]
  ]
  ```

---

## 2. Formes de Recórrer un Array Unidimensional

### A) Bucle `for ... in` (Directe)
Recorrem directament els elements de la llista.
```python
fruites = ["Poma", "Pera", "Plàtan", "Kiwi"]
for fruita in fruites:
    print(fruita)
```

### B) Bucle `for` amb índex i `range()`
Recorrem les posicions numèriques de la llista.
```python
fruites = ["Poma", "Pera", "Plàtan", "Kiwi"]
for index in range(len(fruites)):
    print(f"Posició {index}: {fruites[index]}")
```

### C) Bucle `while`
```python
fruites = ["Poma", "Pera", "Plàtan", "Kiwi"]
index = 0
while index < len(fruites):
    print(fruites[index])
    index += 1
```

---

## 3. Arrays Multidimensionals (2D o més)

Per iterar sobre un array bidimensional utilitzem **bucles anidats**:

```python
matriu = [
    ["Pera", "Poma"],
    ["Plàtan", "Maduixa"],
    ["Sergio", "Pesao"]
]

# Recorregut per índexs de files i columnes
for fila in range(len(matriu)):
    print(f"\n--- Processant Fila {fila + 1} ---")
    for columna in range(len(matriu[fila])):
        print(f"Element a [{fila}][{columna}] -> {matriu[fila][columna]}")
```