# M05075 - BigData Aplicat

## Activitat 3: Gestió i Administració d'HDFS

* **Nom de l'alumnat:** Sergi Gallart Fanlo
* **Professor:** Joan Pou
* **Curs:** 2026/2027
* **Centre:** Institut Sa Palomera (CE IA&BD)

---

## Taula de Continguts

1. [Comandes bàsiques en HDFS](#1-comandes-bàsiques-en-hdfs)
   * [1.1 Creació del directori de treball](#11-creació-del-directori-de-treball)
   * [1.2 Càrrega del fitxer local a HDFS](#12-càrrega-del-fitxer-local-a-hdfs)
   * [1.3 Còpia interna d'un fitxer](#13-còpia-interna-dun-fitxer)
   * [1.4 Visualització de les primeres línies (`hdfs dfs -head`)](#14-visualització-de-les-primeres-línies-hdfs-dfs--head)
   * [1.5 Canvi de nom / Reanomenament de fitxers](#15-canvi-de-nom--reanomenament-de-fitxers)
   * [1.6 Descàrrega local amb verificació d'integritat (`-get-crc`)](#16-descàrrega-local-amb-verificació-dintegritat--get-crc)
   * [1.7 Verificació des de la interfície Web HDFS](#17-verificació-des-de-la-interfície-web-hdfs)
   * [1.8 Eliminació recursiva de directoris](#18-eliminació-recursiva-de-directoris)
   * [1.9 Procés de lectura en HDFS (Explicació Teòrica)](#19-procés-de-lectura-en-hdfs-explicació-teòrica)
2. [Gestió d'instantànies (Snapshots) i Administració](#2-gestió-dinstantànies-snapshots-i-administració)
   * [2.1 - 2.4 Preparació del directori i creació de còpies](#21---24-preparació-del-directori-i-creació-de-còpies)
   * [2.5 Creació de la primera instantània (`ss1`)](#25-creació-de-la-primera-instantània-ss1)
   * [2.6 - 2.8 Esborrat accidental i recuperació des de Snapshot](#26---28-esborrat-accidental-i-recuperació-des-de-snapshot)
   * [2.9 - 2.10 Segona instantània (`ss2`) i comparativa d'estats](#29---210-segona-instantània-ss2-i-comparativa-destats)
3. [HDFS per dins: Metadades i Checkpoints](#3-hdfs-per-dins-metadades-i-checkpoints)
   * [3.1 Identificació del directori de metadades (`hdfs-site.xml`)](#31-identificació-del-directori-de-metadades-hdfs-sitexml)
   * [3.2 - 3.3 Exploració del directori `current` i fitxer `VERSION`](#32---33-exploració-del-directori-current-i-fitxer-version)
   * [3.4 - 3.7 Execució d'un Checkpoint manual (`saveNamespace` i Safemode)](#34---37-execució-dun-checkpoint-manual-savenamespace-i-safemode)
   * [3.8 Anàlisi i justificació del checkpoint sobre `fsimage`](#38-anàlisi-i-justificació-del-checkpoint-sobre-fsimage)
4. [Accés programàtic a HDFS amb Python](#4-accés-programàtic-a-hdfs-amb-python)
   * [4.1 Script de lectura via WebHDFS (`llegir_hdfs.py`)](#41-script-de-lectura-via-webhdfs-llegir_hdfspy)
   * [4.2 Script de creació i escriptura de CSV (`crear_csv_hdfs.py`)](#42-script-de-creació-i-escriptura-de-csv-crear_csv_hdfspy)

---

## 1. Comandes bàsiques en HDFS

Un cop arrencat el clúster Hadoop (`start-dfs.sh`), es realitzen les següents tasques d'administració de fitxers.

### 1.1 Creació del directori de treball
Es crea el directori `/user/iabd/exercicis` dins del sistema de fitxers de HDFS mitjançant l'opció `-mkdir -p` per assegurar la creació de les rutes pare si no existien.

```bash
hadoop@hadoop-server:~$ hdfs dfs -mkdir -p /user/iabd/exercicis
```

### 1.2 Càrrega del fitxer local a HDFS
S'ha pujat el fitxer local `tirantloblanc.txt` a la carpeta HDFS `/user/iabd/exercicis/` emprant la comanda `hdfs dfs -put`.

```bash
hadoop@hadoop-server:~$ hdfs dfs -put tirantloblanc.txt /user/iabd/exercicis/
hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/exercicis/
Found 1 items
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-20 16:57 /user/iabd/exercicis/tirantloblanc.txt
```

### 1.3 Còpia interna d'un fitxer
S'ha realitzat una còpia interna dins d'HDFS del fitxer original generant `tirantloblanc2.txt` mitjançant la comanda `hdfs dfs -cp`.

```bash
hadoop@hadoop-server:~$ hdfs dfs -cp /user/iabd/exercicis/tirantloblanc.txt /user/iabd/exercicis/tirantloblanc2.txt
hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/exercicis/
Found 2 items
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-20 16:57 /user/iabd/exercicis/tirantloblanc.txt
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-20 16:59 /user/iabd/exercicis/tirantloblanc2.txt
```

### 1.4 Visualització de les primeres línies (`hdfs dfs -head`)
Visualitzem les primeres línies del fitxer de la còpia fent servir l'ordre `hdfs dfs -head`.

```bash
hadoop@hadoop-server:~$ hdfs dfs -head /user/iabd/exercicis/tirantloblanc2.txt
SINOPSI
El Tirant lo Blanc és la més important de les novel·les escrites en
llengua catalana i, probablement, la millor de la literatura europea
del seu temps. L'obra de Joanot Martorell transcendeix els llibres de
cavalleries medievals, per la mentalitat, per l'amplitud de mires, per
l'humor, perquè no descriu gestes miraculoses en escenaris irreals i
perquè les qualitats de l'heroi són ben humanes. El Tirant és una
novel·la de cavallers i de batalles, però també una història de
seduccions i d'amors, amb episodis divertits, una sensualitat festiva i
una ironia intel·ligent. Al Quixot, Cervantes ja va escriure que «por
su estilo es éste el mejor libro del mundo». Però el català que
utilitzava Joanot Martorell al segle XV és un impediment per a molts
lectors que avui volen gaudir del nostre clàssic. Per això l'escriptor i
filòleg Màrius Serra ha dut a terme una actualització lingüística del
text, magnífica, impecable, que no pretén suplantar la versió
original, sinó co
```

### 1.5 Canvi de nom / Reanomenament de fitxers
S'ha canviat el nom del fitxer secundari a `tirantloblanc_copia.txt` mitjançant la comanda d'HDFS `hdfs dfs -mv`.

```bash
hadoop@hadoop-server:~$ hdfs dfs -mv /user/iabd/exercicis/tirantloblanc2.txt /user/iabd/exercicis/tirantloblanc_copia.txt
hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/exercicis/
Found 2 items
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-20 16:51 /user/iabd/exercicis/tirantloblanc.txt
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-20 16:53 /user/iabd/exercicis/tirantloblanc_copia.txt
```

### 1.6 Descàrrega local amb verificació d'integritat (`-get-crc`)
S'ha descarregat el fitxer al directori local utilitzant `hdfs dfs -get-crc`. En llistar els fitxers locals amb `ls -la`, es comprova que s'ha creat el fitxer de verificació d'integritat d'HDFS ocult `.tirantloblanc_copia.txt.crc`.

```bash
hadoop@hadoop-server:~$ hdfs dfs -get-crc /user/iabd/exercicis/tirantloblanc_copia.txt .
hadoop@hadoop-server:~$ ls -la
total 506600
drwxr-x--- 6 hadoop hadoop      4096 oct 20 17:03 .
drwxr-xr-x 4 root   root        4096 sep 30 10:22 ..
-rw-r--r-- 1 hadoop hadoop   1879325 oct 20 17:03 tirantloblanc_copia.txt
-rw-r--r-- 1 hadoop hadoop     14692 oct 20 17:03 .tirantloblanc_copia.txt.crc
-rw-r--r-- 1 hadoop hadoop   1879325 ago  3 08:22 tirantloblanc.txt
```

### 1.7 Verificació des de la interfície Web HDFS
Entrem a la interfície web del NameNode (`http://192.168.56.104:9870`) visualitzant la carpeta `/user/iabd/exercicis/`, confirmant la presència dels dos fitxers en el clúster.

* **Ruta:** `/user/iabd/exercicis/`
* **Fitxers visibles:** `tirantloblanc.txt` (1.79 MB), `tirantloblanc_copia.txt` (1.79 MB).

### 1.8 Eliminació recursiva de directoris
Eliminem de forma recursiva tot el directori `/user/iabd/exercicis` i tot el seu contingut mitjançant la comanda `hdfs dfs -rm -r`.

```bash
hadoop@hadoop-server:~$ hdfs dfs -rm -r /user/iabd/exercicis
Deleted /user/iabd/exercicis
hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd
```

---

### 1.9 Procés de lectura en HDFS (Explicació Teòrica)

Davant la petició de lectura del fitxer `/logs/101213.log`, el procés d'interacció entre el Client, NameNode i DataNodes segueix els passos següents:

```
+--------+            1. open() / RPC            +----------+
|        | ------------------------------------> |          |
|        | <------------------------------------ |          |
|        |   3. Llista de blocs i ubicacions     | NameNode |
|        |                                       +----------+
| Client |
|        |            4. read() Stream Directe   +----------+
|        | ------------------------------------> | DataNode |
|        | <------------------------------------ | (Node 1) |
+--------+                                       +----------+
```

1. **Petició d'obertura del fitxer (Client → NameNode):** El client inicia la lectura cridant el mètode `open()` en l'objecte `FileSystem`. S'envia una petició RPC al NameNode sol·licitant la ubicació dels blocs que componen el fitxer `/logs/101213.log`.
2. **Consulta de metadades al NameNode:** El NameNode comprova si el client té els permisos de lectura adequats i cerca a la seva taula de metadades en memòria RAM. Identifica que el fitxer `/logs/101213.log` està compost per dos blocs:
   * **Bloc B4:** Emmagatzemat als nodes Node 1, Node 2 i Node 4.
   * **Bloc B5:** Emmagatzemat als nodes Node 1, Node 3 i Node 5.
3. **Retorn de la llista d'ubicacions:** El NameNode respon al client retornant la llista d'adreces IP/DataNodes de cada bloc. Els DataNodes per a cada bloc s'entreguen ordenats en funció de la seva proximitat de xarxa (topologia de xarxa) respecte al client per optimitzar la velocitat de transferència.
4. **Lectura directa del primer bloc B4 (Client → DataNode):** El client crea un flux d'entrada (`FSDataInputStream`) i es connecta directament al primer DataNode de la llista per al bloc B4 (per exemple, el Node 1). El client executa successives cridades a `read()` llegint les dades del bloc B4 mitjançant streaming directe.
5. **Lectura del segon bloc B5:** Una vegada completada la lectura del bloc B4, es tanca la connexió amb aquest DataNode i el flux obre una nova connexió amb el DataNode òptim per al bloc B5 (per exemple, el Node 1 o Node 3).
6. **Tancament de la connexió:** Quan el client acaba de llegir tots els blocs del fitxer, crida el mètode `close()` finalitzant el flux de lectura.

---

## 2. Gestió d'instantànies (Snapshots) i Administració

Practiquem la creació, recuperació i eliminació de punts de restauració (*snapshots*) en HDFS.

### 2.1 - 2.4 Preparació del directori i creació de còpies
Creem el directori, activem la capacitat d'instantànies i hi carreguem els fitxers de prova:

```bash
# 2.1 Creació de la carpeta
hadoop@hadoop-server:~$ hdfs dfs -mkdir -p /user/iabd/snaps

# 2.2 Habilitar Snapshots
hadoop@hadoop-server:~$ hdfs dfsadmin -allowSnapshot /user/iabd/snaps
Allowing snapshot on /user/iabd/snaps succeeded

# 2.3 Pujar fitxer original
hadoop@hadoop-server:~$ hdfs dfs -put tirantloblanc.txt /user/iabd/snaps

# 2.4 Còpia interna del fitxer
hadoop@hadoop-server:~$ hdfs dfs -cp /user/iabd/snaps/tirantloblanc.txt /user/iabd/snaps/tirantloblanc_snapshot.txt
hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/snaps
Found 2 items
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-27 10:27 /user/iabd/snaps/tirantloblanc.txt
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-27 10:29 /user/iabd/snaps/tirantloblanc_snapshot.txt
```

### 2.5 Creació de la primera instantània (`ss1`)
Generem la primera instantània (`ss1`) del directori `/user/iabd/snaps` que registra l'estat dels dos fitxers existents en aquest moment.

```bash
hadoop@hadoop-server:~$ hdfs dfs -createSnapshot /user/iabd/snaps ss1
Created snapshot /user/iabd/snaps/.snapshot/ss1
```

### 2.6 - 2.8 Esborrat accidental i recuperació des de Snapshot
Simulem la pèrdua de dades esborrant els fitxers i posteriorment recuperem el fitxer original des del directori ocult de la instantània (`.snapshot/ss1/`).

```bash
# 2.6 Eliminació de tots dos fitxers
hadoop@hadoop-server:~$ hdfs dfs -rm /user/iabd/snaps/tirantloblanc.txt /user/iabd/snaps/tirantloblanc_snapshot.txt
Deleted /user/iabd/snaps/tirantloblanc.txt
Deleted /user/iabd/snaps/tirantloblanc_snapshot.txt

# 2.7 Comprovació de directori buit
hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/snaps

# 2.8 Recuperació del fitxer des de la instantània ss1
hadoop@hadoop-server:~$ hdfs dfs -cp /user/iabd/snaps/.snapshot/ss1/tirantloblanc.txt /user/iabd/snaps/
hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/snaps
Found 1 items
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-27 10:35 /user/iabd/snaps/tirantloblanc.txt
```

### 2.9 - 2.10 Segona instantània (`ss2`) i comparativa d'estats
S'ha creat la segona instantània (`ss2`), la qual enregistra l'estat actual del directori on només es troba un únic fitxer (`tirantloblanc.txt`).

```bash
# 2.9 Creació de ss2
hadoop@hadoop-server:~$ hdfs dfs -createSnapshot /user/iabd/snaps ss2
Created snapshot /user/iabd/snaps/.snapshot/ss2

# 2.10 Comparació de continguts
hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/snaps
Found 1 items
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-27 10:35 /user/iabd/snaps/tirantloblanc.txt

hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/snaps/.snapshot/ss1
Found 2 items
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-27 10:27 /user/iabd/snaps/.snapshot/ss1/tirantloblanc.txt
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-27 10:29 /user/iabd/snaps/.snapshot/ss1/tirantloblanc_snapshot.txt

hadoop@hadoop-server:~$ hdfs dfs -ls /user/iabd/snaps/.snapshot/ss2
Found 1 items
-rw-r--r--   1 hadoop supergroup    1879325 2026-10-27 10:35 /user/iabd/snaps/.snapshot/ss2/tirantloblanc.txt
```

> **Demostració:** La instantània `ss1` manté la còpia dels dos fitxers originals malgrat haver sigut esborrats posteriorment del directori actiu, mentre que `ss2` reflecteix la situació actual amb un sol fitxer.

---

## 3. HDFS per dins: Metadades i Checkpoints

Analitzem com el NameNode gestiona la memòria i la persistència en disc del sistema de fitxers.

### 3.1 Identificació del directori de metadades (`hdfs-site.xml`)
Revisem el fitxer de configuració `$HADOOP_HOME/etc/hadoop/hdfs-site.xml` i identifiquem la propietat `dfs.namenode.name.dir`:

```xml
<property>
    <name>dfs.namenode.name.dir</name>
    <value>/home/hadoop/hdfs/namenode</value>
</property>
```
> **Ruta obtinguda:** `/home/hadoop/hdfs/namenode` és el directori local on el NameNode guarda les seves metadades persistents.

### 3.2 - 3.3 Exploració del directori `current` i fitxer `VERSION`
Accedim al directori `current` del NameNode i llistem els fitxers d'estat de les metadades:

```bash
hadoop@hadoop-server:~$ cd /home/hadoop/hdfs/namenode/current
hadoop@hadoop-server:~/hdfs/namenode/current$ ls -la
total 6312
drwx------ 2 hadoop hadoop    4096 oct 27 10:17 .
-rw-rw-r-- 1 hadoop hadoop    4685 oct 27 10:17 fsimage_0000000000000001417
-rw-rw-r-- 1 hadoop hadoop      62 oct 27 10:17 fsimage_0000000000000001417.md5
-rw-rw-r-- 1 hadoop hadoop 1048576 oct 27 10:37 edits_inprogress_0000000000000001418
-rw-rw-r-- 1 hadoop hadoop     213 oct 27 10:17 VERSION
```

Examen del fitxer `VERSION`:

```bash
hadoop@hadoop-server:~/hdfs/namenode/current$ cat VERSION
#Tue Oct 27 10:17:48 UTC 2026
namespaceID=998234356
blockpoolID=BP-1710563444-127.0.1.1-1790847296867
storageType=NAME_NODE
cTime=1790847296867
clusterID=CID-dcbf01be-08a5-4094-96ce-ebec0d626cda
layoutVersion=-67
```

### 3.4 - 3.7 Execució d'un Checkpoint manual (`saveNamespace` i Safemode)
Per consolidar el registre de canvis (`edits`) amb la imatge del sistema (`fsimage`), realitzem la següent seqüència:

```bash
# 3.4 Activar Safemode
hadoop@hadoop-server:~/hdfs/namenode/current$ hdfs dfsadmin -safemode enter
Safe mode is ON

# 3.6 Forçar la creació del checkpoint manual
hadoop@hadoop-server:~/hdfs/namenode/current$ hdfs dfsadmin -saveNamespace
Save namespace successful

# 3.7 Desactivar Safemode
hadoop@hadoop-server:~/hdfs/namenode/current$ hdfs dfsadmin -safemode leave
Safe mode is OFF
```

> **Verificació Web UI:** Durant el pas 3.5, es va accedir a `http://192.168.56.104:9870` observant el missatge: *"Safe mode is ON. It was turned on manually."*

### 3.8 Anàlisi i justificació del checkpoint sobre `fsimage`
Tornem a llistar el directori `current` després de l'operació:

```bash
hadoop@hadoop-server:~/hdfs/namenode/current$ ls -la
total 6316
-rw-rw-r-- 1 hadoop hadoop 6557 oct 27 10:54 edits_0000000000000001418-0000000000000001470
-rw-rw-r-- 1 hadoop hadoop 1048576 oct 27 10:54 edits_inprogress_0000000000000001471
-rw-rw-r-- 1 hadoop hadoop 4685 oct 27 10:17 fsimage_0000000000000001417
-rw-rw-r-- 1 hadoop hadoop 2649 oct 27 10:54 fsimage_0000000000000001470
-rw-rw-r-- 1 hadoop hadoop   62 oct 27 10:54 fsimage_0000000000000001470.md5
```

#### Raonament Teòric:
La comanda `saveNamespace` ha obligat el NameNode a consolidar totes les operacions que estaven pendents en els fitxers `edits`. En fer aquesta fusió, s'ha generat una imatge d'estat completament nova i actualitzada en disc (`fsimage_0000000000000001470`).

Aquest procés reinicia el registre de transaccions en un nou fitxer `edits_inprogress`, garantint una recuperació molt més ràpida del sistema en cas de fallada i evitant que els fitxers d'edicions creixin de manera indefinida.

---

## 4. Accés programàtic a HDFS amb Python

Instal·lació prèvia de dependències a la màquina:
```bash
sudo apt install python3-pip
pip install hdfs
```

### 4.1 Script de lectura via WebHDFS (`llegir_hdfs.py`)

Codi font de l'script:

```python
from hdfs import InsecureClient

# Connexió al client WebHDFS utilitzant el port 9870
client = InsecureClient('http://localhost:9870', user='iabd')

# Lectura de les primeres línies del fitxer
ruta_fitxer = '/user/iabd/snaps/tirantloblanc.txt'

with client.read(ruta_fitxer, encoding='utf-8') as reader:
    contingut = reader.read()
    # Mostrem els primers 300 caràcters / primeres línies
    print(contingut[:300])
```

Execució i sortida per pantalla:

```bash
hadoop@hadoop-server:~$ python3 llegir_hdfs.py
SINOPSI
El Tirant lo Blanc és la més important de les novel·les escrites en
llengua catalana i, probablement, la millor de la literatura europea
del seu temps. L'obra de Joanot Martorell transcendeix els llibres de
cavalleries medievals, per la mentalitat, per l'amplitud de mires, per
l'humor, perq
```

### 4.2 Script de creació i escriptura de CSV (`crear_csv_hdfs.py`)

Codi font de l'script:

```python
from hdfs import InsecureClient
from datetime import datetime

# Connexió a WebHDFS
client = InsecureClient('http://localhost:9870', user='iabd')

# Dades personalitzades
nom = "Sergi"
cognoms = "Gallart Fanlo"
data_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Contingut del fitxer CSV amb capçalera
contingut_csv = f"Nom, Cognoms, Data\n{nom}, {cognoms}, {data_actual}\n"

# Ruta de destí a HDFS
ruta_hdfs = '/user/iabd/dades.csv'

# Escriptura directa a HDFS (overwrite=True per si ja existeix)
client.write(ruta_hdfs, data=contingut_csv, encoding='utf-8', overwrite=True)
print(f"Fitxer desat correctament a {ruta_hdfs}")
```

Execució i verificació final a HDFS:

```bash
hadoop@hadoop-server:~$ python3 crear_csv_hdfs.py
Fitxer desat correctament a /user/iabd/dades.csv

hadoop@hadoop-server:~$ hdfs dfs -cat /user/iabd/dades.csv
Nom, Cognoms, Data
Sergi, Gallart Fanlo, 2026-10-27 11:09:26
```