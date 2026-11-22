# APUNTS EXTENSOS — ECOSISTEMA HADOOP

## 1. Objectius d'aprenentatge [AMPLIACIÓ]

En acabar aquests apunts hauries de ser capaç de:

- Identificar **les quatre categories** de components que utilitza el document.
- Enumerar **totes les tecnologies** de cada grup i explicar-ne la funció principal.
- Diferenciar una eina d'ingesta d'una de processament o d'una interfície d'administració.
- Entendre quan interessa un sistema de consultes SQL, un magatzem NoSQL o un motor de càlcul.
- Distingir **processament batch** de **processament en streaming**.
- Dissenyar conceptualment un pipeline que recull, emmagatzema, processa i consulta dades.
- Detectar confusions típiques: Kafka no és Hive; HBase no és HDFS; Hue no processa les dades per si mateix.

## 2. Visió general de l'ecosistema Hadoop [AMPLIACIÓ]

**Hadoop** no és una aplicació única que resolgui totes les necessitats de Big Data. És un conjunt de tecnologies i un ecosistema al voltant de l'emmagatzematge distribuït, la gestió de recursos i el processament de grans volums de dades. Diferents productes cobreixen problemes diferents.

Conceptualment, podem separar quatre funcions:

1. **Entrada i moviment de dades:** arribar des de sistemes externs, com una base de dades, aplicacions o registres de servidor.
2. **Persistència i accés:** emmagatzemar dades i facilitar-ne la lectura per lots o per registres.
3. **Càlcul i analítica:** filtrar, transformar, agrupar, enriquir i consultar informació.
4. **Operació i ús:** consultar el sistema mitjançant interfícies i administrar-ne els serveis.

En una arquitectura clàssica de Hadoop, **HDFS** és el sistema de fitxers distribuït, **YARN** gestiona recursos i **MapReduce** és un model de processament distribuït. Aquests tres noms donen context a les eines de la guia, però **la pàgina del PDF no els presenta com a llista de les quatre categories**.

### Exemple conceptual

```text
Base de dades relacional ── Sqoop ─────────┐
                                          │
Logs de servidors ──────── Flume ──────────┼──> HDFS / emmagatzematge
                                          │              │
Esdeveniments ──────────── Kafka ──────────┘              ▼
                                                   Hive / Spark
                                                        │
                                               Consultes / resultats
                                                        │
                                                   Hue / Zeppelin
```

> Aquest esquema és una **síntesi didàctica**, no un diagrama literal del document. Les eines no necessàriament es connecten així en tots els desplegaments.

## 3. Les quatre famílies de components [GUIA]

La guia classifica les eines de l'ecosistema Hadoop en quatre grups:

| Grup de la guia | Finalitat segons el PDF | Eines enumerades |
|---|---|---|
| Accés i processament de dades | Accedir, emmagatzemar o processar dades amb mecanismes alternatius o complementaris a HDFS | Pig, Hive, Impala, HBase, Phoenix, Spark |
| Ingesta i fluxos de treball | Intercanviar dades amb sistemes externs i automatitzar processos | Sqoop, Flume, Oozie |
| Interfícies i eines de treball | Facilitar l'accés, l'ús i l'administració mitjançant interfícies visuals | Hue, Zeppelin, Ambari, Cloudera Manager |
| Processament en streaming | Analitzar o processar dades a mesura que es produeixen | Kafka, Spark, Flink, Storm |

**Punt important:** **Apache Spark apareix en dos grups de la guia**, perquè pot servir per al processament general i per al streaming. Això no és un error: una mateixa eina pot tenir diferents capacitats.

### Com memoritzar els grups [AMPLIACIÓ]

- **Accedir/processar:** «On i com consulto o transformo les dades?»
- **Ingestar/orquestrar:** «Com entren les dades, com surten i quan executo cada feina?»
- **Treballar/administar:** «Com interactuo visualment amb el sistema?»
- **Streaming:** «Com processo el flux mentre arriben esdeveniments?»

---

# PART I · ACCÉS I PROCESSAMENT DE DADES

## 4. Què significa aquesta categoria? [GUIA + AMPLIACIÓ]

**[GUIA]** Aquests components ofereixen maneres d'emmagatzemar dades, d'accedir-hi de forma diferent d'HDFS —inclòs l'accés aleatori a dades concretes— o de processar fitxers mitjançant llenguatges de consulta i treballs programats. El PDF enumera **Pig, Hive, Impala, HBase, Phoenix i Spark**.

**[AMPLIACIÓ]** No tots fan el mateix:

- **Pig** descriu transformacions de dades en forma de fluxos.
- **Hive** presenta una capa SQL sobre conjunts de dades.
- **Impala** està orientat a consultes analítiques SQL interactives.
- **HBase** permet accés per clau a registres distribuïts.
- **Phoenix** aporta una capa SQL sobre HBase.
- **Spark** és un motor general de processament distribuït.

Aquesta distinció és essencial: el fet que diverses eines «processin dades» no implica que siguin substituts directes.

## 5. Apache Pig [GUIA: nom · AMPLIACIÓ: descripció]

### Què és?

**Apache Pig** és una eina de tractament de dades que permet expressar cadenes de transformacions amb un llenguatge anomenat **Pig Latin**. És especialment fàcil d'entendre com una successió de passos: carregar → filtrar → agrupar → projectar → guardar.

### Per què existeix?

Programar directament tasques MapReduce és laboriós. Pig abstrau una part d'aquesta complexitat: descrius què cal fer amb els registres i el sistema transforma la lògica en un pla de treball executable.

### Exemple il·lustratiu de Pig Latin

```pig
professors = LOAD '/dades/professors.csv'
    USING PigStorage(',')
    AS (id:int, nom:chararray, edat:int, materia:chararray);

adults = FILTER professors BY edat >= 30;
resultat = FOREACH adults GENERATE nom, materia;
DUMP resultat;
```

**Lectura:** carrega un fitxer CSV, filtra els professors que tenen almenys 30 anys i mostra nom i matèria. Les rutes i dades són d'exemple.

### Punts clau

- És més proper a un **script de transformació** que a una consulta SQL convencional.
- Resulta adequat per descriure fluxos ETL històrics sobre Hadoop.
- No és un motor per gestionar transaccions interactives per registre.
- La seva presència al temari té valor conceptual i històric; per a projectes nous cal valorar eines actualment mantingudes.

**Pregunta típica:** en què es diferencia Pig de Hive? **Pig utilitza Pig Latin per definir fluxos de transformació; Hive utilitza un llenguatge semblant a SQL.**

## 6. Apache Hive [GUIA: nom · AMPLIACIÓ: descripció]

### Què és?

**Apache Hive** és una capa d'analítica i gestió de dades que permet definir taules i executar consultes mitjançant **HiveQL/HiveSQL**, similar a SQL. És útil per construir processos de tipus data warehouse sobre emmagatzematge distribuït.

### Elements que convé conèixer

- **Taula:** estructura lògica de columnes i tipus de dades.
- **Metastore:** catàleg amb noms de taules, esquemes, particions, ubicacions i altres metadades.
- **HiveServer2:** servei de connexió per clients com Beeline.
- **Beeline:** client de línia d'ordres.
- **Taula interna/gestionada:** Hive gestiona el cicle de vida de les seves dades segons la configuració.
- **Taula externa:** Hive referencia dades que es mantenen separadament del cicle de vida de la taula.

### Exemples de HiveQL

```sql
CREATE DATABASE IF NOT EXISTS iabd;
USE iabd;

CREATE EXTERNAL TABLE IF NOT EXISTS professors (
    id INT,
    nom STRING,
    edat INT,
    materia STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/dades/professors/';

SELECT materia, COUNT(*) AS total
FROM professors
GROUP BY materia
ORDER BY total DESC;
```

L'exemple **pressuposa** que a HDFS existeix la ruta i que els fitxers tenen exactament l'estructura indicada.

### Quan l'utilitzaries?

- Consultes analítiques sobre volums elevats.
- ETL SQL i taules de dades històriques.
- Consulta de datasets compartits en un data lake.

**No és el mateix que una base de dades OLTP:** Hive no està pensat principalment per respondre milers de petites transaccions de negoci per segon.

## 7. Apache Impala [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Impala** és un motor SQL de processament analític distribuït amb orientació a **baixa latència en consultes interactives**. El seu objectiu és permetre explorar dades amb SQL sense haver de pensar en feines MapReduce tradicionals per a cada consulta.

### Idea principal

Davant un analista que executa successivament filtres i agregacions, l'experiència amb un motor interactiu com Impala pot resultar més àgil que amb sistemes històricament orientats al batch.

### Exemple de consulta

```sql
SELECT materia, AVG(edat) AS edat_mitjana
FROM professors
GROUP BY materia;
```

La **sintaxi** és molt semblant a SQL; els motors subjacents i el comportament de rendiment són diferents.

### Hive versus Impala

| Aspecte | Hive | Impala |
|---|---|---|
| Enfocament | Processament i analítica SQL distribuïda | SQL analític interactiu |
| Cas habitual | ETL, anàlisi de grans datasets | Exploració i consultes de baixa latència |
| Metadades | Disposa de metastore | Sovint es pot integrar amb metadades compartides |
| És una BD relacional clàssica? | No | No |

**Matís:** la velocitat real depèn dels fitxers, les particions, la memòria, la configuració i la consulta. No es pot assegurar que un motor sempre sigui més ràpid que un altre.

## 8. Apache HBase [GUIA: nom · AMPLIACIÓ: descripció]

### Definició

**Apache HBase** és una base de dades distribuïda **NoSQL de família de columnes**. Està orientada a guardar grans col·leccions de registres i recuperar o actualitzar registres concrets mitjançant una **row key**.

### Conceptes essencials

- **Row key:** identificador que permet localitzar una fila.
- **Column family:** agrupació de columnes definida en l'estructura.
- **Column qualifier:** identificador d'una columna concreta dins d'una família.
- **Cèl·lula i versions:** una columna pot conservar diferents versions associades a timestamps, segons la configuració.

### Exemple conceptual

```text
Taula: sensors
Row key: sensor-007
  info:ubicacio   = "laboratori"
  lectura:temperatura = "22.4"
```

### Per què no és HDFS?

HDFS està orientat a l'emmagatzematge distribuït de fitxers i lectures/escriptures adequades al seu model. HBase ofereix una abstracció de **taules amb accés per clau**. Pot utilitzar HDFS com a capa d'emmagatzematge, però la manera d'accedir-hi és diferent.

### Quan és útil?

- Historials d'esdeveniments indexats per identificador.
- Dades de dispositius consultades per una clau.
- Aplicacions que requereixen lectura i escriptura de registres concrets a gran escala.

**Dificultat important:** una mala elecció de `row key` pot concentrar moltes operacions a la mateixa regió i generar colls d'ampolla.

## 9. Apache Phoenix [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Phoenix** és una capa d'accés SQL sobre **HBase**. Permet que un usuari o una aplicació que coneix SQL interactuï amb dades emmagatzemades en HBase sense treballar sempre amb l'API nativa.

### Relació entre HBase i Phoenix

```text
Aplicació / client SQL
        │
      Phoenix
        │
      HBase
        │
   Emmagatzematge
```

No vol dir que Phoenix substitueixi HBase: **Phoenix usa HBase com a sistema subjacent**.

### Exemple orientatiu

```sql
CREATE TABLE IF NOT EXISTS sensors (
    id VARCHAR PRIMARY KEY,
    ubicacio VARCHAR,
    temperatura DOUBLE
);

SELECT id, temperatura
FROM sensors
WHERE id = 'sensor-007';
```

Aquesta és una **mostra de la idea de consultar per SQL**; les opcions de tipus, claus, connexió i compatibilitat s'han de validar al desplegament concret.

### Pregunta d'examen

**«Si ja tinc HBase, per què voldria Phoenix?»** Per disposar d'un model d'accés SQL i facilitar consultes i integracions que altrament necessitarien programació amb APIs natives.

## 10. Apache Spark [GUIA: accés/processament i streaming · AMPLIACIÓ: descripció]

**Apache Spark** és un motor distribuït de processament de dades. Pot executar transformacions a gran escala, operacions SQL i fluxos amb **Structured Streaming**.

### Components conceptuals

- **Spark Core:** infraestructura del motor de càlcul distribuït.
- **DataFrame:** abstracció tabular distribuïda amb esquema.
- **Spark SQL:** API de consulta i transformació de dades estructurades.
- **Structured Streaming:** API de processament incremental de fluxos.
- **MLlib:** biblioteca d'aprenentatge automàtic.

### Exemple senzill amb PySpark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ExempleProfessorat").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(
    "/dades/professors.csv"
)

resultat = df.filter(col("edat") >= 30).groupBy("materia").count()
resultat.show()

spark.stop()
```

És un exemple didàctic. La ruta, els permisos i la configuració de Spark s'han d'adaptar.

### Per què apareix en dues categories de la guia?

- En **processament**, perquè pot tractar grans datasets per lots.
- En **streaming**, perquè també pot consumir fluxos contínuament amb les seves APIs.

**No confonguis Spark amb Spark SQL:** Spark és el motor més ampli; Spark SQL és una de les seves capacitats.

---

# PART II · INGESTA I FLUXOS DE TREBALL

## 11. Definició de la categoria [GUIA]

La guia agrupa aquí les eines destinades a **intercanviar dades amb l'exterior** i a **automatitzar processos i fluxos de treball**. Inclou **Sqoop, Flume i Oozie**.

[AMPLIACIÓ] Hi ha dues preguntes diferents:

- **Moviment:** com es traslladen les dades del punt A al punt B?
- **Orquestració:** en quin ordre s'han d'executar diversos processos, amb quines dependències i quan?

Sqoop i Flume resolen sobretot necessitats de moviment; Oozie s'enfoca a l'orquestració.

## 12. Apache Sqoop [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Sqoop** és una tecnologia històrica per intercanviar dades **entre bases de dades relacionals i Hadoop**. El seu model típic és una importació o exportació per lots.

### Escenari d'importació

```text
MariaDB / MySQL ──(JDBC)──> Sqoop ──> HDFS
```

### Exemple didàctic

```bash
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username iabd -P \
  --table customers \
  --target-dir /user/iabd/sqoop/customers \
  --fields-terminated-by ',' \
  --num-mappers 1
```

**Explicació:** selecciona la taula `customers`, estableix la destinació HDFS i executa una importació amb un únic mapper. `-P` sol·licita la contrasenya interactiva, en lloc de posar-la visible a la línia d'ordres.

### Importació i exportació

| Operació | Direcció |
|---|---|
| `sqoop import` | Base de dades relacional → Hadoop |
| `sqoop export` | Hadoop → base de dades relacional |

### Precaucions

- Sqoop és un projecte **retirat de l'Apache Software Foundation**: el seu estudi resulta útil per comprendre pipelines històrics, però no s'ha d'assumir que és la primera opció per a un projecte nou.
- Els connectors JDBC i les versions de Hadoop poden generar incompatibilitats.
- Per moure canvis continus amb garanties actuals s'han de valorar alternatives mantingudes.

## 13. Apache Flume [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Flume** és una eina d'ingesta basada en **agents i esdeveniments**, que permet recollir i enviar dades de diverses fonts cap a una destinació.

### Arquitectura bàsica

```text
Origen de dades
      │
      ▼
 Source ───> Channel ───> Sink ───> HDFS / destí
             (buffer)
```

- **Source:** captura o rep els esdeveniments.
- **Channel:** els manté temporalment en una cua.
- **Sink:** els consumeix i els envia al següent component.

### Exemple de configuració conceptual

```properties
agent1.sources = origen
agent1.channels = memoria
agent1.sinks = sortida

agent1.sources.origen.type = netcat
agent1.sources.origen.bind = localhost
agent1.sources.origen.port = 44444

agent1.channels.memoria.type = memory
agent1.channels.memoria.capacity = 1000
agent1.channels.memoria.transactionCapacity = 100

agent1.sinks.sortida.type = logger

agent1.sources.origen.channels = memoria
agent1.sinks.sortida.channel = memoria
```

Aquest exemple no envia dades a HDFS; **les mostra al registre** perquè sigui fàcil comprovar el flux.

### Flume versus Sqoop

| Aspecte | Sqoop | Flume |
|---|---|---|
| Font característica | Base de dades relacional | Logs i esdeveniments |
| Forma de treball habitual | Càrrega per lots | Flux d'esdeveniments |
| Unitat de treball | Registres importats/exportats | Esdeveniments |
| Exemples | Taula MariaDB a HDFS | Logs de servidors a HDFS |

**Recordatori:** la guia els agrupa junts com a eines d'ingesta, no com a tecnologies idèntiques.

## 14. Apache Oozie [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Oozie** és un sistema històric d'**orquestració** de treballs de l'ecosistema Hadoop. Serveix per definir **dependències entre passos**, programar execucions i coordinar tasques.

### Exemple d'un workflow lògic

```text
INICI
  │
  ▼
Importar dades
  │ (si acaba bé)
  ▼
Transformar dades
  │ (si acaba bé)
  ▼
Validar resultat
  │
  ▼
FINAL
```

### Diferència fonamental

- **Sqoop:** mou dades.
- **Flume:** transporta esdeveniments.
- **Oozie:** decideix **quan** i en **quin ordre** s'executen tasques d'un flux.

Una eina d'orquestració pot llançar altres sistemes, però **no és el mateix que el motor que transforma les dades**.

### Conceptes útils

- **Workflow:** seqüència lògica de tasques i dependències.
- **Coordinator:** programació condicionada per temps o disponibilitat de dades.
- **Bundle:** agrupació de coordinadors.
- **Reintent i gestió d'errors:** mecanismes de control que depenen del flux configurat.

Per a entorns actuals cal estudiar la disponibilitat i el manteniment de l'orquestrador abans d'adoptar-lo.

---

# PART III · INTERFÍCIES I EINES DE TREBALL

## 15. Definició de la categoria [GUIA]

La guia defineix aquestes eines com a interfícies que **faciliten l'accés, l'ús de funcionalitats i l'administració de Hadoop**. Enumera **Hue, Zeppelin, Ambari i Cloudera Manager**.

**[AMPLIACIÓ]** És important diferenciar dues subfamílies:

- **Interfícies d'usuari i analítica:** Hue i Zeppelin.
- **Gestió/administració de clústers:** Ambari i Cloudera Manager.

Aquesta subdivisió és explicativa: **el PDF els mostra en un únic grup**.

## 16. Apache Hue [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Hue** és una interfície web que facilita el treball amb dades, consultes i serveis d'un entorn analític, segons els connectors instal·lats.

### Aplicacions habituals

- Escriure i executar consultes SQL sense haver de fer-ho exclusivament al terminal.
- Explorar taules i resultats.
- Consultar fitxers o recursos accessibles per les integracions de la instal·lació.

### Exemple d'ús

Un estudiant que ha carregat dades a Hive pot obrir Hue, seleccionar el motor disponible, executar:

```sql
SELECT materia, COUNT(*)
FROM professors
GROUP BY materia;
```

i inspeccionar el resultat visualment.

**Idea clau:** Hue no és, per definició, el motor SQL. És una **interfície** que es connecta a motors i serveis.

## 17. Apache Zeppelin [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Zeppelin** és un entorn de **notebooks** orientat al treball amb dades. Permet combinar explicacions, codi, consultes i visualitzacions dins d'un mateix document interactiu.

### Notebook: què vol dir?

Un notebook organitza la feina en cel·les o paràgrafs que poden contenir codi, textos, gràfics o resultats. Això és útil per fer exploració de dades, demostracions o compartir anàlisis.

### Comparativa amb Hue

| Hue | Zeppelin |
|---|---|
| Orientat a consulta i interacció amb serveis de dades | Orientat a documents analítics i execució de codi |
| Útil per explorar taules i consultes | Útil per construir anàlisis explicades i reproduïbles |
| Pot donar accés a motors SQL | Pot integrar diversos intèrprets i motors |

**Recorda:** la compatibilitat concreta depèn de les extensions i versions desplegades.

## 18. Apache Ambari [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Ambari** és una eina d'administració, configuració i monitoratge d'entorns Hadoop. Conceptualment, resol necessitats del personal encarregat de gestionar serveis distribuïts.

### Què mira un administrador?

- Quins nodes formen el clúster.
- Quins serveis s'han iniciat i quins han fallat.
- Quin consum de recursos s'està produint.
- Quins paràmetres de configuració s'han aplicat.

### Per què és diferent de Hue?

**Hue** s'enfoca principalment a l'usuari que consulta dades. **Ambari** s'enfoca principalment a l'administrador que ha de desplegar, configurar i supervisar serveis.

## 19. Cloudera Manager [GUIA: nom · AMPLIACIÓ: descripció]

**Cloudera Manager** és una plataforma de gestió i supervisió de clústers de l'ecosistema de Cloudera.

### Funcions conceptuals

- Gestió de configuracions i serveis.
- Supervisió de processos, nodes i alertes.
- Administració del funcionament de components del clúster.
- Ajuda en tasques operatives i de diagnòstic.

### Ambari versus Cloudera Manager

Comparteixen la idea de facilitar **l'administració** de plataformes de dades, però no són el mateix producte ni necessàriament gestionen les mateixes distribucions, versions o components.

| Aspecte | Ambari | Cloudera Manager |
|---|---|---|
| Tipus d'eina | Administració de clústers | Administració de clústers |
| Focus | Serveis i operativa Hadoop compatibles | Plataforma i distribució Cloudera |
| Usuari principal | Administració de sistemes | Administració de plataformes |

---

# PART IV · PROCESSAMENT EN STREAMING

## 20. Definició de la categoria [GUIA]

**[GUIA]** Aquesta categoria inclou eines per tractar dades **quan encara estan arribant**, sense esperar que tot el dataset estigui complet o en repòs. El PDF enumera **Kafka, Spark, Flink i Storm**.

**Nota de terminologia [AMPLIACIÓ]:** el document escriu «Apache Flink (structured streaming)». Convé distingir que **Structured Streaming** és el nom habitual de l'API de streaming de **Spark**, mentre que **Flink** disposa de les seves pròpies APIs de processament de fluxos. Als apunts mantenim Flink dins del grup que indica el PDF, però no atribuïm el nom de l'API de Spark a Flink.

### Batch i streaming

```text
BATCH:
[fitxer complet] ─────> [processar] ─────> [resultats]

STREAMING:
esdeveniment 1 ─┐
esdeveniment 2 ─┼─────> [processament continu] ──> resultats progressius
esdeveniment 3 ─┘
```

No sempre «temps real» significa latència zero. En enginyeria sovint significa que els resultats s'actualitzen amb una latència adequada al cas d'ús.

## 21. Apache Kafka [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Kafka** és una plataforma distribuïda de streaming d'esdeveniments que permet **publicar, conservar i consumir fluxos de registres**.

### Vocabulari essencial

- **Producer:** aplicació que envia esdeveniments.
- **Topic:** categoria lògica d'esdeveniments.
- **Partition:** partició d'un topic per distribuir-ne el trànsit i l'emmagatzematge.
- **Consumer:** aplicació que llegeix esdeveniments.
- **Consumer group:** grup de consumidors que coordinen la lectura.
- **Offset:** posició d'un registre dins d'una partició.

### Esquema

```text
Aplicació A ─┐
             ├──> Kafka (topic: vendes) ──> Consumidor 1 (analítica)
Aplicació B ─┘                         └──> Consumidor 2 (alertes)
```

### És un motor analític?

**No s'ha de confondre un sistema de transport/streaming d'esdeveniments amb un motor de càlcul distribuït.** Kafka permet alimentar sistemes de processament. Per al processament més avançat es pot combinar, per exemple, amb Spark o Flink.

### Exemple de cas d'ús

Una botiga envia un esdeveniment cada vegada que s'efectua una venda. Els esdeveniments arriben a Kafka i diversos consumidors poden utilitzar-los per elaborar indicadors, generar alertes o persistir l'històric.

## 22. Apache Flink [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Flink** és un motor de processament distribuït especialment conegut per les seves capacitats de **stream processing amb estat**.

### Conceptes útils

- **Stream:** seqüència d'esdeveniments al llarg del temps.
- **Event time:** moment en què l'esdeveniment s'ha produït a l'origen.
- **Processing time:** moment en què el motor el processa.
- **Watermark:** indicació utilitzada per raonar sobre esdeveniments que poden arribar tard.
- **Window:** agrupació d'esdeveniments en intervals temporals o lògics.
- **State:** memòria lògica mantinguda entre esdeveniments per calcular resultats incrementals.

### Exemple conceptual

```text
Vendes entrants ──> Agrupar per finestres de 5 minuts ──> Total per botiga
```

Per què s'utilitza una finestra? Perquè, en un flux potencialment infinit, no sempre podem esperar que «acabin» les dades per calcular resultats.

### Spark Structured Streaming versus Flink

Tots dos poden processar fluxos, però disposen d'arquitectures, semàntiques i APIs pròpies. No s'ha de decidir només pel nom: cal valorar estat, finestres, latència, fonts, ecosistema i operació.

## 23. Apache Storm [GUIA: nom · AMPLIACIÓ: descripció]

**Apache Storm** és una tecnologia de processament distribuït de fluxos. Històricament s'ha utilitzat per construir **topologies** que consumeixen i transformen esdeveniments.

### Terminologia clàssica

- **Topology:** graf de components que processen el flux.
- **Spout:** origen que produeix tuples.
- **Bolt:** component que processa, transforma, filtra o agrega tuples.
- **Tuple:** unitat de dades dins del flux.

### Esquema

```text
Spout (esdeveniments)
        │
        ▼
Bolt (filtre)
        │
        ▼
Bolt (comptador)
        │
        ▼
Resultat / destinació
```

### Diferència amb Flume

Flume s'associa principalment a la ingesta i moviment d'esdeveniments. Storm s'orienta a **processar** fluxos mitjançant una topologia d'operadors. En projectes reals, les fronteres poden solapar-se, però aquesta diferenciació ajuda a estudiar.

---

# PART V · COMPARATIVES I ARQUITECTURES

## 24. Taula general de decisió [AMPLIACIÓ]

| Necessitat | Eina/es a considerar | Motiu |
|---|---|---|
| Consultar un dataset amb SQL | Hive / Impala | Capa de consulta SQL |
| Crear transformacions amb scripts Pig Latin | Pig | Fluxos de tractament de dades |
| Llegir per identificador registres distribuïts | HBase | Accés per row key |
| Consultar HBase amb SQL | Phoenix | Capa SQL sobre HBase |
| Transformacions distribuïdes amb Python/SQL | Spark | Motor de càlcul distribuït |
| Importar taules de MariaDB a HDFS | Sqoop (entorn històric) | Connectivitat RDBMS-Hadoop |
| Recollir logs en forma d'esdeveniments | Flume (entorn històric) | Agents source-channel-sink |
| Definir dependències entre treballs | Oozie (entorn històric) | Orquestració |
| Executar consultes des d'una interfície web | Hue | Frontend de dades |
| Crear notebooks analítics | Zeppelin | Interacció amb codi i visualitzacions |
| Administrar serveis Hadoop | Ambari / Cloudera Manager | Operativa del clúster |
| Distribuir esdeveniments a consumidors | Kafka | Plataforma d'esdeveniments |
| Analitzar fluxos amb estat i finestres | Flink / Spark | Processament de streaming |
| Definir topologies clàssiques d'esdeveniments | Storm | Spouts i bolts |

**Nota:** és una taula didàctica d'orientació, no una recomanació tancada per a un desplegament actual. Cal confirmar l'estat de manteniment i compatibilitat de cada producte.

## 25. Arquitectures d'exemple [AMPLIACIÓ]

### Cas A: data warehouse a partir d'una BD relacional

**Objectiu:** analitzar històrics de compres que es troben en MariaDB.

```text
MariaDB ── Sqoop ──> HDFS ──> Hive ──> Hue
```

**Lectura:** Sqoop importa dades, HDFS les emmagatzema, Hive les presenta en taules i Hue permet consultar-les visualment. **Oozie** podria coordinar execucions periòdiques.

### Cas B: anàlisi de logs

**Objectiu:** consolidar registres generats per servidors.

```text
Servidors web ──> Flume ──> HDFS ──> Spark ──> resultats
```

Flume transporta els esdeveniments; Spark pot transformar o analitzar els fitxers que han quedat emmagatzemats.

### Cas C: alertes sobre esdeveniments

**Objectiu:** identificar lectures anòmales de sensors.

```text
Sensors ──> Kafka ──> Flink ──> Alertes
                       │
                       └─────> Històric
```

Flink processa lectures a mesura que arriben i pot aplicar finestres, estadístiques i regles. Kafka permet la distribució de missatges als consumidors.

### Cas D: analítica i exploració

```text
Dades distribuïdes ──> Hive / Impala ──> Hue
                              │
                              └────────> Aplicació analítica
```

S'escull el motor en funció del tipus de consulta i dels requisits d'execució.

### Cas E: consultes per clau i SQL

```text
Aplicació ──> Phoenix ──> HBase ──> emmagatzematge distribuït
```

La decisió aquí es basa en el patró d'accés a registres individuals, no només en la mida total del dataset.

## 26. Conceptes transversals [AMPLIACIÓ]

### 26.1. Batch

**Batch** significa processar conjunts de dades en lots. Els processos poden ser periòdics (cada hora o cada nit) i sovint treballen amb dades acumulades.

**Exemple:** calcular a les 02:00 el total de vendes del dia anterior.

### 26.2. Streaming

**Streaming** significa processar registres com a flux continu o successiu, sense requerir que tot el conjunt de dades estigui complet.

**Exemple:** comptar vendes cada minut mentre van entrant.

### 26.3. ETL i ELT

- **ETL:** Extract → Transform → Load. Les transformacions es realitzen abans de carregar la dada a la destinació analítica final.
- **ELT:** Extract → Load → Transform. Primer es carreguen les dades i després es transformen dins de l'entorn de destinació.

Els dos patrons poden aparèixer en ecosistemes Big Data.

### 26.4. SQL i NoSQL

- **SQL:** llenguatge de consulta declaratiu molt habitual en sistemes relacionals i motors analítics.
- **NoSQL:** etiqueta que agrupa diversos models de bases de dades no relacionals clàssiques.

**HBase és NoSQL**, mentre que **Phoenix proporciona una capa SQL** sobre HBase. Això il·lustra que l'API de consulta i el sistema subjacent són conceptes diferents.

### 26.5. Ingesta, persistència i processament

```text
INGESTA      = les dades arriben
PERSISTÈNCIA = les dades es guarden
PROCESSAMENT = les dades es transformen o analitzen
VISUALITZACIÓ = el resultat es consulta o representa
ORQUESTRACIÓ = es coordina quan i com s'executen les tasques
```

Una arquitectura completa sovint necessita **més d'una** d'aquestes funcions.

### 26.6. Latència i throughput

- **Latència:** temps que triga una operació o esdeveniment a produir un resultat.
- **Throughput:** quantitat d'elements o bytes processats per unitat de temps.

Un procés pot moure un volum molt elevat de dades, però trigar minuts a retornar cada resultat; tenir bon throughput no implica sempre latència baixa.

### 26.7. Escalabilitat horitzontal

Vol dir augmentar la capacitat afegint nous nodes o instàncies en lloc de dependre només d'una màquina més potent. Moltes eines Big Data estan dissenyades amb aquest objectiu, però l'escalabilitat real depèn del repartiment de dades, recursos i configuració.

---

# PART VI · PRÀCTICA, ERRORS I REPÀS

## 27. Exemples pràctics il·lustratius [AMPLIACIÓ]

> **Important:** el PDF original **no inclou exercicis ni comandes**. Els exemples següents són afegits per facilitar l'aprenentatge i no impliquen que totes aquestes eines estiguin instal·lades a la teva màquina virtual.

### Exercici A: classifica cada necessitat

1. Necessito importar una taula de MySQL cada nit → **Sqoop**, amb orquestració separada si cal.
2. Vull consultar milions de files amb SQL → **Hive o Impala**.
3. Necessito consultar una lectura concreta per identificador → **HBase**.
4. Vull construir un notebook amb explicacions i resultats → **Zeppelin**.
5. Vull conèixer l'estat dels serveis del clúster → **Ambari o Cloudera Manager**.
6. Necessito calcular tendències de fluxos que arriben contínuament → **Flink o Spark**.

### Exercici B: identifica components en un pipeline

```text
MariaDB → [A] → HDFS → [B] → [C]
```

Una solució possible:

- **A = Sqoop** per importar registres.
- **B = Hive** per consultar-los amb SQL.
- **C = Hue** per executar les consultes des del navegador.

### Exercici C: reconeix l'error conceptual

> «Si instal·lo Hue ja tinc el motor de processament de dades.»

**Resposta:** fals. Hue és principalment una interfície; necessita connexió a serveis que executin les operacions.

### Exercici D: proposa un sistema per temps real

**Problema:** cada segon arriben dades de temperatura de diversos sensors i cal detectar pujades sobtades.

**Solució possible:** Kafka per rebre i distribuir esdeveniments, i Flink per calcular desviacions amb estat i finestres. El sistema podria persistir les lectures en un magatzem extern per conservar-ne l'històric.

## 28. Errors habituals i confusions [AMPLIACIÓ]

| Confusió | Correcció |
|---|---|
| «Hadoop és només HDFS» | Hadoop és un ecosistema de diversos components; HDFS és el sistema de fitxers |
| «Hive emmagatzema totes les dades dins del metastore» | El metastore emmagatzema principalment **metadades**, no els datasets complets |
| «HBase i HDFS fan exactament el mateix» | HBase afegeix accés per registres/claus; HDFS és emmagatzematge de fitxers |
| «Phoenix substitueix HBase» | Phoenix ofereix una capa SQL sobre HBase |
| «Hue és un motor de càlcul» | Hue és una interfície |
| «Kafka i Flink són idèntics» | Kafka se centra en esdeveniments; Flink, en processar fluxos |
| «Sqoop és per a qualsevol tipus de log» | Sqoop està associat a bases de dades estructurades; Flume és més propi dels logs |
| «Oozie fa les agregacions SQL» | Oozie orquestra tasques; altres motors executen els càlculs |
| «Spark només serveix per a batch» | Spark també té capacitats de streaming |
| «Structured Streaming és l'API de Flink» | És una API de Spark; Flink té el seu propi model de streaming |
| «Un motor interactiu sempre guanya en velocitat» | El rendiment depèn del context i del tipus de consulta |
| «Streaming equival a zero latència» | Sempre hi ha retard; la latència adequada depèn de l'objectiu |
| «Totes les eines del PDF són igualment vigents avui» | Cal comprovar l'estat de manteniment i compatibilitat de cada eina |

## 29. Glossari [AMPLIACIÓ]

| Terme | Definició breu |
|---|---|
| Hadoop | Ecosistema de tecnologies per a dades distribuïdes |
| HDFS | Sistema de fitxers distribuït de Hadoop |
| YARN | Gestió de recursos i planificació de treballs en Hadoop |
| MapReduce | Model de processament distribuït basat en fases Map i Reduce |
| Batch | Processament en lots |
| Streaming | Processament d'esdeveniments en flux |
| Ingesta | Entrada i captació de dades |
| Data lake | Repositori de dades en diversos formats per al seu ús posterior |
| Data warehouse | Entorn organitzat per a anàlisi i explotació de dades |
| ETL | Extracció, transformació i càrrega |
| ELT | Extracció, càrrega i transformació |
| Metastore | Catàleg de metadades sobre taules i dades |
| HiveQL | Dialecte SQL utilitzat a Hive |
| Row key | Clau d'identificació de files en HBase |
| NoSQL | Famílies de bases de dades no relacionals clàssiques |
| JDBC | Interfície per connectar aplicacions Java amb bases de dades |
| Source | Component que origina o rep esdeveniments en Flume |
| Channel | Buffer entre source i sink en Flume |
| Sink | Component de sortida en Flume |
| Topic | Canal lògic de registres en Kafka |
| Partition | Partició d'un topic o conjunt distribuït de dades |
| Consumer | Aplicació que llegeix esdeveniments |
| Offset | Posició d'un registre dins d'una partició de Kafka |
| Window | Agrupació de dades segons una finestra temporal/lògica |
| Watermark | Mecanisme per tractar el progrés temporal i dades tardanes |
| Workflow | Seqüència de tasques amb dependències |
| Notebook | Document interactiu amb text, codi i resultats |
| Clúster | Conjunt de nodes que treballen coordinadament |
| Latència | Retard fins a obtenir un resultat |
| Throughput | Volum de treball processat per unitat de temps |
| Escalabilitat horitzontal | Increment de capacitat afegint nodes |

## 30. Preguntes d'autoavaluació amb resposta

> **Metodologia:** les preguntes **1–16** comproven la classificació de la pàgina original. Les **17–60** són d'ampliació explicativa.

### Bloc A — Classificació de la guia [GUIA]

1. **Quantes famílies presenta la guia?** Quatre.
2. **Quina família inclou Pig?** Accés i processament de dades.
3. **Quina família inclou Hive?** Accés i processament de dades.
4. **Quina família inclou Impala?** Accés i processament de dades.
5. **Quina família inclou HBase?** Accés i processament de dades.
6. **Quina família inclou Phoenix?** Accés i processament de dades.
7. **Quina família inclou Spark?** Accés i processament, i també streaming.
8. **Quines eines es troben al grup d'ingesta?** Sqoop, Flume i Oozie.
9. **Quina família inclou Oozie?** Ingesta i fluxos de treball.
10. **Quines eines formen el grup d'interfícies?** Hue, Zeppelin, Ambari i Cloudera Manager.
11. **Quina família inclou Hue?** Interfícies i eines de treball.
12. **Quina família inclou Zeppelin?** Interfícies i eines de treball.
13. **Quines eines enumera el grup streaming?** Kafka, Spark, Flink i Storm.
14. **La guia situa Kafka a la categoria streaming?** Sí.
15. **Quina categoria fa referència a accions periòdiques?** Ingesta i fluxos de treball.
16. **Quina categoria parla de dades que es van incorporant i s'analitzen?** Processament en streaming.

### Bloc B — Conceptes generals [AMPLIACIÓ]

17. **Què és HDFS?** Sistema de fitxers distribuït.
18. **Què és YARN?** Gestor de recursos i planificació de tasques de Hadoop.
19. **Què significa batch?** Processament d'un conjunt de dades en un lot.
20. **Què significa streaming?** Processament d'un flux continu o successiu d'esdeveniments.
21. **Què és ETL?** Extract, Transform, Load.
22. **Què és ELT?** Extract, Load, Transform.
23. **Què és la latència?** Temps fins a obtenir una resposta o resultat.
24. **Què és throughput?** Quantitat processada per unitat de temps.
25. **Què és un clúster?** Conjunt de nodes coordinats.
26. **Què significa escalar horitzontalment?** Afegir nodes.

### Bloc C — Accés i processament [AMPLIACIÓ]

27. **Quin llenguatge utilitza Pig?** Pig Latin.
28. **Quina és la idea fonamental de Hive?** Consultar i gestionar dades amb SQL distribuït.
29. **Què guarda el metastore de Hive?** Metadades de taules, esquemes i ubicacions, entre d'altres.
30. **Per a quin tipus de consultes destaca Impala?** Analítiques SQL interactives.
31. **Què és una row key?** Identificador utilitzat per localitzar una fila en HBase.
32. **HBase és una base de dades relacional clàssica?** No, és NoSQL.
33. **Per a què serveix Phoenix?** Oferir SQL sobre HBase.
34. **Spark executa només SQL?** No, és un motor distribuït general.
35. **Què és un DataFrame a Spark?** Abstracció de dades tabulars amb esquema.
36. **En què es diferencien Spark i Spark SQL?** Spark és el motor; Spark SQL és una de les seves APIs/capacitats.

### Bloc D — Ingesta i orquestració [AMPLIACIÓ]

37. **Quina eina històrica importava taules de BD relacionals a Hadoop?** Sqoop.
38. **Què fa `sqoop import`?** Mou registres de la base de dades cap a Hadoop.
39. **Què fa `sqoop export`?** Mou dades de Hadoop cap a la base de dades.
40. **Quins tres components té un agent Flume?** Source, Channel i Sink.
41. **Què fa el Channel?** Emmagatzema temporalment esdeveniments.
42. **Quina diferència hi ha entre Flume i Sqoop?** Flume s'enfoca a fluxos/esdeveniments; Sqoop, a intercanvi de dades estructurades amb BD.
43. **Què és un workflow?** Seqüència de passos amb dependències.
44. **Quin paper té Oozie?** Orquestrar treballs i calendaris.

### Bloc E — Interfícies i administració [AMPLIACIÓ]

45. **Hue transforma dades sense un motor extern?** No és aquesta la seva funció principal.
46. **Què és un notebook?** Document interactiu amb codi i resultats.
47. **Quina eina del temari és coneguda pels notebooks?** Zeppelin.
48. **Què comparteixen Ambari i Cloudera Manager?** Funcions d'administració i supervisió.
49. **Què vol dir monitorar un clúster?** Revisar estat, mètriques i incidències.
50. **Què diferencia Hue d'Ambari?** Hue s'orienta a dades/consultes; Ambari a administració.

### Bloc F — Streaming [AMPLIACIÓ]

51. **Què és un topic de Kafka?** Canal lògic que agrupa esdeveniments.
52. **Què fa un producer?** Publica esdeveniments.
53. **Què fa un consumer?** Consumeix esdeveniments.
54. **Què és un offset?** Posició d'un registre en una partició.
55. **Kafka és el mateix que Flink?** No; Kafka gestiona fluxos d'esdeveniments i Flink els processa.
56. **Què és una window?** Agrupació de dades en una finestra temporal o lògica.
57. **Què és un watermark?** Mecanisme per gestionar el progrés del temps d'esdeveniment i el retard.
58. **Què és un spout de Storm?** Component d'origen d'esdeveniments.
59. **Què és un bolt de Storm?** Component de processament d'una topologia.
60. **A quina eina pertany Structured Streaming?** A Spark.

## 31. Exercicis de raonament resolts [AMPLIACIÓ]

### Exercici 1 — Diferencia emmagatzematge i consulta

**Enunciat:** «Una empresa té milers de fitxers a HDFS i vol consultar-ne el contingut amb SQL. Quins components de la guia podrien ajudar-la?»

**Solució:** Hive o Impala poden proporcionar motors de consulta SQL sobre dades distribuïdes compatibles. Hue pot actuar com a interfície, però no substitueix el motor.

### Exercici 2 — Dades concretes en lloc d'escanejos massius

**Enunciat:** «Necessito recuperar molt sovint l'estat d'un sensor identificat pel seu codi.»

**Solució:** HBase és un candidat per a accés per clau; Phoenix seria un complement si es vol accedir amb SQL. Caldria dissenyar bé la clau i comprovar els patrons d'accés.

### Exercici 3 — Ingesta periòdica i dependències

**Enunciat:** «Cada nit s'importen taules de MariaDB, després es transformen i finalment s'actualitza un informe.»

**Solució:** Sqoop pot fer la importació en un entorn històric; Spark o Hive poden transformar les dades; Oozie pot coordinar les dependències. En un projecte nou caldria revisar alternatives mantingudes.

### Exercici 4 — Dades en temps real

**Enunciat:** «Vull saber quantes peticions rep la web durant cada interval de 30 segons.»

**Solució:** un productor podria publicar esdeveniments a Kafka i Flink/Spark processar-los per finestres temporals. També cal considerar dades fora d'ordre, duplicats i persistència.

### Exercici 5 — Manteniment

**Enunciat:** «Un administrador observa que diversos serveis del clúster no estan disponibles.»

**Solució:** Ambari o Cloudera Manager són eines de la categoria d'administració que poden ajudar a identificar l'estat dels serveis, sempre que siguin compatibles amb l'entorn.

### Exercici 6 — Confusió entre Spark i Kafka

**Enunciat:** «Si ja tinc Kafka, no necessito mai Spark.»

**Solució:** fals. Kafka pot gestionar la distribució i conservació d'esdeveniments; Spark pot fer transformacions i anàlisis que Kafka no substitueix per si sol. Poden treballar junts.

### Exercici 7 — Duplicació de categories

**Enunciat:** «La guia posa Spark en dos grups. És incorrecte?»

**Solució:** no. Spark té capacitats de processament de dades i de streaming, per això encaixa en més d'una família funcional.

### Exercici 8 — Cal instal·lar totes les eines?

**Enunciat:** «Per fer una solució Hadoop, cal instal·lar totes les tecnologies que apareixen al PDF?»

**Solució:** no. Es tria una arquitectura mínima en funció de les fonts de dades, el tipus de consultes, la latència, el cost i el manteniment. El catàleg del PDF és un mapa de possibilitats, no una llista d'instal·lació obligatòria.

## 32. Resum final i checklist d'examen

### Resum de memòria ràpida [GUIA]

```text
ACCÉS I PROCESSAMENT
  Pig · Hive · Impala · HBase · Phoenix · Spark

INGESTA I FLUXOS DE TREBALL
  Sqoop · Flume · Oozie

INTERFÍCIES I EINES DE TREBALL
  Hue · Zeppelin · Ambari · Cloudera Manager

PROCESSAMENT EN STREAMING
  Kafka · Spark · Flink · Storm
```

### Regla mnemotècnica [AMPLIACIÓ]

- **P**ig: **P**rocessos de transformació.
- **H**ive: consultes tipus **H**QL.
- **I**mpala: analítica **I**nteractiva.
- **H**Base: accés per clau a una base **H**Base/NoSQL.
- **P**hoenix: SQL sobre HBase.
- **S**park: càlcul distribuït i streaming.
- **S**qoop: SQL/BD relacional ↔ Hadoop.
- **F**lume: **F**luxos d'esdeveniments.
- **O**ozie: **O**rquestració.
- **H**ue: interfície de consulta.
- **Z**eppelin: notebooks.
- **A**mbari i **C**loudera Manager: administració.
- **K**afka: canal d'esdeveniments.
- **F**link: processament de fluxos amb estat.
- **S**torm: topologies de streaming.

### Checklist per saber si ja ho domines

- [ ] Puc enumerar els quatre grups de la guia sense mirar els apunts.
- [ ] Puc classificar correctament les 16 eines diferents del document.
- [ ] Recordo que Spark surt en dues categories.
- [ ] Puc explicar en una frase per a què serveix cada eina.
- [ ] Distingeixo clarament Sqoop, Flume i Oozie.
- [ ] Distingeixo HDFS, HBase, Hive i Phoenix.
- [ ] Distingeixo Hue/Zeppelin d'Ambari/Cloudera Manager.
- [ ] Distingeixo Kafka de Flink i Storm.
- [ ] Entenc per què es necessita batch en alguns casos i streaming en d'altres.
- [ ] Puc dissenyar un flux de dades amb ingesta, persistència, processament i consulta.
- [ ] Sé que les descripcions ampliades i els exemples no formen part del PDF original.

---

## Font i abast

**Document base:** *M5075 BigData Aplicat — Ecosistema Hadoop*, PDF d'**una pàgina** proporcionat a la conversa. Inclou exclusivament la classificació general i els noms de les eines de les quatre famílies.

**Ampliació pedagògica:** les definicions detallades, exemples SQL/Python/Pig, arquitectures, taules comparatives, advertiments, exercicis, glossari i preguntes són contingut explicatiu afegit per facilitar l'estudi. No s'han de presentar com si fossin cites literals de la guia.

**Nota d'actualitat:** abans d'emprar aquestes eines en un projecte nou, s'han de verificar la disponibilitat de versions, l'estat del manteniment, la compatibilitat i els requisits de seguretat del desplegament.
