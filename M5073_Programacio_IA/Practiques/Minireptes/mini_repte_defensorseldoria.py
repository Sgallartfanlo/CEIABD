# -*- coding: utf-8 -*-
import random
import time

# ---------------------------------------------------------
# 1. CLASSE BASE: Personatge
# ---------------------------------------------------------
class Personatge:
    def __init__(self, nom, nivell, salut, **kwargs):
        super().__init__(**kwargs)
        self.nom = nom
        self.nivell = nivell
        self.salut = salut

    def info(self):
        return f"{self.nom} (Nv. {self.nivell}) - Salut: {max(0, self.salut)}"

    def rebre_dany(self, amount):
        self.salut -= amount
        if self.salut < 0:
            self.salut = 0

    def es_viu(self):
        return self.salut > 0

    def accio(self, objectiu):
        pass


# ---------------------------------------------------------
# 2. CLASSES ESPECIALITZADES
# ---------------------------------------------------------
class Combatent(Personatge):
    def __init__(self, forca, **kwargs):
        super().__init__(**kwargs)
        self.forca = forca

    def atacar(self, objectiu):
        dany = self.forca + (self.nivell * 2)
        print(f"⚔️ {self.nom} fa un atac físic a {objectiu.nom} causant {dany} de dany.")
        objectiu.rebre_dany(dany)


class Magic(Personatge):
    def __init__(self, mana, **kwargs):
        super().__init__(**kwargs)
        self.mana = mana

    def llancar_encanteri(self, objectiu):
        if self.mana >= 5:
            self.mana -= 5
            dany = 10 + (self.nivell * 2)
            print(f"✨ {self.nom} llança un encanteri a {objectiu.nom} causant {dany} de dany (-5 mana).")
            objectiu.rebre_dany(dany)
            return True
        else:
            print(f"⚠️ {self.nom} no té prou mana per llançar un encanteri!")
            return False

    def curar(self):
        if self.mana >= 5:
            self.mana -= 5
            cura = 10 + self.nivell
            self.salut += cura
            print(f"💖 {self.nom} es cura {cura} punts de salut (-5 mana).")
            return True
        else:
            print(f"⚠️ {self.nom} no té prou mana per curar-se!")
            return False


# ---------------------------------------------------------
# 3. CLASSES FINALS
# ---------------------------------------------------------
class Barbar(Combatent):
    def __init__(self, nom, nivell, salut, forca):
        super().__init__(nom=nom, nivell=nivell, salut=salut, forca=forca)

    def accio(self, objectiu):
        self.atacar(objectiu)


class Bruixot(Magic):
    def __init__(self, nom, nivell, salut, mana):
        super().__init__(nom=nom, nivell=nivell, salut=salut, mana=mana)

    def accio(self, objectiu):
        if not self.llancar_encanteri(objectiu):
            print(f"⌛ {self.nom} passa el torn per falta de mana.")


class Paladi(Combatent, Magic):
    def __init__(self, nom, nivell, salut, forca, mana):
        super().__init__(nom=nom, nivell=nivell, salut=salut, forca=forca, mana=mana)

    def accio(self, objectiu):
        if self.salut < 40 and self.mana >= 5:
            self.curar()
        else:
            self.atacar(objectiu)


# ---------------------------------------------------------
# 4. CLASSE ENEMIC
# ---------------------------------------------------------
class Enemic:
    def __init__(self, nom, salut):
        self.nom = nom
        self.salut = salut

    def rebre_dany(self, amount):
        self.salut -= amount
        if self.salut < 0:
            self.salut = 0

    def es_viu(self):
        return self.salut > 0

    def atac_fisic(self, herois):
        herois_vius = [h for h in herois if h.es_viu()]
        if herois_vius:
            target = random.choice(herois_vius)
            dany = random.randint(15, 30)
            print(f"👾 {self.nom} ataca a {target.nom} i li causa {dany} de dany!")
            target.rebre_dany(dany)


# ---------------------------------------------------------
# 5. BUCLE DE SIMULACIÓ AMB TIMINGS
# ---------------------------------------------------------
def simulacio_combat():
    arthur = Paladi("Arthur", 7, 110, 18, 12)
    brakka = Barbar("Brakka", 6, 135, 26)
    morgana = Bruixot("Morgana", 6, 80, 40)

    herois = [arthur, brakka, morgana]
    enemic = Enemic("Ombra Antiga", 250)

    torn = 1
    PAUSA = 1.5  # Segons de pausa entre accions

    while enemic.es_viu() and any(h.es_viu() for h in herois):
        print(f"\n==================== TORN {torn} ====================")
        time.sleep(PAUSA)
        
        # Acció dels herois
        for heroi in herois:
            if heroi.es_viu() and enemic.es_viu():
                heroi.accio(enemic)
                time.sleep(PAUSA)

        # Acció de l'enemic
        if enemic.es_viu():
            enemic.atac_fisic(herois)
            time.sleep(PAUSA)

        # Resum del torn
        print("\n--- Estat dels participants ---")
        for h in herois:
            estat = h.info()
            if hasattr(h, 'mana'):
                estat += f" | Mana: {h.mana}"
            print(estat)
        print(f"{enemic.nom} - Salut: {max(0, enemic.salut)}")
        
        time.sleep(PAUSA)
        torn += 1

    print("\n==================================================")
    time.sleep(PAUSA)
    if enemic.es_viu():
        print("❌ DERROTA! Els herois d'Eldoria han estat derrotats...")
    else:
        print("✅ VICTÒRIA! L'Ombra Antiga ha estat derrotada!")

if __name__ == "__main__":
    simulacio_combat()