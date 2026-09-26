# -*- coding: utf-8 -*-
import random as rd
from enum import Enum

# --- ENUMS PER A LES RESTRICCIONS ---
class TipusRoba(Enum):
    PANTALONS = "Pantalons"
    SAMARRETES = "Samarretes"
    JERSEY = "Jersey"
    PANTALO_CURT = "Pantaló curt"
    ROBA_INTERIOR = "Roba interior"

class Color(Enum):
    BLAU = "Blau"
    GRIS = "Gris"
    NEGRE = "Negre"

# --- CLASSE PEÇA DE ROBA ---
class PecaRoba:
    def __init__(self, tipus: TipusRoba, color: Color):
        self.tipus = tipus
        self.color = color
        self.preu = self._assignar_preu()

    def _assignar_preu(self):
        rangs = {
            TipusRoba.PANTALONS: (25, 75),
            TipusRoba.SAMARRETES: (10, 25),
            TipusRoba.JERSEY: (20, 45),
            TipusRoba.PANTALO_CURT: (15, 55),
            TipusRoba.ROBA_INTERIOR: (5, 15)
        }
        minim, maxim = rangs[self.tipus]
        return rd.randint(minim, maxim)

# --- CLASSE ARMARI (INVENTARI) ---
class Armari:
    def __init__(self):
        self.roba = []

    def afegir_peca(self, peca: PecaRoba):
        self.roba.append(peca)

    def quantitat_per_tipus(self, tipus: TipusRoba):
        return sum(1 for p in self.roba if p.tipus == tipus)

    def quantitat_per_color(self, color: Color):
        return sum(1 for p in self.roba if p.color == color)

    def quantitat_combinada(self, tipus: TipusRoba, color: Color):
        return sum(1 for p in self.roba if p.tipus == tipus and p.color == color)

    def total_diners_gastats(self):
        return sum(p.preu for p in self.roba)

# --- SIMULACIÓ ---
def main():
    armari = Armari()
    
    # Generació aleatòria de 50 peces
    for _ in range(50):
        tipus = rd.choice(list(TipusRoba))
        color = rd.choice(list(Color))
        armari.afegir_peca(PecaRoba(tipus, color))

    print("=== RESULTATS DE L'INVENTARI DE L'ARMARI ===")
    
    # 1. Per tipus
    print("\n--- Unitats per tipus de roba ---")
    for tipus in TipusRoba:
        print(f"- {tipus.value}: {armari.quantitat_per_tipus(tipus)} unitats")

    # 2. Per color
    print("\n--- Unitats per color ---")
    for color in Color:
        print(f"- {color.value}: {armari.quantitat_per_color(color)} unitats")

    # 3. Combinats (Exemple amb un parell de combinacions)
    print("\n--- Exemple de combinacions (Tipus + Color) ---")
    sample_tipus = TipusRoba.PANTALONS
    sample_color = Color.NEGRE
    print(f"- {sample_tipus.value} de color {sample_color.value}: "
          f"{armari.quantitat_combinada(sample_tipus, sample_color)} unitats")

    # 4. Despesa total
    print(f"\n💰 Diners totals gastats a l'armari: {armari.total_diners_gastats()}€")

if __name__ == "__main__":
    main()