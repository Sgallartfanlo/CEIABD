# Sessió 7: Herència i Polimorfisme

L'**Herència** és un dels pilars de la POO. Permet que una classe (filla o subclasse) hereti atributs i mètodes d'una altra classe (pare o superclasse), promovent la reutilització de codi.

---

## 1. Conceptes Fonamentals

* **Reescriptura de Mètodes (*Overriding*):** Una classe filla pot redefinir un mètode de la classe pare per canviar-ne el comportament.
* **Ús de `super()`:** Permet accedir a mètodes o al constructor de la classe pare des de la classe filla.

```python
class Animal:
    def moure(self):
        print("L'animal es mou")

class Gos(Animal):
    def moure(self):
        super().moure()  # Crida el mètode de la classe pare
        print("El gos corre a 4 potes!")
```

---

## 2. Exercicis Pràctics

### A) Sistema de Figures Geomètriques (Polimorfisme)

```python
import math

class Figura:
    def area(self):
        print("Aquesta figura no té àrea definida")

class Cercle(Figura):
    def __init__(self, radi: float):
        super().__init__()
        self.radi = radi

    def area(self):
        res = math.pi * (self.radi ** 2)
        print(f"L'àrea del cercle és: {round(res, 2)}")

class Rectangle(Figura):
    def __init__(self, base: float, altura: float):
        super().__init__()
        self.base = base
        self.altura = altura

    def area(self):
        print(f"L'àrea del rectangle és: {self.base * self.altura}")
```

### B) Jerarquia d'Empleats

```python
class Empleat:
    def __init__(self, nom: str):
        self.nom = nom

    def mostrar_info(self) -> str:
        return f"Nom: {self.nom}"

class Programador(Empleat):
    def __init__(self, nom: str, llenguatge: str):
        super().__init__(nom)
        self.llenguatge = llenguatge

    def mostrar_info(self) -> str:
        return super().mostrar_info() + f" | Llenguatge: {self.llenguatge}"

class Gerent(Empleat):
    def __init__(self, nom: str, departament: str):
        super().__init__(nom)
        self.departament = departament

    def mostrar_info(self) -> str:
        return super().mostrar_info() + f" | Departament: {self.departament}"
```

### C) Sistema Bancari amb Comptes Específics

```python
class CompteBancari:
    def __init__(self, titular: str, saldo: float):
        self.titular = titular
        self.saldo = saldo

    def dipositar(self, quantitat: float):
        self.saldo += quantitat

    def retirar(self, quantitat: float):
        self.saldo -= quantitat

class CompteEstalvis(CompteBancari):
    def retirar(self, quantitat: float):
        if self.saldo - quantitat < 0:
            print("Error: Un compte d'estalvis no pot tenir saldo negatiu.")
        else:
            super().retirar(quantitat)

class CompteCorrent(CompteBancari):
    def retirar(self, quantitat: float):
        if self.saldo - quantitat < -500:
            print("Error: Has superat el límit de descobert de -500€.")
        else:
            super().retirar(quantitat)
```