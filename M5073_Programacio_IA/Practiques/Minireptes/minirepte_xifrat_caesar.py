# -*- coding: utf-8 -*-

def xifrar_cesar(text: str, desplacament: int) -> str:
    resultat = ""
    for caracter in text:
        if caracter.isupper():
            posicio = ord(caracter) - ord('A')
            nova_posicio = (posicio + desplacament) % 26
            resultat += chr(nova_posicio + ord('A'))
        elif caracter.islower():
            posicio = ord(caracter) - ord('a')
            nova_posicio = (posicio + desplacament) % 26
            resultat += chr(nova_posicio + ord('a'))
        else:
            resultat += caracter
    return resultat


def desxifrar_cesar(text_xifrat: str, desplacament: int) -> str:
    return xifrar_cesar(text_xifrat, -desplacament)


def main():
    print("=== PROGRAMA DE XIFRATGE CÈSAR ===")
    
    # Entrades de l'usuari
    text_original = input("Introdueix la paraula o frase: ")
    
    while True:
        try:
            clau = int(input("Introdueix el desplaçament (un número enter): "))
            break
        except ValueError:
            print("⚠️ Si us plau, entra un número enter vàlid.")

    # Processament
    text_xifrat = xifrar_cesar(text_original, clau)
    text_desxifrat = desxifrar_cesar(text_xifrat, clau)

    # Mostrar resultats
    print("\n--- RESULTATS ---")
    print(f"🔒 Text xifrat:   {text_xifrat}")
    print(f"🔓 Text desxifrat: {text_desxifrat}")

if __name__ == "__main__":
    main()