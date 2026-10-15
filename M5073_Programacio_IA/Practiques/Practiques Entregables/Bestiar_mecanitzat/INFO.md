# Informació del programa

## De què tracta?

Aquest programa simula una batalla per torns entre tres tancs, cadascun
pertanyent a una facció diferent: Chimpanzini Bananini, Lirilí Larilá i
Tralalero Tralala. La simulació utilitza decisions i esdeveniments aleatoris,
de manera que cada execució pot donar un resultat diferent.

Durant cada ronda, un tanc operatiu ataca un altre tanc amb el següent projectil
del seu carregador. Hi ha projectils regulars i perforants, amb diferents
precisions i danys. Cada tanc té blindatge superior i inferior, i les faccions
tenen característiques pròpies que poden influir en el blindatge o en els
efectes dels atacs. El programa mostra l'estat dels tancs i el resultat de cada
ronda. La batalla acaba quan només queda un tanc operatiu, que és declarat
guanyador.

## Aspectes tècnics

El projecte està implementat en Python i aprofita diverses estructures bàsiques
de programació orientada a objectes i enumeracions:

- `TipusProjectil` és un `Enum` que defineix les propietats de cada munició:
  - `PR`: projectil regular, amb dany moderat i precisió alta.
  - `PP`: projectil perforant, amb dany més elevat però precisió més baixa.
- `Faccio` també és un `Enum` i encapsula el nom de la facció, la prioritat de
  blindatge (`superior`, `inferior` o `igual`) i la seqüència de projectils que
  utilitza cada tanc.
- La classe `Tank` gestiona l'estat del vehicle i inclou:
  - atributs per al nom, la facció i el carregador,
  - un blindatge representat com una matriu 2x3, on la primera fila és
    blindatge superior i la segona, inferior,
  - mètodes per obtenir el següent projectil, aplicar danys i comprovar si el
    tanc continua operatiu.
- La simulació de combat es centralitza a `SimulacioBatalla`, que selecciona
  aleatòriament l'atacant i l'objectiu, executa una ronda, mostra l'estat del
  combat i continua fins que queda un sol tanc actiu.

### Mecanisme de combat

La lògica clau del joc es basa en:

1. Selecció aleatòria de l'atacant entre els tancs encara operatius.
2. Extracció del següent projectil del carregador circular del tanc.
3. Comprovació de precisió amb `random()`: si el valor excedeix la precisió,
   el projectil falla i no causa dany.
4. Aplicació de modificadors per facció:
   - Chimpanzini Bananini pot reduir parcialment el dany rebut.
   - Lirilí Larilá pot esquivar alguns atacs.
   - Tralalero Tralala pot esquivar o reduir el dany en funció d'una probabilitat.
5. Selecció aleatòria d'una de les 3 posicions del blindatge superior o inferior.
6. Descompte del dany i redondeig del valor final del blindatge.
7. Comprovació del estat del tanc: si qualsevol valor del blindatge queda negatiu,
   el tanc deixa de ser operatiu.

### Estructura de dades i probabilitat

El model fa servir dos elements molt importants:

- `Enum`: per mantenir constants semàntiques (tipus de projectils i faccions).
- `random` de la biblioteca estàndard: per introduir aleatorietat en la precisió,
  l'impacte, l'elecció d'atacants i la selecció de la zona del blindatge.

Això fa que cada partida sigui diferent, però seguixi una regla coherent i
replicable a partir del codi. El sistema també empra llistes i matrius
anidades per representar el blindatge, cosa que facilita la modificació de la
lògica de defensa i les probabilitats de cada facció.

## Com executar-lo?

Per iniciar la simulació, obre PowerShell a la carpeta del projecte i executa
el fitxer `main.py`:

```powershell
python .\main.py
```

## Fitxers principals

- `main.py`: punt d'entrada del programa; crea els tres tancs i inicia la
  simulació.
- `simulacio.py`: conté tota la lògica del model, incloent les enumeracions,
  la classe `Tank`, la classe `SimulacioBatalla` i la seqüència de rounds.

Aquest esquema manté la lógica separada del punt d'entrada, cosa que facilita
la mantenibilitat, la lectura del codi i les possibles ampliacions futures del
sistema.
