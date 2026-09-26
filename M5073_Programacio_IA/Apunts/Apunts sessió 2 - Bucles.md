# Sessió 2: Bucles i Estructures Iteratives

Les estructures iteratives (o bucles) s'utilitzen en programació per executar un bloc de codi múltiples vegades de manera automàtica, evitant la repetició manual i optimitzant el flux d'execució.

---

## 1. El Bucle `for`

El bucle `for` s'utilitza principalment quan coneixem d'antemanat el nombre de vegades que volem repetir una acció o quan volem recórrer una seqüència d'elements (llistes, rangs, cadenes de text, etc.).

### Sintaxi bàsica
```python
for variable in seqüència:
    # Codi a executar en cada iteració
```

---

## 2. La Funció `range()`

La funció `range()` genera una seqüència immutable de números enters. S'utilitza sovint al costat del bucle `for`.

### Formes d'ús de `range()`:

1. **`range(stop)`**: Genera des de `0` fins a `stop - 1`.
   ```python
   list(range(3))  # Resultat: [0, 1, 2]
   ```
2. **`range(start, stop)`**: Genera des de `start` fins a `stop - 1`.
   ```python
   list(range(10, 15))  # Resultat: [10, 11, 12, 13, 14]
   ```
3. **`range(start, stop, step)`**: Genera des de `start` fins a `stop - 1` incrementant o decrementant segons el valor de `step`.
   ```python
   list(range(10, 20, 2))  # Resultat: [10, 12, 14, 16, 18]
   list(range(10, 0, -2))  # Resultat: [10, 8, 6, 4, 2]
   ```

---

## 3. El Bucle `while`

El bucle `while` executa un bloc de codi **mentre una condició lògica es mantingui com a vertadera (`True`)**. És ideal quan no sabem exactament quantes vegades s'executarà el bucle.

### Sintaxi
```python
numero = 3
while numero > 0:
    print(f"El valor actual és: {numero}")
    numero -= 1  # Decrement necessari per evitar un bucle infinit
```

> **Atenció:** Sempre cal assegurar-se que la condició acabi sent `False` en algun moment per evitar un **bucle infinit**.