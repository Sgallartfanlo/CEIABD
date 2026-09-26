# Sessió 6: Programació Orientada a Objectes (POO)

La **POO** és un paradigma de programació estructurat al voltant d'**objectes**, els quals contenen **dades** (atributs) i **comportament** (mètodes).

---

## 1. Conceptes Clau

* **Classe:** Plantilla o model per crear objectes.
* **Objecte:** Instància concreta d'una classe.
* **Atribut:** Variable interna d'un objecte que en defineix les propietats.
* **Mètode:** Funció interna d'un objecte que defineix què pot fer.
* **Constructor (`__init__`):** Mètode especial que s'executa automàticament en instanciar un objecte per inicialitzar els seus atributs.
* **Paràmetre `self`:** Referència a la pròpia instància de l'objecte actual.

---

## 2. Exemple Base: Classe `CompteBancari`

```python
class CompteBancari:
    # Variable / Constant de classe
    INTERES_FIX = 2

    def __init__(self, nom: str, saldo: float):
        self.nom = nom        # Atribut d'instància
        self.saldo = saldo    # Atribut d'instància

    def ingressar(self, quantitat: float):
        self.saldo += quantitat

    def retirar(self, quantitat: float):
        if quantitat <= self.saldo:
            self.saldo -= quantitat
        else:
            print("Saldo insuficient")

    def mostrar_info(self):
        print(f"Titular: {self.nom} | Saldo: {self.saldo}€ | Interès: {self.INTERES_FIX}%")
```

---

## 3. Relacions entre Objectes: Exercici Biblioteca

A continuació veiem com relacionar dues classes (`Llibre` i `Biblioteca`):

```python
class Llibre:
    def __init__(self, titol: str, autor: str):
        self.titol = titol
        self.autor = autor
        self.disponible = True

    def mostrar_info(self):
        estat = "Sí" if self.disponible else "No"
        print(f"Títol: {self.titol} | Autor: {self.autor} | Disponible: {estat}")


class Biblioteca:
    def __init__(self):
        self.llibres: list[Llibre] = []

    def afegir_llibre(self, llibre: Llibre):
        self.llibres.append(llibre)

    def cercar_llibre(self, nom: str) -> int:
        for i, llibre in enumerate(self.llibres):
            if llibre.titol == nom:
                return i
        return -1

    def prestar_llibre(self, nom_llibre: str):
        idx = self.cercar_llibre(nom_llibre)
        if idx != -1:
            if self.llibres[idx].disponible:
                self.llibres[idx].disponible = False
                print(f"S'ha prestat: {nom_llibre}")
            else:
                print(f"El llibre '{nom_llibre}' ja està prestat.")
        else:
            print("Llibre no trobat.")

    def tornar_llibre(self, nom_llibre: str):
        idx = self.cercar_llibre(nom_llibre)
        if idx != -1:
            self.llibres[idx].disponible = True
            print(f"S'ha retornat: {nom_llibre}")

    def mostrar_llibres(self):
        print("\n--- Llista de Llibres ---")
        for llibre in self.llibres:
            llibre.mostrar_info()
```