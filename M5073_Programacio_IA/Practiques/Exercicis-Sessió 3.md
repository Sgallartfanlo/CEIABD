# Exercicis de Programació - Sessió 3

---

## Exercici 1: Llegeix i mostra
Demana a l'usuari que introdueixi 5 números sencers i desa'ls en un array. Després mostra tots els valors per pantalla.

```python
array = []

# Demanem 5 números sencers a l'usuari
for i in range(5):
    valor = int(input(f"Introdueix el valor {i + 1}: "))
    array.append(valor)

# Mostrem els valors per pantalla
print("\nEls valors introduïts són:")
for valor in array:
    print(valor, end=" ")
print()  # Per afegir un salt de línia al final
```

---

## Exercici 2: Suma d'elements
Dona un array de números enters i calcula la suma de tots els seus elements.

```python
numeros = [4, 8, 15, 16, 23, 42]

# Utilitzant la funció sum() de Python
suma = sum(numeros)

print(f"Array: {numeros}")
print(f"La suma de tots els elements és: {suma}")
```

---

## Exercici 3: Valor màxim i mínim
Demana 10 números a l’usuari, guarda’ls en un array i mostra quin és el valor més gran i quin és el més petit.

```python
numeros = []

for i in range(10):
    val = int(input(f"Introdueix el número {i+1}: "))
    numeros.append(val)

print(f"Array introduït: {numeros}")
print(f"El valor màxim és: {max(numeros)}")
print(f"El valor mínim és: {min(numeros)}")
```

---

## Exercici 4: Comptar aparicions
A partir d'una llista de números, cal que l'usuari indiqui un número a cercar. Digues quantes vegades apareix dins l’array.

```python
llista = [2, 5, 8, 2, 9, 2, 7, 5, 1]
cercat = int(input("Indica el número que vols cercar: "))

vegades = llista.count(cercat)

print(f"El número {cercat} apareix {vegades} vegades dins de l'array.")
```

---

## Exercici 5: Invertir array
Demana 8 paraules i desa-les en un array. Mostra-les primer en l’ordre original i després en ordre invers. **Fes una versió fent servir mètodes d'array i un altre fent servir un procediment manual**.

```python
# Demanar 8 paraules
paraules = []
for i in range(8):
    p = input(f"Introdueix la paraula {i+1}: ")
    paraules.append(p)

print(f"\nOrdre original: {paraules}")

# Versió 1: Fent servir mètodes d'array (reverse / slicing)
versio_metode = paraules.copy()
versio_metode.reverse()
print(f"Invertit (amb mètodes): {versio_metode}")

# Versió 2: Procediment manual
versio_manual = []
for i in range(len(paraules) - 1, -1, -1):
    versio_manual.append(paraules[i])
print(f"Invertit (manualment): {versio_manual}")
```

---

## Exercici 6: Eliminar duplicats
Dona un array amb números repetits. Genera un nou array amb els mateixos números però sense duplicats (sense alterar l'ordre d'aparició).

```python
array_duplicats = [4, 2, 4, 7, 2, 8, 1, 7, 9, 4]
sense_duplicats = []

for num in array_duplicats:
    if num not in sense_duplicats:
        sense_duplicats.append(num)

print(f"Original: {array_duplicats}")
print(f"Sense duplicats: {sense_duplicats}")
```

---

## Exercici 7: Fusió ordenada
Demana a l'usuari dos arrays d'enters (ja ordenats). Fusiona'ls en un tercer array que també quedi ordenat.

```python
# Demanem dos arrays d'enters (assumim que s'introdueixen ja ordenats)
array1 = [1, 3, 5, 8]
array2 = [2, 4, 6, 7, 9]

# Algorisme de fusió (merge) mantenint l'ordre
i, j = 0, 0
fusionat = []

while i < len(array1) and j < len(array2):
    if array1[i] < array2[j]:
        fusionat.append(array1[i])
        i += 1
    else:
        fusionat.append(array2[j])
        j += 1

# Afegim els elements restants si en queden
fusionat.extend(array1[i:])
fusionat.extend(array2[j:])

print(f"Array 1: {array1}")
print(f"Array 2: {array2}")
print(f"Array fusionat i ordenat: {fusionat}")
```

---

## Exercici 8: Matriu 2D – Suma de files i columnes
Demana a l’usuari una matriu de 3x3 nombres enters. Calcula i mostra la suma de cada fila i de cada columna.

**Exemple de sortida:**
```python
matriu = [
  [1, 2, 3],
  [2, 3, 4],
  [10, 20, 30]
]
resultat_suma_files = [6, 9, 60]
resultat_suma_columnes = [13, 25, 37]
```

**Codi:**
```python
matriu = []

print("Introdueix els elements de la matriu 3x3:")
for f in range(3):
    fila = []
    for c in range(3):
        val = int(input(f"Fila {f}, Columna {c}: "))
        fila.append(val)
    matriu.append(fila)

# Suma de files
resultat_suma_files = [sum(fila) for fila in matriu]

# Suma de columnes
resultat_suma_columnes = []
for c in range(3):
    suma_col = sum(matriu[f][c] for f in range(3))
    resultat_suma_columnes.append(suma_col)

print("\nMatriu:")
for fila in matriu:
    print(fila)

print(f"resultat_suma_files = {resultat_suma_files}")
print(f"resultat_suma_columnes = {resultat_suma_columnes}")
```

---

## Exercici 9: Desplaçar zeros
Escriu una funció que, donat un array de números enters, desplaci tots els zeros al final, mantenint l'ordre relatiu de la resta d'elements.

**Exemple:**
* **Entrada:** `[3, 0, 8, 0, 5, 3, 0]`
* **Sortida:** `[3, 8, 5, 3, 0, 0, 0]`

**Codi:**
```python
def desplacar_zeros(arr):
    sense_zeros = [num for num in arr if num != 0]
    zeros = [0] * (len(arr) - len(sense_zeros))
    return sense_zeros + zeros

# Exemple d'ús
entrada = [3, 0, 8, 0, 5, 3, 0]
sortida = desplacar_zeros(entrada)

print(f"Entrada: {entrada}")
print(f"Sortida: {sortida}")
```

---

## Exercici 10: Joc del màxim consecutiu
Demana un array d'enters i troba la subseqüència de números consecutius (valors idèntics repetits un darrere l'altre) més llarga. Indica quin número es repeteix i quantes vegades.

**Exemple:**
* **Entrada:** `[1, 1, 1, 2, 3, 4, 4, 4, 4, 4, 7, 8, 8, 8]`
* **Sortida:** `"El valor més repetit és el '4' que es repeteix 5 vegades"`

**Codi:**
```python
def maxim_consecutiu(arr):
    if not arr:
        return None, 0

    max_num = arr[0]
    max_count = 1

    num_actual = arr[0]
    count_actual = 1

    for i in range(1, len(arr)):
        if arr[i] == num_actual:
            count_actual += 1
        else:
            num_actual = arr[i]
            count_actual = 1

        if count_actual > max_count:
            max_count = count_actual
            max_num = num_actual

    return max_num, max_count

# Exemple d'ús
entrada = [1, 1, 1, 2, 3, 4, 4, 4, 4, 4, 7, 8, 8, 8]
num, vegades = maxim_consecutiu(entrada)

print(f"El valor més repetit és el '{num}' que es repeteix {vegades} vegades")
```