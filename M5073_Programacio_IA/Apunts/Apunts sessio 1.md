# Apunts Programació en Python: Control d'Errors i Funcions

---

## 1. Gestió d'Exceptions (`try / except`)

La sentència **`try / except`** permet executar blocs de codi susceptibles a produir errors en temps d'execució sense que el programa s'aturi bruscament (*'peti'*)[cite: 11].

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
    # S'executa si l'usuari ha introduit text o caràcters no numèrics
    print("La operació ha fallat! Revisa el teu codi!")
    exit()

```

---

## 2. Les Funcions en Python

Les **funcions** són blocs de codi reutilitzables dissenyats per complir un objectiu concret.

### Principals Beneficis

* **Simplificació i reducció de redundància:** Eviten haver de repetir el mateix codi múltiples vegades al llarg del programa.


* **Manteniment del codi:** Faciliten la correcció d'errors i la millora de funcionalitats.


* **Llegibilitat:** Augmenten la claredat i l'organització del programa.



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

```

```
