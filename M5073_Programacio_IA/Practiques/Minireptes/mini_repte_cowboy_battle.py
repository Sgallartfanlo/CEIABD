# -*- coding: utf-8 -*-

class Gun:
    def __init__(self, max_bullets: int):
        self.MAX_BULLETS = max_bullets
        self.bullets = max_bullets

    def shoot(self) -> bool:
        if self.bullets > 0:
            self.bullets -= 1
            return True
        return False

    def reload(self) -> None:
        self.bullets = self.MAX_BULLETS


class Cowboy:
    def __init__(self, name: str, health: int, gun: Gun):
        self.name = name
        self.health = health
        self.gun = gun

    def is_alive(self) -> bool:
        return self.health > 0

    def get_shoot(self) -> None:
        self.health -= 1

    def shoot(self) -> bool:
        # Utilitza el mètode interior de la seva instància de Gun
        return self.gun.shoot()

    def reload(self) -> None:
        # Utilitza el mètode de recàrrega de Gun
        self.gun.reload()


def round_action(cowboy_A: Cowboy, cowboy_B: Cowboy):
    '''
    Executa una ronda de confrontació entre dos cowboys.
    '''
    print(f"El cowboy {cowboy_A.name} vol disparar!!")

    if cowboy_A.shoot(): # Si el cowboy_A és capaç de disparar...
        print("DISPARA!!!")
        cowboy_B.get_shoot() # El cowboy_B rep el tret.
    else: # Altrament...
        print("NO ha pogut disparar, no té bales!!     RECARREGA")
        cowboy_A.reload() # Recarrega l'arma


def cowboy_battle():
    '''
    Funció principal que executa la batalla entre 2 cowboys.
    '''
    # Definim/Instanciem els nostres cowboys...
    cowboy_1 = Cowboy("Sergio", 3, Gun(1))
    cowboy_2 = Cowboy("Dani", 6, Gun(1))

    # Fem un comptador de rondes
    round_count = 1

    # Bucle principal de l'escenari proposat
    while cowboy_1.is_alive() and cowboy_2.is_alive(): # Mentre tots dos segueixin vius...
        if round_count % 2 == 0: # Si el número de la ronda és parell... ataca el cowboy 1
            round_action(cowboy_1, cowboy_2)
        else: # Altrament ataca el cowboy 2
            round_action(cowboy_2, cowboy_1)
        
        print(f"   ###  FINAL DE LA RONDA {round_count} \n"
              f"   >>>  El cowboy {cowboy_1.name} ha quedat amb {cowboy_1.health} vides.\n"
              f"   >>>  El cowboy {cowboy_2.name} ha quedat amb {cowboy_2.health} vides.\n\n")
        round_count += 1

    # A algun dels cowboys ja no li queden vides, per tant...
    guanyador = cowboy_1.name if cowboy_1.is_alive() else cowboy_2.name
    print(f"El cowboy guanyador es: {guanyador}")


if __name__ == "__main__":
    cowboy_battle()