# Apunts Programació en Python: Control d'Errors i Funcions

---

## 1. Gestió d'Exceptions (`try / except`)

La sentència **`try / except`** permet executar blocs de codi susceptibles a produir errors en temps d'execució sense que el programa s'aturi bruscament (*'peti'*)[cite: 10].

### Sintaxi General
```python
try:
    # Codi que es vol intentar executar
    [Acció 1]
    [Acció 2]
    [Acció n]
except:
    # Codi que s'executa si es produeix qualsevol error al bloc 'try'
    [Acció error 1]
    [Acció error 2]
    [Acció error n]

```

### Exemple Pràctic

```python
# Sol·licitem una dada a l'usuari
valor = input("Introdueix un valor enter: ")

try:
    # Intentem convertir la cadena de text a un número enter
    cast = int(valor)
    print(f"El valor decimal que l'usuari ha introduït és {cast}")
except:
    # S'executa si l'usuari ha introduït text o caràcters no numèrics
    print("La operació ha fallat! Revisa el teu codi!")
    exit()

```

### Ampliació: Tipus d'Errors i Blocs Opcionals (`else` / `finally`)

Pots capturar tipus d'errors específics (com `ValueError` o `ZeroDivisionError`) i afegir blocs addicionals de control:

```python
try:
    num1 = int(input("Introdueix el numerador: "))
    num2 = int(input("Introdueix el denominador: "))
    resultat = num1 / num2
except ValueError:
    print("Error: Has d'introduir un número enter vàlid.")
except ZeroDivisionError:
    print("Error: No es pot dividir per zero.")
else:
    # S'executa NOMÉS si no hi ha hagut cap error
    print(f"El resultat de la divisió és: {resultat}")
finally:
    # S'executa SEMPRE, hi hagi error o no (útil per tancar fitxers o connexions)
    print("Procés de divisió finalitzat.")

```

---

## 2. Les Funcions en Python

Les **funcions** són blocs de codi reutilitzables dissenyats per complir un objectiu concret.

### Principals Beneficis

* **Simplificació i reducció de redundància:** Eviten haver de repetir el mateix codi múltiples vegades al llarg del programa.


* **Manteniment del codi:** Faciliten la correcció d'errors i la millora de funcionalitats.


* **Llegibilitat i modularitat:** Augmenten la claredat i l'organització dividint el programa en peces més petites.



---

### Tipus de Funcions

#### 2.1. Funcions sense paràmetres

Funcions que no reben cap informació de l'exterior quan són cridades.

```python
def la_meva_funcio():
    pass

```

#### 2.2. Funcions amb paràmetres

Funcions que reben un o més paràmetres d'entrada. Els noms assignats als paràmetres actuen com a variables locals dins de la funció.

```python
def funcio_amb_parametre(parametre_1, parametre_2):
    print(f"L'usuari {parametre_1} té {parametre_2} anys")

# Invocació de la funció
funcio_amb_parametre("Sergio", 28)

```

#### 2.3. Funcions amb retorn (`return`)

Funcions que realitzen un càlcul o procés i retornen un valor específic al codi que les ha cridat.

```python
def multiplica_dos_resta_un(valor):
    return valor * 2 - 1

# Guardem el valor retornat en una variable
resultat = multiplica_dos_resta_un(4)  # resultat = 7

```

> **Nota:** Un cop s'executa la instrucció `return`, la funció finalitza immediatament i qualsevol línia posterior dins de la funció s'ignora.

#### 2.4. Funcions amb valors per defecte

Funcions on un o més paràmetres tenen assignat un valor predeterminat. Si l'usuari no passa cap valor per a aquest paràmetre, s'utilitzarà el valor per defecte, però **es pot sobreescriure si es proporciona un nou argument**.

```python
def calcula_edat(any_naixement, any_actual=2025):
    return any_actual - any_naixement

# Utilitzant el valor per defecte (any_actual = 2025)
print(calcula_edat(1996))        # Output: 29

# Sobreescribint el valor per defecte
print(calcula_edat(1996, 2026))  # Output: 30

```

---

## 3. Conceptes Avançats de Funcions

### 3.1. Abast de les Variables (*Scope*: Local vs. Global)

* **Variable Local:** Declarada dins d'una funció. Només existeix i és accessible durant l'execució d'aquesta.
* **Variable Global:** Declarada fora de qualsevol funció. És accessible des de qualsevol punt del fitxer.

```python
x = "Soc global"  # Variable global

def la_meva_funcio():
    y = "Soc local"  # Variable local
    print(x)  # Accedeix a la variable global
    print(y)  # Accedeix a la variable local

la_meva_funcio()
# print(y)  --> Donaria un NameError perquè 'y' no existeix fora de la funció.

```

### 3.2. Nombre Variable d'Arguments (`*args` i `**kwargs`)

Quan no saps quants paràmetres rebrà una funció:

* **`*args`**: Rep un nombre indeterminat d'arguments posicionals com una **tupla**.
* **`**kwargs`**: Rep un nombre indeterminat d'arguments de paraula clau (*key-value*) com un **diccionari**.

```python
# Exemple amb *args
def suma_tots(*numeros):
    total = 0
    for n in numeros:
        total += n
    return total

print(suma_tots(1, 2, 3, 4))  # Output: 10

# Exemple amb **kwargs
def mostrar_informacio(**dades):
    for clau, valor in dades.items():
        print(f"{clau}: {valor}")

mostrar_informacio(nom="Anna", edat=25, ciutat="Barcelona")

```
