# Apunts Extensos de NumPy i Exercicis Resolts

**NumPy** (Numerical Python) és la llibreria fonamental per al càlcul científic, la ciència de dades i l'aprenentatge automàtic en Python. El seu element central és l'array multidimensional, conegut com a `ndarray`. 

Aquesta estructura permet emmagatzemar dades numèriques de forma contigua en memòria i executar operacions matemàtiques vectoritzades a gran velocitat, evitant l'ús de bucles explícits en Python (`for` / `while`).

---

## Part 1: Teoria Extensa

### 1. Creació d'Arrays i Atributs Fonamentals

Un array de NumPy es pot crear a partir de llistes existents o mitjançant funcions generadores d'inicialització:

- `np.array(objecte)`: Converteix llistes o tuples en un array.
- `np.zeros(shape)`: Crea un array omplert de zeros de la forma (shape) especificada.
- `np.ones(shape)`: Crea un array omplert d'uns.
- `np.arange(inici, fi, pas)`: Genera valors espaiats uniformement segons un pas definit (exclou el valor final `fi`).
- `np.linspace(inici, fi, num)`: Genera $n$ valors distribuïts de manera uniforme en un interval tancat $[inici, fi]$.
- `np.random.rand(d0, d1, ...)`: Genera valors aleatoris reals provinents d'una distribució uniforme en l'interval $[0, 1)$.
- `np.random.randint(low, high, size)`: Genera nombres enters aleatoris a l'interval $[low, high)$.

#### Atributs Clau d'un `ndarray`

```python
import numpy as np

arr = np.zeros((3, 4))

print("Forma (shape):", arr.shape)       # (3, 4) -> 3 files i 4 columnes
print("Dimensions (ndim):", arr.ndim)     # 2 -> matriu bidimensional
print("Tipus de dades (dtype):", arr.dtype)# float64
print("Total d'elements (size):", arr.size)# 12 elements
```

---

### 2. Tipus de Dades (`dtype`) i Conversió

A diferència de les llistes de Python, **tots els elements d'un array de NumPy han de ser del mateix tipus de dades (homogenis)**. Això permet optimitzar l'ús de memòria i utilitzar operacions vectoritzades a nivell de C.

- **Tipus habituals:** `int32`, `int64`, `float32`, `float64`, `bool`, `str_`.
- **Conversió explicitat amb `astype()`:** Permet canviar el tipus de dades d'un array. Genera una còpia de l'array amb el nou tipus.

```python
x = np.array([0.5, 1.2, 2.9])
x_int = x.astype(int)  # Resultat: [0, 1, 2] (trunca la part decimal)
```

---

### 3. Indexació, Slicing i Fancy Indexing

L'accés a les dades es fa mitjançant claudàtors `[]`:

- **Arrays 1D:** `a[índex]` o `a[inici:fi:pas]`.
- **Arrays 2D:** `b[fila, columna]`.
- **Slicing multidimensional:** `b[files_inici:files_fi, cols_inici:cols_fi]`. Per exemple, `b[:, -1]` extreu l'última columna completa.

#### Indexació Avançada (*Fancy Indexing*)

Consisteix a passar llistes o arrays d'enters per seleccionar posicions específiques no consecutives:

```python
X = np.arange(16).reshape(4, 4)

# Seleccionar les posicions (0,1), (2,3) i (3,0)
rows = [0, 2, 3]
cols = [1, 3, 0]

resultat = X[rows, cols]  # [1, 11, 12]
```

---

### 4. Operacions Aritmètiques i Broadcasting

Totes les operacions d'aritmètica bàsica (`+`, `-`, `*`, `/`, `**`) s'executen **element a element** (*element-wise*).

- **Producte de matrius (àlgebra lineal):** Utilitza l'operador `@` o la funció `np.dot(A, B)`.

#### Broadcasting

El **broadcasting** és el mecanisme que permet a NumPy realitzar operacions aritmètiques entre arrays de diferents formes (*shapes*) sense duplicar dades en memòria.

**Regla de Broadcasting:** Dues dimensions són compatibles quan són iguals o quan una d'elles és igual a 1.

```python
M = np.zeros((4, 3))    # Matriu 4x3
v = np.array([1, 2, 3]) # Vector 1x3

# El vector 'v' s'expandeix virtualment a 4 files per poder sumar-se a 'M'
resultat = M + v
```

---

### 5. Funcions Universals (*ufuncs*)

Les *ufuncs* són funcions altament optimitzades que s'apliquen sobre tots els elements d'un array de forma vectoritzada:

- **Matemàtiques:** `np.sqrt()`, `np.exp()`, `np.log()`, `np.sin()`, `np.cos()`.
- **Condicionals:** `np.where(condicio, valor_si_cert, valor_si_fals)`.

```python
x = np.array([0, 1, 4, 9])
print(np.sqrt(x)) # [0., 1., 2., 3.]
```

---

### 6. Agregacions, Estadística i Mascaretes Booleanes

NumPy proporciona funcions per reduir dimensions calculant valors resum:

- `sum()`, `mean()`, `std()`, `var()`, `max()`, `min()`.
- **Paràmetre `axis`:** 
  - `axis=0`: Opera al llarg de les files (calcula resultats per a cada columna).
  - `axis=1`: Opera al llarg de les columnes (calcula resultats per a cada fila).

#### Mascaretes Booleanes

S'utilitzen condicions per crear un array de valors booleans (`True`/`False`) que serveixen per filtrar o modificar valors:

```python
x = np.arange(10)
mascareta = (x % 2 == 0) # [True, False, True, False, ...]
x[mascareta] = -1         # Canvia tots els nombres parells per -1
```

---

### 7. Reorganització i Manipulació d'Arrays

- `reshape((fil, col))`: Canvia la forma de l'array sense modificar les dades en memòria.
- `ravel()`: Aplatana un array a 1D retornant una **vista** (*view*). Les modificacions afecten l'array original.
- `flatten()`: Aplatana un array a 1D retornant una **còpia** independent.
- `np.tile(v, n)`: Repeteix el bloc del vector $n$ vegades de manera global.
- `np.repeat(v, n)`: Repeteix cada element individual del vector $n$ vegades consecutives.

---

### 8. Aleatorietat

El submòdul `np.random` permet generació de nombres aleatoris i simulacions:

- `np.random.seed(n)`: Fixa la llavor aleatòria per fer els experiments reproduïbles.
- `np.random.rand(d0, d1)`: Valors uniformes en el rang $[0, 1)$.
- `np.random.randint(low, high, size)`: Valors enters en l'interval $[low, high)$.

---

## Part 2: Exercicis Resolts Pas a Pas

### Nivell 1 — Bàsic

#### Exercici 1: Creació d'arrays
*Crea un array 1D amb els enters de l'1 al 10 i un array 2D de forma (3,4) amb els enters del 0 a l'11.*

```python
import numpy as np

# 1. Array 1D de l'1 al 10
array_1d = np.arange(1, 11)

# 2. Array 2D de 3 files i 4 columnes del 0 a l'11
array_2d = np.arange(12).reshape(3, 4)

print("Array 1D:\n", array_1d)
print("\nArray 2D (3x4):\n", array_2d)
```

---

#### Exercici 2: Tipus i `astype`
*Crea un array de floats `[0.5, 1.0, 2.5]` i converteix-lo a enters.*

```python
import numpy as np

# Definició de l'array de tipus float
x_float = np.array([0.5, 1.0, 2.5])

# Conversió a enters (els decimals es truncen)
x_int = x_float.astype(int)

print("Array de floats:", x_float)
print("Tipus d'origen:", x_float.dtype)
print("Array convertit a int:", x_int)
print("Nou tipus:", x_int.dtype)
```

---

#### Exercici 3: Indexació i slicing
*Donat `b` de l'exercici 1, extreu la segona fila, l'última columna i un subarray que sigui les files 0:2 i columnes 1:3.*

```python
import numpy as np

b = np.arange(12).reshape(3, 4)

# 1. Segona fila (índex 1)
segona_fila = b[1]

# 2. Última columna (índex -1 a la segona dimensió)
ultima_columna = b[:, -1]

# 3. Subarray amb files 0 a 1 i columnes 1 a 2 (el límit superior és excloent)
subarray = b[0:2, 1:3]

print("Matriu b original:\n", b)
print("\nSegona fila:", segona_fila)
print("Última columna:", ultima_columna)
print("Subarray (files 0:2, cols 1:3):\n", subarray)
```

---

#### Exercici 4: Operacions aritmètiques bàsiques
*Donats `a = [1,2,3]` i `b = [4,5,6]`, calcula la suma, resta, producte element a element i divisió.*

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("Suma (a + b):", a + b)
print("Resta (a - b):", a - b)
print("Producte element a element (a * b):", a * b)
print("Divisió (a / b):", a / b)
```

---

#### Exercici 5: Funcions universals (*ufuncs*)
*Aplica `np.sqrt`, `np.exp` i `np.sin` a un array `x = [0, 1, 4, 9]`.*

```python
import numpy as np

x = np.array([0, 1, 4, 9])

arrel_quadrada = np.sqrt(x)
exponencial = np.exp(x)
sinus = np.sin(x)

print("Array x:", x)
print("np.sqrt(x):", arrel_quadrada)
print("np.exp(x):", exponencial)
print("np.sin(x):", sinus)
```

---

### Nivell 2 — Intermedi

#### Exercici 6: Broadcasting
*Suma el vector `[1,2,3]` a cada fila de la matriu `M = np.zeros((4,3))` utilitzant broadcasting.*

```python
import numpy as np

M = np.zeros((4, 3))
v = np.array([1, 2, 3])

# Broadcasting: NumPy adapta v (forma 1x3) a la matriu M (forma 4x3)
resultat = M + v

print("Matriu M (zeros):\n", M)
print("\nVector v:", v)
print("\nResultat de M + v (broadcasting):\n", resultat)
```

---

#### Exercici 7: Agregacions
*Per a `b` de l'exercici 1, calcula: `suma total`, `suma per fila`, `mitjana per columna`, `valor màxim` i `mínim`.*

```python
import numpy as np

b = np.arange(12).reshape(3, 4)

suma_total = b.sum()
suma_per_fila = b.sum(axis=1)      # Opera al llarg de les columnes
mitjana_per_columna = b.mean(axis=0)# Opera al llarg de les files
valor_max = b.max()
valor_min = b.min()

print("Matriu b:\n", b)
print("\nSuma total de tots els elements:", suma_total)
print("Suma per fila (axis=1):", suma_per_fila)
print("Mitjana per columna (axis=0):", mitjana_per_columna)
print("Valor màxim:", valor_max)
print("Valor mínim:", valor_min)
```

---

#### Exercici 8: Mascaretes booleanes
*Donat un array `x = np.arange(10)`, selecciona els elements parells i substitueix-los per -1.*

```python
import numpy as np

x = np.arange(10)
print("Array x inicial:", x)

# Condició booleana per detectar els nombres parells
mascareta_parells = (x % 2 == 0)

# Substitució directe usant la mascareta
x[mascareta_parells] = -1

print("Array x modificat:", x)
```

---

#### Exercici 9: `where`
*Crea un array `a = np.random.randint(0, 10, 10)`. Utilitza `np.where` per crear un nou array que sigui `"parell"` quan l'element és parell i `"senar"` quan és senar.*

```python
import numpy as np

# Fixem una llavor per a la reproductibilitat de l'exercici
np.random.seed(42)

a = np.random.randint(0, 10, 10)

# np.where(condició, valor_si_cert, valor_si_fals)
resultat = np.where(a % 2 == 0, "parell", "senar")

print("Array d'enters aleatoris a:", a)
print("Array de text classificat:", resultat)
```

---

#### Exercici 10: Ordenació i `argsort`
*Ordena un array 1D `x = [3,1,2]` i troba els índexs que ordenarien l'array.*

```python
import numpy as np

x = np.array([3, 1, 2])

# Retorna els índexs de les posicions originals que ordenarien l'array
indexs_ordenats = np.argsort(x)

# Genera una còpia de l'array amb els valors ordenats
x_ordenat = np.sort(x)

print("Array original x:", x)
print("Índexs que ordenen l'array (argsort):", indexs_ordenats)
print("Array ordenat (sort):", x_ordenat)
```

---

### Nivell 3 — Avançat

#### Exercici 11: Reshape i `ravel`
*Converteix un array 1D de 12 elements en (3,4), i després torna'l a 1D utilitzant `ravel()` i `flatten()`; explica breument la diferència.*

```python
import numpy as np

arr = np.arange(12)
arr_2d = arr.reshape(3, 4)

# Aplatana l'array tornant una VISTA
arr_ravel = arr_2d.ravel()

# Aplatana l'array tornant una CÒPIA
arr_flatten = arr_2d.flatten()

print("Array 2D (3x4):\n", arr_2d)
print("\nResultat de ravel():", arr_ravel)
print("Resultat de flatten():", arr_flatten)

# Demostració de la diferència en memòria:
arr_ravel[0] = 999
print("\nDesprés de modificar el primer element de ravel():")
print("Array 2D original (s'ha après de la modificació): \n", arr_2d)
print("Array flatten (no s'ha après perquè és una còpia):", arr_flatten)
```

**Explicació:**
- `ravel()` retorna una **vista** (*view*) de l'array original si és possible. Modificar l'array resultat altera directament les dades de l'array d'origen sense requerir memòria addicional.
- `flatten()` allocated una nova zona de memòria per crear una **còpia** (*copy*) independent. Els canvis realitzats en la còpia no afecten l'array original.

---

#### Exercici 12: Producte punt i matriu
*Crea matrius `A` (2x3) i `B` (3x2) amb valors aleatoris i calcula `A @ B`.*

```python
import numpy as np

np.random.seed(0)

# Creació de les matrius amb valors aleatoris reals
A = np.random.rand(2, 3)
B = np.random.rand(3, 2)

# Producte matricial (2x3) x (3x2) -> Matriu resultat de (2x2)
C = A @ B  # També equival a np.dot(A, B)

print("Matriu A (2x3):\n", A)
print("\nMatriu B (3x2):\n", B)
print("\nProducte Matricial A @ B (2x2):\n", C)
```

---

#### Exercici 13: Indexació avançada (*fancy indexing*)
*Donat `X = np.arange(16).reshape(4,4)`, extreu les posicions (0,1), (2,3) i (3,0) utilitzant fancy indexing.*

```python
import numpy as np

X = np.arange(16).reshape(4, 4)

# Definició de les coordenades
files = [0, 2, 3]
columnes = [1, 3, 0]

# Extracció simultània de les posicions X[0,1], X[2,3] i X[3,0]
valors_extrets = X[files, columnes]

print("Matriu X (4x4):\n", X)
print("\nValors extrets a les posicions (0,1), (2,3) i (3,0):", valors_extrets)
```

---

#### Exercici 14: `tile` i `repeat`
*Donat `v = [1,2]`, utilitza `np.tile` i `np.repeat` per produir:*
- *tile:* `[1, 2, 1, 2, 1, 2]`
- *repeat:* `[1, 1, 1, 2, 2, 2]`

```python
import numpy as np

v = np.array([1, 2])

# tile: repeteix el bloc complet de l'array 3 vegades
res_tile = np.tile(v, 3)

# repeat: repeteix cada element de l'array 3 vegades de forma consecutiva
res_repeat = np.repeat(v, 3)

print("Vector original v:", v)
print("np.tile(v, 3):  ", res_tile)
print("np.repeat(v, 3):", res_repeat)
```