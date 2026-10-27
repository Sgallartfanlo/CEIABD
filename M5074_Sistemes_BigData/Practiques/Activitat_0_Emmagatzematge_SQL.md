# Activitat 0: Emmagatzematge NoSQL, Teorema CAP i Moviment NewSQL

## Taula de Continguts
1. [Resum Executiu i Objectius](#1-resum-executiu-i-objectius)
2. [Part 1: Preguntes i Conceptes Fonamentals NoSQL](#2-part-1-preguntes-i-conceptes-fonamentals-nosql)
   - [1.a. El significat del prefix "No" a NoSQL](#1a-el-significat-del-prefix-no-a-nosql)
   - [1.b. Replicació i Particionat Simultani](#1b-replicació-i-particionat-simultani)
   - [1.c. Selecció i Justificació de Models de Dades](#1c-selecció-i-justificació-de-models-de-dades)
   - [1.d. Persistència Poliglota (Polyglot Persistence)](#1d-persistència-poliglota-polyglot-persistence)
   - [1.e. Classificació de Bases de Dades segons el Teorema CAP](#1e-classificació-de-bases-de-dades-segons-el-teorema-cap)
3. [Part 2: El Moviment NewSQL i Bases de Dades Modernes](#3-part-2-el-moviment-newsql-i-bases-de-dades-modernes)
   - [Concepte i Context Històric](#concepte-i-context-històric)
   - [Característiques Principals de NewSQL](#característiques-principals-de-newsql)
   - [Comparativa Tripartida: SQL vs. NoSQL vs. NewSQL](#comparativa-tripartida-sql-vs-nosql-vs-newsql)
   - [Estudi de Cas 1: CockroachDB](#estudi-de-cas-1-cockroachdb)
   - [Estudi de Cas 2: VoltDB](#estudi-de-cas-2-voltdb)
   - [Conclusions de la Presentació](#conclusions-de-la-presentació)
4. [Taula de Referència Ràpida](#4-taula-de-referència-ràpida)
5. [Recursos i Referències](#5-recursos-i-referències)

---

## 1. Resum Executiu i Objectius

Aquesta pràctica té com a objectiu analitzar les diferències conceptuals i arquitectòniques entre els sistemes de gestió de bases de dades relacionals tradicionals (RDBMS), les tecnologies **NoSQL** i l'emergència del moviment **NewSQL**.

### Objectius d'Aprenentatge
* Comprendre el significat i l'evolució de l'acrònim **NoSQL** (*Not Only SQL*).
* Analitzar les tècniques de distribució de dades: **Particionat (Sharding)** i **Replicació (Replication)**.
* Identificar el model de dades adequat (Relacional, Documental, Grafs, Clau-Valor, etc.) segons els requisits d'un cas d'ús real.
* Assimilar el concepte arquitectònic de **Persistència Poliglota** (*Polyglot Persistence*).
* Aplicar el **Teorema CAP** (Consistency, Availability, Partition Tolerance) per classificar els SGBD no relacionals més rellevants del mercat.
* Analitzar el moviment **NewSQL**, avaluant les solucions d'alta disponibilitat i alt rendiment com **CockroachDB** i **VoltDB**.

---

## 2. Part 1: Preguntes i Conceptes Fonamentals NoSQL

### 1.a. El significat del prefix "No" a NoSQL

L'acrònim **NoSQL** inicialment s'associava a la negació "No a SQL". Tanmateix, en l'actualitat el prefix "No" fa referència a **"Not Only SQL"** (*No només SQL*).

* **Context:** Aquest concepte indica que les bases de dades NoSQL no intenten substituir per complet els sistemes relacionals (RDBMS), sinó actuar com a alternança o complement especialitzat.
* **Prioritats:** Els sistemes NoSQL sacrifiquen sovint la consistència immediata i l'atomicitat estricta de les transaccions a canvi d'oferir **alta disponibilitat**, **baixa latència** i **escalabilitat horitzontal massiva**.

---

### 1.b. Replicació i Particionat Simultani

**Pregunta:** *Un sistema pot suportar al mateix temps replicació i particionat?*

**Resposta:** **Sí.** De fet, en entorns de distribució de dades de producció i Big Data, la combinació de totes dues tècniques constitueix l'arquitectura estàndard per garantir el millor rendiment i la màxima tolerància a fallades.

#### Mètodes de Distribució
1. **Particionat (Sharding / Horizontal Partitioning):**
   * Divideix el conjunt total de dades en subconjunts o fragments (*shards*) assignats a servidors o nodes diferents.
   * *Objectiu:* Distribuir la carregar de lectura/escriptura i augmentar la capacitat d'emmagatzematge (Escalabilitat horitzontal).
2. **Replicació (Replication):**
   * Copia les mateixes dades en múltiples nodes (*Primary/Secondary* o *Peer-to-Peer*).
   * *Objectiu:* Tolerar fallades de maquinari (*High Availability*) i millorar la capacitat de lectura paral·lela.

#### Arquitectura Combinada (Sharded Cluster + Replica Sets)
En un entorn real (com MongoDB o Cassandra):
* La base de dades es **particiona** en $N$ shards.
* Cada shard no és una única màquina solitària, sinó un **grup de rèpliques** (*Replica Set* de 3 o més nodes).
* **Resultat:** Si un node d'una partició cau, un altre node del mateix grup de rèpliques el substitueix immediatament sense que la partició sencera quedi inoperativa.

---

### 1.c. Selecció i Justificació de Models de Dades

#### Supòsit 1: Wiki sobre personatges de còmics
* **Model recomanat:** **Documental** (o opcionalment de **Grafs**).
* **Justificació:** 
  * Un gestor de contingut tipus Wiki té atraccions molt heterogènies segons el personatge (ex. poders, afiliacions, primera aparició, creadors, enemics).
  * L'ús de formats flexibles com **JSON/BSON** permet modificar o afegir atributs a cada personatge sense haver d'executar actualitzacions d'esquema complexes (`ALTER TABLE`).
  * Si la Wiki requereix analitzar intensament relacions complexes entre personatges (ex. "amics de", "enemics de", "equips compartits"), un model de **Grafs** (ex. Neo4j) també seria una opció vàlida.

#### Supòsit 2: Informació acadèmica d'un país (centres, alumnes, professors, assignatures, qualificacions...)
* **Model recomanat:** **Relacional (SQL)**.
* **Justificació:** 
  * Aquest entorn exigeix una **integritat referencial rigorosa** i transaccions complexes que requereixen garanties **ACID** (Atomicitat, Consistència, Aïllament i Durabilitat).
  * Les notes oficials, matrícules i expedients acadèmics no poden permetre inconsistències de dades o escriptures parcials.
  * Les bases de dades NoSQL documentals no estan optimitzades per a sistemes operacionals on predominen les operacions transaccionals denses i interconnectades.

---

### 1.d. Persistència Poliglota (Polyglot Persistence)

La **Persistència Poliglota** és un patró d'arquitectura de programari introduït per Neal Ford i popularitzat per Martin Fowler.

* **Definició:** Consisteix a utilitzar **múltiples tecnologies de bases de dades diferents** dins d'una mateixa aplicació o ecosistema de microserveis, en comptes de forçar una única base de dades a gestionar tots els tipus de dades.
* **Premissa:** *"No existeix una única base de dades ideal per a tots els casos d'ús"* (*One size does NOT fit all*).

#### Exemple d'Arquitectura Poliglota (E-commerce)
```
                  ┌────────────────────────────────────────┐
                  │          Aplicació Web / APIS          │
                  └───┬──────────────┬──────────────┬──────┘
                      │              │              │
        ┌─────────────┴──┐   ┌───────┴────────┐   ┌─┴──────────────┐
        │  PostgreSQL    │   │     Redis      │   │ Elasticsearch  │
        │  (Relacional)  │   │  (Clau-Valor)  │   │ (Cerca Text)   │
        └─────────────┬──┘   └───────┬────────┘   └─┬──────────────┘
                      │              │              │
             Comandes/Pagaments    Sessió/Caché    Cercador Catàleg
```

1. **PostgreSQL (SQL):** Gestiona les comandes, facturació i pagaments (garanteix ACID).
2. **Redis (Clau-Valor en memòria):** Emmagatzema sessions d'usuari i la meva de la compra per a un accés ultraràpid.
3. **Elasticsearch (Motor de cerca / Documental):** Permet cerques de text complet sobre el catàleg de productes.
4. **Neo4j (Grafs):** Gestiona el motor de recomanacions de productes basat en el comportament d'altres usuaris.

---

### 1.e. Classificació de Bases de Dades segons el Teorema CAP

El **Teorema CAP** (o Teorema d'Brewer) estableix que en un sistema distribuït de dades és impossible garantir simultàniament les tres propietats següents:

1. **C**onsistency (Consistència): Tots els nodes veuen les mateixes dades al mateix temps.
2. **A**vailability (Disponibilitat): Tota petició rep una resposta (sense garantia de ser la darrera versió).
3. **P**artition Tolerance (Tolerància a Particions): El sistema continua funcionant malgrat fallades de xarxa entre nodes.

Degut a que en qualsevol xarxa distribuïda les particions físiques poden ocórrer (**P**), els sistemes s'han de dissenyar prioritzant **CP** (Consistència davant Partició) o **AP** (Disponibilitat davant Partició). Els sistemes **CA** només existeixen quan no hi ha distribució en xarxa (nodes únics tradicionals).

#### Classificació dels SGBD NoSQL

| Base de Dades | Model Principal | Classificació CAP | Descripció de la Triada |
| :--- | :--- | :---: | :--- |
| **BigTable** | Columnar / Wide-column | **CP** | Prioritza consistència; en cas de discordança bloqueja l'accés fins a sincronitzar. |
| **Cassandra** | Columnar / Wide-column | **AP** | Masterless arquitectura; prioritza l'alta disponibilitat i consistència eventual. |
| **CouchDB** | Documental | **AP** | Dissenyat per sincronització fora de línia amb consistència eventual. |
| **DynamoDB** | Clau-Valor / Documental | **AP** | Alta disponibilitat gestionada per AWS amb consistència configurable. |
| **HBase** | Columnar (sobra Hadoop) | **CP** | Basat en l'arquitectura de BigTable; garanteix lectures/escriptures consistents. |
| **MongoDB** | Documental | **CP** | El node primari rep escriptures; si hi ha partició, la secció sense majoria denega escriptures. |
| **Redis** | Clau-Valor (In-Memory) | **CP** | Master-Slave primari; si es perd connexió amb la majoria, es pot restringir l'escriptura. |
| **Riak** | Clau-Valor | **AP** | Basat en el paper Dynamo d'Amazon; resol conflictes de lectura (eventual). |
| **Voldemort** | Clau-Valor | **AP** | Desenvolupat per LinkedIn; arquitectura distribuïda d'alta disponibilitat. |

---

## 3. Part 2: El Moviment NewSQL i Bases de Dades Modernes

### Concepte i Context Històric

El terme **NewSQL** va ser encunyat l'any 2011 per l'analista de 451 Group, Matthew Aslett. Sorgiment com a resposta a una cruïlla tecnològica:

* **SQL Tradicional:** Bon suport transaccional (ACID) i estàndard consolidat, però amb dificultats extremes per escalar horitzontalment.
* **NoSQL:** Alta escalabilitat horitzontal i disponibilitat, però a costa de renuncia al llenguatge SQL i a les transaccions complexes d'alta consistència.

**NewSQL** neix per unir el millor de tots dos mons: **mantenir el model relacional, el llenguatge SQL i les transaccions ACID**, però adoptant les **arquitectures distribuïdes i escalables d'alta disponibilitat** pròpies de NoSQL.

---

### Característiques Principals de NewSQL

1. **Interfície i Model SQL:** Permet executar consultes complexes directament amb la sintaxi estàndard SQL.
2. **Garantia ACID Estricta:** Assegura que totes les transaccions d'escriptura/lectura compleixin Atomicitat, Consistència, Aïllament i Durabilitat en entorns distribuïts.
3. **Escalabilitat Horitzontal Automàtica (*Elastic Scalability*):** Permet afegir nous nodes al clúster per augmentar la capacitat sense interrompre el servei.
4. **Arquitectura No-Blocking / Alta Disponibilitat:** Replicació automàtica basada en algorismes de consens distribuït (com **Raft** o **Paxos**).
5. **Alt Rendiment Transaccional (OLTP):** Optimitza el motor d'emmagatzematge usant tecnologies en memòria (*In-Memory*) o estructures d'índexs LSM-Trees modernes.

---

### Comparativa Tripartida: SQL vs. NoSQL vs. NewSQL

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EVOLUCIÓ DELS PARADIGMES                           │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│   SQL Tradicional    │        NoSQL         │            NewSQL             │
│ (ex. PostgreSQL, MySQL)│ (ex. MongoDB, Cassandra)│ (ex. CockroachDB, VoltDB)     │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ • Model Relacional   │ • Model Flexible     │ • Model Relacional            │
│ • Escalabilitat Vert.│ • Escalabilitat Horiz.│ • Escalabilitat Horitzontal    │
│ • Transaccions ACID  │ • Consistència Event.│ • Transaccions ACID           │
│ • Llenguatge SQL     │ • APIs / No-SQL      │ • Llenguatge SQL              │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

| Característica | SQL Tradicional (RDBMS) | NoSQL | NewSQL |
| :--- | :--- | :--- | :--- |
| **Model de dades** | Relacional (Taules, Esquema rígid) | Documental, Clau-Valor, Graf, Columnes | Relacional (Taules, Esquema flexible/estricte) |
| **Escalabilitat** | Principalment **Vertical** (Scale-up) | **Horitzontal** (Scale-out) | **Horitzontal** (Scale-out) |
| **Llenguatge** | SQL | APIs pròpies, JSON, No-SQL | SQL (sovint compatible amb PostgreSQL/MySQL) |
| **Consistència** | **ACID** (Immediata) | BASE (Consistència eventual / Configurable) | **ACID** (Immediata i Distribuïda) |
| **Algorisme de Consens**| N/A (Node únic o Primary-Replica) | Eventual, Quòrum, Gossip | Paxos, Raft, Multi-Version Concurrency (MVCC) |
| **Cas d'ús ideal** | Sistemes transaccionals clàssics | Gran volum, dades desestructurades | OLTP a gran escala, fintech, aplicacions globals |

---

### Estudi de Cas 1: CockroachDB

**CockroachDB** és una base de dades SQL distribuïda Cloud-Native dissenyada per ser pràcticament "indestructible" (d'aquí el seu nom, en referència a la resistència de les cucaratxes).

#### Característiques Clau
* **Compatibilitat:** Utilitza el protocol de comunicació de **PostgreSQL**, permetent als desenvolupadors usar els mateixos drivers i eines.
* **Consens Distribuït:** Utilitza l'algorisme **Raft** per a la replicació i consens de dades en grups de tres o més nodes.
* **Transaccions ACID Globals:** Implementa MVCC (Multi-Version Concurrency Control) combinat amb transaccions de serialització distribuïda.
* **Survivabilitat i Auto-reparació:** Pot resistir fallades de nodes individuals, servidors interns o regions senceres d'un proveïdor cloud sense pèrdua de dades.

#### Cas d'Ús d'Exemple
> **E-Commerce Global i Plataformes de Pagaments:**  
> Una botiga en línia multinacional utilitza CockroachDB per gestionar les comandes i el saldo dels clients. Encara que un centre de dades sencer a Europa caigui, el clúster a Amèrica i Àsia manté la consistència exacta de l'inventari i el saldo dels usuaris sense cap desfasament temporal.

---

### Estudi de Cas 2: VoltDB

**VoltDB** és una base de dades relacional NewSQL dissenyada especialment per al **processament de transaccions d'alta velocitat (Fast Data / Real-Time Analytics)**.

#### Característiques Clau
* **Arquitectura In-Memory:** Tota la base de dades s'executa principalment en memòria RAM, eliminant els colls d'ampolla del disc tradicional.
* **Processament Single-Thread per Partició:** Elimina els bloquejos complexos de transaccions (*lockless architecture*), executant procediments emmagatzemats de manera seqüencial ultra-ràpida a cada partició.
* **Latència Ultrabaixa:** Capaç d'executar centenars de milers d'operacions per segon amb latències de sub-mil·lisisegons.
* **Transaccions ACID sobre Dades en Vol:** Manté garanties ACID estrictes per a dades en moviment continu.

#### Cas d'Ús d'Exemple
> **Telecomunicacions i Detecció de Frau en Temps Real:**  
> Una companyia de telecomunicacions utilitza VoltDB per analitzar milions d'esdeveniments de trucades i dades per segon. VoltDB avalua si una transacció amb targeta de crèdit o una trucada és fraudulenta i autoritza o denega l'operació en menys d'1 mil·lisisegon.

---

### Conclusions de la Presentació

1. **Evolució Necessària:** NewSQL representa l'evolució natural del model relacional per adaptar-se a les exigències de les arquitectures cloud i el Big Data.
2. **Complementarietat:** NewSQL no elimina NoSQL ni SQL tradicional, sinó que ofereix la millor alternativa per a aplicacions transaccionals (OLTP) que requereixen escalar horitzontalment.
3. **Dualitat d'Enfocaments NewSQL:**
   * **CockroachDB:** Orientat a l'alta disponibilitat distribuïda globalment, la consistència forta i la resistència a fallades físiques.
   * **VoltDB:** Orientat al rendiment extrem, processament en memòria i baixíssima latència en temps real.

---

## 4. Taula de Referència Ràpida

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           RESUM DE MAPATGE TECNOLÒGIC                            │
├─────────────────┬─────────────────────┬───────────────────────┬───────────────────┤
│ Categoria       │ Tecnologia Exemple  │ Model Principal       │ Prioritat CAP     │
├─────────────────┼─────────────────────┼───────────────────────┼───────────────────┤
│ NoSQL           │ MongoDB             │ Documental (BSON)     │ CP                │
│ NoSQL           │ Cassandra           │ Wide-Column           │ AP                │
│ NoSQL           │ Redis               │ Clau-Valor (Memòria)  │ CP                │
│ NewSQL          │ CockroachDB         │ Relacional Distribuït │ CP (Strong Cons.) │
│ NewSQL          │ VoltDB              │ In-Memory Relacional  │ CP                │
│ SQL Tradicional │ PostgreSQL / MySQL  │ Relacional            │ CA (Node Únic)    │
└─────────────────┴─────────────────────┴───────────────────────┴───────────────────┘
```

---

## 5. Recursos i Referències

* **Documentació Teorema CAP:** *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services* (Seth Gilbert & Nancy Lynch).
* **Persistència Poliglota:** *Martin Fowler - Polyglot Persistence Articles (martinfowler.com)*.
* **CockroachDB Docs:** [https://www.cockroachlabs.com/docs/](https://www.cockroachlabs.com/docs/)
* **VoltDB Docs:** [https://www.voltdb.com/](https://www.voltdb.com/)
