# M5074 - Sistemes de Big Data
**Emmagatzematge de dades - NoSQL**

* **Nom:** Sergi Gallart Fanlo
* **Professor:** Francesc Barragan
* **Curs:** 2026/2027
* **Centre:** Institut Sa Palomera | CE IA&BD | Generalitat de Catalunya - Departament d'Educació i FP

---

## Activitat 0: Emmagatzematge SQL

### 1. Contesta les següents preguntes:

#### a. Què significa el prefix No de l'acrònim NoSQL?
En l'acrònim NoSQL, fa referència a **«Not Only»** (és a dir, «No només» SQL). 

Això implica que aquests sistemes s'enfocen com a alternatives i complements als sistemes gestors de bases de dades relacionals tradicionals, centrant les seves prioritats en l'escalabilitat i la disponibilitat sobre l'atomicitat i la consistència estricta de les dades.

#### b. Un sistema pot suportar al mateix temps replicació i particionat?
**Sí**, un sistema pot suportar al mateix temps la replicació i el particionat. 

De fet, segons la documentació, l'entorn més segur i amb millor rendiment és aquell que combina ambdues tècniques, és a dir, tenir les dades particionades i, al seu torn, cada partició (o màquina que té un subconjunt de les dades) replicada en dos o més nodes.

#### c. Per als següents supòsits, indica quin model de dades utilitzaries justificant la teva resposta:

1. **Wiki sobre de personatges de còmics.**
   * **Model:** Documental (o de Grafs).
   * **Justificació:** És ideal per a gestors de contingut o plataformes de tipus blog. Utilitza estructures flexibles (com JSON) que permeten emmagatzemar informació variada i personalitzable per a cada personatge sense necessitat d'un esquema rígid.

2. **Informació acadèmica d'un país (centres, alumnes, professors, assignatures, qualificacions, ...)**
   * **Model:** Relacional.
   * **Justificació:** Requereix transaccions complexes i propietats ACID strictly (atomicitat, consistència, aïllament i durabilitat) per garantir la integritat de dades oficials i notes. El document assenyala precisament que les bases de dades NoSQL documentals no convenen per a sistemes operacionals amb transaccions complexes.

#### d. Investiga en què consisteix la persistència poliglota.
La **persistència poliglota** és un patró arquitectònic que consisteix a utilitzar múltiples tecnologies de bases de dades diferents dins d'una mateixa aplicació en lloc d'una de sola. 

Aquest enfocament s'adopta sota la premissa que una única solució no serveix per a tot, assignant cada tipus de dada al model d'emmagatzematge més eficient per al seu cas concret, ja sigui relacional, documental, clau-valor, de grafs o columnar.

#### e. Classifica les següents bases de dades segons el teorema de CAP en CA, CP o AP:
*BigTable, Cassandra, CouchDB, DynamoDB, HBase, MongoDB, Redis, Riak, Voldemort.*

| Base de Dades | Classificació CAP |
| :--- | :--- |
| **BigTable** | CP |
| **Cassandra** | AP |
| **CouchDB** | AP |
| **DynamoDB** | AP |
| **HBase** | CP |
| **MongoDB** | CP |
| **Redis** | CP |
| **Riak** | AP |
| **Voldemort** | AP |

---

### 2. Crea una presentació de 5-6 diapositives on expliquis en què consisteix el moviment NewSQL, la seva relació amb NoSQL i què ofereixen bases de dades com CockroachDB i/o VoltDB.

#### Diapositiva 1: NewSQL
**NewSQL** és un moviment tecnològic que busca combinar els avantatges de les bases de dades SQL tradicionals amb l'escalabilitat i el rendiment dels sistemes distribuïts moderns.

Les bases de dades NewSQL mantenen el model relacional, el llenguatge SQL i les transaccions ACID, però estan dissenyades per gestionar grans quantitats de dades i molts usuaris simultàniament.

#### Diapositiva 2: Característiques principals de NewSQL
Les bases de dades NewSQL ofereixen diverses característiques importants:
* **Llenguatge SQL:** permet consultar i gestionar les dades mitjançant sentències SQL.
* **Transaccions ACID:** garanteixen la fiabilitat i la integritat de les operacions.
* **Escalabilitat horitzontal:** permet augmentar la capacitat afegint més servidors.
* **Alta disponibilitat:** poden continuar funcionant encara que algun servidor falli.
* **Rendiment elevat:** estan preparades per gestionar moltes transaccions simultànies.

#### Diapositiva 3: Relació entre NewSQL i NoSQL
Les bases de dades NoSQL van sorgir, en part, per donar resposta a les limitacions d'escalabilitat de les bases de dades relacionals tradicionals. Ofereixen diferents models d'emmagatzematge, com ara documents, clau-valor o columnes.

NewSQL adopta idees dels sistemes distribuïts associats a NoSQL, però manté les característiques relacionals i les garanties transaccionals pròpies de SQL.

**Comparativa:**
* **SQL tradicional:** utilitza un model relacional i transaccions fiables, amb escalabilitat sovint vertical.
* **NoSQL:** ofereix models de dades diversos i, habitualment, escalabilitat horitzontal.
* **NewSQL:** combina el model relacional, el llenguatge SQL, les transaccions ACID i l'escalabilitat horitzontal.

#### Diapositiva 4: CockroachDB
**CockroachDB** és una base de dades SQL distribuïda dissenyada per oferir escalabilitat, consistència i alta disponibilitat.

**Característiques principals:**
* Utilitza SQL i és compatible amb el protocol de PostgreSQL.
* Distribueix i replica les dades entre diferents nodes.
* Proporciona transaccions ACID i consistència forta.
* Pot continuar funcionant davant de determinades fallades de servidors.

> **Exemple:** Una botiga en línia pot utilitzar CockroachDB per gestionar comandes i pagaments de molts clients, mantenint les dades coherents encara que algun servidor deixi de funcionar.

#### Diapositiva 5: VoltDB
**VoltDB** és una base de dades relacional orientada al processament de transaccions a gran velocitat. Utilitza emmagatzematge en memòria per reduir la latència i processar moltes operacions en poc temps.

**Característiques principals:**
* Utilitza SQL per gestionar les dades.
* Ofereix transaccions ACID.
* Està dissenyada per processar grans volums de transaccions amb baixa latència.
* Pot distribuir el processament entre diversos nodes.

> **Exemple:** Una empresa de telecomunicacions pot utilitzar VoltDB per processar esdeveniments i detectar activitats sospitoses pràcticamente en temps real.

#### Diapositiva 6: Conclusions
* NewSQL representa una evolució de les bases de dades relacionals tradicionals, ja que combina la fiabilitat i la consistència de SQL amb l'escalabilitat dels sistemes distribuïts.
* **CockroachDB** destaca per la seva capacitat de distribuir dades i mantenir-ne la consistència en entorns amb diversos servidors.
* **VoltDB**, en canvi, se centra especialment en el processament transaccional d'alt rendiment i baixa latència.
* En conclusió, NewSQL és una alternativa interessant per a aplicacions que necessiten gestionar moltes transaccions, mantenir la integritat de les dades i escalar sense renunciar al model relacional.