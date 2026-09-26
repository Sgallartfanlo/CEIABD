# Exercicis de Programació - Sessió 0

Recopilació d'exercicis pràctics d'introducció a Python.

---

## Exercici 1: Suma senzilla

Crea un programa que defineixi dues variables amb nombres enters i mostri per pantalla la seva suma.

```python
num1 = 3
num2 = 2
print(num1 + num2)

```

---

## Exercici 2: Multiplicació i resta

Fes un programa que guardi dos nombres en variables i mostri per pantalla la seva multiplicació i també la seva resta.

```python
num1 = 10
num2 = 7

multiplicacio = num1 * num2
resta = num1 - num2

print(f"El resultat de {num1} multiplicat per {num2} és: {multiplicacio}")
print(f"El resultat de {num1} restat per {num2} és: {resta}")

```

---

## Exercici 3: Àrea d'una circumferència

Calcula l'àrea d'una **circumferència** desant el seu radi en una variable. **Fes servir la llibreria `math` per obtenir el número PI.**

$$\text{Àrea} = 2 \times \pi \times \text{radi}$$

* [Documentació de la llibreria `math](https://www.google.com/search?q=https://docs.python.org/3/library/math.html%23)`
* [Com fer servir la llibreria `math](https://www.w3schools.com/python/ref_math_pi.asp)`

```python
import math

radi = float(input("Introdueix un radi per la circumferència: "))
area = 2 * math.pi * radi

print(f"L'àrea és: {area}")

```

---

## Exercici 4: Condició simple

Escriu un programa que guardi en una variable l'edat d'una persona. El programa ha d'imprimir "Ets major d'edat" si té 18 anys o més, i "Ets menor d'edat" en cas contrari.

```python
edat = int(input("Introdueix la teva edat: "))

if edat >= 18:
    print("Ets major d'edat")
else:
    print("Ets menor d'edat")

```

---

## Exercici 5: Longitud d’una cadena

Fes un programa que guardi una paraula en una variable i mostri per pantalla quantes lletres té.

```python
paraula = str(input("Introdueix una paraula: "))
print(len(paraula))

```

---

## Exercici 6: Cadena en majúscules

Escriu un programa que guardi un text en una variable i mostri:

1. El text original.
2. El mateix text en majúscules.

```python
paraula = str(input("Introdueix una paraula: "))
majus = paraula.upper()

print(f"Paraula normal: {paraula}")
print(f"Paraula en majúscules: {majus}")

```

---

## Exercici 7: Màquina expenedora

Crea un programa que simuli una màquina expenedora amb 3 opcions:

* **Aigua:** 1.0 €
* **Refresc:** 1.5 €
* **Suc:** 2.0 €

El programa ha de:

1. Mostrar el menú.
2. Demanar al client quina beguda vol.
3. Demanar amb quants diners paga.
4. Indicar si els diners són suficients i calcular el canvi.

```python
aigua = 1.0
refresc = 1.5
suc = 2.0

print("1. Aigua (1 €)")
print("2. Refresc (1.5 €)")
print("3. Suc (2 €)")

item = int(input("Quina opció esculls: "))

preu_beguda = 0
nom_beguda = ""

if item == 1:
    nom_beguda = "Aigua"
    preu_beguda = aigua
elif item == 2:
    nom_beguda = "Refresc"
    preu_beguda = refresc
elif item == 3:
    nom_beguda = "Suc"
    preu_beguda = suc
else:
    print("Opció no vàlida.")

if preu_beguda > 0:
    print(f"Has escollit {nom_beguda}")
    diners = float(input("Amb quants diners pagaràs? "))

    if diners >= preu_beguda:
        canvi = diners - preu_beguda
        print("Tens diners suficients.")
        print(f"El teu canvi és de {canvi:.2f} €")
    else:
        print("No tens diners suficients.")
else:
    print("No s'ha pogut processar la comanda.")

```

---

## Exercici 8: Comptador de vocals

Fes un programa que, donat una cadena de text (`String`), imprimeixi per pantalla el número de vocals que ha trobat.

```python
# Demanem el text a l'usuari
text = input("Introdueix una cadena de text: ")

# Definim quines són les vocals (tant en minúscules com en majúscules)
vocals = "aeiouaéèíóòúüAEIOUAÉÈÍÓÒÚÜ"

# Comptem quantes vocals hi ha al text
comptador = 0
for caracter in text:
    if caracter in vocals:
        comptador += 1

# Imprimim el resultat
print(f"El número de vocals que s'han trobat és: {comptador}")

```

---

## Exercici 9: Anàlisi de la primera lletra d'una frase

Donada una frase:

* Si comença per **vocal**, retorna el número de vocals.
* Si comença per **consonant**, retorna el número de consonants.

> **Requisits:**
> * S'ha de fer servir com a mínim 1 funció.
> * Cal tenir en compte si la cadena de text no comença ni per vocal ni per consonant.

```python
def comptar_vocals(text):
    vocals = "aeiouàèéíòóúüAEIOUÀÈÉÍÒÓÚÜ"
    return sum(1 for caracter in text if caracter in vocals)

def comptar_consonants(text):
    consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZçÇ"
    return sum(1 for caracter in text if caracter in consonants)

def analitzar_frase(frase):
    # Eliminem espais en blanc a l'inici per seguretat
    frase_neta = frase.strip()

    if not frase_neta:
        return "La frase està buida."

    primer_caracter = frase_neta[0]

    # Definim els conjunts de referència per a la primera lletra
    vocals_inicials = "aeiouàèéíòóúüAEIOUÀÈÉÍÒÓÚÜ"
    consonants_inicials = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZçÇ"

    if primer_caracter in vocals_inicials:
        num_vocals = comptar_vocals(frase_neta)
        return f"Comença per vocal. Total de vocals a la frase: {num_vocals}"

    elif primer_caracter in consonants_inicials:
        num_consonants = comptar_consonants(frase_neta)
        return f"Comença per consonant. Total de consonants a la frase: {num_consonants}"

    else:
        return "Error: La frase no comença ni per vocal ni per consonant (comença per un número, símbol o espai)."

# --- Exemples d'ús ---
print(analitzar_frase("Hola món!"))
print(analitzar_frase("Avui fa bon dia."))
print(analitzar_frase("123 Hola"))
