**1. Tipus de Dades Bàsics i Declaració**

* **Incialització i reassignació:** Declaració de números enters, decimals, cadenes de text, llistes i diccionaris.


```python
sencer = 12[cite: 4]
real = 12.2[cite: 4]
text3 = "Podem trobar un text entre cometes simples (') o dobles (\")."[cite: 4]
llista = [1,2,3,4][cite: 4]
diccionari = {"Exemple 1": [1,2,3,4], "Exemple 2": ['a', 'b', 'c']}[cite: 4]

```


* **Comprovació de tipus amb `type()`:**

```python
nova_variable = "Exemple"[cite: 4]
print(type(nova_variable)) # <class 'str'>[cite: 4]

investiga_tipus = 10[cite: 4]
if type(investiga_tipus) == int:[cite: 4]
    print(investiga_tipus + 10)[cite: 4]

```



---

**2. Operadors i Formateig de Text**

* **Aritmètica bàsica, divisió entera i residu:**

```python
num1 = 10[cite: 2, 4]
num2 = 7[cite: 2, 4]
print(num1 * num2)  # Multiplicació (70)[cite: 2, 4]
print(num1 - num2)  # Resta (3)[cite: 2, 4]
print(10 // 3)      # Divisió entera (3)[cite: 4]
print(10 % 2)       # Residu (0)[cite: 4]
print(10 ** 2)      # Exponent (100)[cite: 4]

```


* **Lògica i Comparació:** Avaliats com `True` o `False`.


```python
print(10 % 2 == 0 and 10 / 2 == 3)  # AND (False)[cite: 4]
print(10 % 2 == 0 or 10 / 2 == 3)   # OR (True)[cite: 4]
print(not(not(10 % 2 == 0) or 10 / 2 == 3)) # NOT (True)[cite: 4]

```


* **Manipulació de Text (`str`):** Concatenació, majúscules, longitud i f-strings.


```python
paraula = input("Paraula: ")[cite: 2, 4]
print(len(paraula))          # Longitud del text[cite: 2, 4]
print(paraula.upper())       # Text en majúscules[cite: 2, 4]
print(f"Número: {2.15}")    # Formateig amb f-strings[cite: 4]

```



---

**3. Llibreria `math**`

* **Càlcul de l'àrea d'una circumferència:** $Àrea = 2 \times \pi \times radi$

```python
import math[cite: 2, 4]
radi = float(input("Introdueix un radi per la circumferència: "))[cite: 2, 4]
area = 2 * math.pi * radi[cite: 2, 4]
print(f"El area és: {area}")[cite: 2, 4]

```



---

**4. Estructures Condicionals**

* **Avaluació `if / else` i Condicional Ternari:**

```python
# Major d'edat[cite: 2, 4]
edat = int(input("Introdueix la teva edat: "))[cite: 2, 4]
if edat >= 18:[cite: 2, 4]
    print("Ets major d'edat")[cite: 2, 4]
else:[cite: 2, 4]
    print("Ets menor d'edat")[cite: 2, 4]

# Parell / Senar Ternari[cite: 4]
valor = 11[cite: 4]
print("Parell" if valor % 2 == 0 else "Senar")[cite: 4]

```


* **Avaluació `elif` i patró `match`:**

```python
nota = float(input("Introdueix la nota (0-10): "))[cite: 4]
if nota < 5:[cite: 4]
    print("Suspès")[cite: 4]
elif nota < 7:[cite: 4]
    print("Aprovat")[cite: 4]
else:[cite: 4]
    print("Excel·lent")[cite: 4]

# Sintaxi amb match[cite: 4]
match nota:[cite: 4]
    case nota if nota < 5: print("Suspès")[cite: 4]
    case _: print("Aprovat / Notable / Excel·lent")[cite: 4]

```



---

**5. Bucle `for` i Iteracions**

* **Ús de `range()` i `enumerate()`:**

```python
# Iterar en passos de 5[cite: 4]
for x in range(50, 100, 5):[cite: 4]
    print(x)[cite: 4]

# Iterar llista amb índex[cite: 4]
fruites = ["Poma", "Pera", "Maduixa", "Mandarina"][cite: 4]
for index, valor in enumerate(fruites):[cite: 4]
    print(f"La posició {index} conté {valor}")[cite: 4]

```



---

**6. Exercicis de Lògica i Funcions**

* **Màquina expenedora:**

```python
aigua, refresc, suc = 1.0, 1.5, 2.0[cite: 2, 4]
item = int(input("Tria opció (1. Aigua, 2. Refresc, 3. Suc): "))[cite: 2, 4]

preu = aigua if item == 1 else (refresc if item == 2 else (suc if item == 3 else 0))[cite: 2, 4]
if preu > 0:[cite: 2, 4]
    diners = float(input("Diners que entregues: "))[cite: 2, 4]
    if diners >= preu:[cite: 2, 4]
        print(f"Canvi: {diners - preu:.2f} €")[cite: 2, 4]
    else:[cite: 2, 4]
        print("No tens diners suficients.")[cite: 2, 4]

```


* **Comptador de vocals en text:**

```python
text = input("Introdueix un text: ")[cite: 2, 4]
vocals = "aeiouaéèíóòúüAEIOUAÉÈÍÓÒÚÜ"[cite: 2, 4]
comptador = sum(1 for caracter in text if caracter in vocals)[cite: 2, 4]
print(f"Total vocals: {comptador}")[cite: 2, 4]

```


* **Anàlisi de frases segons la primera lletra:**

```python
def comptar_vocals(text):[cite: 2, 4]
    return sum(1 for c in text if c in "aeiouàèéíòóúüAEIOUÀÈÉÍÒÓÚÜ")[cite: 2, 4]

def comptar_consonants(text):[cite: 2, 4]
    return sum(1 for c in text if c in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZçÇ")[cite: 2, 4]

def analitzar_frase(frase):[cite: 2, 4]
    f_neta = frase.strip()[cite: 2, 4]
    if not f_neta: return "Buit"[cite: 2, 4]

    primer = f_neta[0][cite: 2, 4]
    if primer in "aeiouàèéíòóúüAEIOUÀÈÉÍÒÓÚÜ":[cite: 2, 4]
        return f"Vocal. Total vocals: {comptar_vocals(f_neta)}"[cite: 2, 4]
    elif primer in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZçÇ":[cite: 2, 4]
        return f"Consonant. Total consonants: {comptar_consonants(f_neta)}"[cite: 2, 4]
    else:[cite: 2, 4]
        return "Comença per número o símbol"[cite: 2, 4]

print(analitzar_frase("Hola món!"))[cite: 2, 4]

```
