# Apunts extensos — PySpark: JDBC, MongoDB i Spark SQL Catalog

## 1. Per què connectem Spark a JDBC?

JDBC (*Java Database Connectivity*) permet que Spark llegeixi i escrigui dades d'un gestor relacional, com MySQL o MariaDB. La guia parteix de la base de dades **`retail_db`**, amb la taula `customers`. Una connexió necessita **driver JDBC** compatible, **URL** i **propietats** (usuari, contrasenya i, si s'escau, opcions addicionals).

```text
PySpark (SparkSession)
        │
   JDBC Connector + driver .jar
        │ xarxa TCP
        ▼
  MySQL / MariaDB
        │
      retail_db
        │
     customers
```

Spark no converteix MySQL en una base de dades distribuïda: recupera dades cap a DataFrames i pot aplicar transformacions paral·leles segons la configuració de particions JDBC.

## 2. Driver, URL i propietats

Exemple fidel al plantejament docent, sense fixar contrasenyes reals al codi:

```python
import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('spark-jdbc').getOrCreate()
url = 'jdbc:mysql://localhost:3306/retail_db'
props = {
    'driver': 'com.mysql.cj.jdbc.Driver',
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
}
```

El PDF mostra la versió `mysql-connector-j-8.0.31.jar`. Pots instal·lar el `.jar` compatible a `$SPARK_HOME/jars` o proporcionar-lo al llançament:

```bash
pyspark --jars /ruta/mysql-connector-j-8.0.31.jar
# O bé:
spark-submit --jars /ruta/mysql-connector-j-8.0.31.jar script.py
```

També existeix `--packages` amb coordenades Maven quan el sistema pot descarregar dependències.

**Precaució:** l'exemple original empra credencials d'aula senzilles; evita contrasenyes dins del notebook compartit o del repositori.

## 3. Spark i MySQL amb Docker Compose

La guia col·loca Spark i MySQL a la mateixa xarxa Docker i exposa el port de Jupyter. Exemple actualitzat com a **ampliació**:

```yaml
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: retail_db
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
  spark:
    image: jupyter/pyspark-notebook
    ports:
      - '127.0.0.1:8888:8888'
      - '127.0.0.1:4040:4040'
    volumes:
      - ./:/home/jovyan/work
      - ./mysql-connector-j-8.0.31.jar:/usr/local/spark/jars/mysql-connector-j-8.0.31.jar:ro
    depends_on:
      - mysql
volumes:
  mysql_data:
```

```bash
docker compose up -d
docker compose ps
docker compose logs -f mysql
```

**Punt d'examen:** des del contenidor Spark, `localhost` és **el mateix contenidor Spark**, no MySQL. La URL serà `jdbc:mysql://mysql:3306/retail_db` si el servei de Compose es diu `mysql`.

`depends_on` ordena la creació dels serveis, però no garanteix per si sol que MySQL ja accepti consultes. Per a una execució robusta cal healthcheck o reintents.

## 4. Lectura de dades JDBC

```python
df = spark.read.jdbc(url=url, table='customers', properties=props)
df.printSchema()
df.show(2, truncate=False)
```

El PDF ensenya també una API més configurable:

```python
df = (spark.read.format('jdbc')
    .option('url', url)
    .option('dbtable', 'customers')
    .option('driver', props['driver'])
    .option('user', props['user'])
    .option('password', props['password'])
    .load())
```

### `table` i `dbtable`

En `read.jdbc`, l'argument és `table`; amb `.format('jdbc')` la propietat és `dbtable`. Les dues formes representen una consulta al mateix origen.

### Esquema i precaucions

`printSchema()` mostra els tipus inferits pel driver SQL. `show()` només presenta unes files i pot exposar dades sensibles (al PDF la taula `customers` inclou correus i una columna `customer_password`). No publiquis dades personals ni credencials reals en captures d'exercicis.

## 5. Consultes SQL i rendiment

```python
consulta = '(SELECT customer_id, customer_fname, customer_lname FROM customers WHERE customer_city = \'Las Vegas\') AS c'
subset = (spark.read.format('jdbc')
          .option('url', url)
          .option('dbtable', consulta)
          .option('user', props['user'])
          .option('password', props['password'])
          .option('driver', props['driver'])
          .load())
```

Una altra forma és `.option('query', 'SELECT ...')`. **No barrejar** `query` amb certes opcions de particionat JDBC que requereixen `dbtable` o una subconsulta aliased.

### Lectura paral·lela (ampliació)

```python
particionat = (spark.read.format('jdbc')
    .option('url', url)
    .option('dbtable', 'customers')
    .option('user', props['user'])
    .option('password', props['password'])
    .option('driver', props['driver'])
    .option('partitionColumn', 'customer_id')
    .option('lowerBound', 1)
    .option('upperBound', 15000)
    .option('numPartitions', 4)
    .load())
```

Aquesta divisió pot llançar diverses consultes simultànies a la BD. Els límits defineixen com es generen les particions; **no** s'han de tractar com a filtres de files. Augmentar `numPartitions` sense controlar el servidor pot sobrecarregar MySQL.

## 6. Escriptura JDBC

```python
clients_reduits = df.select('customer_id', 'customer_fname', 'customer_lname')

(clients_reduits.write.format('jdbc')
    .option('url', url)
    .option('dbtable', 'clients_resum')
    .option('driver', props['driver'])
    .option('user', props['user'])
    .option('password', props['password'])
    .mode('errorifexists')
    .save())
```

### Modes d'escriptura

| Mode | Comportament | Risc |
|---|---|---|
| `errorifexists` | error si ja existeix | baix |
| `append` | afegeix files | duplicats si es repeteix |
| `overwrite` | substitueix dades, sovint recrea taula | pèrdua de dades, índexs o claus segons configuració |
| `ignore` | no fa res si existeix | pot ocultar una operació no executada |

El PDF explica `.option('truncate','true')` amb `overwrite` per netejar files sense recrear la taula, **quan el driver i el dialecte JDBC ho admeten**; cal verificar restriccions, permisos i comportament abans d'usar-ho en producció.

```python
# Exemple prudent només en una taula de proves
clients_reduits.write.format('jdbc').options(
    url=url, dbtable='clients_prova',
    user=props['user'], password=props['password'], driver=props['driver']
).mode('append').save()
```

## 7. Databricks i JDBC

El document mostra connexions des de Databricks a una base de dades remota (exemple amb AWS RDS) amb driver MariaDB, i també l'ús de formats dedicats de connexió quan la plataforma ho permet.

**Important:** un entorn Databricks pot tenir connectors preinstal·lats, però això depèn del runtime i de les funcions disponibles. No presuposis que una sintaxi d'una captura serveix a totes les versions.

**Seguretat (ampliació):** desa secrets en un gestor de secrets i evita imprimir en notebook l'URL amb credencials. Limita connexions a xarxes autoritzades i fes servir TLS quan sigui possible.

## 8. Spark i MongoDB

Per a una base documental, Spark necessita el **MongoDB Spark Connector** compatible amb la versió de Scala, Spark i connector. La guia mostra:

```bash
pyspark --packages org.mongodb.spark:mongo-spark-connector_2.12:10.1.1
```

Aquesta és **la versió usada a l'exemple**, no una recomanació universal. La guia presenta les opcions de connexió amb base de dades i col·lecció:

```python
# Requereix el connector adequat i una URI configurada en un secret o variable d'entorn.
mongo_uri = os.environ['MONGO_URI']

df_mongo = (spark.read.format('mongodb')
    .option('connection.uri', mongo_uri)
    .option('database', 'iabd')
    .option('collection', 'espias')
    .load())

df_mongo.printSchema()
```

El document mostra registres amb `_id`, `edat`, `nom`; el connector ha de traduir els tipus BSON a tipus Spark.

## 9. MongoDB local i escriptura

```python
from pyspark.sql.functions import col

transformats = df_mongo.withColumn('edat_doble', col('edat') * 2)
(transformats.write.format('mongodb')
    .mode('append')
    .option('connection.uri', mongo_uri)
    .option('database', 'iabd')
    .option('collection', 'espias_nou')
    .save())
```

MongoDB al host sol escoltar al port 27017; en Docker, `localhost` torna a referir-se al contenidor que executa Spark, no al host. L'ús amb Databricks requereix instal·lar la dependència apropiada i garantir xarxa/credencials, tal com exposen les pàgines 11–12.

## 10. Què és un Spark SQL Catalog?

Un **catàleg** descriu les dades disponibles i les seves metadades: bases de dades, taules, columnes, ubicacions, propietaris, esquemes i comentaris. El document introdueix també el rol de **data steward**, dedicat a qualitat, governança i comunicació del valor de les dades.

**Metadades ≠ dades de negoci:** el catàleg pot indicar que la taula existeix en un directori de Parquet, però els registres poden estar en HDFS, S3 o un altre sistema.

## 11. Hive Metastore i Spark

El PDF descriu l'ús compartit de l'**Hive Metastore** configurant `hive-site.xml` dins de `$SPARK_HOME/conf` i la implementació del catàleg a Spark. Exemple de configuració de classe:

```properties
spark.sql.warehouse.dir /opt/spark-3.3.1/warehouse/
spark.sql.catalogImplementation hive
```

En una configuració programàtica habitual:

```python
spark = (SparkSession.builder
         .appName('spark-hive')
         .enableHiveSupport()
         .getOrCreate())
```

**Condició:** el runtime ha de tenir llibreries i configuració Hive compatibles. El PDF situa metadades a MariaDB i en alguns casos les dades del warehouse a una ruta local, mentre que altres BD de l'entorn apunten a HDFS. Cal conèixer la ruta real de cada taula.

## 12. Bases de dades

```python
spark.sql('SHOW DATABASES').show()
spark.catalog.listDatabases()
spark.catalog.currentDatabase()

spark.sql('CREATE DATABASE IF NOT EXISTS s8a')
spark.sql('USE s8a')
spark.catalog.currentDatabase()
```

La guia explica que a la VM les bases existents poden ser `default`, `iabd` i després `s8a`, creada en un warehouse local. No confondre el nom lògic de BD amb la seva ubicació física.

## 13. Vistes i taules

### Vista temporal

```python
df.createOrReplaceTempView('clients_temp')
spark.sql('SELECT customer_id FROM clients_temp LIMIT 5').show()
```

Té abast de sessió i no persisteix automàticament les dades.

### Taula gestionada

```python
df.write.mode('errorifexists').saveAsTable('s8a.clients')
spark.catalog.listTables('s8a')
```

En una **managed table**, el catàleg administra el cicle de vida de la taula i, segons el tipus i entorn, de les dades. Compte amb `DROP TABLE`.

### Taula externa

La guia mostra un cas amb dades existents a `/user/iabd/hive/customer` de HDFS i la clàusula SQL `LOCATION`. La idea és separar la definició lògica de la ubicació dels fitxers.

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS s8a.clients_externs (
  custId INT,
  fName STRING,
  lName STRING,
  city STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
LOCATION 'hdfs://SERVIDOR:9000/user/iabd/hive/customer';
```

**Atenció a un error del PDF:** al bloc original apareix `FIDELDS TERMINATED BY`; la paraula correcta és **`FIELDS`**. L'execució de DDL d'estil Hive requereix suport Hive real al runtime i accés a HDFS.

## 14. Formats i persistència

```python
# Taula en format Parquet, segons el suport del catàleg
(df.write.format('parquet')
   .mode('errorifexists')
   .saveAsTable('s8a.clients_parquet'))

# Taula en JSON
(df.write.format('json')
   .mode('errorifexists')
   .saveAsTable('s8a.clients_json'))
```

A l'entorn del PDF, per defecte les taules de fonts de dades de Spark es guarden sovint en Parquet comprimit amb Snappy. No pressuposis que qualsevol taula Hive externa usa Parquet: el format depèn de la definició.

## 15. Cache i refresc de taules

```python
spark.catalog.cacheTable('s8a.clients_parquet')
spark.catalog.isCached('s8a.clients_parquet')
spark.catalog.uncacheTable('s8a.clients_parquet')
spark.catalog.clearCache()
spark.catalog.refreshTable('s8a.clients_parquet')
```

- `cacheTable`: registra la taula per guardar-la en cache quan es materialitzi.
- `uncacheTable`: retira la persistència d'una taula.
- `clearCache`: neteja les caches del catàleg de la sessió.
- `refreshTable`: invalida metadades/dades cachejades associades a una taula, útil després de canvis externs.

El document remarca el risc de cache obsoleta si les dades s'actualitzen **des d'una aplicació aliena** a la SparkSession.

## 16. Com guarda el Metastore les metadades?

A les pàgines 20–22 el professor consulta la base `hive` de MariaDB i destaca aquestes taules:

| Taula de metadades | Informació principal |
|---|---|
| `DBS` | base de dades, `DB_ID`, nom, propietari i ubicació |
| `TBLS` | taules, `TBL_ID`, `DB_ID`, `TBL_NAME`, tipus |
| `TABLE_PARAMS` | atributs de taula i esquema/format registrats |

Exemples de lectura **només en un entorn docent autoritzat**:

```sql
USE hive;
SELECT DB_ID, NAME, DB_LOCATION_URI FROM DBS;
SELECT TBL_ID, DB_ID, TBL_NAME, TBL_TYPE FROM TBLS;
SELECT TBL_ID, PARAM_KEY, PARAM_VALUE FROM TABLE_PARAMS WHERE TBL_ID = 61;
```

No modifiquis directament les taules internes del Metastore des de SQL: les seves estructures són pròpies del servei i poden canviar entre versions.

## 17. Data discovery: documentar taules i columnes

La guia posa l'exemple de deixar comentaris a les metadades perquè altres equips entenguin què és cada camp.

```python
spark.sql('''
ALTER TABLE s8a.clients_parquet
SET TBLPROPERTIES (
 'comment' = 'Clients importats des de retail_db per a anàlisi docent',
 'active' = 'true'
)
''')

spark.catalog.listTables('s8a')
```

En catàlegs/taules que ho admeten:

```sql
ALTER TABLE s8a.clients_parquet
ALTER COLUMN customer_id COMMENT 'Identificador del client';
```

**Conceptes:** `table comment` és documentació de la taula; `column comment` documenta camps; les propietats personals addicionals han de tenir definició i manteniment clars.

## 18. Pràctica integrada (ampliació)

**Objectiu:** llegir clients de MySQL, retirar dades sensibles, filtrar, crear una taula permanent i fer una consulta agregada.

```python
from pyspark.sql import functions as F

clients = spark.read.jdbc(url=url, table='customers', properties=props)
publicables = clients.select('customer_id','customer_city','customer_state')
resum = (publicables.groupBy('customer_state')
         .agg(F.count('*').alias('nombre_clients')))
resum.show(20)

# Només en un entorn docent controlat i amb el catàleg habilitat:
resum.write.mode('errorifexists').saveAsTable('s8a.clients_per_estat')
spark.sql('SELECT * FROM s8a.clients_per_estat LIMIT 10').show()
```

**Preguntes:** On es desen les dades? Què és el catàleg? Què passa si fas `DROP TABLE`? Com reexecutaries la pràctica sense crear duplicats? Com tractaries secrets JDBC?

## 19. Errors habituals i recomanacions

| Problema | Possible causa | Com actuar |
|---|---|---|
| `ClassNotFoundException: com.mysql.cj.jdbc.Driver` | .jar absent o incompatible | afegir driver al classpath correcte |
| `Connection refused` | servidor aturat, host/port incorrecte | validar contenidor i xarxa |
| `Access denied for user` | credencial o permisos | comprovar grants i secrets |
| MySQL inaccessible des de Spark Docker | `localhost` apunta al contenidor incorrecte | usar nom de servei Docker |
| Table already exists | mode d'escriptura per defecte | usar nom nou o `append` amb criteri |
| Duplicats després d'`append` | no hi ha idempotència | deduplicació/clau o staging |
| MongoDB `Data source mongodb not found` | connector no disponible | revisar Scala/Spark/package |
| No apareixen BD Hive | falta configuració o servei | revisar HiveSupport i `hive-site.xml` |
| HDFS unavailable | NameNode/ports/configuració | verificar URL i serveis |
| `DROP TABLE` elimina dades | taula managed | backup i validar tipus de taula |
| Cache amb registres obsolets | modificacions externes | `refreshTable` |

**Nota sobre el material:** els exemples del PDF contenen alguna errada de format o nom (`volums` en un Compose, `FIDELDS`, variables `jdbcDF` vs `df` i exemples amb credencials). En els apunts s'ha conservat la intenció pedagògica i se n'han indicat les correccions per evitar copiar errors.

## 20. Glossari i resum

- **JDBC:** connector estàndard Java per bases relacionals.
- **Driver:** biblioteca `.jar` que implementa el protocol de la BD.
- **`dbtable`:** taula o subconsulta SQL d'origen/destí.
- **`append`:** afegeix files a una taula existent.
- **`overwrite`:** substitueix les dades; pot modificar l'estructura física.
- **MongoDB Spark Connector:** integració Spark ↔ MongoDB.
- **Catalog:** inventari de metadades.
- **Hive Metastore:** servei/esquema de metadades compartides.
- **Managed table:** taula gestionada pel catàleg.
- **External table:** taula referenciada sobre una ubicació externa.
- **Temporary view:** nom consultable temporalment en una sessió.
- **Data steward:** responsable de governança i qualitat.
- **`cacheTable`:** reutilització de dades consultades.
- **`refreshTable`:** invalidació/refresc de dades cachejades.

**L'essencial per a l'examen:** la distinció entre llegir i escriure per JDBC; `localhost` versus host Docker; connector MongoDB; catàleg versus fitxers; taules temporals, gestionades i externes; metadades de `DBS`, `TBLS` i `TABLE_PARAMS`; modes d'escriptura i riscos.

---

## Autoavaluació — 40 preguntes amb respostes

**1. Què vol dir JDBC?**  
**Resposta:** Java Database Connectivity.

**2. Quins elements fan falta per a JDBC?**  
**Resposta:** Driver, URL, credencials i accés de xarxa.

**3. Què és un driver JDBC?**  
**Resposta:** Una biblioteca Java que permet parlar amb el gestor de base de dades.

**4. Quina és la classe del driver MySQL modern de l’exemple?**  
**Resposta:** com.mysql.cj.jdbc.Driver.

**5. Què és dbtable?**  
**Resposta:** La taula o subconsulta de la qual es llegeix o a la qual s’escriu.

**6. Com es llegeix una taula JDBC a Spark?**  
**Resposta:** Amb spark.read.jdbc o spark.read.format("jdbc").

**7. Què fa printSchema?**  
**Resposta:** Mostra columnes i tipus.

**8. Per què `localhost` falla de vegades amb Docker?**  
**Resposta:** Perquè apunta al mateix contenidor, no a un altre servei.

**9. Com s’arriba a MySQL dins de Compose?**  
**Resposta:** Utilitzant el nom del servei de Docker com a host de la URL.

**10. Què fa append?**  
**Resposta:** Afegeix registres a una taula existent.

**11. Què fa overwrite?**  
**Resposta:** Substitueix dades existents i pot recrear la taula.

**12. Què fa errorifexists?**  
**Resposta:** Falla si la taula de destí ja existeix.

**13. Per què un append pot generar duplicats?**  
**Resposta:** Perquè reexecutar la càrrega pot tornar a inserir les mateixes files.

**14. Què fa truncate en alguns dialectes JDBC?**  
**Resposta:** Permet buidar taules preservant l’estructura en context overwrite, si és compatible.

**15. Quin avantatge té el pushdown SQL?**  
**Resposta:** Filtrar o seleccionar a l’origen i reduir la transferència.

**16. Per què vigilar numPartitions JDBC?**  
**Resposta:** Pot generar massa connexions o càrrega sobre el gestor.

**17. Què és MongoDB Spark Connector?**  
**Resposta:** Connector de lectura i escriptura entre Spark i MongoDB.

**18. Quin format de dades s’utilitza amb aquest connector?**  
**Resposta:** mongodb.

**19. Què indica collection a MongoDB?**  
**Resposta:** La col·lecció de documents d’origen o destí.

**20. Què és el camp _id?**  
**Resposta:** Identificador de document MongoDB.

**21. Què és Spark SQL Catalog?**  
**Resposta:** Un inventari de bases, taules i metadades accessibles a Spark.

**22. Què és Hive Metastore?**  
**Resposta:** Un servei i repositori de metadades de taules Hive i altres clients compatibles.

**23. Quina diferència hi ha entre metadades i dades?**  
**Resposta:** Les metadades descriuen, les dades són els registres.

**24. Què és una vista temporal?**  
**Resposta:** Una vista SQL visible a la sessió sense persistència automàtica.

**25. Què fa saveAsTable?**  
**Resposta:** Registra i desa un DataFrame com una taula del catàleg.

**26. Què és una taula managed?**  
**Resposta:** Taula gestionada pel catàleg incloent el cicle de vida de dades segons sistema.

**27. Què és una taula external?**  
**Resposta:** Taula que apunta a dades en una ubicació externa especificada.

**28. Quin risc té DROP TABLE sobre una managed table?**  
**Resposta:** Pot eliminar també les dades gestionades.

**29. Què és LOCATION?**  
**Resposta:** Ruta física d’emmagatzematge d’una taula externa.

**30. Quin format usa sovint Spark per defecte en saveAsTable del material?**  
**Resposta:** Parquet amb compressió Snappy.

**31. Què fa spark.catalog.listDatabases?**  
**Resposta:** Enumera bases del catàleg.

**32. Què fa spark.catalog.listTables?**  
**Resposta:** Enumera taules i vistes d’una base.

**33. Què fa cacheTable?**  
**Resposta:** Marca una taula per persistència en cache.

**34. Què fa uncacheTable?**  
**Resposta:** Deixa de guardar-la en cache.

**35. Què fa refreshTable?**  
**Resposta:** Invalida/refresca dades i metadades cachejades de taula.

**36. Què guarda la taula DBS del Hive Metastore?**  
**Resposta:** Informació sobre bases de dades.

**37. Què guarda TBLS?**  
**Resposta:** Informació sobre taules i la seva base de dades.

**38. Què guarda TABLE_PARAMS?**  
**Resposta:** Propietats i metadades de taules.

**39. Què és data discovery?**  
**Resposta:** Trobar i entendre dades disponibles a través de metadades.

**40. Per què afegir comentaris a les columnes?**  
**Resposta:** Per facilitar interpretació, governança i reutilització.

---

## Checklist final per estudiar

- [ ] Puc explicar sense mirar els apunts els conceptes principals.
- [ ] Sé escriure i executar els exemples sense copiar-los literalment.
- [ ] Entenc què passa a cada etapa de les comandes.
- [ ] Sé identificar els errors típics i resoldre'ls.
- [ ] He provat els exercicis en un entorn de pràctiques.
- [ ] He fet les preguntes d'autoavaluació sense mirar les respostes.

**Fonts:** document docent indicat a la capçalera. Els exercicis d'ampliació i les recomanacions són complementaris al material original. Per verificar les APIs d'una versió concreta, consulta la documentació oficial d'Apache Spark i dels connectors instal·lats.
