# T1.5. IA fiable i marc legal

**Mòdul:** M5071 - Models d'Intel·ligència Artificial  
**Professor:** Miquel Floriach (`mfloriach@sapalomera.cat`)  
**Llicència:** Reconeixement-CompartirIgual 4.0 Internacional (CC BY-SA)

---

## 1. Introducció a la IA Fiable

L'any 2019 es van establir unes directrius ètiques fonamentals per garantir el desenvolupament d'una **IA fiable**. Perquè un sistema d'intel·ligència artificial es consideri fiable, no n'hi ha prou que s'adapti strictament a la legalitat vigent, sinó que s'exigeix el compliment simultani de tres grans dimensions:

1. **Legal:** Respecte absolut de totes les disposicions legals i reglamentàries aplicables.
2. **Ètica:** Respecte rigorós dels principis i valors ètics de la societat.
3. **Robusta:** Des d'una perspectiva estrictament tècnica, tenint sempre en compte l'entorn social on s'implementa.

### Responsabilitats compartides
Aquests requisits no recauen només sobre un sol actor, sinó que s'han de treballar, implementar i avaluar constantment per totes les parts implicades:
* **Desenvolupadors:** Han d'introduir i aplicar els requisits tècnics i ètics des de la fase de disseny.
* **Organitzacions (responsables del desplegament):** Han d'assegurar-se que els sistemes funcionen complint tots els requisits en l'entorn real.
* **Usuaris finals i societat:** Han de romandre informats sobre aquests requisits i disposar de la capacitat de demanar-ne el compliment.

---

## 2. Requisits per a una IA Fiable

La IA fiable es descompon en 7 pilars o requisits clau que s'han de garantir durant tot el cicle de vida del sistema:

### 2.1. Acció i supervisió humanes
* **Drets fonamentals:** Respectar els drets fonamentals de les persones, minimitzant qualsevol impacte negatiu o avaluant acuradament el balanç quan es pretenguen protegir els drets i llibertats d'altres persones.
* **Acció humana:** Assegurar que els usuaris puguin prendre decisions autònomes amb coneixement de causa. Cal anar amb compte especial amb els sistemes dissenyats per manipular el subconscient. Es recorda el dret a no ser sotmès a conseqüències legals derivades exclusivament de processos automatitzats (protegit també per la normativa de protecció de dades).
* **Supervisió humana (Mecanismes de governança):**
  * *Participació humana:* Capacitat d'intervenir de manera activa en tots els cicles de decisió del sistema.
  * *Control humà:* Capacitat d'intervenir durant el disseny del sistema i en el seguiment del seu funcionament.
  * *Mandat humà:* Capacitat de supervisar l'activitat global (efectes) i decidir com i quan utilitzar el sistema.
  * *Supervisió pública:* En qualsevol cas, cal la supervisió per part de responsables públics quan escaigui.

### 2.2. Solidesa tècnica i seguretat
* **Principi de prevenció del danys:** Desenvolupament amb un enfocament preventiu per minimitzar danys involuntaris i inesperats.
* **Resistència a atacs i seguretat:** Protecció davant vulnerabilitats malicioses dirigides a:
  * Les dades (ex. *enverinament de dades* / *data poisoning*).
  * El model (fallades algorísmiques).
  * La infraestructura tecnològica.
* **Pla de replegament i seguretat general:** Disposar de salvaguardes de seguretat, com ara mecanismes per passar automàticament a un model basat en normes o exigir la intervenció immediata d'un operador humà.
* **Precisió:** Utilitzar models que assoleixin alts nivells de precisió o que indiquin clarament el marge d'error.
* **Fiabilitat i reproductibilitat:** Els resultats del sistema han de ser consistents i iguals sota les mateixes condicions d'entrada.

### 2.3. Privacitat i gestió de dades
* **Protecció de la intimitat i les dades:** Garantir la salvaguarda de la intimitat i de les dades dels usuaris, tant les proporcionades directament com els continguts generats o la informació inferida.
* **Qualitat i integritat de les dades:** Analitzar exhaustivament que les dades utilitzades estiguin lliures de biaixos i no siguin malicioses abans de ser emprades en l'entrenament.
* **Accés a les dades:** Establir protocols estrictes que detallen qui pot accedir a les dades i sota quines circumstàncies concretes.

### 2.4. Transparència
* **Traçabilitat:** Documentar absolutament tot el procés seguint la norma més rigorosa possible.
* **Explicabilitat:** Les decisions preses pel model han de ser comprensibles per als éssers humans. Si pot haver-hi un impacte significatiu en la vida d'una persona, el sistema ha de ser explicable (tot cercant un equilibri amb la precisió si cal).
* **Comunicació clara:** Un sistema d'IA no es pot presentar mai com un humà; les persones tenen dret a saber que estan interactuant amb una IA i se'ls ha de donar l'opció de parlar amb una persona real. Segons el cas, cal comunicar la precisió i les limitacions del sistema.

### 2.5. Diversitat, no discriminació i equitat
* **Eliminació de biaixos:** Evitar biaixos injustos eliminant elements discriminatoris en la fase de recopilació de dades. Es recomana fomentar equips de desenvolupament diversos (cultures, gèneres, disciplines).
* **Accessibilitat i disseny universal:** Garantir que els sistemes puguin ser utilitzats per qualsevol persona independentment de la seva edat, gènere, capacitats o discapacitats.
* **Participació de parts interessades:** Consultar els col·lectius que es puguin veure afectats pel sistema d'IA tant en la fase de disseny com al llarg de tot el seu cicle de vida.

### 2.6. Benestar social i mediambiental
* **IA sostenible:** Minimitzar l'impacte ambiental del sistema d'IA i de tota la seva cadena de subministrament (consum energètic, emissions), prioritzant opcions menys perjudicials.
* **Impacte social:** Vigilar l'efecte del sistema sobre la salut física i mental de les persones.
* **Societat i democràcia:** Avaluar l'impacte sobre les institucions democràtiques, especialment en contextos de presa de decisions polítiques i processos electorals.

### 2.7. Rendiment de comptes (Accountability)
* **Auditabilitat:** Els components del sistema (dades, algorismes i disseny) han de poder ser avaluats. Si afecten drets fonamentals, s'exigeixen auditories independents.
* **Minimització i notificació d'efectes negatius:** Garantir canals per informar sobre decisions adverses i protegir legalment a qui traslladi preocupacions legítimes.
* **Cerca d'equilibris i compensacions:** Documentar i justificar els equilibris entre requisits i disposar de mecanismes accessibles per assegurar compensacions adequades en cas d'efectes adversos.

---

## 3. Marc legal: Regulació de la IA (AI Act)

El marc normatiu europeu de la IA (regulació de 2024, amb modificacions recents fins al 2026) s'estructura al voltant d'una **piràmide basada en el nivell de risc** dels sistemes.

```
          /\
         /  \          <-- 1. Risc Inacceptable (Prohibit)
        /----\
       /      \        <-- 2. Alt Risc (Estrictament Regulat)
      /--------\
     /          \      <-- 3. Risc de Transparència (Obligacions d'informació)
    /------------\
   /              \    <-- 4. Risc Mínim o Sense Risc (Sense normativa específica)
  ------------------
```

### 3.1. Nivell 1: Risc inacceptable (Prohibit)
Es consideren una amenaça clara per a la societat i estan totalment prohibits:
* Manipulació i engany perjudicials basats en IA (inclosos mètodes subliminals).
* Explotació nociva de vulnerabilitats de col·lectius específics.
* Sistemes de puntuació social (*social scoring*).
* Avaluació o predicció de la probabilitat de comissió d'infraccions penals basades únicament en perfils sense fets objectius.
* *Scrapping* indiscriminat d'internet o càmeres de videovigilància (CCTV) per nodrir bases de dades de reconeixement facial.
* Sistemes de reconeixement d'emocions en l'àmbit laboral o educatiu.
* Categorització biomètrica per deduir característiques protegides.
* Identificació biomètrica remota en temps real amb finalitats policials en espais d'accés públic.
* **Deepfakes sexuals no consentits i material d'abús sexual a menors** (aplicacions de "nudificació", incorporades en la modificació de desembre de 2026).
*(Nota: Cal revisar sempre la lletra petita de la llei per conèixer matisos i excepcions específiques).*

### 3.2. Nivell 2: Alt risc
Sistemes que poden plantejar riscos greus per a la salut, la seguretat o els drets fonamentals:
* Components de seguretat en infraestructures crítiques.
* Sistemes educatius que condicionen l'accés a l'educació o la carrera professional.
* Eines d'IA per a la gestió de treballadors i accés a l'ocupació.
* Serveis essencials (públics i privats).
* Identificació biomètrica remota (no indiscriminada), reconeixement d'emocions i categorització biomètrica autoritzada.
* Ús policial, gestió de la immigració/asil, control fronterer, administració de justícia i processos democràtics.

**Obligacions específiques per a l'alt risc (aplicables a partir del 2 de desembre de 2027):**
* Implementar sistemes adequats d'avaluació i mitigació de riscos.
* Assegurar una alta qualitat de les dades per evitar discriminacions.
* Mantenir registres d'activitat (*logs*) per garantir la traçabilitat.
* Elaborar una documentació tècnica detallada.
* Proporcionar informació clara i adequada a l'implementador.
* Establir mesures efectives de supervisió humana.
* Garantir un alt nivell de robustesa, ciberseguretat i precisió.

*El cicle de vida de l'alt risc inclou:* Desenvolupament $\rightarrow$ Avaluació de conformitat $\rightarrow$ Registre en base de dades europea $\rightarrow$ Declaració de conformitat (marcatge CE) $\rightarrow$ Posada al mercat i monitoratge post-mercat.

### 3.3. Nivell 3: Risc de transparència
Aplica quan hi ha riscos associats a la manca de transparència comunicativa (amb obligacions a partir d'agost de 2026):
* Informar obligatòriament quan s'interacciona directament amb un sistema d'IA (si no és evident).
* Garantir que els proveïdors facin que els continguts generats per IA siguin clarament identificables.
* Informar sobre el funcionament de sistemes de reconeixement d'emocions o categorització biomètrica.
* Identificar marcadament els continguts modificats o generats artificialment (com ara **Deepfakes** o textos publicats amb la finalitat d'informar sobre assumptes d'interès públic).

### 3.4. Nivell 4: Risc mínim o sense risc
* Inclou aplicacions innòcues com els filtres de correu brossa (*spam filters*) o la IA en videojocs. No se'ls aplica cap restricció normativa específica.

---

## 4. Marc legal: Protecció de dades i drets digitals

### 4.1. Drets dels ciutadans (Reglaments europeus i estatals)
L'objectiu principal és garantir i protegir la privacitat i la intimitat de les persones físiques mitjançant un catàleg de drets:
* **Dret d'accés:** Faculta l'accés remot, directe i segur a les dades personals pròpies.
* **Dret de rectificació:** Correcció immediata de dades inexactes.
* **Dret de supressió (Dret a l'oblit):** Eliminació de les dades personals quan correspongui legalment.
* **Dret a la limitació del tractament:** Restricció de l'ús posterior de les dades en supòsits determinats.
* **Dret a la portabilitat:** Rebre les dades personals en un format estructurat per transmetre-les a un altre responsable.
* **Dret d'oposició:** Negar-se al tractament de les dades en circumstàncies concretes.

### 4.2. Responsabilitat proactiva (*Accountability*)
S'obliga formalment a les empreses i administracions públiques a adoptar mesures tècniques i organitzatives prèvies per garantir i poder demostrar en tot moment que el tractament de dades es realitza de manera segura i legal.

### 4.3. Llei orgànica 3/2018 (LOPDGDD)
* Implementa la normativa de protecció de dades europea al marc espanyol.
* Fixa l'edat mínima per al consentiment en el tractament de dades en **14 anys**.
* Incorpora un capítol específic dedicat a la **garantia dels drets digitals** (Títol X).