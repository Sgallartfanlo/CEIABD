# Arquitectures de Big Data i Tractament de Dades

**Mòdul M5075 – Big Data Aplicat**

## 1. Introducció i Fonaments del Big Data

### Què és una Arquitectura de Big Data?

Una **arquitectura de Big Data** és el disseny dels sistemes estructurats que donen suport a la ingesta, emmagatzematge, processament i anàlisi de dades. Es dissenya especialment quan les dades tenen un volum o una complexitat que fa impossible el seu tractament mitjançant bases de dades relacionals o sistemes tradicionals.

No es tracta d'una tecnologia concreta, sinó d'una forma d'organitzar components, fluxos de dades i prioritats.

```
┌────────────────┐      ┌────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   Data Sources │ ───> │     Ingest     │ ───> │  Process & Store │ ───> │ Analyze / Insight│
└────────────────┘      └────────────────┘      └──────────────────┘      └──────────────────┘

```

### Les 5 V del Big Data

Per entendre la necessitat d'una infraestructura robusta, s'analitzen les 5 dimensions fonamentals de la dada:

* **Volum:** La quantitat massiva de dades generades (escala de terabytes o petabytes).


* **Velocitat:** La rapidesa amb la qual les dades es generen, s'ingereixen i requereixen resposta.


* **Varietat:** Heterogeneïtat de formats (estructurats, semiestructurats com JSON/XML, o no estructurats com imatges/àudio).


* **Veracitat:** La qualitat, precisió i fiabilitat de la dada font.


* **Valor:** El benefici de negoci o informació útil que se n'extreu des de les dades.



---

## 2. Característiques i Principis de Disseny

### Característiques Clau d'una Arquitectura Distribuïda

Qualsevol disseny distribuït en entorns Big Data ha de complir els principis següents:

1. **Escalabilitat:** Capacitat d'incrementar el rendiment o la capacitat de processament i emmagatzematge segons creix la demanda.


* **Escalat Vertical (*Scale-up*):** Afegir més CPU, memòria RAM o disc a un únic node. Té un límit físic i econòmic clar.


* **Escalat Horitzontal (*Scale-out*):** Afegir més nodes/servidors a un *cluster*. És la base de les arquitectures modernes de Big Data.




2. **Tolerància a Fallades (*Fault Tolerance*):** El sistema ha de mantenir-se operatiu i evadir la pèrdua de dades tot i que fallin servidors físics o processos ("*Everything fails, all the time*").


3. **Dades Distribuïdes:** La informació es reparteix entre diferents nodes per evitar el punt únic de fallada (*Single Point of Failure* o SPOF) i superar els límits d'un sol disc.


4. **Processament Distribuït:** Repartir el tractament de les dades de manera paral·lela entre diferents màquines per reduir els temps d'execució.


5. **Localització de la Dada (*Data Locality*):** Apropar els processos de computació cap al node on hi ha emmagatzemada la dada. Evita el trànsit innecessari de xarxa que penalitza la latència.



---

### Principis WAF (*Well-Architected Framework*)

A l'hora de dissenyar entorns *Cloud*, s'apliquen els pilars recomanats pels proveïdors (AWS, Azure) per evitar la sobreenginyeria:

* **Excel·lència Operativa (*Operational Excellence*):** Executar i monitorar sistemes per aportar valor.


* **Seguretat (*Security*):** Aplicar el *principi de mínim privilegi* i model de responsabilitat compartida.


* **Fiabilitat (*Reliability*):** Planificar per a la recuperació davant de fallades, definint RTO (*Recovery Time Objective*) i RPO (*Recovery Point Objective*).


* **Eficiència del Rendiment (*Performance Efficiency*):** Utilitzar els recursos de manera optimitzada segons la demanda.


* **Optimització de Costos (*Cost Optimization*):** Reduir despeses innecessàries i apagar recursos no utilitzats.


* **Sostenibilitat (*Sustainability*):** Minimitzar l'impacte ambiental de la infraestructura de computació.



---

### Principis Addicionals de Disseny

* **Baix Acoblament:** Ús d'APIs REST, microserveis o marques de missatges perquè cada component es pugui modificar de manera independent.


* **Reversibilitat ("Principi de les dues portes"):** Facilitar el retorn a un estat anterior davant de decisions d'arquitectura errònies.


* **Arquitectura Viva:** Creixement i evolució adaptats als canvis tecnològics i de negoci.



---

## 3. Tipus de Processament: Batch vs. Streaming

| Característica | Processament Batch (Per lots) | Processament en Streaming |
| --- | --- | --- |
| **Definició** | Processament sobre un conjunt finit de dades amb inici i fi definit en el temps.

 | Processament continu de dades a mesura que arriben, sense límit temporal.

 |
| **Volum / Àmbit** | Tot el conjunt de dades històric.

 | Finestres temporals o increments recents.

 |
| **Latència** | Alta (minuts, hores o dies).

 | Baixa (milisegons a segons).

 |
| **Precisió** | Màxima precisió (treballa sobre el 100% de la informació).

 | Ràpida resposta, possiblement amb algun sacrifici de precisió o context.

 |
| **Casos d'ús** | Informes de tancament diari, càlcul de nòmines, conversió de formats (.csv a Parquet).

 | Detecció de frau en temps real, alertes de sensors IoT, monitoratge d'usuaris actius.

 |

> **Nota:** *Temps Real* no implica immediatesa absoluta, sinó una resposta garantida dins d'un límit temporal molt petit (baixa latència).
> 
> 

---

## 4. Arquitectura Lambda ($\lambda$)

Introduïda el 2012 per Nathan Marz, cerca combinar la precisió de processament històric amb la baixa latència de les dades recents.

```
                   ┌─────────────────────────────────────────┐
             ┌───> │  Speed Layer (Hot path / Streaming)     │ ───┐
             │     └─────────────────────────────────────────┘    │
Unified Log  │                                                    ▼
─────────────┤                                            ┌──────────────┐
(Event Data) │     ┌──────────────┐     ┌──────────────┐  │  Serving     │ ───> Analytics Client
             └───> │ Batch Layer  │ ──> │ Serving Layer│ ─>│  Layer       │
                   │ (Cold path)  │     │ (Batch views)│  └──────────────┘
                   └──────────────┘     └──────────────┘

```

### Capes de l'Arquitectura Lambda

1. **Batch Layer (Capa per lots / Cold Path):**
* Rep i emmagatzema les dades en cru de forma immutable (*Master Data*).


* Les dades noves mai se sobreescriuen; s'afegeixen per preservar el llinatge/traçabilitat de la dada.


* Executa algorismes sobre tot el conjunt històric per generar les **Batch Views**. Proporciona la màxima precisió però amb alta latència.




2. **Speed / Streaming Layer (Capa ràpida / Hot Path):**
* Compensa la latència de la capa Batch processant només les dades recents (els increments d'ençà de l'última execució batch).


* Utilitza algorismes incrementals per actualitzar les **Real-time Views** de manera immediata.




3. **Serving Layer (Capa de servei):**
* Indexa les vistes generades per la capa batch (*Batch Views*) per permetre consultes ràpides.


* En respondre una consulta d'un client, combina la informació de la *Batch View* amb la *Real-time View* per donar una resposta completa i actualitzada.





### Classificació per Temperatura de les Dades

* **Calent (*Hot*):** Accés molt freqüent, emmagatzematge ràpid (RAM, SSD), cost elevat (ex. memòria cau, paginació).


* **Tebi (*Warm*):** Accés poc freqüent, cost mitjà (ex. generació de nòmines, informes mensuals).


* **Fred (*Cold*):** Accés molt poc freqüent, cost d'emmagatzematge molt baix i alta latència de recuperació (ex. *backups*, còpies de seguretat en cinta o Glacier).



---

## 5. Arquitectura Kappa ($\kappa$)

Proposada per Jay Kreps el 2014 per resoldre la principal debilitat de l'arquitectura Lambda: **la duplicació de codi i lògica** en haver de mantenir dos sistemes diferents (Batch i Streaming).

```
                          ┌──────────────────────────┐
                          │   Stream Processing      │
                          │   System (e.g. Spark)    │
                          │ ┌──────────────────────┐ │     ┌────────────┐
Input Topic               │ │  Job Version n       │ ┼───> │ Output     │
(e.g. Kafka Log) ───────> │ └──────────────────────┘ │     │ Table      │ ───> App Query
                          │ ┌──────────────────────┐ │     └────────────┘
                          │ │  Job Version n+1     │ ┼───> (Reprocessed)
                          │ └──────────────────────┘ │
                          └──────────────────────────┘

```

### Els 4 Pilars de l'Arquitectura Kappa

1. **Tot és un Stream:** El processament per lots es considera un cas particular del processament en streaming sobre un marc temporal definit.


2. **Dades Immutables:** Les dades d'origen no es modifiquen mai. S'emmagatzemen com un registre d'esdeveniments (*Log*) ordenat.


3. **Un Únic Flux de Processament:** Es manté un sol codi i una única lògica basant-se en motors de streaming (ex. Apache Kafka + Apache Flink / Spark Streaming).


4. **Capacitat de Reprocessament:** Si la lògica canvia, no es modifiquen les dades d'origen; simplement es torna a llegir el *Log* des de l'inici (*replay*) amb la nova versió de l'algorisme.



---

## 6. Arquitectura Delta i Concepte de Lakehouse

L'arquitectura Delta i el paradigma **Lakehouse** uneixen el millor dels dos mons tradicionals: l'escala i flexibilitat dels **Data Lakes** amb les capacitats de gestió, estructuració i transaccions dels **Data Warehouses**.

$$\text{Data Lake (Fitxers no estructurats/Parquet)} + \text{Capacitats de gestió i ACID (Delta Lake)} = \text{Lakehouse}$$

### La Tecnologia Delta Lake

* Implementa la capacitat de realitzar transaccions **ACID** (Atomicitat, Consistència, Aïllament i Durabilitat) sobre arxius emmagatzemats en formats com Parquet.


* Disposa d'aplicació d'esquemes (*schema enforcement*), evolució d'esquema i viatge en el temps (*time travel* / control de versions de dades).



### El Model de Capes Medalló (Bronze / Silver / Gold)

```
  ┌────────────────┐        ┌────────────────┐        ┌────────────────┐
  │     BRONZE     │ ────>  │     SILVER     │ ────>  │      GOLD      │
  │ (Raw Data)     │        │ (Cleaned/Filter│        │ (Aggregated/   │
  └────────────────┘        └────────────────┘        └────────────────┘

```

1. **Bronze (Dades en cru / Raw):** Ingesta inicial directa des de les fonts originals.


2. **Silver (Dades netes / Filtrades):** Dades transformades, normalitzades, enriquides i validades.


3. **Gold (Nivell de negoci / Business ready):** Agregacions preparades per a analítica avançada, quadres de comandament, BI o Machine Learning.



---

## 7. Arquitectura per Capes (*Layered Architecture*)

Permet estructurar funcionalment el cicle de vida complet de la dada en 6 capes independents:

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌──────────────┐
│  Ingesta    │──>│ Col·lecció  │──>│Processament │──>│Emmagatzemat-│──>│  Consulta   │──>│Visualització │
│             │   │             │   │             │   │ment         │   │             │   │              │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └──────────────┘

```

1. **Capa d'Ingesta:** Captura de la dada des de les fonts orígens (sensors, RDBMS, logs).


2. **Capa de Col·lecció:** Transport i desempaquetament de les dades cap al pipeline.


3. **Capa de Processament:** Neteja, transformació, modelatge i classificació (Batch/Streaming).


4. **Capa d'Emmagatzematge:** Persistència distribuïda eficient (Data Lake, HDFS, S3).


5. **Capa de Consulta:** Execució d'algorismes i processament analític.


6. **Capa de Visualització / Presentació:** Dashboards, interfícies de negoci i eines de BI.



---

## 8. El Principi SCV (Speed, Consistency, Volume)

Analogament al Teorema CAP aplicat a bases de dades NoSQL, el **Principi SCV** s'aplica al processament distribuït de la dada. Estableix que un sistema analític distribuït només pot assegurar, com a màxim, **2 de les 3** propietats següents:

* **Speed (Velocitat):** Rapidesa en l'execució de l'algorisme des que la dada entra al sistema.


* **Consistency (Consistència):** Precisió dels resultats (analitzar el 100% de les dades en comptes de mostres).


* **Volume (Volum):** Capacitat per tractar grans masses de dades.



```
                Speed (S)
                  /   \
                 /     \
                /  SCV  \
               /         \
 Consistency (C) --------- Volume (V)

```

### Escenaris del Principi SCV

1. **Velocitat + Consistència (S + C):** Només és possible si reduïm el **Volum** de dades.


2. **Consistència + Volum (C + V):** Requereix analitzar la totalitat d'un conjunt massiu; el sistema no pot oferir alta **Velocitat** (típic de Batch).


3. **Velocitat + Volum (S + V):** Cal utilitzar tècniques de mostreig (*sampling*) o estimacions, per tant es renuncia a la **Consistència** exacta (típic de Streaming en grans volums).



---

## 9. Ecosistema de Tecnologies i Bones Pràctiques

### Mapatge Tecnològic de Referència

* **Ingesta i Cueing:** Apache Kafka, Apache NiFi.


* **Emmagatzematge Distribuït:** HDFS, Amazon S3, Azure Blob Storage.


* **Motors de Processament:** Apache Spark (Structured Streaming / Batch), Apache Hadoop (MapReduce), Apache Flink, Apache Storm.


* **Serving Layer & NoSQL:** Apache HBase, MongoDB, Redis, AWS DynamoDB, Presto, Apache Drill.


* **Plataforma Unificada:** Databricks / Delta Lake.



---

### Guia de Decisió d'Arquitectures

```
¿Cal combinar dades històriques complexes amb respostes en temps real de diferent lògica?
  ├── SÍ ───> Arquitectura Lambda
  └── NO ───> ¿La lògica per a dades recents i històriques és la mateixa i es disposa d'esdeveniments reordenables?
               ├── SÍ ───> Arquitectura Kappa
               └── NO ───> ¿Es busca reduir salts de dada, integració ACID i unificar en un Data Lake / Lakehouse?
                            └── SÍ ───> Arquitectura Delta / Lakehouse (Medalló)

```

### Bones Pràctiques Generals

* **Avaluació de fonts:** No totes les eines serveixen per a qualsevol tipus de dada.


* **Evitar la sobreenginyeria:** No implementar arquitectures complexes en temps real si el negoci pot funcionar amb execucions Batch periòdiques (*micro-batches*).


* **Centralització de la font de veritat:** Dissenyar per unificar les dades en un repositori unificat i no duplicat.
