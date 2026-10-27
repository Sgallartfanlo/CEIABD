# Guia Completa d'Apache Sqoop (Big Data)

## 1. Introducció a Apache Sqoop

**Apache Sqoop** (de l'anglès *SQL-to-Hadoop*) és una eina dissenyada per transferir de forma eficient dades massives (*raw data*) entre l'ecosistema **Hadoop** (HDFS, Hive, HBase) i emmagatzematges de dades estructurats externs, com ara **Bases de Dades Relacionals (RDBMS)** (MariaDB, MySQL, PostgreSQL, Oracle, SQL Server).

```
+------------------+         Sqoop Import         +-------------------+
|                  | ---------------------------> |                   |
|  RDBMS / SQL DB  |                              |    Hadoop Core    |
| (MariaDB, MySQL, |                              |  (HDFS / Hive /   |
|  Oracle, etc.)   | <--------------------------- |      HBase)       |
+------------------+         Sqoop Export         +-------------------+
```

### Context actual de Sqoop
* **Estat del projecte:** Des de juny de **2021**, Apache Sqoop ha passat a estar a l'**Àtic d'Apache** (projecte retiret/sense manteniment oficial).
* **Alternatives modernes:** Tot i la seva importància històrica en arquitectures Big Data, actualment les seves funcionalitats se substitueixen sovint per eines com **Apache NiFi**, **Apache Spark (Spark SQL/JDBC)** o pipelines de data integration basats en el núvol.
* **Utilitat pedagògica:** Segueix sent un estàndard fonamental per entendre la ingesta distribuïda batch i la integració entre el món relacional i el món HDFS.

### Rol en l'arquitectura Hadoop
Sqoop se situa a la capa de **Ingesta de Dades (*Data Ingestion*)**, treballant colze a colze amb altres eines com Flume (per a dades en streaming/logs) o Storm:

* **Arquitectura de connectors:** Utilitza un model extensible basat en plugins/connectors JDBC per comunicar-se amb qualsevol SGBD compatible.
* **Paral·lelisme via MapReduce:** Sqoop no compta amb un motor d'execució propi; tradueix totes les operacions d'importació i exportació en treballs **MapReduce** (executats sobre YARN) que llegeixen o escriuen dades en paral·lel.
* **Nombre de mappers per defecte:** Per defecte, qualsevol treball de Sqoop utilitza **4 mappers** (`-m 4`), el que significa que la carga o exportació es divideix en 4 fluxos simultanis des de/cap a diferents nodes del clúster.

---

## 2. Instal·lació i Configuració de l'Entorn

### 2.1 Passos previ i ajustos del sistema
En entorns virtualitzats o de pràctiques (com el node `master` d'un clúster local):

1. **Actualització de la IP del host master:**  
   Cal verificar la IP assignada a la interfície de xarxa (ex: `ensp03`) i actualitzar el fitxer `/etc/hosts` per associar aquesta IP al nom del node master:
   ```bash
   ip a
   sudo nano /etc/hosts
   # Afegir/Modificar: <IP_OBTINGUDA> master
   ```

2. **Historificació de comandes Bash (opcional):**  
   Per mantenir un registre extens de les ordres executades a la terminal, s'edita `/home/iabd/.bashrc`:
   ```bash
   HISTSIZE=500
   HISTFILESIZE=500
   ```

3. **Dependències i Drivers (JDBC):**  
   Perquè Sqoop es pugui comunicar amb bases de dades relacionals, necessita els conectors corresponents i certes llibreries al seu directori `lib/`:
   * **Driver MySQL/MariaDB:** Copiar `mysql-connector-java.jar` a `$SQOOP_HOME/lib/`.
   * **Llibreries auxiliars:** Copiar `commons-lang-2.6.jar` a `$SQOOP_HOME/lib/`.

4. **Verificació de la connexió:**  
   Podem provar la connectivitat consultant les bases de dades disponibles a MariaDB:
   ```bash
   sqoop list-databases \
     --connect jdbc:mysql://localhost \
     --username=iabd \
     --password=iabd
   ```

---

## 3. Arquitectura del Procés d'Importació i Exportació

### Procés d'Importació (`sqoop import`)
Quan s'executa una comanda d'importació, el procés es divideix estrictament en dues fases:

1. **Fase de Metadades (Generació de Codi):**
   * Sqoop connecta a la base de dades relacional via JDBC.
   * Examina les metadades de la taula (estructura de columnes, tipus de dades, claus primàries).
   * Genera automàticament una classe Java que representa cada registre de la taula (serialització/deserialització de dades).

2. **Fase d'Execució Paral·lela (MapReduce):**
   * Sqoop executa un treball només de tipus *Map* (*Map-Only Job*, 0 reducers).
   * Determina el rang de la clau primària (mitjançant `SELECT MIN(id), MAX(id) FROM table`).
   * Divideix aquest rang en fragments iguals entre el nombre de mappers especificats (ex: 4 parts).
   * Cada mapper s'encarrega d'executar un `SELECT` amb un rang determinat (`WHERE id >= X AND id < Y`) i escriure els resultats directament a directori corresponent d'HDFS.

```
Fase 1: SQL Metadades ---> Generació de Codi (.java / .jar)
                               |
Fase 2: Divideix Rangs  -----> Mapper 1 (SELECT valors 1-25)  ---> HDFS part-m-00000
                               Mapper 2 (SELECT valors 26-50) ---> HDFS part-m-00001
                               Mapper 3 (SELECT valors 51-75) ---> HDFS part-m-00002
                               Mapper 4 (SELECT valors 76-100)---> HDFS part-m-00003
```

---

## 4. Casos d'Ús Pràctics

### Preparació Prèvia: Zona Horària i Entorn MariaDB
Sqoop captura els *timestamps* de la base de dades i els tradueix a l'hora del servidor. Per evitar desfasaments temporal, cal definir la zona horària a MariaDB (`/etc/mysql/my.cnf`):

```ini
[mariadb]
default_time_zone = 'Europe/Madrid'
```

Configuració de permissos per a l'usuari de pràctiques `iabd`:
```sql
sudo mariadb -u root
GRANT ALL PRIVILEGES ON *.* TO 'iabd'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EXIT;
```

---

### Cas 1: Importació de Dades des de MariaDB a HDFS

#### 1. Creació del model de dades a MariaDB
```sql
mariadb -u iabd -piabd

CREATE DATABASE sqoopCas1;
USE sqoopCas1;

CREATE TABLE professors(
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    nom CHAR(30) NOT NULL,
    edat INTEGER,
    materia CHAR(30),
    PRIMARY KEY (id)
);

INSERT INTO professors (nom, edat, materia) VALUES 
("Carles", 24, "Matematiques"),
("Pere", 32, "Anglès"),
("Joan", 35, "Tecnologia"),
("Josep", 48, "Matematiques"),
("Paula", 24, "Informàtica"),
("Sussana", 32, "Informàtica"),
("Lorena", 54, "Informatica");
```

#### 2. Inici dels serveis de Hadoop
Asegurar-se que el sistema de fitxers i el gestor de recursos estan actius:
```bash
start-dfs.sh
start-yarn.sh
```

#### 3. Llistat de taules disponibles
```bash
sqoop list-tables \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd
```

#### 4. Execució de la importació
Executarem una importació usant **2 mappers** (`-m 2`) i especificant separadors personalitzats. Per evitar errors si el directori destí ja existeix, s'afegeix `--delete-target-dir`:

```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_hdfs \
  --fields-terminated-by=',' \
  --lines-terminated-by='\n' \
  --delete-target-dir \
  -m 2
```

#### 5. Gestió de problemes d'espai a YARN (Node Incomod / Unhealthy Node)
Si el disc local està molt ple, YARN pot marcar el node com a *Unhealthy* i aturar els treballs MapReduce. Per desactivar temporalment aquest límit estricte, podem configurar `/opt/hadoop/etc/hadoop/yarn-site.xml`:

```xml
<property>
    <name>yarn.nodemanager.disk-health-checker.min-healthy-disks</name>
    <value>0.0</value>
</property>
<property>
    <name>yarn.nodemanager.disk-health-checker.max-disk-utilization-per-disk-percentage</name>
    <value>100.0</value>
</property>
```

#### 6. Comprovar els fitxers a HDFS
Per llistar les dades importades:
```bash
hdfs dfs -ls /user/iabd/sqoop/professors_hdfs
```
Si es vol descarregar tota la informació repartida entre els diferents fitxers `part-m-XXXXX` i unificar-la en un sol fitxer local CSV:
```bash
hdfs dfs -getmerge /user/iabd/sqoop/professors_hdfs professors.csv
```

#### 7. Importar totes les taules d'una base de dades
Per importar completament una base de dades relacional sense especificar les taules d'una en una, s'utilitza `import-all-tables` indicant el directori arrel destí usant `--warehouse-dir`:

```bash
sqoop import-all-tables \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --driver=com.mysql.jdbc.Driver \
  --warehouse-dir=/user/iabd/sqoop \
  --fields-terminated-by=',' \
  --lines-terminated-by='\n'
```

---

### Cas 2: Exportació de Dades d'HDFS a MariaDB

En l'exportació, el procés pren els fitxers delimitats o estructurats emmagatzemats a HDFS i insereix les seves files en una taula prèviament existent a la base de dades relacional.

#### 1. Creació de la taula de destinació a MariaDB
> **Nota important:** La taula de destinació ha d'existir prèviament; en cas contrari, Sqoop llançarà un error.

```sql
mariadb -u iabd -piabd

CREATE DATABASE sqoopCas2;
USE sqoopCas2;

CREATE TABLE professors2(
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    nom CHAR(30) NOT NULL,
    edat INTEGER,
    materia CHAR(30),
    PRIMARY KEY (id)
);
```

#### 2. Execució de la comanda d'exportació bàsica
```bash
sqoop export \
  --connect jdbc:mysql://localhost/sqoopCas2 \
  --username=iabd \
  --password=iabd \
  --table=professors2 \
  --export-dir=/user/iabd/sqoop/professors_hdfs
```

#### 3. Exportació avançada: Actualització i Inserció (`UPSERT`)
Si s'exporta sobre una taula que ja conté registres o claus primàries existents, s'obtindrà un error de clau duplicada. Per permetre actualitzar les files modificades i/o afegir noves entrades:

* `--update-key <columna>`: Especifica quina columna s'utilitza com a clau per a la sentència `UPDATE`.
* `--update-mode allowinsert`: Permet inserir nous registres quan la clau no coincideix amb cap registre existent (comportament `UPSERT`).

```bash
sqoop export \
  --connect jdbc:mysql://localhost/sqoopCas2 \
  --username=iabd \
  --password=iabd \
  --table=professors2 \
  --export-dir=/user/iabd/sqoop/professors_hdfs \
  --update-key id \
  --update-mode allowinsert
```

---

## 5. Formats de Dades Avançats: Avro i Parquet

Per defecte, Sqoop desa les dades en fitxers de text delimitat (CSV). Tanmateix, per millorar el rendiment i la gestió d'esquemes en entorns Big Data, és molt comú utilitzar formats binaris com **Avro** o **Parquet**.

| Format | Tipus d'orientació | Característiques principals |
| :--- | :--- | :--- |
| **Avro** | Orientat a **Files** (*Row-based*) | Desarrollat per Hadoop. Desa l'esquema en format **JSON** i les dades en **Binari**. Excel·lent per a evolució d'esquemes i escriptura ràpida. |
| **Parquet** | Orientat a **Columnes** (*Columnar*) | Optimitzat per a consultes analítiques (OLAP). Permet emmagatzemar estructures anidades i alta compressió per columna. |

---

### 5.1 Treballant amb Avro

#### Configuració prèvia del JAR d'Avro
Perquè la serialització Avro funcioni en Hadoop, cal assegurar-se que la versió de la llibreria `avro.jar` de Sqoop coincideixi amb la de Hadoop:

```bash
cp $SQOOP_HOME/lib/avro-1.8.1.jar $HADOOP_HOME/share/hadoop/common/lib/
rm $HADOOP_HOME/share/hadoop/common/lib/avro-1.7.7.jar
```

#### Importació en format Avro
S'afegeix el paràmetre `--as-avrodatafile`:

```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_avro \
  --as-avrodatafile
```

#### Visualització de contingut Avro
Si intentem llegir un fitxer Avro amb `hdfs dfs -cat` o `hdfs dfs -tail`, veurem caràcters binaris no llegibles. Per visualitzar les dades en format de text clar tenim dues opcions:

1. **Mitjançant la comanda nativa HDFS (`-text`):**
   ```bash
   hdfs dfs -text /user/iabd/sqoop/professors_avro/part-m-00000.avro
   ```
2. **Mitjançant les eines `avro-tools`:**
   * Descarregar el JAR executables d'Avro Tools:
     ```bash
     cd /tmp
     wget https://repo1.maven.org/maven2/org/apache/avro/avro-tools/1.11.3/avro-tools-1.11.3.jar
     sudo mkdir -p /opt/avro-tools
     sudo mv avro-tools-1.11.3.jar /opt/avro-tools/
     ```
   * Crear un script wrapper executable `/usr/local/bin/avro-tools`:
     ```bash
     #!/bin/bash
     java -jar /opt/avro-tools/avro-tools-1.11.3.jar "$@"
     ```
   * Donar permisos i consultar les dades convertides a JSON:
     ```bash
     sudo chmod +x /usr/local/bin/avro-tools
     hdfs dfs -cat /user/iabd/sqoop/professors_avro/part-m-00000.avro | avro-tools tojson -
     ```

---

### 5.2 Treballant amb Parquet

#### Importació en format Parquet
S'afegeix el paràmetre `--as-parquetfile`:

```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_parquet \
  --as-parquetfile
```

#### Inspecció de fitxers Parquet (`parquet-tools`)
Els fitxers Parquet són completament binaris i optimitzats per columnes.

* **Instal·lació via Python (Local/S3):**
  ```bash
  sudo apt install python3-pip
  pip3 install parquet-tools
  ```
* **Lectura via Java (HDFS Natia):**
  Podem fer servir el JAR de `parquet-tools` directament sobre les rutes distribuïdes d'HDFS:
  ```bash
  # Veure les primeres 5 files d'un fitxer Parquet
  hadoop jar parquet-tools-1.11.2.jar head -n5 \
    hdfs://master:9000/user/iabd/sqoop/professors_parquet/<NOM_FITXER>.parquet

  # Inspeccionar les metadades i l'esquema columnar
  hadoop jar parquet-tools-1.11.2.jar meta \
    hdfs://master:9000/user/iabd/sqoop/professors_parquet/<NOM_FITXER>.parquet
  ```

---

## 6. Compressió de Dades en Ingesta

La compressió redueix considerablement l'ús d'emmagatzematge en el Data Lake i millora l'amplada de banda de xarxa durant el processament.

### 1. Compressió GZIP (Per defecte amb `--compress`)
```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_gzip \
  --compress
```

### 2. Compressió BZIP2
Format d'alta taxa de compressió:
```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_bzip \
  --compress \
  --compression-codec bzip2
```

### 3. Compressió Snappy
Algorisme d'alta velocitat de compressió/descompressió optimitzat per a entorns Big Data:
```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_snappy \
  --compress \
  --compression-codec snappy
```

---

## 7. Importacions amb Filtres i Consultes Personalitzades

Sqoop no està limitat a carregar taules completes; permet executar filtres en origen per descarregar només els subconjunts de dades necessaris.

### 1. Filtrar per claus de condició (`--where`)
```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_materia_info \
  --where "materia='Informàtica'"
```

### 2. Selecció de columnes específiques (`--columns`)
```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_cols \
  --columns "nom, materia"
```

### 3. Importació basada en consultes SQL (`--query`)
Quan s'utilitza una consulta SQL personalitzada:
1. **No s'ha d'incloure el paràmetre `--table`.**
2. La consulta **HA d'INCLOURE** la clàusula `$CONDITIONS` (escapada com `\$CONDITIONS` a la terminal bash), de manera que Sqoop pugui injectar dinàmicament els rangs de particionat dels mappers.
3. S'ha de definir un camp de partició amb `--split-by`.

```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_query \
  --query "SELECT * FROM professors WHERE edat > 40 AND \$CONDITIONS" \
  --split-by "id"
```

---

## 8. Importació Incremental

En pipelines de producció de tipus Batch, sovint cal descarregar només els registres que s'han inserit de nou des de l'última executada.

### Paràmetres clau:
* `--incremental append`: Mode d'afegiment de dades incrementals.
* `--check-column <columna>`: Nom de la columna d'origen utilitzada per controlar l'increment (habitualment una clau primària `id` o una data de creació `updated_at`).
* `--last-value <valor>`: Valor límit a partir del qual es recuperaran els nous registres (registres amb valor superior al passat).

```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_inc \
  --incremental append \
  --check-column id \
  --last-value 4
```

Al final de l'execució, el log de Sqoop indicarà quin paràmetre `--last-value` s'ha d'utilitzar en la següent execució per mantenir la sincronització continuada:

```text
INFO tool.ImportTool: Incremental import complete! To run another incremental import
INFO tool.ImportTool: --incremental append
INFO tool.ImportTool: --check-column id
INFO tool.ImportTool: --last-value 7
```

---

## 9. Integració amb Apache Hive

Sqoop permet no només desar les dades a HDFS sinó crear directament les metadades i les taules gestionades a **Apache Hive**.

### 1. Importar des de MariaDB cap a una taula de Hive
> **Atenció:** En aquest cas no s'especifica `--target-dir`, ja que les dades s'ubiquen automàticament al directori magatzem de Hive (*Hive Warehouse*).

```bash
sqoop import \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd \
  --password=iabd \
  --table=professors \
  --driver=com.mysql.jdbc.Driver \
  --hive-import \
  --hive-database default \
  --create-hive-table \
  --hive-table professors_mariadb
```

Per verificar el correcte registre a la consola de Hive:
```sql
DESCRIBE FORMATTED professors_mariadb;
```

### 2. Exportar dades des de Hive cap a MariaDB
Per exportar taules directament des del Metastore de Hive utilitzant HCatalog:

```bash
sqoop export \
  --connect jdbc:mysql://localhost/sqoopCas2 \
  --username=iabd \
  --password=iabd \
  --table=professors2 \
  --driver=com.mysql.jdbc.Driver \
  --h-catalog-table professors_mariadb
```

---

## 10. Monitorització i Diagnòstic

### Interfícies web del Clúster:
* **YARN Resource Manager (Estat dels Treballs MapReduce):**  
  `http://master:8088/cluster` (O `http://localhost:8088/cluster`)  
  Permet consultar l'estat dels jobs (`RUNNING`, `SUCCEEDED`, `FAILED`), l'ús de vCores i memòria utilitzada pels mappers de Sqoop.

* **Hadoop HDFS NameNode (Visualitzador de fitxers):**  
  `http://master:9870` (O `http://localhost:9870`)  
  Permet navegar per les rutes `/user/iabd/sqoop/...` i comprovar la mida i particionat dels fitxers `part-m-XXXXX`.

---

## 11. Taula Resum de Comandes Fonamentals

| Operació | Comanda bàsica | Paràmetres clau |
| :--- | :--- | :--- |
| **Llistar BD** | `sqoop list-databases` | `--connect` |
| **Llistar Taules** | `sqoop list-tables` | `--connect`, `--username`, `--password` |
| **Importar Taula** | `sqoop import` | `--table`, `--target-dir`, `-m` |
| **Importar Tot** | `sqoop import-all-tables` | `--warehouse-dir` |
| **Exportar a DB** | `sqoop export` | `--table`, `--export-dir` |
| **UPSERT/Export** | `sqoop export` | `--update-key`, `--update-mode allowinsert` |
| **Format Avro** | `sqoop import` | `--as-avrodatafile` |
| **Format Parquet**| `sqoop import` | `--as-parquetfile` |
| **Incremental** | `sqoop import` | `--incremental append --check-column --last-value` |
| **Integració Hive**| `sqoop import` | `--hive-import --hive-table` |

---

## 12. Referències i Recursos
* **Pàgina oficial d'Apache Sqoop:** [https://sqoop.apache.org](https://sqoop.apache.org)
* **Sqoop User Guide (v1.4.7):** Documentació de referència per a paràmetres CLI.
* **Apache Sqoop Cookbook** (Kathleen Ting, Jarek Jarcec Cecho - O'Reilly Media).