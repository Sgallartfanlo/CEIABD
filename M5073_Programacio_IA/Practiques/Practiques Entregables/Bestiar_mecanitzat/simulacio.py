import random as rd
from enum import Enum


# ==========================================
# DEFINICIÓ DE CLASSES ENUM I ESTRUCTURES
# ==========================================

class TipusProjectil(Enum):
    PR = ("Projectil Regular", 1, 0.80)
    PP = ("Projectil Perforant", 3, 0.35)

    def __init__(self, nom: str, dany: float, precisio: float):
        self.nom_complet = nom
        self.dany = dany
        self.precisio = precisio


class Faccio(Enum):
    CHIMPANZINI = ("Chimpanzini Bananini", "inferior", [TipusProjectil.PR, TipusProjectil.PP, TipusProjectil.PP])
    LIRILI = ("Lirilí Larilá", "superior", [TipusProjectil.PP, TipusProjectil.PR, TipusProjectil.PR])
    TRALALERO = ("Tralalero Tralala", "igual", [TipusProjectil.PR, TipusProjectil.PP])

    def __init__(self, nom: str, prioritat_blindatge: str, seq_carregador: list):
        self.nom_complet = nom
        self.prioritat_blindatge = prioritat_blindatge
        self.seq_carregador = seq_carregador


# ==========================================
# DEFINICIÓ DE LA CLASSE TANK
# ==========================================

class Tank:
    BASE_BLINDATGE = 10.0

    def __init__(self, nom: str, faccio: Faccio):
        self.nom = nom
        self.faccio = faccio
        self.carregador = faccio.seq_carregador.copy()
        self.index_carregador = 0
        self.blindatge = self._inicialitzar_blindatge()

    def _inicialitzar_blindatge(self):
        val_superior = self.BASE_BLINDATGE
        val_inferior = self.BASE_BLINDATGE

        if self.faccio.prioritat_blindatge == "superior":
            val_superior *= 1.3
        elif self.faccio.prioritat_blindatge == "inferior":
            val_inferior *= 0.7

        return [
            [round(val_superior, 2) for _ in range(3)],
            [round(val_inferior, 2) for _ in range(3)]
        ]

    def esta_operatiu(self) -> bool:
        for fila in self.blindatge:
            for valor in fila:
                if valor < 0:
                    return False
        return True

    def obtenir_seguent_projectil(self) -> TipusProjectil:
        projectil = self.carregador[self.index_carregador]
        self.index_carregador = (self.index_carregador + 1) % len(self.carregador)
        return projectil

    def rebre_atac(self, projectil: TipusProjectil) -> str:
        if rd.random() > projectil.precisio:
            return "El projectil ha fallat!"

        dany = projectil.dany
        
        if self.faccio == Faccio.CHIMPANZINI:
            if rd.random() < 0.20:
                dany *= 0.5

        elif self.faccio == Faccio.LIRILI:
            if rd.random() < 0.20:
                return "El projectil és esquivat!"

        elif self.faccio == Faccio.TRALALERO:
            prob = rd.random()
            if prob < 0.05:
                return "El projectil és esquivat!"
            elif prob < 0.15:
                dany *= 0.5

        fila_idx = rd.choice([0, 1])
        col_idx = rd.choice([0, 1, 2])
        
        self.blindatge[fila_idx][col_idx] -= dany
        self.blindatge[fila_idx][col_idx] = round(self.blindatge[fila_idx][col_idx], 2)

        posicio_str = f"({fila_idx}, {col_idx})"
        
        if dany < projectil.dany:
            return f"El {self.nom} aconsegueix mitigar els danys i rep {dany} punts d'impacte a la posició {posicio_str}"
        else:
            return f"El projectil impacta a la posició {posicio_str}"

    def __str__(self):
        sup = self.blindatge[0]
        inf = self.blindatge[1]
        return f"El {self.nom} de la facció [{self.faccio.nom_complet}] li queda un blindatge de: superior {sup}, inferior {inf}"


# ==========================================
# CONTROLADOR DE LA SIMULACIÓ
# ==========================================

class SimulacioBatalla:
    def __init__(self, tancs: list):
        self.tancs = tancs
        self.ultim_atacant = None
        self.ronda = 1

    def tancs_villus(self):
        return [t for t in self.tancs if t.esta_operatiu()]

    def mostrar_estat_inicial(self):
        print("=" * 60)
        print("DADES INICIALS DELS TANCS")
        print("=" * 60)
        for tanc in self.tancs:
            print(f"- {tanc.nom} [{tanc.faccio.nom_complet}]")
            print(f"  Blindatge superior: {tanc.blindatge[0]}")
            print(f"  Blindatge inferior: {tanc.blindatge[1]}\n")

    def executar_ronda(self):
        villus = self.tancs_villus()
        if len(villus) <= 1:
            return

        candidats_atacants = [t for t in villus if t != self.ultim_atacant]
        if not candidats_atacants:
            candidats_atacants = villus

        atacant = rd.choice(candidats_atacants)
        self.ultim_atacant = atacant

        candidats_objectiu = [t for t in villus if t != atacant]
        objectiu = rd.choice(candidats_objectiu)

        projectil = atacant.obtenir_seguent_projectil()
        
        print(f"\n--- RONDA {self.ronda} ---")
        print(f"> El {atacant.nom} de la facció [{atacant.faccio.nom_complet}] es disposa a atacar amb el projectil de tipus {projectil.nom_complet} al {objectiu.nom} de la facció [{objectiu.faccio.nom_complet}]")
        print(f"  > El projectil es dirigeix al {objectiu.nom}")
        
        resultat = objectiu.rebre_atac(projectil)
        print(f"      >> {resultat}")

        print("\n> Resum final de la ronda:")
        for tanc in self.tancs:
            estat = tanc.__str__()
            if not tanc.esta_operatiu():
                estat += " [FORA DE COMBAT]"
            print(f"  > {estat}")

        self.ronda += 1

    def iniciar(self):
        self.mostrar_estat_inicial()

        while len(self.tancs_villus()) > 1:
            self.executar_ronda()

        guanyador = self.tancs_villus()[0]
        print("\n" + "=" * 60)
        print("LA BATALLA HA FINALITZAT!")
        print(f"El guanyador és el {guanyador.nom} de la facció [{guanyador.faccio.nom_complet}]!")
        print("=" * 60)