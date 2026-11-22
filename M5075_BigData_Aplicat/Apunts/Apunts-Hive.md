# Apache Hive I — Apunts extensos

## Índex

1. [Introducció a Hive](#1-introducció-a-hive)
2. [Hive dins l'ecosistema Hadoop](#2-hive-dins-lecosistema-hadoop)
3. [Característiques, avantatges i limitacions](#3-característiques-avantatges-i-limitacions)
4. [Alternatives a Hive](#4-alternatives-a-hive)
5. [Arquitectura i components](#5-arquitectura-i-components)
6. [HiveServer2, Metastore, Beeline i motors](#6-hiveserver2-metastore-beeline-i-motors)
7. [Tipus de dades i conversions](#7-tipus-de-dades-i-conversions)
8. [Instal·lació i configuració](#8-installació-i-configuració)
9. [Primeres passes, clients i accés remot](#9-primeres-passes-clients-i-accés-remot)
10. [Cas 1 — Creació i esborrat de taules](#10-cas-1--creació-i-esborrat-de-taules)
11. [Hue: interfície web](#11-hue-interfície-web)
12. [Cas 2 — Càrrega i inserció de dades](#12-cas-2--càrrega-i-inserció-de-dades)
13. [Actualització i esborrat transaccional](#13-actualització-i-esborrat-transaccional)
14. [Ingesta des de Sqoop i exportació](#14-ingesta-des-de-sqoop-i-exportació)
15. [Cas 3 — JOINs](#15-cas-3--joins)
16. [Comandes i funcions útils](#16-comandes-i-funcions-útils)
17. [Cas 4 — Taules internes i dades complexes](#17-cas-4--taules-internes-i-dades-complexes)
18. [Consultes amb ARRAY, STRUCT i MAP](#18-consultes-amb-array-struct-i-map)
19. [Cas 5 — Taules externes](#19-cas-5--taules-externes)
20. [Hive, MapReduce i Fetch Task](#20-hive-mapreduce-i-fetch-task)
21. [Errors habituals i diagnòstic](#21-errors-habituals-i-diagnòstic)
22. [Resums i taules comparatives](#22-resums-i-taules-comparatives)
23. [Preguntes de repàs amb respostes](#23-preguntes-de-repàs-amb-respostes)
24. [Glossari i checklist final](#24-glossari-i-checklist-final)

---

## 1. Introducció a Hive

**Apache Hive** és una tecnologia orientada a consultar, llegir, escriure i gestionar conjunts massius de dades en un entorn Hadoop. Permet utilitzar un llenguatge similar a SQL, anomenat **HiveQL / HiveSQL**, per operar sobre dades que habitualment resideixen a **HDFS**. El document es refereix a volums que poden arribar a l'escala de petabytes.

Hive es va originar a Facebook per aproximar l'experiència de consultar Hadoop a l'experiència de treballar amb un *data warehouse* tradicional. Sense Hive, un usuari de Hadoop podia necessitar desenvolupar processos específics de MapReduce; amb Hive, expressa bona part del treball mitjançant sentències declaratives com `SELECT`, `CREATE TABLE` o `INSERT`.

**Idea fonamental:** Hive no és simplement una base de dades SQL clàssica instal·lada sobre un servidor. És una capa de consulta i gestió de metadades que treballa sobre dades distribuïdes i utilitza motors de processament del seu ecosistema.

### 1.1 Exemple molt simple

```sql
CREATE DATABASE IF NOT EXISTS iabd;
USE iabd;
SHOW TABLES;
SELECT * FROM customers LIMIT 5;
```

El primer comandament crea una base de dades lògica; el segon la selecciona; el tercer mostra les taules disponibles; el quart consulta cinc registres de `customers`, si aquesta taula existeix.

### 1.2 Quan té sentit utilitzar Hive?

- Quan disposem de moltes dades a HDFS i volem fer-ne anàlisi amb SQL.
- Quan necessitem treballs analítics de tipus *batch*, ETL i agregacions.
- Quan volem un esquema lògic sobre fitxers, sense convertir-los necessàriament en una base de dades transaccional tradicional.
- Quan diferents processos del món Hadoop han de poder consultar datasets estructurats.

**No és l'opció preferida** per a operacions interactives de molt baixa latència ni per a transaccions freqüents registre a registre, especialment en el context del sistema que es treballa als apunts.

## 2. Hive dins l'ecosistema Hadoop

Hadoop aporta emmagatzematge distribuït i components d'execució; Hive ofereix una interfície d'alt nivell sobre aquest entorn.

```text
                  USUARI / ANALISTA
                         |
                  HiveQL / SQL
                         |
                 Beeline o Hue
                         |
                    HiveServer2
                         |
                   Driver / pla
                    /         \
             Metastore      Motor d'execució
             (esquema)      (MR / Tez / Spark)
                                  |
                             YARN / HDFS
                                  |
                          Fitxers distribuïts
```

**HDFS** desa els fitxers físics; **Hive Metastore** desa les definicions de bases de dades, taules, columnes, formats i ubicacions; **HiveServer2** ofereix l'accés als clients; **l'execució** resol la consulta amb el motor configurat.

La figura de l'ecosistema Hadoop de la pàgina 6 del PDF situa Hive a la capa de consulta i processament, connectat amb altres tecnologies de l'ecosistema. L'esquema d'arquitectura de la pàgina 8 distingeix clients, serveis i emmagatzematge.

### 2.1 Schema-on-read

Hive declara un **schema** o estructura sobre les dades emmagatzemades. En consultar un fitxer delimitat, cal saber per exemple que el primer camp és `INT`, el segon `STRING` i que el separador és `|`.

```text
Fitxer HDFS:  12|Anna|Girona
Esquema Hive: id INT | nom STRING | ciutat STRING
Resultat:     12    Anna       Girona
```

El *metastore* registra aquesta correspondència. La definició de la taula no implica que les dades hagin de ser copiades a una base de dades relacional de manera tradicional.

## 3. Característiques, avantatges i limitacions

### 3.1 Característiques

- Consulta declarativa mitjançant HiveQL.
- Integració amb HDFS, Hadoop i altres components.
- Gestió d'esquemes i metadades.
- Possibilitat de processament distribuït i paral·lel.
- Formats d'emmagatzematge diferents, com TEXTFILE, PARQUET i ORC.
- Suport de dades simples i **tipus complexos** (`ARRAY`, `MAP`, `STRUCT`).
- Suport de particionat i tècniques d'optimització segons la configuració.
- Interacció via terminals i interfícies gràfiques.

### 3.2 Avantatges

1. Evita haver d'escriure manualment molts treballs MapReduce.
2. Ofereix una sintaxi familiar per a persones amb coneixements SQL.
3. Resulta útil per a conjunts grans i anàlisi de tipus *data warehouse*.
4. Separa l'esquema lògic de la ubicació física i el format dels fitxers.
5. Facilita l'accés a les dades mitjançant Beeline, Hive CLI o Hue.

### 3.3 Limitacions

- Les consultes distribuïdes poden tenir una **latència d'inicialització** significativa.
- Les operacions petites poden ser menys eficients que en bases de dades dissenyades per a consultes ràpides.
- El suport d'actualitzacions i esborrats requereix configuració i taules adequades.
- El dialecte SQL i el comportament depenen de la versió i el motor.

**Per recordar:** *Hive prioritza l'anàlisi de grans volums; una BD OLTP prioritza operacions curtes i transaccionals.*

## 4. Alternatives a Hive

| Tecnologia | Enfocament descrit al temari | Diferència rellevant |
|---|---|---|
| **Apache Impala** | Consultes distribuïdes amb motor MPP | Adequat per a anàlisi interactiva i baixa latència; pot aprofitar el metastore de Hive |
| **Presto** | Motor SQL distribuït | Alternativa per a consultes analítiques |
| **Apache Drill** | Consultes distribuïdes | Arquitectura de consulta alternativa |
| **Spark SQL** | SQL sobre el motor Spark | No és el mateix que seleccionar Spark com a motor dins Hive |
| **Apache Pig** | Scripts `Pig Latin` | Abstracció de fluxos de dades diferent d'una interfície SQL |

El document destaca especialment **Impala**: en lloc del model clàssic basat en treballs MapReduce, fa servir processament massiu en paral·lel (MPP). També remarca que Pig ha perdut protagonisme en comparació amb alternatives més modernes.

## 5. Arquitectura i components

### 5.1 Vista de conjunt

L'arquitectura té peces diferenciades que convé no confondre:

| Component | Funció principal |
|---|---|
| Client SQL | Envia ordres HiveQL |
| HiveServer2 | Accepta connexions de clients i coordina les consultes |
| Driver / motor | Planifica i executa les consultes |
| Hive Metastore | Emmagatzema metadades d'esquemes, taules i ubicacions |
| Base de dades del metastore | Desa les metadades físicament (MySQL/MariaDB, Derby, etc.) |
| HDFS | Conté els fitxers de dades |
| YARN | Gestiona recursos i planifica tasques distribuïdes |

### 5.2 Exemple de recorregut d'una consulta

```sql
SELECT city, COUNT(*)
FROM customers
GROUP BY city;
```

1. Beeline envia la consulta a HiveServer2.
2. Hive interpreta la sentència i consulta les metadades de `customers`.
3. Determina on són els fitxers, quines columnes existeixen i quin format tenen.
4. Planifica l'execució amb el motor configurat.
5. Llegeix i processa les dades.
6. Retorna els resultats al client.

## 6. HiveServer2, Metastore, Beeline i motors

### 6.1 HiveServer2

És el servei que permet a aplicacions i clients remots executar consultes Hive. El material de classe fa servir l'ordre:

```bash
hiveserver2
```

El port habitual configurat als exemples és **10000**. El servei permet clients concurrents i ofereix connectivitat basada en Thrift/JDBC.

> **Nota de versions del temari:** el PDF esmenta diferents versions de Hive en apartats diferents i contextualitza la compatibilitat de la màquina virtual. Abans de copiar rutes o biblioteques, comprova la versió realment instal·lada a `HIVE_HOME`.

### 6.2 Hive Metastore

El **Metastore** és el repositori de metadades de Hive. No emmagatzema les files de les taules analítiques com si fos el seu motor de dades principal; hi desa definicions com:

- nom de la base de dades i de les taules;
- noms i tipus de les columnes;
- format de fitxer;
- directori `LOCATION` a HDFS;
- altres propietats, particions i estadístiques disponibles.

Pot recolzar-se en **Derby**, **MySQL/MariaDB** o **PostgreSQL**. El PDF indica que, a la màquina docent, es fa servir MySQL/MariaDB per facilitar connexions simultànies.

### 6.3 Metastore embegut, local i remot

| Mode | Esquema conceptual | Observació |
|---|---|---|
| Embegut | Hive + metastore + Derby al mateix procés | Senzill per a proves |
| Local | Hive + metastore local + BD externa | Metadades en servidor relacional |
| Remot | HiveServer/clients → servei Metastore → BD | Servei separat que altres eines poden consultar |

A la figura de la **pàgina 10** es comparen visualment les tres topologies.

Configuració de metastore remot al fitxer `$HIVE_HOME/conf/hive-site.xml`:

```xml
<property>
  <name>hive.metastore.uris</name>
  <value>thrift://master:9083</value>
</property>
```

Arrencada del servei, quan s'ha configurat com a remot:

```bash
hive --service metastore &
hiveserver2
```

El port habitual del metastore remot als exemples és **9083**. No el confonguis amb el **10000** de HiveServer2.

### 6.4 Beeline

**Beeline** és el client de consola recomanat pel temari. Es connecta per JDBC a HiveServer2:

```bash
beeline -u jdbc:hive2://master:10000 -n iabd -p iabd
```

O obrint la consola primer:

```bash
beeline
```

I, a dins:

```text
!connect jdbc:hive2://master:10000
```

Després de connectar:

```sql
SHOW DATABASES;
```

Les ordres pròpies de Beeline acostumen a començar per `!`, mentre que les sentències HiveQL com `SELECT` o `SHOW TABLES` no.

### 6.5 Hive CLI

L'altra via que apareix al document és el client tradicional:

```bash
hive
hive -f script.sql
hive -e 'SELECT * FROM iabd.categories;'
```

- `hive`: sessió interactiva.
- `-f`: executa sentències d'un fitxer.
- `-e`: executa una consulta directament des del terminal.

El temari indica que Beeline és preferible en entorns multiusuari i remots.

### 6.6 MapReduce, Tez i Spark

Hive pot fer servir diferents motors d'execució segons versió i instal·lació. El document comenta **MapReduce**, **Apache Tez** i **Spark**. Per seleccionar Tez en una instal·lació que el tingui disponible:

```sql
SET hive.execution.engine=tez;
```

A la màquina virtual docent, el PDF indica que **Tez no està instal·lat**. No és el mateix usar el motor Spark sota Hive que executar consultes en **Spark SQL**: són interfícies i motors amb integracions particulars.

## 7. Tipus de dades i conversions

### 7.1 Tipus simples

| Tipus | Contingut habitual | Exemple |
|---|---|---|
| `STRING` | Text | `'Blanes'` |
| `INT` | Enter | `42` |
| `TINYINT` | Enter petit | `1` |
| `BIGINT` | Enter de rang ampli | `9000000000` |
| `DOUBLE` | Número de coma flotant | `3.14` |
| `DATE` | Data | `'2026-02-09'` |
| `TIMESTAMP` | Data i hora | `'2026-02-09 12:30:00'` |

Una conversió explícita es fa amb **`CAST`**:

```sql
SELECT CAST('1' AS INT);
```

### 7.2 Tipus compostos

**ARRAY:** col·lecció ordenada d'elements del mateix tipus.

```sql
work_place ARRAY<STRING>
```

Exemple: `['Mont-real', 'Toronto']`.

**MAP:** col·lecció de parelles `clau:valor`.

```sql
skills_score MAP<STRING, INT>
```

Exemple: `{'Python': 80, 'SQL': 90}`.

**STRUCT:** estructura amb camps identificats pel seu nom.

```sql
sex_age STRUCT<sex:STRING, age:INT>
```

Exemple conceptual: `{'sex': 'Female', 'age': 27}`.

Els tipus es poden **niar**. Una declaració del cas pràctic és:

```sql
depart_title MAP<STRING, ARRAY<STRING>>
```

És un mapa en què cada clau de text té associat un array de textos.

## 8. Instal·lació i configuració

> **Context del PDF:** la màquina virtual del curs ja té Hive configurat; aquests passos es presenten com a referència per a una instal·lació pròpia. No copiïs rutes d'una versió diferent sense revisar-les.

### 8.1 Preparar els fitxers de configuració

Situats a `$HIVE_HOME/conf`:

```bash
cp hive-default.xml.template hive-site.xml
cp hive-env.sh.template hive-env.sh
cp hive-exec-log4j2.properties.template hive-exec-log4j2.properties
cp hive-log4j2.properties.template hive-log4j2.properties
```

Al fitxer `hive-env.sh` poden definir-se variables com:

```bash
export HADOOP_HOME=/opt/hadoop
export HIVE_CONF_DIR=$HIVE_HOME/conf
export HCAT_HOME=$HIVE_HOME/hcatalog
```

I a `~/.bashrc`, amb el directori real:

```bash
export HIVE_HOME=/opt/hive-3.1.3
export HIVE_CONF_DIR=$HIVE_HOME/conf
export HCAT_HOME=$HIVE_HOME/hcatalog
```

**Important:** `/opt/hive-3.1.3` és una ruta d'exemple que apareix al material, no una ruta universal.

### 8.2 Preparar HDFS

```bash
hdfs dfs -mkdir -p /tmp
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chmod g+w /tmp
hdfs dfs -chmod g+w /user/hive/warehouse
```

`/user/hive/warehouse` és la ubicació habitual de les taules gestionades del sistema exposat al temari.

### 8.3 Metastore sobre MySQL/MariaDB

El document usa MariaDB/MySQL per emmagatzemar metadades. La inicialització que mostra és:

```bash
schematool -dbType mysql -initSchema
```

**Atenció:** aquesta ordre és d'inicialització; no s'ha de tornar a executar sense comprovar si l'esquema ja existeix.

Exemple de les propietats JDBC incloses a `hive-site.xml`:

```xml
<property>
  <name>javax.jdo.option.ConnectionURL</name>
  <value>jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true</value>
</property>
<property>
  <name>javax.jdo.option.ConnectionDriverName</name>
  <value>com.mysql.jdbc.Driver</value>
</property>
<property>
  <name>javax.jdo.option.ConnectionUserName</name>
  <value>iabd</value>
</property>
<property>
  <name>javax.jdo.option.ConnectionPassword</name>
  <value>iabd</value>
</property>
```

El PDF també inclou les propietats `system:java.io.tmpdir`, `system:user.name` i `datanucleus.schema.autoCreateAll`. Les credencials `iabd` i els ports són **de l'entorn de pràctiques**: no s'han de reutilitzar en entorns de producció.

### 8.4 Relació amb Sqoop

En un exemple d'instal·lació, es mostra la còpia d'una biblioteca de Hive cap a Sqoop:

```bash
cp $HIVE_HOME/lib/hive-common-3.1.3.jar $SQOOP_HOME/lib
```

Aquesta ordre només té sentit si coincideixen la versió i els fitxers disponibles.

## 9. Primeres passes, clients i accés remot

### 9.1 Eines de `$HIVE_HOME/bin`

| Ordre | Finalitat |
|---|---|
| `hive` | Client tradicional i execució de scripts |
| `beeline` | Client SQL JDBC |
| `hiveserver2` | Servei que accepta connexions |
| `schematool` | Gestió de l'esquema del metastore |

### 9.2 Procediment pràctic

1. Inicia Hadoop i YARN a l'entorn docent.
2. Assegura't que el metastore requerit estigui disponible.
3. Executa `hiveserver2` en un terminal.
4. Obre una altra terminal i inicia `beeline`.
5. Connecta a `jdbc:hive2://master:10000`.
6. Prova `SHOW DATABASES;`.

### 9.3 Problemes d'impersonació

El PDF inclou la propietat següent com a possible ajust d'un entorn de pràctiques:

```xml
<property>
  <name>hive.server2.enable.doAs</name>
  <value>false</value>
</property>
```

També mostra les propietats `hadoop.proxyuser.hive.hosts` i `hadoop.proxyuser.hive.groups` amb comodí `*`. **Avís de seguretat:** el comodí amplia molt els permisos; només s'ha de considerar en un laboratori controlat. En sistemes reals cal restringir hosts i grups autoritzats.

### 9.4 Monitoratge

El material mostra la interfície web d'HiveServer2 al port **10002**:

```text
http://localhost:10002
```

Pot permetre observar sessions actives, consultes i informació del servidor, segons la versió i la configuració.

---
## 10. Cas 1 — Creació i esborrat de taules

**Objectiu:** importar dades de clients de MariaDB cap a HDFS, definir-ne l'estructura amb Hive i consultar-les. Aquest cas de les pàgines 22–29 mostra com Sqoop, HDFS i Hive poden col·laborar.

### 10.1 Importar clients amb Sqoop

La BD d'origen es diu `retail_db` i la taula d'origen, `customers`. El PDF importa només quatre columnes, separades pel caràcter `|`:

```bash
sqoop import --connect "jdbc:mysql://localhost/retail_db" \
  --username iabd --password iabd \
  --table customers --target-dir /user/iabd/hive/customer \
  --fields-terminated-by '|' --delete-target-dir \
  --columns "customer_id,customer_fname,customer_lname,customer_city"
```

**Desglossament dels paràmetres:**

| Paràmetre | Funció |
|---|---|
| `sqoop import` | Inicia una importació des d'una base de dades relacional |
| `--connect` | Cadena JDBC d'origen |
| `--username` i `--password` | Autenticació a la base de dades |
| `--table customers` | Taula d'origen |
| `--target-dir` | Carpeta HDFS on s'escriuen els resultats |
| `--fields-terminated-by '|'` | Delimitador entre camps |
| `--delete-target-dir` | Elimina prèviament la destinació si existeix |
| `--columns` | Selecciona les quatre columnes |

> `--delete-target-dir` és destructiu per a la carpeta de destinació. Cal verificar que no contingui dades que vulguem conservar.

Comprovar-ne les primeres línies:

```bash
hdfs dfs -head /user/iabd/hive/customer/part-m-00000
```

Els fitxers de sortida s'anomenen sovint `part-m-...`; el nom concret depèn de l'execució de Sqoop.

### 10.2 Crear la base de dades de Hive

Connectar-se:

```bash
beeline -u jdbc:hive2://master:10000 -n iabd -p iabd
```

Executar HiveQL:

```sql
CREATE DATABASE IF NOT EXISTS iabd;
USE iabd;
```

Si no fem `USE iabd`, les sentències no qualificades es poden executar contra la base de dades `default`, segons la sessió.

### 10.3 Definir la taula sobre els fitxers d'HDFS

```sql
CREATE TABLE customers (
  custId INT,
  fName STRING COMMENT 'Nom',
  lName STRING COMMENT 'Cognom',
  city STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
LOCATION '/user/iabd/hive/customer';
```

**Què fa cada secció?**

- `CREATE TABLE`: registra una taula al metastore de Hive.
- `custId INT`: primera columna, amb identificador enter.
- `fName`, `lName`, `city`: camps de text.
- `COMMENT`: documenta una columna.
- `ROW FORMAT DELIMITED`: assenyala que les dades estan serialitzades amb delimitadors.
- `FIELDS TERMINATED BY '|'`: indica el separador que va utilitzar Sqoop.
- `STORED AS TEXTFILE`: fitxers de text.
- `LOCATION`: indica a Hive on trobar les dades.

**Punt crític:** posar `LOCATION` no converteix la taula en externa. Si no s'ha fet servir `EXTERNAL`, continua sent una **taula gestionada**. El temari alerta que un `DROP TABLE` sobre aquesta taula pot eliminar-ne també els fitxers a HDFS.

### 10.4 Consultes inicials

```sql
SELECT * FROM customers LIMIT 5;
SELECT COUNT(*) FROM customers;
```

La primera serveix per revisar una mostra i detectar errors de delimitadors o de tipus. La segona permet comptar les files, útil per comparar la ingesta amb l'origen.

### 10.5 Duplicar taules: CTAS i LIKE

**CTAS** (*Create Table As Select*) crea una taula i la pobla amb les dades retornades:

```sql
CREATE TABLE customers_new AS
SELECT * FROM customers;
```

**LIKE** només reprodueix l'estructura de la taula:

```sql
CREATE TABLE customers2 LIKE customers;
```

| Sentència | Crea esquema | Copia dades |
|---|---|---|
| `CREATE TABLE ... AS SELECT ...` | Sí | Sí |
| `CREATE TABLE ... LIKE ...` | Sí | No |

### 10.6 Inspeccionar i esborrar

```sql
DESCRIBE customers_new;
DESCRIBE FORMATTED customers_new;
SHOW TABLES;
DROP TABLE customers_new;
DROP TABLE customers2;
```

`DESCRIBE FORMATTED` retorna informació ampliada, com el tipus de taula, el format i la ubicació física a HDFS.

El PDF mostra que una taula gestionada nova sense una `LOCATION` explícita pot situar-se a:

```text
/user/hive/warehouse/iabd.db/customers_new
```

Per suprimir una base de dades:

```sql
DROP DATABASE iabd;
-- Si hi ha taules i es volen eliminar igualment:
DROP DATABASE iabd CASCADE;
```

**Compte:** `CASCADE` pot eliminar taules i dades associades. No executar-lo per fer una simple comprovació.

## 11. Hue: interfície web

**Hue** és una interfície web que permet treballar amb SQL i altres serveis de l'ecosistema Hadoop sense dependre exclusivament del terminal. El temari presenta un desplegament amb Docker de la imatge `gethue/hue`.

### 11.1 Exemple de contenidor del document

```bash
docker stop hue
docker rm hue

docker run -d --restart unless-stopped -p 8888:8888 \
  --add-host=nom-host:IP_HOST \
  -v ~/hue-overrides.ini:/usr/share/hue/desktop/conf/z-hue-overrides.ini \
  --name hue \
  gethue/hue:latest
```

`IP_HOST` i `nom-host` són marcadors que cal substituir pels valors adequats. En Docker, el muntatge `-v` injecta el fitxer de configuració personalitzat.

**Atenció:** `docker stop` i `docker rm` fallen si el contenidor no existeix. A més, les dades persistents de l'aplicació han d'estar ben configurades perquè no es perdin en recrear-lo.

### 11.2 Configuració de Hue

Exemple extret i reformat a partir de les pàgines 25–26:

```ini
[hadoop]
  [[hdfs_clusters]]
    [[[default]]]
      webhdfs_url=http://IP_HOST:9870/webhdfs/v1
      fs_defaultfs=hdfs://IP_HOST:9000

[beeswax]
  hive_server_host=IP_HOST
  hive_server_port=10000
  server_conn_timeout=120

[desktop]
  [[database]]
    engine=mysql
    host=IP_HOST
    port=3306
    user=iabd
    password=iabd
    name=hue
```

Aquí s'han de distingir clarament tres serveis: **HDFS** (NameNode/WebHDFS), **HiveServer2** i la **base de dades pròpia de Hue**.

### 11.3 Diagnosi de Hue

```bash
docker logs --tail 30 hue
docker restart hue
```

El PDF descriu problemes associats a SQLite i proposa fer servir MariaDB. També inclou canviar el `bind-address` de MariaDB a `0.0.0.0` i crear l'usuari i la base `hue`. En un laboratori es pot estudiar aquesta configuració, però en producció cal limitar l'exposició de MariaDB i els privilegis dels usuaris.

## 12. Cas 2 — Càrrega i inserció de dades

El segon cas explica les tres vies principals: `LOAD DATA`, `INSERT` i ingesta amb eines externes com Sqoop.

### 12.1 LOAD DATA: dades des d'HDFS

```sql
LOAD DATA INPATH '/user/iabd/hive/customer'
OVERWRITE INTO TABLE customers2;
```

El PDF subratlla que, en el seu exemple, les dades són **mogudes** des de la ruta d'origen cap a la ubicació de la taula. Això vol dir que la carpeta de partida pot deixar de tenir les dades esperades. `OVERWRITE` substitueix el contingut de destinació.

**Regla d'estudi:** no tractis `LOAD DATA INPATH` com una lectura passiva equivalent a `SELECT`: pot canviar la ubicació dels fitxers.

### 12.2 LOAD DATA LOCAL: dades del sistema Linux

```sql
LOAD DATA LOCAL INPATH '/home/iabd/dadess.csv'
OVERWRITE INTO TABLE customers2;
```

`LOCAL` diferencia la procedència del fitxer: és una ruta del sistema de fitxers local (segons el context del client/servidor), no una ruta HDFS. Verifica que el fitxer existeix i que el format coincideix amb el declarat a la taula.

### 12.3 INSERT INTO i INSERT OVERWRITE

```sql
INSERT INTO desti
SELECT col1, col2 FROM font;

INSERT OVERWRITE TABLE desti
SELECT col1, col2 FROM font;
```

**Diferència:**

- `INSERT INTO`: afegeix files a les que hi ha.
- `INSERT OVERWRITE`: substitueix el contingut de la destinació afectada.

Exemple de còpia de dades transformant el format a **Parquet**:

```sql
CREATE TABLE customersp (
  custId INT,
  fName STRING,
  lName STRING,
  city STRING
)
STORED AS PARQUET;

INSERT INTO customersp
SELECT * FROM customers;
```

**Per què Parquet?** És un format orientat a columnes que pot resultar especialment útil en consultes analítiques que seleccionen només algunes columnes. El document proposa comparar el temps de recompte entre la taula de text i la Parquet.

```sql
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM customersp;
```

La consulta més ràpida depèn del volum, format, motor, estadístiques i entorn: no s'ha de donar un guany garantit sense mesurar-lo.

### 12.4 Insercions múltiples en una sola lectura

Hive permet reutilitzar una mateixa font per escriure simultàniament a més d'una taula:

```sql
CREATE TABLE customers_brooklyn LIKE customers;
CREATE TABLE customers_caguas LIKE customers;

FROM customers
INSERT OVERWRITE TABLE customers_brooklyn
  SELECT custId, fName, lName, city
  WHERE city = 'Brooklyn'
INSERT OVERWRITE TABLE customers_caguas
  SELECT custId, fName, lName, city
  WHERE city = 'Caguas';
```

Aquest patró es coneix com a **multi-table insert**. Evita haver de formular necessàriament dues lectures separades de tota la font i és útil en transformacions ETL.

### 12.5 Còpia versus moviment

| Operació | Intenció | Precaució |
|---|---|---|
| `LOAD DATA INPATH` | Carregar fitxers HDFS a la taula | Pot moure els fitxers d'origen |
| `LOAD DATA LOCAL INPATH` | Carregar un fitxer local | Revisar context i ruta local |
| `INSERT INTO ... SELECT` | Escriure resultats d'una consulta | Afegeix files |
| `INSERT OVERWRITE ... SELECT` | Reemplaçar resultats a destí | Destrueix el contingut substituït |
| `CREATE TABLE AS SELECT` | Crear taula a partir del resultat | Crea esquema i dades |

## 13. Actualització i esborrat transaccional

Per defecte, en el context docent, Hive s'utilitza sobretot per a lectures i insercions massives. El document dedica les pàgines 33–35 a les condicions per aplicar `UPDATE` i `DELETE`.

### 13.1 Per què és diferent d'una BD OLTP?

HDFS no està pensat per actualitzar fitxers aleatòriament registre a registre. El temari explica que Hive pot enregistrar modificacions en **fitxers delta**, i que una compactació posterior els integra amb els fitxers de base.

```text
Fitxers base + fitxers delta
             |
       compactació
             |
      estat consolidat
```

### 13.2 Configuració transaccional de l'exemple

Sentències que s'indiquen a Beeline/Hue:

```sql
SET hive.support.concurrency=true;
SET hive.enforce.bucketing=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;
```

I propietats de `hive-site.xml` documentades en el temari:

```xml
<property>
  <name>hive.support.concurrency</name>
  <value>true</value>
</property>
<property>
  <name>hive.txn.manager</name>
  <value>org.apache.hadoop.hive.ql.lockmgr.DbTxnManager</value>
</property>
<property>
  <name>hive.compactor.initiator.on</name>
  <value>true</value>
</property>
<property>
  <name>hive.compactor.worker.threads</name>
  <value>1</value>
</property>
```

El document recomana reiniciar els serveis després dels canvis. **Aquests requisits són els de l'exemple/versió docent:** les capacitats ACID han evolucionat entre versions de Hive i no s'han de generalitzar sense revisar la instal·lació.

### 13.3 Crear una taula transaccional

```sql
CREATE TABLE customerstx (
  custId INT,
  fName STRING,
  lName STRING,
  city STRING
)
CLUSTERED BY (custId) INTO 4 BUCKETS
STORED AS ORC
TBLPROPERTIES ('transactional' = 'true');
```

A la configuració del document s'utilitzen **ORC**, **bucketing** i la propietat `transactional`.

Carregar les dades:

```sql
INSERT INTO customerstx
SELECT * FROM customers;
```

Canviar una ciutat:

```sql
UPDATE customerstx
SET city = 'Blanes'
WHERE city = 'Caguas';
```

**Conceptes de repàs:** ACID, transacció, compactació, fitxer delta, bucketing, ORC i `TBLPROPERTIES`.

## 14. Ingesta des de Sqoop i exportació

### 14.1 Crear i carregar una taula de Hive amb Sqoop

El temari importa la taula `orders` de `retail_db` directament cap a Hive:

```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
  --username=iabd --password=iabd \
  --table=orders --driver=com.mysql.jdbc.Driver \
  --hive-import --hive-database iabd \
  --create-hive-table --hive-table orders
```

| Paràmetre | Significat |
|---|---|
| `--hive-import` | Indica destinació a Hive |
| `--hive-database iabd` | Base de dades Hive |
| `--create-hive-table` | Demana crear la taula |
| `--hive-table orders` | Nom de la taula destinació |

Comprovar el resultat:

```bash
hdfs dfs -ls /user/hive/warehouse/iabd.db/orders
```

```sql
SELECT * FROM orders LIMIT 10;
```

### 14.2 Exportar el resultat a fitxers locals

Afegir la sortida a un fitxer:

```bash
hive -e "use iabd; select * from customers;" >> prova1
```

Sobreescriure el fitxer:

```bash
hive -e "use iabd; select * from customers;" > prova2
```

| Operador de shell | Efecte |
|---|---|
| `>` | Substitueix el contingut |
| `>>` | Afegeix al final |
| `|` | Envia la sortida d'una ordre com a entrada d'una altra |

### 14.3 Enviar la sortida a HDFS per canonada

Afegir a un fitxer HDFS:

```bash
hive -e "use iabd; select * from customers;" | hdfs dfs -appendToFile - /tmp/prova3
```

Sobreescriure un fitxer HDFS:

```bash
hive -e "use iabd; select * from customers;" | hdfs dfs -put -f - /tmp/prova4
```

El **guió `-`** indica que el contingut s'ha de llegir de l'entrada estàndard, és a dir, de la canonada (*pipe*), no d'un fitxer local amb aquell nom.

### 14.4 Generar un CSV amb capçalera

```bash
hive -e 'use iabd; set hive.cli.print.header=true; select * from customers;' \
  | sed 's/[\t]/,/g' > fitxer.csv
```

La configuració `hive.cli.print.header=true` demana incloure noms de columnes. `sed` substitueix tabuladors per comes. **Limitació:** és un CSV simple; si els camps contenen comes, cometes o salts de línia cal una serialització CSV correcta.

### 14.5 INSERT OVERWRITE LOCAL DIRECTORY

També es pot exportar mitjançant HiveQL:

```sql
INSERT OVERWRITE LOCAL DIRECTORY '/home/iabd/dades_de_hive/prova_local_dir'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT * FROM customers;
```

El document alerta de dues particularitats: la instrucció **sobreescriu** el contingut de destí i pot produir **diversos fitxers**, que caldrà combinar si volem un sol fitxer final.

---
## 15. Cas 3 — JOINs

Les pàgines 38–40 relacionen dues taules del cas pràctic:

- `customers`, amb la clau de client `custId`.
- `orders`, amb la clau forana `order_customer_id`.

La relació és **un client pot tenir moltes comandes**. Enllaçar taules permet recuperar atributs d'una entitat a partir dels registres de l'altra.

### 15.1 INNER JOIN

Volem conèixer, per a cada comanda, la data i la ciutat del client:

```sql
SELECT o.order_id, o.order_date, c.city
FROM orders o
JOIN customers c
  ON o.order_customer_id = c.custId;
```

- `o` i `c` són àlies, útils per identificar camps sense repetir el nom complet.
- `ON` defineix la condició d'unió.
- Un `INNER JOIN` només retorna files amb coincidència entre les dues taules.

### 15.2 Comptar comandes per client

```sql
SELECT c.custId, COUNT(o.order_id) AS total_comandes
FROM customers c
JOIN orders o
  ON c.custId = o.order_customer_id
GROUP BY c.custId
ORDER BY COUNT(o.order_id) DESC;
```

`GROUP BY` reuneix registres amb el mateix `custId`; `COUNT(o.order_id)` compta els identificadors de comanda no nuls; `ORDER BY ... DESC` ordena de més a menys comandes.

Amb `INNER JOIN`, els clients sense comandes no surten.

### 15.3 LEFT OUTER JOIN

Per mostrar **tots** els clients, també els que no tenen comandes:

```sql
SELECT c.custId, COUNT(o.order_id) AS total_comandes
FROM customers c
LEFT OUTER JOIN orders o
  ON c.custId = o.order_customer_id
GROUP BY c.custId
ORDER BY COUNT(o.order_id) DESC;
```

Els clients sense coincidència conserven la fila del costat esquerre, però les columnes d'`orders` queden a `NULL`. En comptar `o.order_id`, aquests clients produeixen **zero**.

**Detall d'examen:** `COUNT(*)` i `COUNT(o.order_id)` no són equivalents amb un `LEFT JOIN`: el primer pot comptar la fila preservada encara que no hi hagi cap comanda.

### 15.4 RIGHT i FULL OUTER JOIN

- `RIGHT OUTER JOIN`: conserva totes les files de la taula de la dreta.
- `FULL OUTER JOIN`: conserva totes les files d'ambdues taules, fins i tot les que no tenen coincidència.

| Tipus | Files retornades |
|---|---|
| `INNER JOIN` | Només coincidències |
| `LEFT JOIN` | Totes les esquerres i coincidències de la dreta |
| `RIGHT JOIN` | Totes les dretes i coincidències de l'esquerra |
| `FULL JOIN` | Totes dues taules amb o sense coincidència |

### 15.5 LEFT SEMI JOIN

Problema del temari: obtenir les ciutats dels clients que han fet alguna comanda. Opció amb subconsulta:

```sql
SELECT DISTINCT c.city
FROM customers c
WHERE c.custId IN (
  SELECT order_customer_id FROM orders
);
```

Opció amb `LEFT SEMI JOIN`:

```sql
SELECT DISTINCT c.city
FROM customers c
LEFT SEMI JOIN orders o
  ON c.custId = o.order_customer_id;
```

El **semi-join** comprova que existeix alguna coincidència, però no incorpora els camps del costat dret al resultat. Al `SELECT` d'un `LEFT SEMI JOIN`, el temari indica que només s'han de projectar columnes de la taula esquerra; les columnes de la dreta apareixen a la condició `ON`.

### 15.6 Map Join

Quan una de les taules és prou petita per cabre a memòria, es pot carregar al costat dels processadors i evitar part del cost de redistribució de dades. Aquest patró s'anomena **map join**.

El document també mostra l'optimització de map joins amb taules organitzades en *buckets*:

```sql
SET hive.optimize.bucketmapjoin=true;
```

**Idea:** evitar un *shuffle* costós pot accelerar unions adequades. La conveniència depèn de la mida de les taules i del motor. El material adverteix de limitacions per a determinats outer joins en el tipus de map join que explica.

### 15.7 Exercicis d'interpretació

- Si vols **només clients amb comandes**, pots usar `INNER JOIN` o `LEFT SEMI JOIN`, segons les columnes que necessitis.
- Si vols **clients sense comandes**, un patró és `LEFT JOIN` i filtrar quan l'ID de comanda sigui `NULL`.
- Si vols **ciutat de cada comanda**, necessites columns de les dues taules: `JOIN` convencional.
- Si només vols saber **si existeix alguna comanda**, considera `LEFT SEMI JOIN`.

## 16. Comandes i funcions útils

Aquesta secció complementa l'apartat *Comandes* de la pàgina 41 amb una referència pràctica de les instruccions que apareixen a la unitat.

### 16.1 Bases de dades

```sql
SHOW DATABASES;
CREATE DATABASE IF NOT EXISTS iabd;
USE iabd;
DROP DATABASE iabd;
DROP DATABASE iabd CASCADE;
```

### 16.2 Taules

```sql
SHOW TABLES;
DESCRIBE customers;
DESCRIBE FORMATTED customers;
SHOW CREATE TABLE customers;
DROP TABLE customers;
```

### 16.3 Consultes bàsiques

```sql
SELECT * FROM customers LIMIT 10;
SELECT city FROM customers WHERE city = 'Brooklyn';
SELECT DISTINCT city FROM customers;
SELECT COUNT(*) FROM customers;
SELECT city, COUNT(*) FROM customers GROUP BY city;
```

### 16.4 Descobrir funcions de Hive

```sql
SHOW FUNCTIONS;
DESCRIBE FUNCTION length;
```

El PDF fa servir `length` com a exemple d'una funció que retorna la longitud d'una cadena o el nombre de bytes d'un valor binari. Hive inclou funcions per a cadenes, dates, valors condicionals, agregació i altres operacions.

### 16.5 Ordres de terminal vs HiveQL

| Context | Exemple | Serveix per a... |
|---|---|---|
| Linux | `hdfs dfs -ls /ruta` | Llistar HDFS |
| Linux | `sqoop import ...` | Importar dades |
| Linux | `beeline -u ...` | Connectar amb HiveServer2 |
| HiveQL | `SELECT ...;` | Consultar dades |
| HiveQL | `CREATE TABLE ...;` | Definir taules |
| Beeline | `!connect ...` | Obrir connexió JDBC |

**Error habitual:** executar una instrucció de Linux dins de HiveQL, o escriure `!connect` al shell quan ja s'hauria d'estar dins de Beeline.

## 17. Cas 4 — Taules internes i dades complexes

### 17.1 Què és una taula interna?

Una **taula interna o gestionada** (`MANAGED_TABLE`) és una taula sobre la qual Hive administra metadades i dades. Al sistema del temari, si no es defineix cap ubicació específica, acostuma a crear-se a `/user/hive/warehouse`. **En eliminar-la, també s'eliminen les dades gestionades.**

Una **taula externa** té una semàntica diferent i es treballa al cas 5.

### 17.2 Fitxer d'exemple `empleats.txt`

A la pàgina 42, el material parteix d'aquestes dades:

```text
Michael|Mont-real,Toronto|Male,30|DB:80|Product:DeveloperLead
Will|Mont-real|Male,35|Perl:85|Product:Lead,Test:Lead
Shelley|New York|Female,27|Python:80|Test:Lead,COE:Architect
Lucy|Vancouver|Female,57|Sales:89,HR:94|Sales:Lead
```

Cada línia representa un empleat. El primer separador principal és `|`; dins de cada camp hi pot haver informació composta amb `,` i `:`.

**Interpretació d'una fila:**

```text
Michael | Mont-real,Toronto | Male,30 | DB:80 | Product:DeveloperLead
   nom  | ciutats treball    | sexe/edat | habilitat | departament/càrrec
```

### 17.3 Definició de la taula interna

```sql
CREATE TABLE IF NOT EXISTS empleats_interna (
  name STRING,
  work_place ARRAY<STRING>,
  sex_age STRUCT<sex:STRING,age:INT>,
  skills_score MAP<STRING,INT>,
  depart_title MAP<STRING,ARRAY<STRING>>
)
COMMENT 'Això és una taula interna'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':';
```

**Explicació detallada:**

- `name`: camp de text simple.
- `work_place`: pot contenir diverses ciutats de treball.
- `sex_age`: agrupa dos atributs amb nom (`sex` i `age`).
- `skills_score`: cada habilitat és una clau associada a una puntuació entera.
- `depart_title`: cada departament és una clau associada a una col·lecció de càrrecs.
- `FIELDS TERMINATED BY '|'`: delimita les columnes principals.
- `COLLECTION ITEMS TERMINATED BY ','`: separa elements de col·leccions i estructures serialitzades.
- `MAP KEYS TERMINATED BY ':'`: separa claus i valors de mapes.

**Detall per estudiar:** una coma entre dos elements d'un `ARRAY` no significa que hi hagi una nova columna; és un delimitador **intern** d'aquell camp.

### 17.4 Formats de taula

El document diferencia formats més orientats a registres o files (`TEXTFILE`, `SEQUENCEFILE`, Avro i JSON en el seu esquema introductori) i formats columnars (`PARQUET`, `ORC`). Les disponibilitats concretes depenen de la versió de Hive i dels components configurats.

```sql
CREATE TABLE dades_exemple (id INT, nom STRING)
STORED AS PARQUET;
```

**Format de files:** útil en diferents fluxos d'ingesta i fitxers de text. **Format columnar:** útil per a consultes analítiques que llegeixen o agreguen un conjunt limitat de columnes.

### 17.5 Carregar el fitxer local

```sql
LOAD DATA LOCAL INPATH '/home/iabd/Downloads/empleats.txt'
OVERWRITE INTO TABLE empleats_interna;
```

Comprovar des de Hive:

```sql
SELECT * FROM empleats_interna;
SHOW CREATE TABLE empleats_interna;
```

Comprovar el fitxer a HDFS:

```bash
hdfs dfs -ls /user/hive/warehouse/iabd.db/empleats_interna
hdfs dfs -cat /user/hive/warehouse/iabd.db/empleats_interna/empleats.txt
```

**Recordatori:** els exemples assumeixen que s'ha seleccionat la base de dades `iabd` i que l'arxiu és accessible des de l'entorn on es fa la càrrega.

## 18. Consultes amb ARRAY, STRUCT i MAP

Aquest és un dels apartats més importants per a l'examen, perquè Hive permet consultar dades aniuades sense haver de convertir tots els camps en columnes simples. El temari els desenvolupa entre les pàgines 46 i 50.

### 18.1 Consultar arrays sencers

```sql
SELECT name, work_place
FROM empleats_interna;
```

Resultat conceptual:

```text
Michael | ["Mont-real", "Toronto"]
Will    | ["Mont-real"]
Shelley | ["New York"]
Lucy    | ["Vancouver"]
```

### 18.2 Accedir a posicions d'un array

```sql
SELECT work_place[0] AS lloc1,
       work_place[1] AS lloc2
FROM empleats_interna;
```

Els índexs d'un `ARRAY` comencen a **0**. Per tant, `[0]` és el primer element i `[1]` el segon. Si una fila no té segon element, el resultat és `NULL`.

### 18.3 Comptar elements d'un array

```sql
SELECT name, SIZE(work_place) AS cantLlocs
FROM empleats_interna;
```

`SIZE()` retorna el nombre d'elements de la col·lecció, no la llargada en caràcters del text.

### 18.4 Convertir un array en múltiples files (EXPLODE)

```sql
SELECT name, lloc
FROM empleats_interna
LATERAL VIEW EXPLODE(work_place) e2 AS lloc;
```

`EXPLODE` transforma els elements d'una col·lecció en files; `LATERAL VIEW` permet conservar columnes de la fila original, com `name`.

```text
Abans:                         Després:
Michael | [Mont-real,Toronto]   Michael | Mont-real
                               Michael | Toronto
Will    | [Mont-real]           Will    | Mont-real
```

**És una operació de canvi de granularitat:** es passa d'una fila amb diversos elements a diverses files amb un sol element cadascuna.

### 18.5 Consultar estructures (STRUCT)

Mostrar la columna completa:

```sql
SELECT sex_age FROM empleats_interna;
```

Extreure atributs amb el punt `.`:

```sql
SELECT sex_age.sex AS sexe,
       sex_age.age AS edat
FROM empleats_interna;
```

La **notació de punt** serveix per recuperar un camp amb nom d'una `STRUCT`. No és el mateix que accedir a un array per posició.

### 18.6 Consultar mapes (MAP)

Mostrar tots els mapes d'habilitats:

```sql
SELECT skills_score
FROM empleats_interna;
```

Recuperar valors per clau:

```sql
SELECT name,
       skills_score['DB'] AS db,
       skills_score['Perl'] AS perl,
       skills_score['Python'] AS python,
       skills_score['Sales'] AS vendes,
       skills_score['HR'] AS hr
FROM empleats_interna;
```

`skills_score['DB']` retorna el valor associat a la clau `DB`. Si l'empleat no té aquesta habilitat, el valor acostuma a ser `NULL`.

### 18.7 Obtenir les claus i els valors

```sql
SELECT name,
       MAP_KEYS(skills_score) AS claus,
       MAP_VALUES(skills_score) AS valors
FROM empleats_interna;
```

- `MAP_KEYS()`: retorna les claus del mapa.
- `MAP_VALUES()`: retorna els valors del mapa.

No assumis un ordre estable de presentació de les entrades d'un mapa si la consulta no n'estableix un.

### 18.8 Mapes que contenen arrays

El camp `depart_title` té el tipus `MAP<STRING, ARRAY<STRING>>`.

Consultar tot el mapa:

```sql
SELECT depart_title
FROM empleats_interna;
```

Consultar determinats departaments:

```sql
SELECT name,
       depart_title['Product'] AS product,
       depart_title['Test'] AS test,
       depart_title['COE'] AS coe,
       depart_title['Sales'] AS sales
FROM empleats_interna;
```

Com que el valor de cada clau és un array, encara podem accedir als elements individuals:

```sql
SELECT name,
       depart_title['Product'][0] AS product0,
       depart_title['Test'][0] AS test0
FROM empleats_interna;
```

**Regla molt important:** `['Product']` selecciona una clau del **MAP**; `[0]` selecciona la primera posició de l'**ARRAY** retornat per aquella clau.

### 18.9 Comparativa de sintaxi de dades compostes

| Objectiu | Sintaxi | Exemple |
|---|---|---|
| Primer element d'un ARRAY | `array[0]` | `work_place[0]` |
| Atribut d'una STRUCT | `struct.camp` | `sex_age.age` |
| Valor associat a una clau MAP | `map['clau']` | `skills_score['HR']` |
| Nombre d'elements | `SIZE(array)` | `SIZE(work_place)` |
| Claus del mapa | `MAP_KEYS(map)` | `MAP_KEYS(skills_score)` |
| Valors del mapa | `MAP_VALUES(map)` | `MAP_VALUES(skills_score)` |
| Desplegar elements | `LATERAL VIEW EXPLODE(...)` | `EXPLODE(work_place)` |
| Array dins de MAP | `map['clau'][0]` | `depart_title['Test'][0]` |

### 18.10 Exercicis resolts

**Exercici A: mostrar empleats amb més d'un centre de treball.**

```sql
SELECT name, work_place
FROM empleats_interna
WHERE SIZE(work_place) > 1;
```

**Exercici B: mostrar nom i edat dels empleats de més de 30 anys.**

```sql
SELECT name, sex_age.age AS edat
FROM empleats_interna
WHERE sex_age.age > 30;
```

**Exercici C: mostrar nom i puntuació en Python.**

```sql
SELECT name, skills_score['Python'] AS puntuacio_python
FROM empleats_interna;
```

**Exercici D: obtenir una fila per centre de treball.**

```sql
SELECT name, ciutat
FROM empleats_interna
LATERAL VIEW EXPLODE(work_place) x AS ciutat;
```

Aquests quatre exercicis són **ampliacions d'estudi elaborades a partir de l'estructura de l'exemple**, no exercicis textuals addicionals del PDF.

## 19. Cas 5 — Taules externes

El darrer cas pràctic, a les pàgines 50–51, repeteix la taula d'empleats però la defineix com a **externa**.

### 19.1 Sintaxi

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS empleats_externa (
  name STRING,
  work_place ARRAY<STRING>,
  sex_age STRUCT<sex:STRING,age:INT>,
  skills_score MAP<STRING,INT>,
  depart_title MAP<STRING,ARRAY<STRING>>
)
COMMENT 'Això és una taula externa'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
LOCATION '/user/iabd/hive/empleats_externa';
```

Les dues diferències clau respecte a la taula interna del cas anterior són:

1. La paraula **`EXTERNAL`** a `CREATE TABLE`.
2. La ruta física declarada explícitament amb **`LOCATION`**.

La propietat `EXTERNAL` és la que determina que Hive tracti la taula com a externa; posar `LOCATION` per si sola no n'és suficient.

### 19.2 Carregar i consultar

```sql
LOAD DATA LOCAL INPATH '/home/iabd/Downloads/empleats.txt'
OVERWRITE INTO TABLE empleats_externa;

SELECT * FROM empleats_externa;
```

### 19.3 Què passa amb DROP TABLE?

| Acció | Taula interna | Taula externa (com al temari) |
|---|---|---|
| Crear taula | Registra esquema | Registra esquema |
| `SELECT` | Consulta fitxers | Consulta fitxers |
| `DROP TABLE` | Esborra metadades i dades gestionades | Esborra metadades i conserva els fitxers |
| Compartir dades amb altres eines | Més delicat | Cas d'ús habitual |

**Matís:** aquesta és la semàntica habitual que exposa el PDF. Versions modernes poden incloure propietats avançades que modifiquen determinades operacions d'eliminació; comprova sempre les propietats abans d'operar amb dades reals.

### 19.4 Patró habitual de treball

```text
Procés extern (Sqoop / Flume / altre)
                  |
            Fitxers a HDFS
                  |
          Taula externa Hive
                  |
        SELECT / transformació
                  |
        Taula interna optimitzada
                  |
           Analítica posterior
```

El document recomana **taules internes** quan tot el cicle de tractament es fa a Hive, i **taules externes** quan el mateix dataset és utilitzat per diverses eines.

## 20. Hive, MapReduce i Fetch Task

### 20.1 No totes les consultes requereixen un treball distribuït

Les pàgines 51–52 expliquen que, en el context de la instal·lació utilitzada, consultes simples de projecció poden aprofitar l'optimització **Fetch Task**.

Exemples:

```sql
SELECT name FROM empleats_interna;
SELECT sex_age.age FROM empleats_interna;
SELECT skills_score['Python'] FROM empleats_interna;
```

Aquestes consultes, si es poden resoldre amb Fetch Task, llegeixen dades directament i retornen el resultat sense llançar una tasca MapReduce. També es pot aplicar a expressions com `LATERAL VIEW EXPLODE` quan no calen operacions de redistribució.

### 20.2 Quan poden caldre tasques d'execució distribuïda?

Operacions com agrupacions, agregacions, unions o ordenacions poden requerir un motor d'execució i redistribució de dades:

```sql
SELECT city, COUNT(*)
FROM customers
GROUP BY city;
```

**Important:** el motor i l'estratègia reals depenen de la configuració i de l'optimitzador. No totes les versions executen les mateixes consultes exactament igual.

### 20.3 Desactivar Fetch Task per observar-ne l'efecte

```sql
SET hive.fetch.task.conversion=none;
```

Aquesta configuració apareix al PDF com una manera de desactivar l'optimització per comparar el comportament. És especialment útil en una pràctica de diagnosi o rendiment.

### 20.4 Idea per memoritzar

- **Fetch Task:** lectura directa, quan el pla ho permet.
- **MapReduce / motor distribuït:** execució de treballs distribuïts per a operacions que ho necessiten.
- **YARN:** gestió de recursos en l'ecosistema Hadoop quan s'hi executen tasques.

## 21. Errors habituals i diagnòstic

### 21.1 Beeline no pot connectar

**Símptoma:** error de connexió a `jdbc:hive2://master:10000`.

**Comprovacions:**

1. Està en marxa `hiveserver2`?
2. El nom `master` resol a la màquina correcta?
3. El port `10000` és accessible?
4. Si hi ha metastore remot, està executant-se?
5. La configuració d'usuari i permisos és correcta?

### 21.2 La consulta mostra NULL o columnes mal alineades

**Possible causa:** els delimitadors del fitxer no coincideixen amb el `ROW FORMAT` o el tipus de dada no encaixa.

Comprovar dades i esquema:

```bash
hdfs dfs -head /user/iabd/hive/customer/part-m-00000
```

```sql
DESCRIBE FORMATTED customers;
SELECT * FROM customers LIMIT 5;
```

### 21.3 DROP TABLE ha esborrat fitxers

**Causa típica:** es tractava d'una taula `MANAGED`, encara que tenia una `LOCATION` fora del directori warehouse. Abans d'eliminar una taula:

```sql
DESCRIBE FORMATTED customers;
```

Busca el tipus de taula i la ubicació física.

### 21.4 LOAD DATA ha buidat la carpeta original

`LOAD DATA INPATH` pot moure els fitxers d'origen. Si el flux ha de conservar l'original, planifica una còpia o una transformació amb `INSERT ... SELECT`, segons el cas.

### 21.5 Hue no funciona

```bash
docker ps -a
docker logs --tail 30 hue
```

Comprovar connexions a HiveServer2, WebHDFS i la BD de Hue. El document inclou un apartat sobre bloquejos de SQLite i configuració de MariaDB.

### 21.6 Hive tarda massa

Considera si la consulta ha iniciat un treball distribuït i si hi ha sobrecàrrega de YARN/MapReduce. Revisa el format de dades, la mida del dataset i la possibilitat d'aplicar Fetch Task. Comparar TEXTFILE amb PARQUET/ORC pot ser útil per a algunes consultes, però cal mesurar.

### 21.7 Taula externa no preserva el que esperaves

Verifica que la instrucció sigui **`CREATE EXTERNAL TABLE`** i no simplement `CREATE TABLE ... LOCATION`. Comprova també que no estàs executant ordres d'esborrat directament sobre HDFS.

### 21.8 Errors de permisos

Les rutes HDFS i locals tenen permisos diferents. Ser capaç de consultar `SHOW TABLES` no implica necessàriament poder escriure a `/user/hive/warehouse`, llegir un fitxer local o accedir a la base de dades del metastore.

## 22. Resums i taules comparatives

### 22.1 Ports a memoritzar en els exemples

| Port | Servei / ús de laboratori |
|---|---|
| `10000` | HiveServer2, connexions JDBC/Beeline |
| `9083` | Hive Metastore remot, Thrift |
| `10002` | Interfície de monitoratge de HiveServer2 mostrada al PDF |
| `9870` | Interfície HTTP de HDFS / WebHDFS a Hadoop 3 |
| `9000` | Endpoint HDFS configurat a l'entorn docent |
| `8888` | Hue, servidor web del contenidor |
| `3306` | MariaDB/MySQL |

Aquests ports són els **de la configuració del material**, no una garantia per a qualsevol desplegament.

### 22.2 Taules internes i externes

| Característica | Interna / gestionada | Externa |
|---|---|---|
| Definició | `CREATE TABLE` | `CREATE EXTERNAL TABLE` |
| Directori per defecte | Warehouse de Hive | Ubicació pròpia, habitualment amb `LOCATION` |
| Hive gestiona les metadades | Sí | Sí |
| Esborrar fitxers amb `DROP TABLE` | Sí, segons el model del temari | No, model del temari |
| Dades compartides | Menys indicada | Recomanada |

### 22.3 Operacions amb dades

| Comanda | Ús principal |
|---|---|
| `LOAD DATA INPATH` | Carregar fitxers d'HDFS |
| `LOAD DATA LOCAL INPATH` | Carregar fitxers locals |
| `INSERT INTO` | Afegir files |
| `INSERT OVERWRITE` | Substituir dades de destinació |
| `CREATE TABLE ... LIKE` | Copiar estructura |
| `CREATE TABLE ... AS SELECT` | Crear i poblar taula |
| `UPDATE` | Modificar files quan les taules/configuracions ho admeten |
| `DROP TABLE` | Eliminar definició i, si és gestionada, dades associades |

### 22.4 Comandes d'inspecció que més convé dominar

```sql
SHOW DATABASES;
SHOW TABLES;
DESCRIBE nom_taula;
DESCRIBE FORMATTED nom_taula;
SHOW CREATE TABLE nom_taula;
SHOW FUNCTIONS;
DESCRIBE FUNCTION length;
```

## 23. Preguntes de repàs amb respostes

Aquest bloc és material didàctic complementari per autoavaluar-te. Les respostes parteixen de les explicacions i pràctiques dels apunts.

### Fonaments

**1. Què és Apache Hive?**  
Una eina de consulta i gestió de grans datasets, habitualment a HDFS, mitjançant HiveQL.

**2. Per què es va crear Hive?**  
Per facilitar a usuaris amb coneixements SQL l'explotació de dades sobre Hadoop sense programar tots els processos en MapReduce.

**3. Hive substitueix HDFS?**  
No. Hive defineix una capa lògica i consulta dades; HDFS les pot emmagatzemar físicament.

**4. Què és HiveQL?**  
Un dialecte similar a SQL utilitzat per definir i consultar dades a Hive.

**5. Quina mena de càrrega és especialment adequada per a Hive?**  
Anàlisi massiva, ETL i càrregues de tipus data warehouse/batch.

**6. Quin inconvenient té en consultes petites amb execució distribuïda?**  
El temps d'inicialització i la latència del treball poden dominar el temps total.

**7. Quina alternativa destaca el document per a consultes interactives?**  
Apache Impala.

**8. Quina diferència hi ha entre Spark SQL i Hive sobre un motor Spark?**  
Spark SQL és una interfície/motor de Spark; Hive pot configurar Spark com a backend d'execució de consultes Hive.

### Arquitectura

**9. Quina funció fa HiveServer2?**  
Rep consultes de clients com Beeline i permet connexions concurrents.

**10. Què és el Metastore?**  
El repositori de metadades de Hive: taules, esquemes, columnes, formats i localitzacions.

**11. On s'emmagatzemen habitualment les dades de les taules analítiques del temari?**  
A HDFS.

**12. En quina base de dades pot viure el metastore?**  
Entre altres, Derby o MySQL/MariaDB.

**13. Quin port fa servir HiveServer2 als exemples?**  
El `10000`.

**14. I el metastore remot?**  
El `9083`.

**15. Com es configura l'URI d'un metastore remot?**  
Amb `hive.metastore.uris`, com `thrift://master:9083`.

**16. Quina ordre arrenca HiveServer2?**  
`hiveserver2`.

**17. Quina ordre obre el client tradicional?**  
`hive`.

**18. Quina ordre permet executar un script SQL amb Hive CLI?**  
`hive -f script.sql`.

**19. Quina ordre mostra les bases de dades?**  
`SHOW DATABASES;`.

**20. Quina diferència hi ha entre Beeline i Hive CLI?**  
Beeline és el client JDBC orientat a HiveServer2; Hive CLI és el client tradicional.

### Definició i emmagatzematge

**21. Què fa `CREATE DATABASE IF NOT EXISTS`?**  
Crea una base de dades si encara no existeix.

**22. Què passa si oblidem `USE iabd`?**  
Les ordres no qualificades poden operar sobre la base de dades actual, sovint `default`.

**23. Per a què serveix `LOCATION`?**  
Per especificar la ubicació física de les dades associades a la taula.

**24. `LOCATION` converteix una taula en externa?**  
No; cal declarar-la explícitament amb `EXTERNAL`.

**25. Què fa `FIELDS TERMINATED BY '|'`?**  
Defineix el caràcter `|` com a separador de columnes de les dades.

**26. Quina és la diferència entre `TEXTFILE` i `PARQUET`?**  
El primer és una representació de text i el segon és un format columnar orientat a anàlisi.

**27. Què fa `DESCRIBE FORMATTED`?**  
Mostra informació detallada d'una taula, incloent-ne propietats i ubicació.

**28. Quina diferència hi ha entre CTAS i LIKE?**  
CTAS crea la taula a partir d'una consulta amb dades; LIKE copia l'estructura sense files.

**29. Què passa en fer `DROP TABLE` sobre una taula interna segons el temari?**  
S'eliminen les metadades i també les dades gestionades.

**30. I sobre una taula externa?**  
S'eliminen les metadades de Hive però es conserven els fitxers d'HDFS.

### Càrrega i transformacions

**31. Per a què serveix `LOAD DATA`?**  
Per carregar fitxers a una taula de Hive.

**32. Quina diferència aporta `LOCAL`?**  
Indica que el fitxer de procedència és del sistema de fitxers local.

**33. Què pot passar amb els fitxers d'origen quan fem `LOAD DATA INPATH`?**  
Poden ser moguts a la ubicació de la taula.

**34. Què fa `INSERT INTO`?**  
Afegeix noves files.

**35. Què fa `INSERT OVERWRITE`?**  
Substitueix dades de la destinació afectada.

**36. Quin avantatge té un multi-table insert?**  
Pot alimentar diverses taules a partir d'una única lectura de la font.

**37. Quines opcions Sqoop fan que importi a Hive?**  
Entre altres, `--hive-import`, `--hive-database` i `--hive-table`.

**38. Quina diferència hi ha entre `>` i `>>` en Linux?**  
`>` sobreescriu; `>>` afegeix.

**39. Què significa `-` després de `hdfs dfs -put -f` quan es fa un pipe?**  
Que l'entrada arriba per `stdin`, no d'un fitxer local.

**40. Per a què serveix `hive.cli.print.header=true`?**  
Per demanar la impressió dels noms de les columnes als resultats de Hive CLI.

### JOINs

**41. Quina relació hi ha entre `orders` i `customers`?**  
`orders.order_customer_id` relaciona una comanda amb `customers.custId`.

**42. Quines files torna un INNER JOIN?**  
Les que tenen una coincidència segons la condició d'unió.

**43. Per què usaríem un LEFT JOIN per comptar comandes?**  
Per conservar també clients que no n'han fet cap.

**44. Per què no és igual `COUNT(*)` que `COUNT(o.order_id)` amb LEFT JOIN?**  
`COUNT(*)` compta files, mentre que `COUNT(o.order_id)` ignora valors nuls de la columna.

**45. Què fa un LEFT SEMI JOIN?**  
Retorna files de l'esquerra que tenen coincidència a la dreta, sense projectar-ne les columnes.

**46. Què és un map join?**  
Una estratègia que usa una taula petita en memòria per facilitar la unió distribuïda.

**47. Per a què serveix `GROUP BY`?**  
Per agrupar files segons una o diverses expressions i calcular agregacions per grup.

### Tipus complexos

**48. Què és un ARRAY?**  
Una col·lecció ordenada d'elements del mateix tipus.

**49. Què és una STRUCT?**  
Una estructura formada per diversos camps amb nom i tipus.

**50. Què és un MAP?**  
Una col·lecció d'associacions clau-valor.

**51. Com accedim al primer element d'un ARRAY?**  
Amb `[0]`, per exemple `work_place[0]`.

**52. Com accedim a l'edat d'una STRUCT `sex_age`?**  
Amb `sex_age.age`.

**53. Com accedim a l'habilitat Python d'un mapa?**  
Amb `skills_score['Python']`.

**54. Per a què serveix SIZE?**  
Per obtenir el nombre d'elements d'una col·lecció.

**55. Què fan MAP_KEYS i MAP_VALUES?**  
Retornen, respectivament, les claus i els valors d'un mapa.

**56. Què fa EXPLODE?**  
Desplega els elements d'una col·lecció en files.

**57. Per què fem servir LATERAL VIEW juntament amb EXPLODE?**  
Per combinar les files generades amb altres columnes de la fila original.

**58. Què selecciona `depart_title['Test'][0]`?**  
El primer element de l'array associat a la clau `Test` del mapa `depart_title`.

### Execució i administració

**59. Què és Fetch Task?**  
Una optimització que resol determinades consultes amb lectura directa, sense llançar un treball MapReduce.

**60. Com desactivem Fetch Task a l'exemple del temari?**  
Amb `SET hive.fetch.task.conversion=none;`.

**61. Què és el bucketing?**  
Una organització de dades en grups físics (*buckets*) segons una columna o expressió.

**62. Què és la compactació en les taules transaccionals?**  
La reorganització que integra fitxers delta amb els fitxers base.

**63. Quin format utilitza l'exemple de taula transaccional?**  
ORC.

**64. Quina propietat identifica la taula com a transaccional?**  
`TBLPROPERTIES ('transactional'='true')`.

**65. On es monitoritza Hue executat en Docker?**  
Es pot revisar el contenidor amb `docker ps` i els logs amb `docker logs`.

## 24. Glossari i checklist final

### Glossari

| Terme | Definició curta |
|---|---|
| Hive | Capa de consulta i gestió de dades de l'ecosistema Hadoop |
| HiveQL | Llenguatge de consulta semblant a SQL |
| HDFS | Sistema distribuït d'emmagatzematge de fitxers |
| Metastore | Repositori central de metadades de Hive |
| HiveServer2 | Servei de consultes de Hive per a clients concurrents |
| Beeline | Client JDBC de consola |
| Hue | Interfície web per treballar amb Hadoop i Hive |
| Sqoop | Eina d'importació/exportació entre sistemes relacionals i Hadoop |
| DDL | Sentències per definir estructures de dades |
| DML | Sentències per manipular dades |
| Schema | Definició dels noms i tipus de les columnes |
| Warehouse | Espai habitual de les taules gestionades |
| Managed table | Taula interna gestionada per Hive |
| External table | Taula amb metadades a Hive i fitxers conservats separadament |
| Parquet | Format d'emmagatzematge columnar |
| ORC | Format columnar utilitzat, entre altres, en el cas transaccional |
| CTAS | `CREATE TABLE AS SELECT` |
| JDBC | Interfície de connectivitat entre client i servidor SQL |
| Thrift | Tecnologia RPC utilitzada en components de Hive |
| ARRAY | Col·lecció ordenada d'elements |
| STRUCT | Estructura amb atributs amb nom |
| MAP | Col·lecció de clau-valor |
| EXPLODE | Funció que genera files a partir d'elements d'una col·lecció |
| Fetch Task | Optimització de lectura directa en consultes adequades |
| Map Join | Estratègia de join amb una taula petita en memòria |
| ACID | Propietats de transaccionalitat |
| Delta | Fitxer de canvis en una taula transaccional |
| Compactació | Fusió/reorganització de fitxers base i delta |
| Bucketing | Distribució de registres en grups físics |

### Checklist abans de l'examen

- [ ] Sé explicar què és Hive i com es relaciona amb Hadoop i HDFS.
- [ ] Distingeixo HiveServer2, Metastore, HDFS, YARN i Beeline.
- [ ] Recordo els ports 10000 i 9083 del laboratori.
- [ ] Sé connectar-me amb Beeline i llistar bases de dades i taules.
- [ ] Sé definir una taula sobre un fitxer delimitat per `|`.
- [ ] Distingeixo `CREATE TABLE ... LIKE` de `CREATE TABLE AS SELECT`.
- [ ] Sé explicar `LOAD DATA`, `INSERT INTO` i `INSERT OVERWRITE`.
- [ ] Sé quin risc comporta `DROP TABLE` en taules gestionades.
- [ ] Sé escriure un `INNER JOIN` i un `LEFT JOIN`.
- [ ] Entenc la diferència entre `COUNT(*)` i `COUNT(columna)`.
- [ ] Sé interpretar `ARRAY`, `STRUCT` i `MAP`.
- [ ] Sé fer servir `work_place[0]`, `sex_age.age` i `skills_score['DB']`.
- [ ] Entenc `LATERAL VIEW EXPLODE`, `SIZE`, `MAP_KEYS` i `MAP_VALUES`.
- [ ] Distingeixo una taula interna d'una externa.
- [ ] Conec la diferència entre Fetch Task i un treball distribuït.
- [ ] Puc diagnosticar un error bàsic de connexió, ruta o delimitadors.

---

## Referències i observacions sobre el material

**Font principal:** Francesc Barragán Pascual, *Hive*, M5075 BigData Aplicat, revisió 09/02/2026, 52 pàgines. S'ha mantingut l'ordre conceptual del PDF: introducció (pàg. 5–8), arquitectura i clients (pàg. 9–14), configuració (pàg. 15–21), casos 1–3 (pàg. 22–40), comandes (pàg. 41) i casos 4–5 (pàg. 42–52).

**Fonts esmentades pel propi PDF:** pàgina oficial d'Apache Hive, *Apache Hive Essentials, Second Edition* de Dayong Du, *Hive Cheatsheet* i el tutorial d'Hive de TutorialsPoint.

### Precaucions sobre el document original

- Hi apareixen rutes i referències a **versions diferents de Hive**. S'han conservat els exemples de l'entorn de classe, amb notes de compatibilitat quan és rellevant.
- El text de configuració de HiveServer2 i Hue inclou **credencials de laboratori i configuracions permissives**; no són recomanacions de seguretat per a producció.
- El PDF parla de `DROP TABLE`, `LOCATION`, `LOAD DATA` i Hive ACID dins del seu context docent. Les versions i propietats específiques de la instal·lació poden afectar el comportament; per això convé revisar `DESCRIBE FORMATTED` i l'entorn real abans de modificar o eliminar dades.
- Les consultes addicionals proposades als apartats d'exercicis i les preguntes d'autoavaluació són material d'estudi complementari, no afirmacions que el professor les hagi demanat explícitament.

**Fi dels apunts — Apache Hive I.**
