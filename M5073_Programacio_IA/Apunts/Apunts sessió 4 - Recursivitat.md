# Sessió 4: Introducció a la Recursivitat

La **recursivitat** és una tècnica de programació on una funció **es crida a si mateixa** per resoldre un problema dividint-lo en subproblemes més petits i similars.

---

## 1. Components d'una Funció Recursiva

Tota funció recursiva ha de tenir obligatòriament dues parts:

1. **Cas Base:** Condició d'aturada que evita crides infinites i retorna un valor directe.
2. **Cas Recursiu:** La crida a la mateixa funció, modificant els paràmetres per reduir la mida del problema i apropar-se al cas base.

---

## 2. Quan és Útil la Recursivitat?

* Problemes matemàtics definits de forma recursiva (Factorial, Fibonacci).
* Exploració d'estructures de dades jeràrquiques (arbres, grafs, sistemes de fitxers).
* Algorismes de cerca i ordenació (Divide i Venceràs).

---

## 3. Exemples Pràctics

### A) Càlcul del Factorial ($n!$)

* **Definició Matemàtica:** $n! = n \times (n-1)!$ amb $0! = 1$
* **Comparativa:**

```python
# Iteratiu
def factorial_iteratiu(n: int) -> int:
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

# Recursiu
def factorial_recursiu(n: int) -> int:
    if n == 0 or n == 1:  # Cas Base
        return 1
    return n * factorial_recursiu(n - 1)  # Cas Recursiu
```

### B) Invertir una Cadena de Text

```python
def cadena_inversa(mot: str) -> str:
    if len(mot) == 0:  # Cas base
        return ""
    # Agafem l'últim caràcter i el concatenem amb la crida per a la resta
    return mot[-1] + cadena_inversa(mot[:-1])

# Exemple: cadena_inversa("Hola") -> "aloH"
```

### C) Conversió a Codi ASCII formatat

```python
def cadena_ascii(mot: str) -> str:
    if len(mot) == 0:
        return ""
    elif len(mot) == 1:
        return str(ord(mot[0]))
    return str(ord(mot[0])) + " - " + cadena_ascii(mot[1:])
```

### D) Suma de Números Senars en un Array

```python
def suma_array_parells(llista: list[int]) -> int:
    if len(llista) == 0:
        return 0
    
    # Si és senar el sumem, si és parell sumem 0
    valor_actual = llista[0] if llista[0] % 2 != 0 else 0
    return valor_actual + suma_array_parells(llista[1:])
```