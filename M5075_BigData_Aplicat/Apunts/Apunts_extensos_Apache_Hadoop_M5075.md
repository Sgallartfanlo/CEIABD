# APUNTS EXTENSOS — APACHE HADOOP

**M5075 — Big Data Aplicat · NF1**  
**Document base:** `M5075_NF1_1_DOC00_Hadoop.pdf` (39 pàgines; Francesc Barragán Pascual, revisió 25/07/2026).  
**Objectiu:** entendre els fonaments i l'arquitectura de Hadoop, aprendre les configuracions principals i executar els casos pràctics del temari.

> **Criteri dels apunts:** els apartats segueixen el temari del PDF. Quan s'aporten aclariments, exemples reformulats, precaucions o bones pràctiques que van més enllà de la guia, s'indiquen com a **Ampliació didàctica** o **Precaució**. Les rutes, versions i noms de servidor dels exemples reflecteixen els escenaris del material i s'han d'adaptar al teu ordinador.

---

## Índex

1. Què és Apache Hadoop?
2. Característiques fonamentals
3. Processament distribuït i localitat de dades
4. Tipus de nodes i maquinari
5. Components del nucli Hadoop
6. Ecosistema Hadoop
7. HDFS: concepte i model d'emmagatzematge
8. Blocs, mida, replicació i càlculs
9. Arquitectura HDFS: NameNode, DataNode i Secondary NameNode
10. Funcionament de les operacions a HDFS
11. MapReduce: introducció i limitacions
12. Map, shuffle/sort i reduce
13. Exemple teòric: recompte de colors
14. YARN: què és i per què es va introduir?
15. Components principals de YARN
16. ResourceManager, Scheduler i ApplicationsManager
17. NodeManager i contenidors
18. ApplicationMaster i execució d'un job
19. Càlcul de recursos del clúster
20. Desplegament: VM, pseudodistribuït, Docker i núvol
21. Fitxers XML de configuració
22. Arrencada i comprovacions
23. Pràctica WordCount: *Tirant lo Blanc*
24. Monitoratge i interpretació de logs
25. Consultes sobre el resultat de WordCount
26. MapReduce amb Python: mapper
27. MapReduce amb Python: reducer
28. Hadoop Streaming
29. Errors habituals i solucions
30. Comparatives essencials per a l'examen
31. Guia ràpida de comandes
32. 60 preguntes d'autoavaluació amb resposta
33. Exercicis de consolidació resolts
34. Glossari
35. Checklist d'estudi

---

## 1. Què és Apache Hadoop?

Apache Hadoop és un projecte de codi obert de la fundació Apache orientat a **emmagatzemar i processar grans volums de dades de manera distribuïda**. No és una única aplicació ni una base de dades convencional: és un conjunt de components i serveis que funcionen coordinadament en un *clúster* de màquines.

El principi central consisteix a distribuir dades i feina entre ordinadors, en comptes de dependre d'un únic servidor cada vegada més potent. D'aquesta manera, Hadoop pot ampliar-se horitzontalment incorporant nodes addicionals.

**Conceptes bàsics:**

- **Big Data:** dades que, pel volum, velocitat o diversitat, exigeixen tècniques especials d'emmagatzematge i processament.
- **Clúster:** conjunt d'ordinadors interconnectats que col·laboren per oferir un servei.
- **Node:** cada màquina que forma part del clúster.
- **Processament distribuït:** dividir el treball i executar-lo en diversos nodes.
- **Emmagatzematge distribuït:** repartir els fitxers entre diversos nodes.
- **Escalabilitat horitzontal:** afegir màquines per incrementar capacitat.

La guia presenta Hadoop com una tecnologia capaç d'operar en entorns molt grans, de milers de nodes i petabytes de dades.

## 2. Característiques fonamentals

| Característica | Explicació | Exemple |
|---|---|---|
| Fiabilitat | Les dades es poden replicar en diversos nodes. | Si una màquina falla, es pot accedir a una altra rèplica. |
| Tolerància a fallades | El sistema detecta fallades i tracta de recuperar-se. | Replanificació de tasques en altres nodes. |
| Escalabilitat | El clúster augmenta recursos quan afegim nous equips. | Afegir DataNodes per guanyar espai. |
| Portabilitat | S'executa sobre sistemes i maquinari diversos. | Entorns Linux locals o al núvol. |
| Distribució | Dades i computació es reparteixen. | Un job MapReduce tracta particions en paral·lel. |

**Diferència important:** fiabilitat i tolerància a fallades estan relacionades, però no són exactament el mateix. La replicació protegeix l'accés a dades davant fallades de disc o nodes; la recuperació de tasques protegeix l'execució.

**Ampliació didàctica:** els avantatges de Hadoop no impliquen que sigui sempre la tecnologia més eficient. Processos petits o interactius poden patir una sobrecàrrega superior a la d'una aplicació tradicional.

## 3. Processament distribuït i localitat de dades

El document destaca la filosofia de **data-local computing**: portar el processament a prop de les dades i reduir la necessitat de transportar-les per xarxa.

```text
Estratègia tradicional
Dades en servidor A ─────── xarxa ───────> servidor B (processa)

Hadoop
Node 1: dades 1 + feina 1
Node 2: dades 2 + feina 2
Node 3: dades 3 + feina 3
                     ↓
              Resultats combinats
```

Si un fitxer està dividit en fragments i cadascun es troba en nodes diferents, diferents processos poden actuar en paral·lel sobre fragments locals. Això redueix transferències i millora el rendiment potencial.

**Ampliació didàctica:** la localitat de dades és un objectiu del planificador, no una garantia absoluta: disponibilitat de recursos, rèpliques i tipus d'operació també influeixen.

## 4. Tipus de nodes i maquinari

La guia distingeix:

- **Master:** executen serveis de coordinació i gestió global, com el NameNode o ResourceManager.
- **Worker:** emmagatzemen blocs i/o executen processos sobre dades.
- **Edge:** són punts d'accés al clúster des de clients, interfícies o serveis externs.

**Commodity hardware** no significa necessàriament ordinadors domèstics: significa maquinari generalista, no especialitzat, que es pot escalar amb un cost relativament moderat.

El material il·lustra configuracions amb molta RAM, diversos processadors i nombrosos discos per node. **No són requisits obligatoris d'una instal·lació d'estudi**: una màquina virtual pseudodistribuïda funciona amb molt menys, tot i que tindrà limitacions.

### JBOD, RAID i HDFS

La guia explica que HDFS pot utilitzar diversos discos configurats com a directoris de dades (`dfs.datanode.data.dir`) i gestionar a nivell lògic la distribució de blocs. Això permet treballar amb discos individuals en lloc de crear necessàriament un RAID per agregació.

- **JBOD:** conjunt de discos utilitzats sense RAID convencional.
- **RAID:** combinació de discos per millorar rendiment i/o redundància segons el nivell.
- **Replicació HDFS:** còpies de blocs en diversos DataNodes.

**Precaució:** replicar tres vegades blocs dins del mateix servidor físic no equival a protegir-se davant la caiguda d'aquell servidor. La tolerància real depèn de la ubicació de les rèpliques.

## 5. Components del nucli Hadoop

| Component | Missió | Pregunta que respon |
|---|---|---|
| Hadoop Common | Biblioteques i utilitats compartides. | Què necessiten la resta de serveis per funcionar? |
| HDFS | Emmagatzematge distribuït. | On són les dades? |
| YARN | Gestió i assignació de recursos. | Amb quins recursos s'executa una aplicació? |
| MapReduce | Model de processament paral·lel per lots. | Com es divideix i agrega el càlcul? |

Cal evitar la confusió **HDFS = dades; YARN = recursos; MapReduce = lògica de processament**.

## 6. Ecosistema Hadoop

Les pàgines 5–7 presenten les tecnologies que poden construir-se sobre Hadoop o interactuar-hi:

| Eina | Paper principal | Exemple de necessitat |
|---|---|---|
| Hive | Consultes de tipus SQL sobre dades massives. | Analitzar vendes emmagatzemades en HDFS. |
| HBase | Base de dades NoSQL escalable. | Consultar registres per clau. |
| Pig | Transformacions amb Pig Latin. | Definir un flux de dades batch. |
| Sqoop | Importació/exportació entre SGBD relacionals i Hadoop. | MariaDB → HDFS. |
| Flume | Ingesta de fluxos i esdeveniments. | Logs de servidors → HDFS. |
| ZooKeeper | Coordinació de serveis distribuïts. | Gestionar estat i coordinació. |
| Spark | Motor de processament distribuït. | Analítica, ML, SQL i streaming. |
| Ambari | Administració i monitoratge. | Gestionar serveis d'un clúster. |

El document també esmenta serveis gestionats com **AWS EMR, Azure HDInsight i Google Dataproc** i distribucions de Cloudera.

**Ampliació didàctica:** Spark no és un substitut d'HDFS com a sistema de fitxers; sovint el complementa. Sqoop i Flume resolen casos d'ingesta diferents: Sqoop està orientat a dades estructurades en bases relacionals i Flume a fluxos d'esdeveniments.

## 7. HDFS: concepte i model d'emmagatzematge

**Hadoop Distributed File System** és un sistema de fitxers distribuït, pensat per emmagatzemar grans fitxers de manera eficient en un clúster. Es fonamenta en dividir-los en blocs, distribuir-los i mantenir-ne rèpliques.

Característiques que remarca la guia:

1. Emmagatzematge escalable horitzontalment.
2. Tolerància a fallades de maquinari.
3. Patró habitual **Write Once, Read Many** (escriure una vegada, llegir moltes).
4. Bona adequació a fitxers grans i lectures seqüencials.
5. Menor adequació a accessos aleatoris de baixa latència, fitxers molt petits i modificacions arbitràries.

### HDFS no és un disc local

L'usuari pot veure rutes com `/user/hadoop/textos`, però són rutes **dins HDFS**, no necessàriament directoris `/user/...` del Linux de la màquina.

```bash
# Sistema local
ls /home/hadoop

# Sistema HDFS
hdfs dfs -ls /user/hadoop
```

**Ampliació didàctica:** el principi WORM descriu l'ús principal, però HDFS permet algunes operacions controlades com `append` en condicions determinades. Això no el converteix en una base de dades que actualitza registres arbitràriament.

## 8. Blocs, mida, replicació i càlculs

El material treballa amb blocs HDFS de **128 MiB** i un factor de replicació habitual de **3**; són valors configurables. Un fitxer es divideix en blocs lògics que es poden emmagatzemar en diferents DataNodes.

**Exemple del PDF:** 600 MB de dades, blocs de 128 MB:

```text
Fitxer 600 MB
  ├── Bloc 1: 128 MB
  ├── Bloc 2: 128 MB
  ├── Bloc 3: 128 MB
  ├── Bloc 4: 128 MB
  └── Bloc 5: resta (88 MB, en el càlcul simplificat del temari)
```

Nombre de blocs (càlcul aproximat del temari):

\[
N = \left\lceil\frac{\text{mida fitxer}}{\text{mida bloc}}\right\rceil
\]

Amb replicació de 3, aquests cinc blocs originen **15 rèpliques de bloc** en total (5 blocs lògics × 3 còpies).

**Matís sobre les unitats:** MB i MiB no són idèntics. A la pràctica, la configuració HDFS s'expressa en bytes i sovint es descriu de manera informal com «128 MB». El resultat de cinc blocs per a 600 MB continua sent correcte amb aquestes magnituds.

**Un fitxer petit no reserva físicament 128 MiB:** si conté un sol MiB, ocupa l'espai efectiu de les seves dades i les metadades corresponents, no 128 MiB complets per còpia.

### Per què els fitxers petits són un problema?

Cada fitxer i bloc comporta metadades al NameNode. Centenars de milers o milions d'arxius diminuts incrementen la pressió sobre les metadades, encara que en dades no ocupin gaire espai.

### Factor de replicació

- **1:** una sola còpia, típic d'una màquina virtual de proves amb un node.
- **2:** dues còpies, millor protecció, més consum.
- **3:** tres còpies, valor habitual en escenaris clàssics.

**Precaució:** en un clúster d'un únic DataNode no és possible allotjar tres còpies en tres DataNodes diferents. Per això els exercicis de classe solen configurar `dfs.replication=1`.

## 9. Arquitectura HDFS: NameNode, DataNode i Secondary NameNode

### NameNode

És el servei mestre que manté les **metadades** del sistema de fitxers: rutes, permisos, estructura de directoris i ubicació lògica dels blocs. No és el repositori habitual del contingut de tots els fitxers.

### DataNode

Emmagatzema físicament els blocs i ofereix operacions de lectura/escriptura de dades. Informa al NameNode sobre la seva disponibilitat i els blocs que conté.

### Secondary NameNode

En el model presentat a la guia participa en els **punts de control (checkpoints)** de metadades. **No és simplement un NameNode secundari que substitueixi automàticament el principal si cau.**

```text
                 +------------------+
Client ─ metadades -> NameNode       |
                 +------------------+
                         |
          ubicació de blocs i control
                         |
          +--------------+--------------+
          |              |              |
     +---------+    +---------+    +---------+
     |DataNode1|    |DataNode2|    |DataNode3|
     +---------+    +---------+    +---------+
          ^              ^              ^
          +--------- Client llegeix/escriu blocs
```

**Ampliació didàctica:** en desplegaments amb alta disponibilitat hi pot haver NameNodes actiu i en espera; és una arquitectura diferent de la funció del Secondary NameNode.

## 10. Funcionament de les operacions a HDFS

### Lectura d'un fitxer

1. El client identifica la ruta HDFS.
2. Demana al NameNode metadades i ubicacions dels blocs.
3. Es connecta als DataNodes que contenen aquests blocs.
4. Rep els fragments i reconstrueix el contingut.

### Escriptura d'un fitxer

1. El client sol·licita crear una ruta.
2. El NameNode comprova i coordina l'operació.
3. Es trien DataNodes de destinació.
4. Les dades s'escriuen en blocs i se'n gestionen rèpliques.
5. Es registra el resultat en les metadades.

**Idea d'examen:** el NameNode coordina i manté metadades; els DataNodes serveixen els blocs de dades.

## 11. MapReduce: introducció i limitacions

MapReduce és el paradigma de processament per lots que presenta la guia. S'ocupa de dividir el problema, processar fragments en paral·lel i agregar resultats mitjançant parelles **clau–valor**.

La seva estructura clàssica té les fases Map i Reduce, amb un pas intermedi de **shuffle i sort**.

L'inconvenient principal és la sobrecàrrega per preparar jobs, transmetre dades i treballar sovint amb fitxers intermedis. És poc adequat per a consultes molt interactives o algoritmes iteratius intensius. La guia assenyala Spark com a alternativa freqüent en aquests casos.

## 12. Map, shuffle/sort i reduce

### Map

Cada mapejador rep una part de les dades i emet parelles `(clau, valor)`. Ex.: `(blau, 1)`.

### Shuffle i sort

El sistema reagrupa els valors amb la mateixa clau i els distribueix als reducers corresponents.

### Reduce

Cada reducer calcula un resultat agregat per clau. Ex.: `(blau, [1,1,1]) → (blau, 3)`.

```text
DOCUMENTS
   |
   v
MAP                 (blau,1) (verd,1) (blau,1)
   |
   v
SHUFFLE / SORT      blau -> [1,1]   verd -> [1]
   |
   v
REDUCE              blau -> 2       verd -> 1
   |
   v
RESULTAT A HDFS
```

**Ampliació didàctica:** un **combiner** opcional pot sumar dades localment abans del shuffle, reduint la quantitat de dades transferides. No tots els càlculs admeten un combiner arbitrari.

## 13. Exemple teòric: recompte de colors

A les pàgines 11–12 el document presenta una fàbrica de joguines que rep comandes amb colors. L'objectiu és saber quantes unitats hi ha de cada color.

Dues línies d'entrada fictícies:

```text
Verd Blau Blau Taronja
Verd Vermell Blau Taronja
```

El mapejador emet vuit parelles amb valor 1; la fase de shuffle agrupa per color i la reducció suma:

| Color | Total |
|---|---:|
| Verd | 2 |
| Blau | 3 |
| Taronja | 2 |
| Vermell | 1 |

**Pregunta típica:** per què no es limita a comptar-ho tot dins d'un únic mapper? Perquè les dades estan repartides i MapReduce reparteix el càlcul entre processos, després consolida els resultats.

## 14. YARN: què és i per què es va introduir?

**Yet Another Resource Negotiator** (YARN) separa la gestió dels recursos del clúster dels mecanismes particulars de processament. Introduït en Hadoop 2, permet que diferents aplicacions i motors comparteixin el clúster.

La funció de YARN és gestionar qui rep recursos, en quin node s'executa i com es monitoritzen les tasques.

**Comparativa:**

| HDFS | YARN |
|---|---|
| Gestiona fitxers i blocs. | Gestiona execucions i recursos. |
| NameNode i DataNode. | ResourceManager, NodeManager i ApplicationMaster. |
| Preocupa la integritat i disponibilitat de dades. | Preocupa la planificació i l'execució. |

## 15. Components principals de YARN

La guia identifica tres components:

- **ResourceManager:** coordinació global dels recursos del clúster.
- **NodeManager:** supervisió dels recursos i contenidors a cada worker.
- **ApplicationMaster:** gestió i seguiment d'una aplicació concreta.

També descriu el **JobHistoryServer**, un servei opcional per consultar informació històrica de jobs MapReduce.

```text
                  ResourceManager
                       |
             assignació / planificació
                       |
       +---------------+---------------+
       |                               |
  NodeManager A                    NodeManager B
   |       |                         |       |
Container  Container             Container Container
               \                   /
                ApplicationMaster
```

## 16. ResourceManager, Scheduler i ApplicationsManager

### ResourceManager

Manté una visió dels nodes i recursos disponibles, i rep peticions d'aplicacions.

### Scheduler

Decideix l'assignació de recursos segons capacitat i polítiques. **No equival a executar tota l'aplicació ni a garantir-ne per si sol la recuperació.**

### ApplicationsManager

Participa en l'admissió d'aplicacions i l'arrencada de l'ApplicationMaster, incloent possibilitats de reinici.

**Idea clau:** el ResourceManager és al processament el que el NameNode és, aproximadament, a l'emmagatzematge: un coordinador central de la seva àrea. No són intercanviables.

## 17. NodeManager i contenidors

El NodeManager s'executa als nodes worker i controla els contenidors que s'hi llancen. Entre les seves funcions hi ha:

1. Informar el ResourceManager dels recursos del node.
2. Gestionar cicles de vida dels contenidors.
3. Monitoritzar el consum de CPU i memòria.
4. Executar i aturar tasques segons el que correspongui.
5. Gestionar registres i comunicar fallades.

### Què és un contenidor YARN?

És una **assignació de recursos per a una execució**: quantitat de memòria i CPU, entre altres restriccions. No s'ha de confondre automàticament amb un contenidor Docker.

Exemple: un contenidor de 4 GiB i 1 vcore pot allotjar una tasca que requereixi aquesta assignació.

## 18. ApplicationMaster i execució d'un job

L'ApplicationMaster coordina les tasques d'una aplicació específica, negocia recursos i controla progrés i estat. La seva vida és temporal, a diferència dels serveis permanents del clúster.

**Seqüència simplificada basada en el document (pàgines 19–20):**

1. El client envia una aplicació a YARN.
2. El ResourceManager accepta la sol·licitud i assigna un primer contenidor.
3. S'engega l'ApplicationMaster de l'aplicació.
4. L'ApplicationMaster demana recursos addicionals.
5. Els NodeManagers posen en marxa els contenidors de tasques.
6. L'ApplicationMaster controla l'execució i comunica el resultat.
7. En acabar, es retornen els recursos i finalitza l'ApplicationMaster.

La guia també menciona **YARN Reservation System** per gestionar reserves de recursos en el temps i **YARN Federation** per coordinar diversos clústers.

## 19. Càlcul de recursos del clúster

Exemple del PDF: 20 nodes amb 256 GB de RAM i 12 cores cadascun.

- RAM total teòrica: `20 × 256 = 5.120 GB` (aproximadament 5 TB segons la nomenclatura emprada).
- CPU: `20 × 12 = 240 cores`.
- Si cada contenidor requereix 32 GB: `5.120 / 32 = 160 contenidors` com a màxim teòric per memòria.

**Ampliació didàctica:** el límit real dependrà també dels vcores per contenidor, recursos reservats pel sistema i configuracions de YARN. No n'hi ha prou de dividir la RAM si la CPU disponible imposa un límit més petit.

## 20. Desplegament: VM, pseudodistribuït, Docker i núvol

El material utilitza principalment una **màquina virtual amb Hadoop instal·lat**. El mode pseudodistribuït significa que NameNode, DataNode, ResourceManager i NodeManager poden executar-se com a processos diferenciats, però al mateix equip físic o virtual.

| Opció | Utilitat | Limitació |
|---|---|---|
| Màquina virtual | Seguir les pràctiques de classe. | Recursos limitats d'un únic host. |
| Mode pseudodistribuït | Aprendre els serveis sense molts servidors. | Sense tolerància real a caiguda del host. |
| Docker Compose | Desplegar diversos serveis en contenidors. | Cal gestionar xarxa, volums i configuracions. |
| Clúster distribuït | Escalabilitat i redundància reals. | Més complexitat operativa. |
| Núvol gestionat | Evitar gran part de l'operació pròpia. | Costos i dependència del proveïdor. |

### Exemple de Docker Compose de la guia

El PDF (pàgines 22–24) fa servir la imatge `apache/hadoop:3.4.1` en quatre serveis: `namenode`, `datanode`, `resourcemanager` i `nodemanager`. El fitxer `config` defineix propietats dels quatre subsistemes.

Exemple sintètic *d'estudi*, no substitut de tota la configuració de la guia:

```yaml
services:
  namenode:
    image: apache/hadoop:3.4.1
    hostname: namenode
    command: ["hdfs", "namenode"]
    ports:
      - "9870:9870"
    env_file: [./config]
    environment:
      ENSURE_NAMENODE_DIR: /tmp/hadoop-root/dfs/name

  datanode:
    image: apache/hadoop:3.4.1
    command: ["hdfs", "datanode"]
    env_file: [./config]

  resourcemanager:
    image: apache/hadoop:3.4.1
    hostname: resourcemanager
    command: ["yarn", "resourcemanager"]
    ports:
      - "8088:8088"
    env_file: [./config]

  nodemanager:
    image: apache/hadoop:3.4.1
    command: ["yarn", "nodemanager"]
    env_file: [./config]
```

Propietats principals de `config` presentades a la guia:

```dotenv
CORE-SITE.XML_fs.defaultFS=hdfs://namenode
HDFS-SITE.XML_dfs.namenode.rpc-address=namenode:8020
HDFS-SITE.XML_dfs.replication=1
MAPRED-SITE.XML_mapreduce.framework.name=yarn
YARN-SITE.XML_yarn.resourcemanager.hostname=resourcemanager
YARN-SITE.XML_yarn.nodemanager.aux-services=mapreduce_shuffle
```

**Ordres del PDF:**

```bash
docker-compose -p iabd-hadoop up -d
docker exec -it iabd-hadoop-namenode-1 /bin/bash
```

**Ampliació didàctica:** amb versions recents del plugin Compose, habitualment s'utilitza `docker compose` (amb espai). Per a dades persistents és recomanable definir volums i no dependre només del sistema de fitxers efímer dels contenidors. Els exemples publicats poden requerir adaptacions segons la imatge i el sistema.

## 21. Fitxers XML de configuració

Els quatre fitxers principals són dins de `$HADOOP_HOME/etc/hadoop`.

### `core-site.xml`

Configura propietats generals; especialment el sistema de fitxers per defecte:

```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://iabd-virtualbox:9000</value>
  </property>
</configuration>
```

### `hdfs-site.xml`

Configura la replicació i els directoris dels serveis HDFS:

```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/home/hadoop/hdfs/namenode</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/home/hadoop/hdfs/datanode</value>
  </property>
</configuration>
```

### `yarn-site.xml`

Assenyala el ResourceManager i els serveis auxiliars dels workers:

```xml
<configuration>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>iabd-virtualbox</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>
</configuration>
```

### `mapred-site.xml`

Indica el framework de processament utilitzat:

```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
```

**No confonguis `fs.defaultFS` (adreça del sistema HDFS) amb `yarn.resourcemanager.hostname` (gestió de recursos).**

**Precaució:** les propietats i les rutes del PDF corresponen a l'entorn d'exemple. No s'han d'enganxar indiscriminadament en una instal·lació diferent.

## 22. Arrencada i comprovacions

### Arrencar HDFS

```bash
start-dfs.sh
```

El material mostra processos com NameNode, DataNode i SecondaryNameNode.

### Arrencar YARN

```bash
start-yarn.sh
```

Ha de posar en marxa ResourceManager i NodeManager.

### Comprovar processos Java

```bash
jps
```

La llista concreta varia segons els serveis iniciats i el sistema. L'absència d'un procés esperat és una pista de diagnòstic.

### Interfícies web habituals

| Servei | Port de la guia | Utilitat |
|---|---:|---|
| NameNode | 9870 | Estat HDFS, DataNodes i explorador. |
| ResourceManager | 8088 | Aplicacions i recursos YARN. |
| JobHistoryServer | 19888 | Informació històrica de jobs MapReduce. |

URLs d'exemple: `http://iabd-virtualbox:9870`, `http://iabd-virtualbox:8088` i `http://192.168.56.104:19888`. Han de resoldre correctament a la teva xarxa.

**Ampliació didàctica:** per apagar ordenadament es poden fer servir `stop-yarn.sh` i `stop-dfs.sh`. Per diagnosticar errors, comprova `jps`, resolució del hostname, SSH, logs i ports.

## 23. Pràctica WordCount: *Tirant lo Blanc*

El cas pràctic de les pàgines 29–33 consisteix a comptar les vegades que apareix cada paraula en el llibre *Tirant lo Blanc*.

### Preparació

1. Disposar del fitxer `tirantloblanc.txt` descarregat segons la referència del PDF.
2. Arrencar Hadoop i YARN.
3. Crear una ruta d'entrada HDFS.
4. Pujar-hi el fitxer.

```bash
hdfs dfs -mkdir -p /user/hadoop/textos
hdfs dfs -put tirantloblanc.txt /user/hadoop/textos/
hdfs dfs -ls /user/hadoop/textos
```

### Executar l'exemple integrat de Hadoop

```bash
hadoop jar "$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.4.3.jar" \
  wordcount \
  /user/hadoop/textos/tirantloblanc.txt \
  /user/hadoop/sortidaWC
```

La guia també utilitza:

```bash
yarn jar "$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.4.3.jar" \
  wordcount \
  /user/hadoop/textos/tirantloblanc.txt \
  /user/hadoop/sortidaWC2
```

Totes dues formes es mostren per a l'exercici. El nom del JAR depèn de la versió instal·lada.

**Precaució:** la ruta de sortida **no ha d'existir prèviament**, o MapReduce fallarà. No executis una eliminació automàtica de rutes si hi pots tenir dades importants.

### Interpretació del resultat

El directori de sortida inclou, habitualment:

- `_SUCCESS`: marcador de finalització correcta del job.
- `part-r-00000`: fitxer amb paraules i comptadors si hi ha un únic reducer.

```bash
hdfs dfs -ls /user/hadoop/sortidaWC2
hdfs dfs -head /user/hadoop/sortidaWC2/part-r-00000
```

**Ampliació didàctica:** un resultat de WordCount és sensible a majúscules, accents i puntuació si no hi afegeixes normalització. `Hola`, `hola` i `hola,` poden ser claus diferents.

## 24. Monitoratge i interpretació de logs

La sortida de WordCount al document (pàgines 30–31) mostra el procés d'enviament i execució:

1. Connexió al ResourceManager.
2. Determinació dels fitxers d'entrada i particions (*splits*).
3. Enviament de l'aplicació a YARN.
4. Progrés `map 0% ... 100%` i `reduce 0% ... 100%`.
5. Missatge `completed successfully`.
6. Comptadors detallats.

### Com interpretar alguns comptadors

| Comptador | Què mesura |
|---|---|
| Map input records | Registres llegits pels mappers. |
| Map output records | Parelles emeses pels mappers. |
| Reduce input groups | Claus agrupades que entren al reducer. |
| Reduce output records | Resultats agregats emesos. |
| HDFS bytes read/written | Volum de dades llegides o escrites a HDFS. |
| Launched map/reduce tasks | Nombre de tasques llançades. |
| Failed Shuffles | Errors de transferència intermediària. |
| CPU time | Temps de CPU consumit pels processos. |

**Exemple real del PDF:** 1 mapper, 1 reducer, 2.186 registres d'entrada del map i 187.018 registres de sortida del map. La reducció agrupa moltes ocurrències repetides.

### JobHistoryServer

```bash
mapred --daemon start historyserver
```

La interfície habitual és al port `19888`.

## 25. Consultes sobre el resultat de WordCount

La guia proposa tres preguntes interessants sobre el resultat.

### 25.1 Rànquing de les 20 paraules més freqüents

```bash
hdfs dfs -cat /user/hadoop/sortidaWC2/part-r-00000 | sort -k2 -n -r | head -20
```

- `hdfs dfs -cat`: envia contingut HDFS a la sortida estàndard.
- `|`: encadena comandes.
- `sort -k2 -n -r`: ordena numèricament per la segona columna, de major a menor.
- `head -20`: mostra els 20 primers resultats.

### 25.2 Quantes paraules apareixen una sola vegada?

```bash
hdfs dfs -cat /user/hadoop/sortidaWC2/part-r-00000 | awk '$2==1' | wc -l
```

`awk '$2==1'` selecciona els registres amb valor 1 i `wc -l` compta línies.

### 25.3 Paraules amb una ocurrència excloent nombres purs

```bash
hdfs dfs -cat /user/hadoop/sortidaWC2/part-r-00000 | awk '$2==1 && $1 !~ /^[0-9]+$/'
```

La regex `/^[0-9]+$/` indica un text format íntegrament per dígits; `!~` el descarta.

## 26. MapReduce amb Python: mapper

El PDF explica com reproduir WordCount amb scripts Python utilitzant Hadoop Streaming.

### `mapper.py` (versió didàctica amb sortida TSV neta)

```python
#!/usr/bin/env python3
import sys

for linia in sys.stdin:
    linia = linia.strip()
    paraules = linia.split()

    for paraula in paraules:
        print(f"{paraula}\t1")
```

**Pas a pas:** `sys.stdin` llegeix línies; `strip()` elimina espais externs; `split()` separa paraules; cada paraula genera una línia `paraula<TAB>1`.

La guia fa servir `print(paraula, "\t1")`, que pot introduir espais addicionals pel separador per defecte de `print()`. La versió anterior produeix exactament un tabulador, útil per a l'exemple de reducer.

### Prova local

```bash
cat tirantloblanc.txt | python3 mapper.py | head
```

**Important:** el mapper no calcula el total global; només emet les ocurrències individuals.

## 27. MapReduce amb Python: reducer

El reducer del PDF acumula valors en un diccionari. És una forma senzilla d'entendre el concepte, però el document adverteix que, amb Big Data, guardar totes les claus a RAM és arriscat.

### Exemple d'acumulació (adaptació didàctica)

```python
#!/usr/bin/env python3
import sys

comptadors = {}
for linia in sys.stdin:
    camps = linia.rstrip("\n").split("\t", 1)
    if len(camps) != 2:
        continue
    paraula, valor = camps
    try:
        n = int(valor)
    except ValueError:
        continue
    comptadors[paraula] = comptadors.get(paraula, 0) + n

for paraula, total in comptadors.items():
    print(f"{paraula}\t{total}")
```

**Limitació:** usa memòria proporcional al nombre de paraules diferents dins d'aquell reducer.

### Exemple més escalable per entrada ordenada

**Ampliació didàctica:** per un reducer que rep les claus agrupades i ordenades, podem acumular només una clau alhora:

```python
#!/usr/bin/env python3
import sys

paraula_actual = None
total = 0

for linia in sys.stdin:
    camps = linia.rstrip("\n").split("\t", 1)
    if len(camps) != 2:
        continue
    paraula, valor = camps
    try:
        n = int(valor)
    except ValueError:
        continue

    if paraula_actual is not None and paraula != paraula_actual:
        print(f"{paraula_actual}\t{total}")
        total = 0

    paraula_actual = paraula
    total += n

if paraula_actual is not None:
    print(f"{paraula_actual}\t{total}")
```

### Comprovació local del pipeline

```bash
cat tirantloblanc.txt | python3 mapper.py | sort -k1,1 | python3 reducer.py > sortida.tsv
head sortida.tsv
```

**Per què `sort`?** La reducció escalable d'una clau cada vegada exigeix rebre les claus consecutives. Hadoop fa el shuffle/sort de manera distribuïda, però en una prova local hem d'afegir el pas explícitament.

## 28. Hadoop Streaming

És el mecanisme que permet utilitzar programes que llegeixen `stdin` i escriuen `stdout` com a mappers i reducers, sense escriure necessàriament el codi en Java.

### Preparar els scripts

```bash
chmod u+x mapper.py
chmod u+x reducer.py
```

El material utilitza el comandament `mapred streaming` i passa els dos scripts locals al job mitjançant `-files`.

```bash
mapred streaming \
  -files mapper.py,reducer.py \
  -input /user/hadoop/textos/tirantloblanc.txt \
  -output /user/hadoop/sortidaPy \
  -mapper mapper.py \
  -reducer reducer.py
```

**Ampliació didàctica:** segons la configuració del shell i de Hadoop, també pots declarar el mapper i reducer com `python3 mapper.py` i `python3 reducer.py` per evitar errors de shebang/permisos.

### Comprovar el resultat

```bash
hdfs dfs -ls /user/hadoop/sortidaPy
hdfs dfs -head /user/hadoop/sortidaPy/part-00000
```

La guia esmenta aquest nom de fitxer. Segons versió i configuració, el resultat pot tenir un nom com `part-00000` o `part-00000`/`part-r-00000`; primer comprova els noms reals amb `hdfs dfs -ls`.

### `resource-types.xml`

A la pàgina 38 es descriu la possible necessitat de crear `resource-types.xml` amb entrades per GPU i FPGA si el sistema reporta problemes. **Precaució:** l'avís «resource-types.xml not found» no sempre és un error crític. No creïs el fitxer ni hi declaris recursos nous sense comprovar que realment és la causa del problema.

## 29. Errors habituals i solucions

| Símptoma | Causes probables | Diagnòstic recomanat |
|---|---|---|
| `Connection refused` a HDFS | NameNode apagat, hostname incorrecte, port. | `jps`, `core-site.xml`, xarxa. |
| NameNode no accessible per web | Servei aturat, DNS o firewall. | Comprovar `9870` i IP real. |
| No hi ha DataNodes | DataNode no arrenca o registra. | `jps` i logs HDFS. |
| YARN no accepta jobs | ResourceManager/NodeManager inactius. | `start-yarn.sh`, `jps`, interfície `8088`. |
| `Output directory already exists` | Ruta de sortida de job ja existent. | Canviar la ruta o revisar abans d'eliminar-la. |
| `Permission denied` | Permisos HDFS, SSH o scripts. | `hdfs dfs -ls`, permisos i usuari actiu. |
| `ClassNotFound` o JAR absent | Versió/ruta del JAR inadequada. | `ls $HADOOP_HOME/share/hadoop/mapreduce/`. |
| No s'executa `mapper.py` | Falten permisos, shebang o `-files`. | Prova local i `chmod u+x`. |
| Nombre de paraules incorrecte | Sortida no normalitzada; reducer no rep claus consecutives. | Verificar TSV i ordenar a la prova local. |
| Logs amb warnings | No necessàriament indiquen fallada. | Buscar la primera excepció real i estat final del job. |

### Advertiment molt important: formatatge HDFS

**No executis `hdfs namenode -format` com a solució rutinària.** Inicialitza les metadades d'un sistema de fitxers i pot fer inaccessible l'emmagatzematge existent. El PDF de teoria no el planteja com una ordre d'arrencada habitual.

## 30. Comparatives essencials per a l'examen

### HDFS vs base de dades tradicional

| HDFS | Base de dades clàssica |
|---|---|
| Fitxers grans distribuïts. | Registres i consultes estructurades. |
| Molt adequat a lots i lectures seqüencials. | Sovint molt adequat a transaccions i accés puntual. |
| Replicació de blocs. | Diferents mecanismes de persistència, índexs i còpies. |
| No ofereix per si mateix SQL. | Moltes ofereixen SQL. |

### MapReduce vs Spark

| MapReduce | Spark |
|---|---|
| Processament distribuït clàssic per lots. | Motor general de processament distribuït. |
| Pot tenir molta sobrecàrrega d'I/O entre etapes. | Pot aprofitar memòria i optimitzacions per pipelines. |
| Molt útil per entendre la programació distribuïda. | Habitual en SQL, ML i analítica complexa. |

### Mapper vs reducer

| Mapper | Reducer |
|---|---|
| Transforma dades d'entrada. | Consolida valors per clau. |
| Genera parelles clau–valor. | Rep grups de valors amb la mateixa clau. |
| Pot treballar en paral·lel amb molts fragments. | Calcula l'agregació final assignada. |

### NameNode vs ResourceManager

| NameNode | ResourceManager |
|---|---|
| Coordina metadades HDFS. | Coordina recursos YARN. |
| Sap on són els blocs. | Sap quins recursos de computació són disponibles. |
| Treballa amb DataNodes. | Treballa amb NodeManagers i ApplicationMasters. |

## 31. Guia ràpida de comandes

```bash
# Processos
jps

# Iniciar serveis
start-dfs.sh
start-yarn.sh
mapred --daemon start historyserver

# Aturar serveis
stop-yarn.sh
stop-dfs.sh

# HDFS
hdfs dfs -mkdir -p /user/hadoop/textos
hdfs dfs -put tirantloblanc.txt /user/hadoop/textos/
hdfs dfs -ls /user/hadoop/textos
hdfs dfs -cat /user/hadoop/sortidaWC/part-r-00000
hdfs dfs -head /user/hadoop/sortidaWC/part-r-00000

# Consultar Hadoop i els JARs d'exemple
hadoop version
ls "$HADOOP_HOME/share/hadoop/mapreduce/"

# Scripts Python
chmod u+x mapper.py reducer.py
cat tirantloblanc.txt | python3 mapper.py | sort -k1,1 | python3 reducer.py

# Monitoratge (interfícies web)
# HDFS: http://servidor:9870
# YARN: http://servidor:8088
# JobHistoryServer: http://servidor:19888
```

---

## 32. 60 preguntes d'autoavaluació amb resposta

### Fonaments

1. **Què és Hadoop?** Un ecosistema de components de codi obert per emmagatzemar i processar dades distribuïdes.
2. **Què és un clúster?** Un conjunt de màquines que col·laboren.
3. **Què és escalar horitzontalment?** Afegir nodes en lloc de dependre només d'una màquina més potent.
4. **Per què Hadoop tolera fallades?** Per replicació de dades i mecanismes de recuperació/replanificació.
5. **Què és localitat de dades?** Executar treball preferentment a prop de les dades.
6. **Quins tipus de nodes descriu la guia?** Master, worker i edge.
7. **Què és commodity hardware?** Maquinari generalista no necessàriament especialitzat.
8. **Quins són els quatre elements del nucli?** Common, HDFS, YARN i MapReduce.
9. **Per a què serveix Hive?** Per consultar dades amb un llenguatge semblant a SQL.
10. **Quina diferència hi ha entre Flume i Sqoop?** Flume ingereix fluxos; Sqoop transfereix dades estructurades de/vers SGBD relacionals.

### HDFS

11. **Què vol dir HDFS?** Hadoop Distributed File System.
12. **Quina és la mida de bloc habitual del temari?** 128 MiB aproximadament.
13. **Què és una rèplica?** Una còpia d'un bloc de dades.
14. **Quin factor de replicació clàssic es presenta?** 3.
15. **Per què en un sol node es configura 1?** Perquè no hi ha tres DataNodes diferents on ubicar rèpliques.
16. **Un fitxer de 1 MiB consumeix físicament 128 MiB per bloc?** No, ocupa bàsicament les dades efectives i metadades.
17. **Quants blocs de 128 MiB necessita aproximadament un fitxer de 600 MB?** 5.
18. **Amb tres còpies de cinc blocs, quantes còpies de bloc totals hi ha?** 15.
19. **Què gestiona el NameNode?** Metadades i ubicació de blocs.
20. **Què guarda un DataNode?** Els blocs de dades.
21. **El Secondary NameNode és un failover automàtic?** No, s'encarrega principalment de checkpoints.
22. **Què significa WORM?** Write Once, Read Many.
23. **Per què HDFS no és ideal per a fitxers molt petits?** Sobrecàrrega de metadades i gestió.
24. **HDFS és el mateix que `/home` local?** No, és un sistema de fitxers diferent.
25. **Quina ordre llista un directori HDFS?** `hdfs dfs -ls <ruta>`.

### MapReduce

26. **Quines són les fases principals de MapReduce?** Map, shuffle/sort i reduce.
27. **Què emet el mapper?** Parelles clau–valor.
28. **Què fa shuffle?** Reagrupa i distribueix els valors per clau.
29. **Què fa sort?** Ordena les claus per facilitar-ne el processament agrupat.
30. **Què fa el reducer?** Agrega els valors de cada clau.
31. **Què emet WordCount per la paraula «gat» al mapper?** `gat\t1` per cada ocurrència.
32. **Si «gat» apareix quatre vegades, què produeix el reducer?** `gat\t4`.
33. **Quin inconvenient té MapReduce per a processos iteratius?** La sobrecàrrega de fases i persistència/intercanvi de dades.
34. **Quin motor alternatiu destaca la guia?** Spark.
35. **Què és un job?** Una feina enviada al sistema de processament.

### YARN

36. **Què significa YARN?** Yet Another Resource Negotiator.
37. **Què administra YARN?** Recursos i execució de les aplicacions del clúster.
38. **Quins tres components destaca la guia?** ResourceManager, NodeManager i ApplicationMaster.
39. **Què fa ResourceManager?** Coordina l'assignació global de recursos.
40. **Què fa Scheduler?** Planifica recursos segons les polítiques.
41. **Què fa NodeManager?** Gestiona i monitoritza contenidors locals.
42. **Què és un contenidor YARN?** Una assignació de recursos a una execució.
43. **Què fa ApplicationMaster?** Coordina les tasques d'una aplicació i negocia recursos.
44. **Hi ha un ApplicationMaster fix per tot el clúster?** No, típicament un per aplicació.
45. **Què fa JobHistoryServer?** Conserva informació de jobs MapReduce finalitzats.
46. **Amb 20 nodes de 12 cores, quants cores teòrics hi ha?** 240.
47. **Amb 5.120 GB i 32 GB per contenidor, quin límit teòric de RAM resulta?** 160 contenidors.
48. **Per què aquest nombre pot no ser real?** CPU, reserves i polítiques poden limitar la simultaneïtat.

### Configuració i pràctiques

49. **Què configura `core-site.xml`?** Propietats generals, com `fs.defaultFS`.
50. **Què configura `hdfs-site.xml`?** Replicació i directoris de metadades/blocs, entre altres opcions.
51. **Què configura `yarn-site.xml`?** Paràmetres dels serveis YARN.
52. **Què configura `mapred-site.xml`?** El framework de MapReduce, com `yarn`.
53. **Quina comanda inicia HDFS?** `start-dfs.sh`.
54. **Quina comanda inicia YARN?** `start-yarn.sh`.
55. **Per a què serveix `jps`?** Per veure processos Java de la sessió/host.
56. **Quin port utilitza la interfície del NameNode?** Habitualment 9870.
57. **Quin port utilitza la interfície del ResourceManager?** Habitualment 8088.
58. **Què significa `_SUCCESS`?** Que el job ha acabat correctament.
59. **Per a què serveix `-files` a Hadoop Streaming?** Per distribuir els scripts o fitxers locals necessaris als contenidors del job.
60. **Per què no s'ha de fer `namenode -format` cada dia?** Perquè reinicialitza metadades i pot perdre's l'accés al sistema de fitxers existent.

---

## 33. Exercicis de consolidació resolts

### Exercici A — Identificar responsabilitats

Assigna cada acció al component:

- Emmagatzemar físicament un bloc → **DataNode**.
- Saber quins blocs té un fitxer → **NameNode**.
- Assignar recursos globals a un job → **ResourceManager**.
- Supervisar un contenidor → **NodeManager**.
- Coordinar les tasques d'una aplicació → **ApplicationMaster**.

### Exercici B — Calcular blocs

Tenim un fitxer de 300 MiB, mida de bloc 128 MiB, replicació 3.

- Blocs lògics = `ceil(300/128) = 3`.
- Rèpliques de bloc totals = `3 × 3 = 9`.
- Espai nominal de dades replicades ≈ `300 × 3 = 900 MiB`, més metadades i sobrecàrregues.

### Exercici C — Entendre WordCount

Entrada:

```text
sol lluna sol
lluna mar sol
```

Sortida lògica després de reduir:

```text
lluna  2
mar    1
sol    3
```

### Exercici D — Detectar un error de ruta

`hadoop jar ... wordcount /entrada /sortida` falla perquè `/sortida` ja existeix.

**Solució segura:** inspecciona `hdfs dfs -ls /sortida`, desa'n les dades si cal i usa una ruta nova com `/sortida-v2`. Evita esborrar dades sense comprovar-ne el contingut.

### Exercici E — Prova local del mapper/reducer

Si el reducer suma un únic grup cada vegada, la prova adequada és:

```bash
cat dades.txt | python3 mapper.py | sort -k1,1 | python3 reducer.py
```

**Raó:** l'ordre de les claus és necessari perquè el reducer pugui finalitzar cada grup quan detecta una clau nova.

---

## 34. Glossari

| Terme | Definició breu |
|---|---|
| Hadoop | Ecosistema de computació distribuïda. |
| HDFS | Sistema distribuït de fitxers. |
| YARN | Gestor de recursos i execucions. |
| MapReduce | Model de processament paral·lel per claus i valors. |
| Clúster | Conjunt de màquines coordinades. |
| Node | Màquina del clúster. |
| Master | Node amb serveis de coordinació. |
| Worker | Node que guarda dades i/o executa tasques. |
| Edge | Punt d'accés extern al clúster. |
| NameNode | Gestor de metadades HDFS. |
| DataNode | Gestor local de blocs HDFS. |
| Secondary NameNode | Component de checkpoints de metadades. |
| Bloc | Fragment lògic d'un fitxer HDFS. |
| Replicació | Creació de diverses còpies de blocs. |
| ResourceManager | Gestor global de recursos YARN. |
| NodeManager | Gestor de contenidors i recursos locals. |
| ApplicationMaster | Coordinador d'una aplicació YARN. |
| Scheduler | Planificador de recursos. |
| Container | Assignació de recursos d'execució. |
| Job | Treball enviat al sistema. |
| Mapper | Transformació inicial en parelles clau–valor. |
| Shuffle | Redistribució i agrupació per claus. |
| Reducer | Agregació dels valors d'una clau. |
| Hadoop Streaming | Interfície per executar scripts via stdin/stdout. |
| `stdin` | Entrada estàndard d'un programa. |
| `stdout` | Sortida estàndard d'un programa. |
| Pseudodistribuït | Diversos serveis Hadoop en una sola màquina. |
| Data locality | Processament proper a les dades. |
| WORM | Escriure una vegada i llegir moltes. |
| `jps` | Eina per enumerar processos Java. |
| `_SUCCESS` | Indicador de finalització correcta d'un job. |

## 35. Checklist d'estudi

- [ ] Puc explicar Hadoop amb paraules pròpies.
- [ ] Diferencio Hadoop Common, HDFS, MapReduce i YARN.
- [ ] Entenc què significa processar a prop de les dades.
- [ ] Sé descriure master, worker i edge.
- [ ] Sé explicar blocs, mida i rèpliques amb exemples numèrics.
- [ ] Diferencio NameNode, DataNode i Secondary NameNode.
- [ ] Sé quan HDFS no és la tecnologia més adequada.
- [ ] Puc dibuixar el recorregut Map → Shuffle/Sort → Reduce.
- [ ] Puc interpretar un WordCount senzill.
- [ ] Diferencio ResourceManager, NodeManager i ApplicationMaster.
- [ ] Sé què és un contenidor YARN i què limita la concurrència.
- [ ] Conec els quatre XML i la seva responsabilitat.
- [ ] Sé iniciar HDFS i YARN i consultar `jps`.
- [ ] Conec els ports 9870, 8088 i 19888.
- [ ] Sé pujar un fitxer a HDFS i executar WordCount.
- [ ] Entenc `part-r-00000`, `_SUCCESS` i els comptadors del job.
- [ ] Entenc `mapper.py`, `reducer.py`, `stdin`, `stdout` i el pipeline Unix.
- [ ] Sé explicar com `-files` permet treballar amb Hadoop Streaming.
- [ ] Reconec els errors més habituals i evito ordres destructives.
- [ ] He practicat les 60 preguntes i els exercicis de consolidació.

---

## Fonts i abast

**Font principal:** Francesc Barragán Pascual, *Hadoop*, M5075 Big Data Aplicat, revisió 25/07/2026, 39 pàgines. La seva organització original inclou: Hadoop i processament distribuït (p. 3–4), components i ecosistema (p. 5–7), HDFS (p. 8–10), MapReduce (p. 11–13), YARN (p. 14–20), instal·lació i configuració (p. 21–26), posada en marxa (p. 27–28), WordCount (p. 29–33) i Hadoop Streaming amb Python (p. 34–38).

**Ampliacions didàctiques incloses:** explicacions conceptuals addicionals, comparatives, proves locals ordenades, advertiments sobre pèrdua de dades i errors de configuració, alternatives de codi Python, exercicis, glossari i preguntes. No s'han d'interpretar com a text literal de la guia.

**Nota sobre versions:** la teoria del document es va revisar el juliol de 2026 i fa referència a diverses versions de Hadoop (com 3.4.1 i 3.4.3). Els exemples s'han conservat en el seu context; comprova sempre la versió local abans d'utilitzar una ruta de JAR o una configuració en una màquina diferent.
