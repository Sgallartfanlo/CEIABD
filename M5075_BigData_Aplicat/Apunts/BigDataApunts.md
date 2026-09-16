# Apunts de Mòdul: Arquitectures de Big Data (M5075)

## 1. Principis i Fonaments de Big Data

### El Paradigmàtic Model de les 5V
El concepte de Big Data es defineix mitjançant cinc dimensions fonamentals que condicionen la necessitat de noves arquitectures[cite: 7]:
* **Volum**: La quantitat massiva de dades generades que supera la capacitat d'emmagatzematge i processament dels sistemes tradicionals (relacionals)[cite: 7].
* **Velocitat**: El ritme elevat al qual es creen, ingereixen i s'han de processar les dades en temps real o quasi real[cite: 7].
* **Varietat**: La diversitat de formats de les dades, classificades en estructurades (taules SQL), semiestructurades (JSON, XML) i no estructurades (imatges, àudio, text pla)[cite: 7].
* **Veracitat**: La fiabilitat, qualitat i grau de neteja de la dada; implica gestionar el soroll, dades incompletes o no fiables[cite: 7].
* **Valor**: L'objectiu final de transformar la dada crua en informació útil i accions de negoci rendibles[cite: 7].

---

### Característiques Clau dels Sistemes Distribuïts
El disseny de qualsevol arquitectura Big Data s'ha de basar en quatre pilars tècnics fonamentals[cite: 6, 7]:
* **Escalabilitat**: Capacitat del sistema per absorbir increments de càrrega afegint recursos sense comprometre el rendiment ni requerir redissenys de programari[cite: 6, 7].
* **Tolerància a fallades**: Disseny basat en el principi *"Everything fails, all the time"*[cite: 7]. Si un node falla, el sistema ha de reencaminar la feina automàticament i evitar la pèrdua de dades mitjançant mecanismes com la replicació[cite: 6, 7].
* **Dades i Processament Distribuïts**: Emmagatzematge fragmentat entre moltes màquines per evitar punts únics de fallada (SPOF) i coordinació del treball mitjançant sistemes de gestió de recursos (com YARN o Kubernetes)[cite: 6, 7].
* **Localitat de la dada (*Data Locality*)**: Principi d'execució que mou el codi/computació cap al node on resideix la dada, en comptes de moure la dada per la xarxa cap al processador, minimitzant la latència i el coll d'ampolla de xarxa[cite: 6, 7].

---

### Tipologies d'Escalat

| Concepte | Escalat Vertical (*Scale-Up*) | Escalat Horitzontal (*Scale-Out*) |
| :--- | :--- | :--- |
| **Mecanisme** | Augmentar la capacitat (CPU, RAM, SSD) d'un servidor existent[cite: 6]. | Afegir més servidors/nodes a la xarxa distribuïda[cite: 6]. |
| **Límits** | Límite físic i tecnològic del maquinari d'un sol equip[cite: 6]. | Teòricament il·limitat; permès per sistemes distribuïts[cite: 6]. |
| **Cost** | Creixement exponencial de preu per equip d'alta gamma[cite: 6]. | Lineal i econòmic (utilitza maquinari de consum/estàndard)[cite: 6]. |
| **Resiliència** | Manté un únic punt de fallada (SPOF)[cite: 6, 7]. | Alta disponibilitat i tolerància a fallades nativa[cite: 6, 7]. |

---

## 2. Modelat i Principis d'Enginyeria

### Marcos d'Arquitectura (*Well-Architected Frameworks*)
Els proveïdors de núvol (AWS, Azure, GCP) proposen principis estructurals per dissenyar solucions eficients i sostenibles[cite: 7]:
* **Excel·lència Operacional**: Capacitat per executar i monitorar sistemes, i millorar contínuament els procediments diaris[cite: 7].
* **Seguretat**: Protecció de la informació, els sistemes i els actius mitjançant l'avaluació de riscos i l'aplicació d'estratègies de xifrat i permisos[cite: 7].
* **Fiabilitat**: Capacitat d'un sistema per recuperar-se de fallades de servei o de la xarxa i complir la seva funció correctament[cite: 7].
* **Eficiència del Rendiment**: Ús d'eficaç dels recursos de computació per satisfer els requisits del sistema i mantenir aquesta eficiència a mesura que la demanda canvia[cite: 7].
* **Optimització de Costos**: Eliminació de despeses innecessàries i selecció de tipus de recursos adequats per a la mida requerida[cite: 7].
* **Sostenibilitat**: Minimització de l'impacte ambiental de les càrregues de treball del Big Data (eficiència energètica i optimització de recursos)[cite: 7].

---

### Principi SCV (Speed, Consistency, Volume)
Model teòric utilitzat per avaluar sistemes de processament distribuït que estableix que només és possible garantir 2 de les 3 propietats simultàniament[cite: 7]:


```

```
         [ Speed ]
          /     \
         /       \
        /  SCV    \
       / TRADEOFF  \

```

[ Consistency ]---[ Volume ]

```

* **Speed + Consistency**: Limita el **Volum** de dades que el sistema pot gestionar, ja que sincronitzar múltiples nodes en temps real manté una latència baixa només amb conjunts reduïts de dades[cite: 7].
* **Consistency + Volume**: Sacrifica la **Velocitat** (genera alta latència), ja que assegurar la coherència estricta de grans volums distribuïts requereix coordinacions complexes (ex: transaccions distributed batch)[cite: 7].
* **Speed + Volume**: Sacrifica la **Consistència**, acceptant resultats aproximats o dades temporalment desactualitzades per respondre a alta velocitat sobre volums massius (requereix tècniques de mostreig o arquitectura eventual)[cite: 7].

---

## 3. Estratègies de Processament de Dades


```

+-----------------------------------------------------------------------+
|                         PROCESSAMENT BATCH                            |
| [Dades en repòs] ---> [Processament per lots] ---> [Resultat final]   |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
|                        PROCESSAMENT STREAMING                         |
| [Dades en moviment] -> [Processament continu] ---> [Resultat en viu]  |
+-----------------------------------------------------------------------+

```

### Anàlisi Comparativa de Paradigmes

| Dimensió | Processament Batch (Lots) | Processament Streaming (Flux) |
| :--- | :--- | :--- |
| **Natura de la dada** | Finita, delimitada en blocs (*bounded*)[cite: 6, 7]. | Infinita, continua i sense fi (*unbounded*)[cite: 6, 7]. |
| **Cicle de vida** | Execucions programades (crons) amb inici i fi[cite: 6]. | Execució permanent (24/7/365)[cite: 6, 7]. |
| **Latència de resposta** | Alta latència: des de minuts fins a hores o dies[cite: 6, 7]. | Molt baixa latència: de mil·lilisegons a pocs segons[cite: 6, 7]. |
| **Model d'accés** | Accés complet a tot el conjunt de dades[cite: 6, 7]. | Accés a finestres temporals o esdeveniments individuals[cite: 6, 7]. |
| **Casos d'ús típics** | Entrenament de ML, informació contable, processos ETL nocturns[cite: 6, 7]. | Detecció de frau, alertes mediques, telemetria d'automoció[cite: 6, 7]. |

---

## 4. Arquitectures de Dades

### Arquitectura Lambda
Diseñada per Nathan Marz, resol les consultes combinant dades històriques d'alta precisió amb dades recents en temps real[cite: 6, 7].


```

```
            +---> Batch Layer (Immutable) ---> Serving Layer --+
            |                                                  |

```

[Dada Entrada] -+                                                  +--> [Consulta]
|                                                  |
+---> Speed Layer (Delta recents) -----------------+

```

* **Batch Layer**:
  * Conserva la dada de manera immutable (*Master Dataset*)[cite: 7].
  * Recalcula periòdicament el conjunt complet de dades per generar *Batch Views*[cite: 7].
  * Ofereix màxima precisió però amb alta latència[cite: 7].
* **Speed Layer**:
  * Processa només les dades que no han estat incloses en l'últim càlcul de la Batch Layer[cite: 7].
  * Genera *Real-time Views* per compensar el retard de la Batch Layer[cite: 7].
  * Sacrifica certa precisió a canvi de latència mínima[cite: 7].
* **Serving Layer**:
  * Indexa les *Batch Views* per permetre consultes d'accés ràpid amb SQL/NoSQL[cite: 7].
  * Les consultes d'usuari fusionen la informació de la Serving Layer i la Speed Layer per donar una resposta completa[cite: 7].
* **Principal Inconvenient**: Obliga a mantenir dos codis de programació diferents per a la mateixa lògica de negoci (un per batch i un altre per streaming)[cite: 7].

---

### Arquitectura Kappa
Dissenyada per Jay Kreps per superar la complexitat de mantenir dues capes paral·leles a l'arquitectura Lambda, eliminant la *Batch Layer*[cite: 7].


```

[Dada Entrada] ---> [Log Event Inmutable (Kafka)] ---> [Engine Streaming] ---> [Serving DB]

```

* **Principis Fonamentals**:
  * **Tot és un flux (*stream*)**: Tant les dades en temps real com les històriques es tracten com un flux contínu d'esdeveniments[cite: 7].
  * **Log d'Esdeveniments Immutable**: Les dades originals es mantenen en un sistema de registre ordenat i persistent (com Apache Kafka)[cite: 7].
  * **Un Sol Codi**: Una única plataforma de processament en streaming fa servir la mateixa lògica tant per a dades recents com per a històriques[cite: 7].
  * **Reprocessament**: Si cal canviar la lògica del sistema, es crea un nou job de streaming que torna a llegir el registre d'esdeveniments des de l'inici (*offset 0*)[cite: 7].

---

### Arquitectura Delta / Data Lakehouse
Paradigma modern que combina el millor dels Data Lakes (emmagatzematge econòmic de dades heterogènies) i dels Data Warehouses (estructures i transaccions ACID)[cite: 7].


```

[Dades Raw] ---> [ Capa BRONZE ] ---> [ Capa SILVER ] ---> [ Capa GOLD ] ---> [ Analytics / BI ]
(Crua/Raw)          (Neta/Filtrada)       (Agregada/Negoci)

```

* **Característiques Tècniques**:
  * Suport per a **transaccions ACID** que eviten dades corruptes durant escriptures concurrents[cite: 7].
  * Format d'emmagatzematge obert (com Parquet) combinat amb un registre de transaccions (*Transaction Log*)[cite: 7].
  * Suport per a "Viatge en el temps" (*Time Travel*): capacitat de consultar versions anteriors de les dades[cite: 7].
* **Modelat de capes Medallion**:
  * **Capa Bronze (Raw)**: Ingesta directa de les dades en el seu format original sense cap tipus de modificació[cite: 7].
  * **Capa Silver (Cleansed)**: Dades validades, estructurades, enriquides i netejades; serveix com a font per a exploració avançada i Data Science[cite: 7].
  * **Capa Gold (Business)**: Dades agregades, transformades i optimitzades per a casos d'ús finals, informes BI i quadres de comandament[cite: 7].

---

## 5. Ecosistema Tecnològic i Eines

* **Ingesta i Transport**:
  * **Apache Kafka**: Plataforma de distribució d'esdeveniments d'alt rendiment que actua com a *buffer* de dades en temps real[cite: 7].
  * **Apache NiFi**: Eina visual d'automatització i gestió del flux de dades (ETL/ELT)[cite: 7].
* **Emmagatzematge Distribuït**:
  * **HDFS (Hadoop Distributed File System)**: Sistema de fitxers distribuït dissenyat per a l'emmagatzematge massiu en clusters[cite: 7].
  * **Object Storage Núvol (AWS S3, Azure Blob, GCS)**: Emmagatzematge escalable de cost reduït per a Data Lakes[cite: 7].
* **Motors de Processament**:
  * **Apache Spark**: Motor unificat de processament en memòria molt ràpid que suporta Batch, Streaming (Structured Streaming), SQL, Machine Learning i Grafs[cite: 7].
  * **Hadoop MapReduce**: Motor clàssic de processament Batch basat en escriptura en disc (en desús gradual)[cite: 7].
* **Capa de Serving i NoSQL**:
  * **Apache HBase / Cassandra**: Bases de dades NoSQL orientades a columnes per a lectutació/escriptura de molt baixa latència[cite: 7].
  * **MongoDB**: Base de dades NoSQL orientada a documents JSON/BSON[cite: 7].
  * **Redis**: Emmagatzematge clau-valor en memòria utilitzat com a memòria cau d'alta velocitat[cite: 7].

```
