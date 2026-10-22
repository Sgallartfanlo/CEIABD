import random as rd
from enum import Enum

class TipusProjectil(Enum):
    PR = ("Projectil Regular", 1, 0.80)
    PP = ("Projectil Perforant", 3, 0.35)

    def __init__(self, nom: str, dany: float, precisio: float):
        self.nom_complet, self.dany, self.precisio = nom, dany, precisio


class Faccio(Enum):
    CHIMPANZINI = ("Chimpanzini Bananini", "inferior", [TipusProjectil.PR, TipusProjectil.PP, TipusProjectil.PP])
    LIRILI = ("Lirilí Larilá", "superior", [TipusProjectil.PP, TipusProjectil.PR, TipusProjectil.PR])
    TRALALERO = ("Tralalero Tralala", "igual", [TipusProjectil.PR, TipusProjectil.PP])

    def __init__(self, nom: str, prioritat_blindatge: str, seq_carregador: list):
        self.nom_complet, self.prioritat_blindatge, self.seq_carregador = nom, prioritat_blindatge, seq_carregador


class Tank:
    BASE_BLINDATGE = 10.0

    def __init__(self, nom: str, faccio: Faccio):
        self.nom, self.faccio = nom, faccio
        self.carregador = faccio.seq_carregador.copy()
        self.index_carregador = 0
        self.blindatge = self._inicialitzar_blindatge()

    def _inicialitzar_blindatge(self):
        # Les faccions modifiquen el blindatge superior o inferior.
        superior = self.BASE_BLINDATGE * (1.3 if self.faccio.prioritat_blindatge == "superior" else 1)
        inferior = self.BASE_BLINDATGE * (0.7 if self.faccio.prioritat_blindatge == "inferior" else 1)
        return [[round(superior, 2) for _ in range(3)], [round(inferior, 2) for _ in range(3)]]

    def esta_operatiu(self) -> bool:
        return all(v >= 0 for fila in self.blindatge for v in fila)

    def obtenir_seguent_projectil(self) -> TipusProjectil:
        projectil = self.carregador[self.index_carregador]
        self.index_carregador = (self.index_carregador + 1) % len(self.carregador)
        return projectil

    def rebre_atac(self, projectil: TipusProjectil) -> str:
        if rd.random() > projectil.precisio:
            return "El projectil ha fallat!"

        dany = projectil.dany
        if self.faccio == Faccio.CHIMPANZINI and rd.random() < 0.20:
            dany *= 0.5
        elif self.faccio == Faccio.LIRILI and rd.random() < 0.20:
            return "El projectil és esquivat!"
        elif self.faccio == Faccio.TRALALERO:
            probabilitat = rd.random()
            if probabilitat < 0.05:
                return "El projectil és esquivat!"
            if probabilitat < 0.15:
                dany *= 0.5

        fila_idx, col_idx = rd.randrange(2), rd.randrange(3)
        self.blindatge[fila_idx][col_idx] = round(self.blindatge[fila_idx][col_idx] - dany, 2)
        posicio = f"({fila_idx}, {col_idx})"

        if dany < projectil.dany:
            return f"El {self.nom} aconsegueix mitigar els danys i rep {dany} punts d'impacte a la posició {posicio}"
        return f"El projectil impacta a la posició {posicio}"

    def __str__(self):
        return f"El {self.nom} de la facció [{self.faccio.nom_complet}] li queda un blindatge de: superior {self.blindatge[0]}, inferior {self.blindatge[1]}"


class SimulacioBatalla:
    def __init__(self, tancs: list):
        self.tancs = tancs
        self.ultim_atacant = None
        self.ronda = 1

    def tancs_actius(self):
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
        # Només els tancs vius poden atacar i defensar-se.
        tancs_actius = self.tancs_actius()
        if len(tancs_actius) <= 1:
            return

        atacants = [t for t in tancs_actius if t != self.ultim_atacant]
        atacant = rd.choice(atacants or tancs_actius)
        self.ultim_atacant = atacant

        objectiu = rd.choice([t for t in tancs_actius if t != atacant])
        projectil = atacant.obtenir_seguent_projectil()

        # Es mostra el desenvolupament de la ronda abans de la resolució del cop.
        print(f"\n--- RONDA {self.ronda} ---")
        print(f"> El {atacant.nom} de la facció [{atacant.faccio.nom_complet}] es disposa a atacar amb el projectil de tipus {projectil.nom_complet} al {objectiu.nom} de la facció [{objectiu.faccio.nom_complet}]")
        print(f"  > El projectil es dirigeix al {objectiu.nom}")

        resultat = objectiu.rebre_atac(projectil)
        print(f"      >> {resultat}")

        print("\n> Resum final de la ronda:")
        for tanc in self.tancs:
            estat = str(tanc)
            if not tanc.esta_operatiu():
                estat += " [FORA DE COMBAT]"
            print(f"  > {estat}")

        self.ronda += 1

    def iniciar(self):
        self.mostrar_estat_inicial()
        while len(self.tancs_actius()) > 1:
            self.executar_ronda()

        guanyador = self.tancs_actius()[0]
        print("\n" + "=" * 60)
        print("LA BATALLA HA FINALITZAT!")
        print(f"El guanyador és el {guanyador.nom} de la facció [{guanyador.faccio.nom_complet}]!")
        print("=" * 60)