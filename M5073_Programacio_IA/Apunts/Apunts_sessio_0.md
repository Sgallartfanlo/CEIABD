# Introducció a la Programació amb Python (Sessió 0: Bases)

## Què és Python?

Python és un llenguatge de programació:
* **Interpretat**
* **D'alt nivell**
* **Multiplataforma** i de codi **lliure**

**Multiparadigma**, ja que suporta:
* Programació imperativa
* Programació funcional
* Programació orientada a objectes (POO)

---

## Continguts del Curs

1. **Declaració de variables (I):** Enters (`int`), Reals (`float`), Cadenes de text (`str`).
2. **Ús d'operadors bàsics:** Aritmètics, de comparació, d'assignació i lògics.
3. **Estructures condicionals:** `if`, `elif`, `else`, `match`.
4. **Estructures de repetició:** Bucle `for` i bucle `while`.
5. **Declaració de variables (II):** Llistes, Tuples, Diccionaris i Rangs.
6. **Ús de mètodes i funcions.**
7. **Recursivitat.**
8. **Programació Orientada a Objectes (POO).**

---

## Guia Ràpida de Markdown

[Guia oficial de Markdown](https://colab.research.google.com/notebooks/markdown_guide.ipynb#scrollTo=5Y3CStVkLxqt)

```markdown
# Secció
## Subsecció
### Sub-subsecció

**negreta**
*cursiva*
`Cita`

1. Llista ordenada (I)
2. Llista ordenada (II)

* Llista no ordenada (I)
* Llista no ordenada (II)
  * Llista no ordenada - subsecció

> Un nivell d'identació
>> Dos nivells d'identació

--- (Separador horitzontal)

<h1>Exemple de codi HTML</h1>

```

---

## Tipus Bàsics de Variables

Tipus de dades principals utilitzats en els exercicis:

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

---

## Operadors

### Operadors Aritmètics

Retornen un valor resultant segons el tipus de dada:

```python
5 + 4    # Suma -> 9
5 - 4    # Resta -> 1
10 / 2   # Divisió -> 5.0 (float)
10 // 3  # Divisió entera -> 3
10 % 2   # Residu de la divisió (mòdul) -> 0
10 ** 2  # Exponent -> 100

```

### Operadors Relacionals i Condicionals

Retornen valors booleans (`True` o `False`):

```python
5 == 4  # Igual a -> False
5 < 4   # Més petit que -> False
5 <= 4  # Més petit o igual a -> False
5 != 4  # Diferent de -> True

```

---

## Exemples d'Execució i Codificació

### 1. Operadors Lògics

```python
print("AND:")
print((10 % 2 == 0 and 10 / 2 == 3))  # False

print("OR:")
print((10 % 2 == 0 or 10 / 2 == 3))   # True

print("NEGACIÓ x2 OR:")
print(not(not(10 % 2 == 0) or 10 / 2 == 3))  # True

```

### 2. Gestió de Cadenes de Text (`str`)

```python
# Concatenació
print("Hola " + "Sergio")

# F-strings (formateig de text)
print(f"Això és un número: {2.15}")

```

### 3. Variables i Identificació de Tipus (`type`)

```python
a = 5
print(a)

b = 50
c = b
c = c + 10
print(c)  # 60

# Comprovar el tipus de variable
nova_variable = "Exemple"
print(type(nova_variable))  # <class 'str'>
print(f"{nova_variable} nou")

nova_variable = 1  # Redefinició
print(type(nova_variable))  # <class 'int'>

# Ús de type() en condicionals
investiga_tipus = 10
if type(investiga_tipus) == int:
    print(investiga_tipus + 10)
elif type(investiga_tipus) == str:
    print("Això és un string " + investiga_tipus)

```

### 4. Estructures Condicionals (`if`, `elif`, `else`, `match`)

#### Valor parell o senar (Versió Clàssica vs Ternària):

```python
# Versió Clàssica
valor = 10
if valor % 2 == 0:
    print("Això és un valor parell")
else:
    print("Això és un valor senar")

# Versió Ternària (una sola línia)
valor = 11
print("Això és un valor parell" if valor % 2 == 0 else "Això és un valor senar")

```

#### Càlcul de qualificacions amb intervals:

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

#### Càlcul de qualificacions amb la sintaxi `match` (Python 3.10+):

```python
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

### 5. Estructures de Repetició (`for`)

```python
# Ús de range(inici, fi, pas)
target = 50
for x in range(target, target + 50, 5):
    print(x)

# Iterar sobre una llista
fruites = ["Poma", "Pera", "Maduixa", "Mandarina"]
for x in fruites:
    print(x)

# Iterar amb l'índex utilitzant enumerate()
for index, valor in enumerate(fruites):
    print(f"La posició {index} de l'array conté la fruita {valor}")

```

### 6. Declaració i Ús de Funcions

```python
name = "Dani"

def imprimir_nom(x):
    print(f"El nom de l'usuari és {x}")

print(name)
imprimir_nom("Sergio")
print(name)

```

```

```
