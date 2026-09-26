# Exercicis Sessió 1 i 2

## 1. Taula de multiplicar
Demana un número a l'usuari i mostra la seva taula de multiplicar del 1 al 10.[cite: 15]

```python
num = int(input("Introdueix un número: "))
for i in range(1, 11):
    print(num, "x", i, "=", num*i)

```

---

## 2. Suma dels primers N números

Demana un número **N** i calcula la suma dels primers **N** primers números naturals (enters).

*Es calcula: 1+2+3+4+5*

Per exemple:

```text
Input = 5
Output: El resultat és 15

```

```python
num = int(input("Introdueix un número: "))
suma = 0
for i in range(1, num+1):
    suma += i
print("El resultat és", suma)

```

---

## 3. Factorial d'un número

Demana un número enter positiu i calcula el seu factorial.

*Es calcula: N = 5 .... llavors .... 5 x 4 x 3 x 2 x 1 = 120*

```python
num = int(input("Introdueix un número: "))
factorial = 1
for i in range(1, num+1):
    factorial *= i
print("El factorial de", num, "és", factorial)

```

---

## 4. Seqüència de Fibonacci

Demana un número **N** i mostra els **N** primers termes de la seqüència Fibonacci.

*Per exemple: N = 7 .... llavors .... 0, 1, 1, 2, 3, 5, 8 (cada terme és la suma dels dos anteriors)*

```python
n = int(input("Introdueix un número: "))

a = 0
b = 1

for i in range(n):
    print(a)
    seguent = a + b
    a = b
    b = seguent

```

### Versió 2:

```python
numeroEntrado = int(input("Entra num per fibbo --> "))

anterior = 0
actual = 1
contador = 0

while contador < numeroEntrado:
    print(f"{anterior}")
    siguiente = anterior + actual
    anterior = actual
    actual = siguiente
    contador += 1

```

---

## 5. Nombre primer

Demana un número enter i indica si és primer o no.

> **Recorda que:** Un número primer és aquell que només és divisible per ell mateix i per 1 (sempre tenint en compte que el resultat és enter i el residu zero).
> 
> 

```python
num = int(input("Introdueix un número: "))

es_primer = True
i = 2

while i < num and es_primer:
    if num % i == 0:
        es_primer = False
    i += 1

if es_primer and num > 1:
    print(num, "és un número primer")
else:
    print(num, "no és un número primer")

```

### Versió 2:

```python
def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

try:
    numero = int(input("Introdueix un número enter: "))
    if es_primo(numero):
        print("És Primer")
    else:
        print("No és Primer")
except ValueError:
    print("Error: Deus introduïr un número válid.")

```

---

## 6. Combinació extrema

Crea una calculadora que permeti realitzar totes les operacions programades anteriorment. Per fer-ho:

1. Mostra un menú on l'usuari seleccioni el tipus d'operació que vol realitzar.


2. Sol·licita el número o els números que les operacions requereixin.


3. Mostra el resultat obtingut.



> **Tingues en compte que TOTES les operacions s'han de cridar a partir de funcions predefinides al vostre codi.**
> 

```python
# --- Funcions per a cada operació ---

def taula_multiplicar(num):
    print(f"\n--- Taula de multiplicar del {num} ---")
    for i in range(1, 11):
        print(f"{num} x {i} = {num * i}")

def suma_n_primers(num):
    suma = 0
    for i in range(1, num + 1):
        suma += i
    print(f"La suma dels primers {num} números és: {suma}")

def calcular_factorial(num):
    if num < 0:
        print("El factorial no està definit per a números negatius.")
        return
    factorial = 1
    for i in range(1, num + 1):
        factorial *= i
    print(f"El factorial de {num} és: {factorial}")

def sequencia_fibonacci(n):
    if n <= 0:
        print("Introdueix un número major que 0.")
        return
    print(f"\nEls primers {n} termes de la seqüència de Fibonacci són:")
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
    print()  # Salt de línia final

def comprovar_primer(num):
    if num <= 1:
        print(f"{num} no és un número primer")
        return

    es_primer = True
    i = 2
    while i < num and es_primer:
        if num % i == 0:
            es_primer = False
        i += 1

    if es_primer:
        print(f"{num} és un número primer")
    else:
        print(f"{num} no és un número primer")

# --- Programa Principal / Menú ---

def menu():
    print("\n==================================")
    print("      CALCULADORA COMBINADA       ")
    print("==================================")
    print("1. Taula de multiplicar")
    print("2. Suma dels primers N números")
    print("3. Factorial d'un número")
    print("4. Seqüència de Fibonacci")
    print("5. Comprovar si un número és primer")
    print("6. Sortir")
    print("==================================")

# Bucle principal de la calculadora
opcio = 0
while opcio != 6:
    menu()
    try:
        opcio = int(input("Selecciona una opció (1-6): "))

        if opcio in [1, 2, 3, 4, 5]:
            numero = int(input("Introdueix el número amb el qual vols operar: "))

            if opcio == 1:
                taula_multiplicar(numero)
            elif opcio == 2:
                suma_n_primers(numero)
            elif opcio == 3:
                calcular_factorial(numero)
            elif opcio == 4:
                sequencia_fibonacci(numero)
            elif opcio == 5:
                comprovar_primer(numero)

        elif opcio == 6:
            print("Gràcies per utilitzar la calculadora. Fins aviat!")
        else:
            print("Opció no vàlida. Introdueix un número entre 1 i 6.")

    except ValueError:
        print("Error: Introdueix un número enter vàlid.")

```
