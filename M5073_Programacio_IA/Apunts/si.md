**Introducció a la Programació amb Python (Teoria)**

Python és un llenguatge de programació interpretat, d'alt nivell, multiparadigma (suporta programació imperativa, funcional i orientada a objectes), multiplataforma i de codi lliure.

---

**1. Tipus Bàsics de Variables**

Python permet emmagatzemar diferents tipus de dades sense necessitat de declarar explícitament el seu tipus.

```python
sencer = 12
real = 12.2
text3 = "Podem trobar un text entre cometes simples (') o dobles (\")."
llista = [1, 2, 3, 4]
diccionari = {
  "Exemple 1": [1, 2, 3, 4],
  "Exemple 2": ['a', 'b', 'c']
}

```

* **Identificació de tipus i reassignació:** Es pot utilitzar la funció `type()` per conèixer el tipus d'una variable i redefinir-ne el contingut en qualsevol moment.



```python
nova_variable = "Exemple"
print(type(nova_variable))  # Retorna <class 'str'>

nova_variable = 1  # Redefinició a enter
print(type(nova_variable))  # Retorna <class 'int'>

investiga_tipus = 10
if type(investiga_tipus) == int:
    print(investiga_tipus + 10)
elif type(investiga_tipus) == str:
    print("Això és un string " + investiga_tipus)

```

---

**2. Operadors**

**Operadors Aritmètics**
Retornen un valor numèric com a resultat de l'operació.

```python
5 + 4    # Suma
5 - 4    # Resta
10 / 2   # Divisió
10 // 3  # Divisió entera (mantenint només la part entera)
10 % 2   # Residu de la divisió (mòdul)
10 ** 2  # Exponent

```

**Operadors Relacionals i Condicionals**
Avaluen una comparació i retornen un valor booleà (`True` o `False`).

```python
5 == 4  # Igualtat (False)
5 < 4   # Més petit que (False)
5 <= 4  # Més petit o igual a (False)
5 != 4  # Diferent de (True)

```

**Operadors Lògics**
Permeten combinar o invertir expressions booleanes (`and`, `or`, `not`).

```python
# Operador AND
print((10 % 2 == 0 and 10 / 2 == 3))

# Operador OR
print((10 % 2 == 0 or 10 / 2 == 3))

# Operador NOT (Negació)
print(not(not(10 % 2 == 0) or 10 / 2 == 3))

```

---

**3. Treball amb Cadenes de Text (`str`)**

Les cadenes de text permeten la concatenació directa o la interpolació de valors mitjançant *f-strings*.

```python
# Concatenació
print("Hola " + "Sergio")

# Formateig amb f-strings
print(f"Això és un número: {2.15}")

```

---

**4. Estructures Condicionals**

Permeten executar diferents blocs de codi segons si es compleix una condició.

**Estructura `if / else` i Condicional Ternari**

```python
# Estructura clàssica
valor = 10
if valor % 2 == 0:
    print("Això és un valor parell")
else:
    print("Això és un valor senar")

# Versió ternària (en una sola línia)
valor = 11
print("Això és un valor parell" if valor % 2 == 0 else "Això és un valor senar")

```

**Estructura `if / elif / else**`

```python
nota = float(input("Introdueix la nota (0-10): "))

if nota >= 0 and nota < 5:
    print("Suspès")
elif nota < 7:
    print("Aprovat")
elif nota < 9:
    print("Notable")
elif nota <= 10:
    print("Excel·lent")
else:
    print("El valor no està entre 0 i 10")

```

**Estructura `match**`
Permet l'avaluació per patrons o valors directes.

```python
# Match amb condicions
nota = float(input("Introdueix la nota (0-10): "))

match nota:
    case nota if nota < 5:
        print("Suspès")
    case nota if nota < 7:
        print("Aprovat")
    case nota if nota < 9:
        print("Notable")
    case _:
        print("Excel·lent")

# Match per valors exactes
lletra = "p"
match lletra:
    case "a":
        print("Això és una A")
    case "b":
        print("B")
    case _:
        print("RES")

```

---

**5. Estructures de Repetició (`for`)**

S'utilitzen per iterar sobre una seqüència (com un rang de números o una llista).

```python
# Iteració amb range(inici, fi, pas)
target = 50
for x in range(target, target + 50, 5):
    print(x)

# Iteració directa sobre elements d'una llista
fruites = ["Poma", "Pera", "Maduixa", "Mandarina"]
for x in fruites:
    print(x)

# Iteració amb índex i valor fent servir enumerate()
for index, valor in enumerate(fruites):
    print(f"La posició {index} de l'array conté la fruita {valor}")

```

---

**6. Declaració de Funcions**

Les funcions es defineixen amb la paraula clau `def` i poden rebre paràmetres d'entrada.

```python
name = "Dani"

def imprimir_nom(x):
    print(f"El nom de l'usuari és {x}")

print(name)
imprimir_nom("Sergio")
print(name)

```
