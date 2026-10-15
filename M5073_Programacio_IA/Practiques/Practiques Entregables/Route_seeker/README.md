# Route Seeker

Aquest programa és una petita aplicació de recerca de camins en una matriu, escrita en Python. La seva finalitat és trobar una ruta possible des d'una casella d'inici fins a una casella objectiu, evitant les cel·les bloquejades i sense retrocedir sobre el mateix moviment anterior.

## Què fa

El programa defineix una graella quadrada amb aquests valors:

- `START`: posició inicial
- `GOAL`: objectiu final
- `R`: cel·les disponibles per on es pot passar
- `x`: cel·les bloquejades que no es poden travessar

A partir d'aquesta matriu, el programa:

1. Localitza la posició de `START`.
2. Comprova els possibles moviments: amunt, avall, esquerra i dreta.
3. Valida si cada moviment és vàlid:
   - no surt de la matriu
   - no entra en una casella bloquejada (`x`)
   - no fa el moviment invers del precedent, per evitar enrere
4. Avança pas a pas fins a arribar a `GOAL`.
5. Mostra la ruta final en format de coordenades, per exemple:
   `(1, 1) > (2, 1) > (2, 2) > ...`

## Estructura del programa

El codi principal té aquestes parts:

- `main()`: configura la matriu, cerca l'inici, recorre el camí i imprimeix el resultat.
- `pot_moure(...)`: funció que determina si un moviment és possible.
- `MOVEMENTS`: llista dels quatre moviments possibles.
- `MATRIX_1`: mapa del laberint o espai navegable.

## Exemple de funcionament

Quan s'executa el programa, genera una sortida semblant a aquesta:

```text
El camí per poder arribar a l'objectiu es:
(6, 1) > (5, 1) > (4, 1) > ... > (1, 6)
```

La ruta exacta pot variar segons la matriu i l'algoritme de desplaçament implementat.

## Execució

Per executar-lo, simplement s'ha de correr el fitxer Python:

```bash
python Route_seeker_Gallart_Sergi.py
```

## Objectiu del projecte

El programa serveix com a exemple pràctic de:

- recerca de camins en una matriu
- validació de moviments
- control de caselles bloquejades
- resolució de problemes de navegació simple mitjançant lògica iterativa

És un exercici d'intel·ligència artificial i programació lògica orientat a la recerca de trajectòries en entorns estructurats.
