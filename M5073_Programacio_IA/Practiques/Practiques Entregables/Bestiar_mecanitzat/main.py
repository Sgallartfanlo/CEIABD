"""Punt d'entrada principal de l'aplicació."""

from simulacio import Tank, Faccio, SimulacioBatalla


def main():
    # 1. Crear els tancs
    tancs = [
        Tank("Tank_A", Faccio.CHIMPANZINI),
        Tank("Tank_B", Faccio.LIRILI),
        Tank("Tank_C", Faccio.TRALALERO)
    ]

    # 2. Executar la simulació
    simulacio = SimulacioBatalla(tancs)
    simulacio.iniciar()


if __name__ == "__main__":
    main()