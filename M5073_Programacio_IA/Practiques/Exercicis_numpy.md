# Apunts Extensos de NumPy

**NumPy** (Numerical Python) és la llibreria fonamental per al càlcul científic, la ciència de dades i l'aprenentatge automàtic en Python. El seu element central és l'array multidimensional, conegut com a `ndarray`. 

Aquesta estructura permet emmagatzemar dades numèriques de forma contigua en memòria i executar operacions matemàtiques vectoritzades a gran velocitat, evitant l'ús de bucles explícits en Python (`for` / `while`).

---

## 1. Creació d'Arrays i Atributs Fonamentals

Un array de NumPy es pot crear a partir de llistes existents o mitjançant funcions generadores d'inicialització:

- `np.array(objecte)`: Converteix llistes o tuples en un array.
- `np.zeros(shape)`: Crea un array omplert de zeros de la forma (shape) especificada.
- `np.ones(shape)`: Crea un array omplert d'uns.
- `np.arange(inici, fi, pas)`: Genera valors espaiats uniformement segons un pas definit (exclou el valor final `fi`).
- `np.linspace(inici, fi, num)`: Genera $n$ valors distribuïts de manera uniforme en un interval tancat $[inici, fi]$.
- `np.random.rand(d0, d1, ...)`: Genera valors aleatoris reals provinents d'una distribució uniforme en l'interval $[0, 1)$.
- `np.random.randint(low, high, size)`: Genera nombres enters aleatoris a l'interval $[low, high)$.

### Atributs Clau d'un `ndarray`

```python
import numpy as np

arr = np.zeros((3, 4))

print("Forma (shape):", arr.shape)       # (3, 4) -> 3 files i 4 columnes
print("Dimensions (ndim):", arr.ndim)     # 2 -> matriu bidimensional
print("Tipus de dades (dtype):", arr.dtype)# float64
print("Total d'elements (size):", arr.size)# 12 elements
```

---

## 2. Tipus de Dades (`dtype`) i Conversió

A diferència de les llistes de Python, **tots els elements d'un array de NumPy han de ser del mateix tipus de dades (homogenis)**. Això permet optimitzar l'ús de memòria i utilitzar operacions vectoritzades a nivell de C.

- **Tipus habituals:** `int32`, `int64`, `float32`, `float64`, `bool`, `str_`.
- **Conversió explicitat amb `astype()`:** Permet canviar el tipus de dades d'un array. Genera una còpia de l'array amb el nou tipus.

```python
x = np.array([0.5, 1.2, 2.9])
x_int = x.astype(int)  # Resultat: [0, 1, 2] (trunca la part decimal)
```

---

## 3. Indexació, Slicing i Fancy Indexing

L'accés a les dades es fa mitjançant claudàtors `[]`:

- **Arrays 1D:** `a[índex]` o `a[inici:fi:pas]`.
- **Arrays 2D:** `b[fila, columna]`.
- **Slicing multidimensional:** `b[files_inici:files_fi, cols_inici:cols_fi]`. Per exemple, `b[:, -1]` extreu l'última columna completa.

### Indexació Avançada (*Fancy Indexing*)

Consisteix a passar llistes o arrays d'enters per seleccionar posicions específiques no consecutives:

```python
X = np.arange(16).reshape(4, 4)

# Seleccionar les posicions (0,1), (2,3) i (3,0)
rows = [0, 2, 3]
cols = [1, 3, 0]

resultat = X[rows, cols]  # [1, 11, 12]
```

---

## 4. Operacions Aritmètiques i Broadcasting

Totes les operacions d'aritmètica bàsica (`+`, `-`, `*`, `/`, `**`) s'executen **element a element** (*element-wise*).

- **Producte de matrius (àlgebra lineal):** Utilitza l'operador `@` o la funció `np.dot(A, B)`.

### Broadcasting

El **broadcasting** és el mecanisme que permet a NumPy realitzar operacions aritmètiques entre arrays de diferents formes (*shapes*) sense duplicar dades en memòria.

**Regla de Broadcasting:** Dues dimensions són compatibles quan són iguals o quan una d'elles és igual a 1.

```python
M = np.zeros((4, 3))    # Matriu 4x3
v = np.array([1, 2, 3]) # Vector 1x3

# El vector 'v' s'expandeix virtualment a 4 files per poder sumar-se a 'M'
resultat = M + v
```

---

## 5. Funcions Universals (*ufuncs*)

Les *ufuncs* són funcions altament optimitzades que s'apliquen sobre tots els elements d'un array de forma vectoritzada:

- **Matemàtiques:** `np.sqrt()`, `np.exp()`, `np.log()`, `np.sin()`, `np.cos()`.
- **Condicionals:** `np.where(condicio, valor_si_cert, valor_si_fals)`.

```python
x = np.array([0, 1, 4, 9])
print(np.sqrt(x)) # [0., 1., 2., 3.]
```

---

## 6. Agregacions, Estadística i Mascaretes Booleanes

NumPy proporciona funcions per reduir dimensions calculant valors resum:

- `sum()`, `mean()`, `std()`, `var()`, `max()`, `min()`.
- **Paràmetre `axis`:** 
  - `axis=0`: Opera al llarg de les files (calcula resultats per a cada columna).
  - `axis=1`: Opera al llarg de les columnes (calcula resultats per a cada fila).

### Mascaretes Booleanes

S'utilitzen condicions per crear un array de valors booleans (`True`/`False`) que serveixen per filtrar o modificar valors:

```python
x = np.arange(10)
mascareta = (x % 2 == 0) # [True, False, True, False, ...]
x[mascareta] = -1         # Canvia tots els nombres parells per -1
```

---

## 7. Reorganització i Manipulació d'Arrays

- `reshape((fil, col))`: Canvia la forma de l'array sense modificar les dades en memòria.
- `ravel()`: Aplatana un array a 1D retornant una **vista** (*view*). Les modificacions afecten l'array original.
- `flatten()`: Aplatana un array a 1D retornant una **còpia** independent.
- `np.tile(v, n)`: Repeteix el bloc del vector $n$ vegades de manera global.
- `np.repeat(v, n)`: Repeteix cada element individual del vector $n$ vegades consecutives.

---

## 8. Aleatorietat

El submòdul `np.random` permet generació de nombres aleatoris i simulacions:

- `np.random.seed(n)`: Fixa la llavor aleatòria per fer els experiments reproduïbles.
- `np.random.rand(d0, d1)`: Valors uniformes en el rang $[0, 1)$.
- `np.random.randint(low, high, size)`: Valors enters en l'interval $[low, high)$.