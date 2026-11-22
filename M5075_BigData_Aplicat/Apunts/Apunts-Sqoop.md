# Apache Sqoop — Apunts extensos

## Índex

1. [Introducció i paper dins de Big Data](#1-introducció-i-paper-dins-de-big-data)
2. [Arquitectura i funcionament intern](#2-arquitectura-i-funcionament-intern)
3. [Instal·lació i comprovacions inicials](#3-installació-i-comprovacions-inicials)
4. [Sintaxi de les importacions](#4-sintaxi-de-les-importacions)
5. [Cas 1: MariaDB → HDFS](#5-cas-1-mariadb--hdfs)
6. [Interpretar els logs i monitorar YARN](#6-interpretar-els-logs-i-monitorar-yarn)
7. [Recuperar fitxers i importar totes les taules](#7-recuperar-fitxers-i-importar-totes-les-taules)
8. [Cas 2: HDFS → MariaDB](#8-cas-2-hdfs--mariadb)
9. [Formats Avro i Parquet](#9-formats-avro-i-parquet)
10. [Eines per inspeccionar Avro i Parquet](#10-eines-per-inspeccionar-avro-i-parquet)
11. [Compressió de dades](#11-compressió-de-dades)
12. [Importacions filtrades i consultes personalitzades](#12-importacions-filtrades-i-consultes-personalitzades)
13. [Importacions incrementals](#13-importacions-incrementals)
14. [Sqoop i Apache Hive](#14-sqoop-i-apache-hive)
15. [Paràmetres i comandes imprescindibles](#15-paràmetres-i-comandes-imprescindibles)
16. [Errors freqüents i diagnòstic](#16-errors-freqüents-i-diagnòstic)
17. [Bones pràctiques](#17-bones-pràctiques)
18. [Comparatives i esquemes per memoritzar](#18-comparatives-i-esquemes-per-memoritzar)
19. [Exercicis pràctics proposats](#19-exercicis-pràctics-proposats)
20. [Preguntes d'autoavaluació amb resposta](#20-preguntes-dautoavaluació-amb-resposta)
21. [Glossari](#21-glossari)
22. [Resum final d'examen](#22-resum-final-dexamen)

---

## 1. Introducció i paper dins de Big Data

### 1.1. Què és Apache Sqoop?

**Apache Sqoop** és una eina per **transferir dades estructurades** entre sistemes de bases de dades relacionals (com MariaDB, MySQL, PostgreSQL, Oracle o SQL Server, segons el connector) i l'ecosistema Hadoop, especialment **HDFS** i **Hive**. La idea és evitar programar a mà la transferència de milions de registres: Sqoop es connecta a la base de dades, detecta l'esquema i organitza la transferència en tasques paral·leles.

- **Importar:** base de dades relacional → Hadoop/HDFS (i, opcionalment, Hive).
- **Exportar:** Hadoop/HDFS → base de dades relacional.
- **Importació incremental:** recuperar únicament els registres nous respecte d'una càrrega anterior.
- **Transformar la representació:** guardar dades en fitxers de text, Avro o Parquet, entre d'altres opcions compatibles.

El PDF presenta Sqoop i Flume com a dues eines d'ingesta: **Sqoop** està enfocada principalment en dades estructurades de bases de dades, mentre que **Flume** està orientada a fluxos d'esdeveniments i registres.

### 1.2. Per què és útil?

Imagina una aplicació de gestió escolar amb una taula de professors en MariaDB. Per fer anàlisis massives en Hadoop, necessitem copiar-ne la informació. Sqoop evita exportar manualment la taula a CSV, pujar el fitxer i programar la càrrega: una comanda pot coordinar aquesta operació.

Exemples d'utilització:

- Alimentar un *data lake* a partir de dades transaccionals.
- Fer còpies analítiques periòdiques de taules relacionals.
- Preparar dades perquè s'explotin amb Hive.
- Tornar a publicar un resultat processat cap a una base de dades operacional.

### 1.3. Estat del projecte

**Important:** segons el PDF, el projecte Apache Sqoop va passar a l'Apache Attic el juny de 2021 i ja no té manteniment actiu. S'estudia per conèixer-ne el funcionament i perquè continua present en entorns heretats i en la màquina virtual docent. El document esmenta **Apache NiFi** i **Spark** com a eines capaces de cobrir moltes de les seves funcionalitats. Això no significa que siguin substituts idèntics en totes les configuracions.

---

## 2. Arquitectura i funcionament intern

### 2.1. Relació amb Hadoop

Sqoop utilitza **connectors JDBC**, inspecciona les metadades d'una taula i crea tasques **MapReduce** que es reparteixen les dades. En el funcionament que presenta el PDF, les tasques *map* llegeixen fragments de la taula i escriuen cadascuna un fitxer de sortida a HDFS.

```text
                    IMPORTACIÓ
┌───────────────────────┐
│ MariaDB / base SQL    │
│ Taula: professors     │
└───────────┬───────────┘
            │ JDBC + metadades
            ▼
┌───────────────────────┐
│ Apache Sqoop          │
│ Divideix el treball   │
└───────────┬───────────┘
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
   Map 1  Map 2  Map N
     │      │      │
     ▼      ▼      ▼
┌───────────────────────┐
│ HDFS                  │
│ part-m-00000          │
│ part-m-00001          │
│ ...                   │
└───────────────────────┘
```

**No s'ha de confondre** el nombre de *mappers* amb el nombre físic de nodes: quatre mappers no vol dir necessàriament quatre ordinadors diferents. Es poden executar al mateix node, especialment a la màquina virtual de classe.

### 2.2. Fases d'una importació

**Primera fase — Inspecció:** Sqoop es connecta a MariaDB, consulta els tipus i els camps de la taula i prepara el codi necessari per llegir els registres. En els logs del PDF apareixen consultes com `SELECT t.* FROM professors AS t WHERE 1 = 0`: permeten obtenir l'esquema sense retornar totes les files.

**Segona fase — Divisió i càrrega:** calcula les divisions (per exemple, amb `MIN(id)` i `MAX(id)`), genera un *job* i cadascun dels mappers llegeix els registres que li corresponen. Els resultats s'escriuen a HDFS.

### 2.3. Què significa `-m`?

L'opció `-m` (o `--num-mappers`) indica el nombre de tasques map per a la transferència. **En el PDF, per defecte són 4** si no s'indica un altre valor.

```bash
-m 1   # un únic mapper
-m 2   # dos mappers
-m 4   # quatre mappers
```

- Amb `-m 1`, la lectura és simple, però hi ha menys paral·lelisme.
- Amb múltiples mappers, Sqoop necessita dividir les dades mitjançant una columna adequada, habitualment una clau numèrica.
- Per a taules petites, executar molts mappers pot consumir més recursos dels que s'estalvien.

### 2.4. `--split-by` i divisió de registres

`--split-by id` especifica la columna emprada per repartir la lectura. Per exemple, si els valors van de l'1 al 1000, Sqoop pot construir fragments de rangs per consultar-los en paral·lel. **El repartiment per rangs no garanteix que tots els mappers rebin exactament la mateixa quantitat de files**: dependrà de la distribució real dels identificadors.

El PDF mostra que el log informa de la consulta de valors límit i del nombre de *splits*.

---

## 3. Instal·lació i comprovacions inicials

### 3.1. Màquina virtual de classe

El PDF indica que **Hadoop i Sqoop ja estan instal·lats**. La prioritat és comprovar connectivitat, configuració de `master`, serveis i llibreries JDBC.

**Resolució del nom `master`:** identificar la IP de la interfície de xarxa de la màquina virtual (el document esmenta `enp0s3`, escrit amb una variant tipogràfica) i revisar `/etc/hosts`, de manera que el nom `master` apunti a la IP correcta.

```bash
ip addr
cat /etc/hosts
sudo nano /etc/hosts
```

La línia corresponent ha de seguir el patró:

```text
IP_DE_LA_MAQUINA  master
```

Substitueix el marcador per la IP real. **No copiïs una IP d'una altra màquina.**

### 3.2. Historial de comandes

El professor proposa editar `/home/iabd/.bashrc` i configurar:

```bash
HISTSIZE=500
HISTFILESIZE=500
```

`HISTSIZE` controla aproximadament les comandes conservades en memòria per la sessió del shell i `HISTFILESIZE` la mida de l'historial guardat. Reinicia la sessió o recarrega el fitxer si cal.

### 3.3. Connectors i dependències

El material indica dues dependències que s'han incorporat a `$SQOOP_HOME/lib`:

1. **Driver JDBC de MySQL** per comunicar-se amb la base de dades MariaDB/MySQL de l'entorn.
2. **`commons-lang-2.6`**, llibreria Java requerida en aquesta instal·lació.

Les versions exactes de les llibreries depenen de la distribució i de la compatibilitat de l'entorn. No convé copiar JARs arbitràriament entre versions sense comprovar-les.

### 3.4. Comprovació de bases de dades

```bash
sqoop list-databases \
  --connect jdbc:mysql://localhost \
  --username=iabd \
  --password=iabd
```

Aquest exemple utilitza les credencials **de laboratori del PDF**, no aptes per a entorns reals. Una opció més segura quan es treballa amb Sqoop és `-P`, que demana la contrasenya de forma interactiva i evita deixar-la directament a la línia d'ordres.

```bash
sqoop list-databases \
  --connect jdbc:mysql://localhost \
  --username=iabd -P
```

Si retorna les bases de dades, la connectivitat bàsica JDBC funciona. Alguns avisos (*WARN*) poden no ser fatals.

---

## 4. Sintaxi de les importacions

### 4.1. Estructura general

```bash
sqoop import \
  --connect jdbc:mysql://HOST/BASE_DE_DADES \
  --table NOM_TAULA \
  --username USUARI \
  -P \
  -m 2
```

Aquesta ordre transfereix la taula cap a Hadoop. Per controlar on s'escriu i quin format es genera, s'afegeixen altres paràmetres.

### 4.2. Paràmetres freqüents

| Paràmetre | Funció |
|---|---|
| `--connect` | URI JDBC de la base de dades |
| `--username` | Nom d'usuari de la base de dades |
| `--password` | Contrasenya literal (no recomanable fora del laboratori) |
| `-P` | Demana la contrasenya de manera interactiva |
| `--table` | Taula d'origen |
| `--target-dir` | Carpeta de destinació a HDFS |
| `--driver` | Classe del controlador JDBC emprat |
| `--fields-terminated-by` | Separador entre camps en fitxers de text |
| `--lines-terminated-by` | Separador de registres |
| `--delete-target-dir` | Elimina el directori de destí si ja existeix |
| `-m` | Nombre de mappers |
| `--split-by` | Columna usada per al particionat de lectura |
| `--where` | Filtre SQL |
| `--columns` | Llista de columnes a importar |
| `--query` | Consulta SQL personalitzada |

### 4.3. Separadors de text

Aquest fragment:

```bash
--fields-terminated-by=',' --lines-terminated-by='\n'
```

indica que els camps d'un registre han d'anar separats per comes i que els registres acabin amb un salt de línia. En fitxers CSV reals, també s'han de considerar camps que ja contenen comes, cometes i salts de línia; un delimitador simple no resol necessàriament tots aquests casos.

### 4.4. Directori de destinació

```bash
--target-dir=/user/iabd/sqoop/professors_hdfs
```

La ruta és **d'HDFS**, no del disc local. Per comprovar-ne l'existència:

```bash
hdfs dfs -ls /user/iabd/sqoop/professors_hdfs
```

**Atenció:** `--delete-target-dir` és destructiu: esborra prèviament el contingut del directori d'arribada. En exercicis és còmode; en producció només s'ha d'utilitzar amb garanties que la carpeta és la correcta.

---

## 5. Cas 1: MariaDB → HDFS

**Objectiu:** crear una taula `professors` a MariaDB i copiar-ne les files a HDFS amb Sqoop (pàgines 7–13).

### 5.1. Preparar la base de dades

El PDF proposa revisar els privilegis de l'usuari `iabd`. Mostra una instrucció `GRANT ALL PRIVILEGES ON *.* ... WITH GRANT OPTION`; és un permís molt ampli i s'ha de considerar **exclusiu de la màquina docent**, no una configuració recomanada en sistemes reals.

Entrem a MariaDB:

```bash
mariadb -u iabd -p
```

Creem la base i la taula:

```sql
CREATE DATABASE sqoopCas1;
USE sqoopCas1;

CREATE TABLE professors (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    nom CHAR(30) NOT NULL,
    edat INTEGER,
    materia CHAR(30),
    PRIMARY KEY (id)
);
```

**Explicació dels camps:** `id` identifica inequívocament cada professor i augmenta automàticament; `nom` conté un text de longitud fixa màxima; `edat` és un enter; `materia` és la matèria impartida. L'identificador facilita el particionat dels registres per mappers.

### 5.2. Afegir registres de prova

```sql
INSERT INTO professors (nom, edat, materia) VALUES
('Carles', 24, 'Matematiques'),
('Pere', 32, 'Anglès'),
('Joan', 35, 'Tecnologia'),
('Josep', 48, 'Matematiques'),
('Paula', 24, 'Informàtica'),
('Sussana', 32, 'Informàtica'),
('Lorena', 54, 'Informatica');

SELECT * FROM professors;
SELECT COUNT(*) FROM professors;
```

Hi haurà **7 registres** si la taula era buida. Observa que el PDF escriu `Informàtica` i `Informatica` amb i sense accent: aquesta diferència pot afectar els filtres en funció de la col·lació de MariaDB.

### 5.3. Zona horària

El material recomana verificar la zona horària de MariaDB, perquè les dades temporals poden convertir-se segons el sistema. Indica l'ajust a `Europe/Madrid` a la configuració de MariaDB i afirma que a la màquina de classe ja està preparat. La secció corresponent del document conté una errada tipogràfica al nom del bloc de configuració; comprova la sintaxi adequada abans de modificar un servidor.

### 5.4. Arrencar els serveis Hadoop

```bash
start-dfs.sh
start-yarn.sh
```

- **HDFS:** proporciona l'emmagatzematge distribuït.
- **YARN:** gestiona els recursos i l'execució de treballs.

Pots revisar els processos Java:

```bash
jps
```

### 5.5. Llistar les taules disponibles

```bash
sqoop list-tables \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd
```

La taula `professors` hauria d'aparèixer si s'ha creat a la base correcta i el connector funciona.

### 5.6. Fer la importació

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_hdfs \
  --fields-terminated-by=',' --lines-terminated-by='\n' \
  --delete-target-dir -m 2
```

**Què fa aquesta comanda?** Es connecta a `sqoopCas1`, llegeix `professors`, crea registres separats per comes, esborra el directori de destinació si existeix, i transfereix les dades a HDFS amb dos mappers.

**Observació sobre el PDF:** l'exemple original escriu `-m=2`, mentre que aquí apareix `-m 2`, forma més habitual. El log reproduït en el document mostra *quatre* mappers, de manera que no s'ha de concloure que aquell log prové exactament de l'execució de la comanda amb dos.

### 5.7. Comprovar el resultat a HDFS

```bash
hdfs dfs -ls /user/iabd/sqoop/professors_hdfs
hdfs dfs -cat /user/iabd/sqoop/professors_hdfs/part-m-00000
```

El nombre de fitxers `part-m-*` depèn de com s'ha executat el job. El PDF mostra també un fitxer `_SUCCESS`, que marca que el job s'ha completat correctament.

### 5.8. Interpretació de l'èxit

Si els comptadors indiquen `Retrieved 7 records`, vol dir que la importació del cas d'exemple ha llegit set files. Però comprova també la carpeta HDFS: l'existència de fitxers i la seva lectura donen una verificació independent dels logs.

---

## 6. Interpretar els logs i monitorar YARN

### 6.1. Informació que convé localitzar

El document inclou diverses pàgines de logs. En una revisió d'examen no cal memoritzar les marques de temps exactes, sinó interpretar els missatges importants:

| Entrada del log | Significat |
|---|---|
| `Running Sqoop version ...` | Versió de Sqoop |
| `Setting your password on the command-line is insecure` | Avís de seguretat |
| `Beginning code generation` | Preparació de les classes per llegir la taula |
| `SELECT ... WHERE 1 = 0` | Lectura de metadades sense files |
| `BoundingValsQuery: SELECT MIN(id), MAX(id)` | Consulta dels límits de particionat |
| `number of splits` | Nombre de fragments de treball |
| `Submitting ... job` | Enviament del treball a Hadoop/YARN |
| `map 0%`, `map 50%`, `map 100%` | Progrés de les tasques map |
| `completed successfully` | El job ha finalitzat amb èxit |
| `Map input records` / `Map output records` | Registres llegits i processats |
| `Retrieved 7 records` | Files transferides en l'exemple |

### 6.2. `WARN` no vol dir sempre error

Poden aparèixer avisos de dependències, opcions antigues o contrasenyes a la línia de comandes. Cal distingir un **avís** d'un **error que interromp l'execució**. Si no existeixen fitxers de sortida o el job queda com a `FAILED`, cal examinar-ne l'excepció concreta.

### 6.3. Monitoratge al navegador

El PDF mostra dues interfícies:

- **YARN ResourceManager:** `http://iabd-virtualbox:8088/cluster`, per veure l'aplicació, el seu estat i els jobs.
- **HDFS NameNode:** `http://iabd-virtualbox:9870`, per navegar pels directoris i fitxers distribuïts.

Els noms de màquina són propis de l'entorn docent. Poden canviar segons `/etc/hosts` i la configuració de Hadoop.

### 6.4. Error «Unhealthy node»

El material explica que una màquina virtual amb poc espai de disc pot fer que YARN declari el node **no saludable**. Com a possibilitat de laboratori, esmenta canviar límits del verificador de salut de discs a `yarn-site.xml` perquè sigui més permissiu.

**Criteri important:** abans de relaxar les comprovacions de YARN, és preferible alliberar espai, inspeccionar el disc amb `df -h` i revisar fitxers temporals i logs. Desactivar proteccions pot ocultar un problema real i provocar errors posteriors. Les propietats mostrades al PDF s'han de revisar amb cura per evitar errades de nomenclatura.

---

## 7. Recuperar fitxers i importar totes les taules

### 7.1. Per què hi ha diversos fragments?

Cada mapper acostuma a escriure una part del resultat. Per això no hem d'esperar un únic CSV, sinó diversos fitxers com `part-m-00000` i `part-m-00001`.

### 7.2. Fusionar-los amb `-getmerge`

```bash
hdfs dfs -getmerge /user/iabd/sqoop/professors_hdfs professors.csv
```

Aquesta comanda **llegeix els fragments d'HDFS i els fusiona en un fitxer local** anomenat `professors.csv`. És especialment útil per entregar o inspeccionar el resultat, però pot requerir molt espai local quan el volum de dades és gran.

### 7.3. Importar totes les taules d'una base

```bash
sqoop import-all-tables \
  --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --driver=com.mysql.jdbc.Driver \
  --warehouse-dir=/user/iabd/sqoop \
  --fields-terminated-by=',' --lines-terminated-by='\n'
```

**Diferència:** `sqoop import` selecciona una taula concreta amb `--table`; `sqoop import-all-tables` intenta importar les taules de la base i crea una carpeta per taula sota el `--warehouse-dir`. El PDF presenta aquest mecanisme a les pàgines 13–14.

**Precaució:** els permisos, les claus, les característiques de cada taula i la compatibilitat de tipus poden fer que alguna importació no prosperi. Cal revisar el resultat de cada taula.

---

## 8. Cas 2: HDFS → MariaDB

### 8.1. Objectiu

Ara fem el recorregut contrari: partim dels fitxers que hem creat a HDFS i els carreguem a una **taula existent** de MariaDB.

```text
HDFS /user/iabd/sqoop/professors_hdfs
                 │
                 ▼
           sqoop export
                 │ JDBC
                 ▼
    MariaDB: sqoopCas2.professors2
```

### 8.2. Crear una base i taula receptores

```bash
mariadb -u iabd -p
```

```sql
CREATE DATABASE sqoopCas2;
USE sqoopCas2;

CREATE TABLE professors2 (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    nom CHAR(30) NOT NULL,
    edat INTEGER,
    materia CHAR(30),
    PRIMARY KEY (id)
);
```

**Molt important:** Sqoop Export no pressuposa que la taula final s'hagi de crear; el PDF explica que si no existeix prèviament, l'operació fallarà.

### 8.3. Exportar les dades

```bash
sqoop export \
  --connect jdbc:mysql://localhost/sqoopCas2 \
  --username=iabd --password=iabd \
  --table=professors2 \
  --export-dir=/user/iabd/sqoop/professors_hdfs \
  --input-fields-terminated-by=','
```

L'exemple del PDF **no inclou** `--input-fields-terminated-by=','`, malgrat haver importat els fitxers de text separats per comes al Cas 1. L'hem afegit perquè l'exportació interpreti correctament aquests fitxers: és una **adaptació pràctica**, no una transcripció literal.

Verificació:

```sql
USE sqoopCas2;
SELECT * FROM professors2;
SELECT COUNT(*) FROM professors2;
```

### 8.4. Què passa si ja existeixen els identificadors?

Si s'intenten inserir files amb una clau primària que ja existeix, pot aparèixer un error de duplicació. El document introdueix:

```bash
--update-key id
```

amb la intenció d'actualitzar les files segons la columna `id`. Si volem una combinació d'actualització de files existents i inserció de files que encara no hi són, el PDF mostra:

```bash
--update-key id --update-mode allowinsert
```

Exemple adaptat (la taula `professors2` és la creada en aquest cas):

```bash
sqoop export \
  --connect jdbc:mysql://localhost/sqoopCas2 \
  --username=iabd --password=iabd \
  --table=professors2 \
  --export-dir=/user/iabd/sqoop/professors_hdfs \
  --input-fields-terminated-by=',' \
  --update-key id --update-mode allowinsert
```

**Precisió sobre el PDF:** en l'exemple d'actualització apareix `--table=professors`, però en `sqoopCas2` la taula que acabem de crear es diu `professors2`. S'ha ajustat el nom per fer-lo coherent amb la pràctica.

---

## 9. Formats Avro i Parquet

### 9.1. Per què és important el format?

Sqoop pot transportar els mateixos registres però representar-los de maneres diferents. Això afecta la mida, la lectura, la integració amb altres sistemes i el rendiment de consultes analítiques.

| Propietat | Avro | Parquet |
|---|---|---|
| Organització | Orientat a files | Orientat a columnes |
| Descripció de l'esquema | Esquema Avro, habitualment expressat en JSON | Metadades d'esquema integrades al fitxer |
| Representació de dades | Binària | Binària |
| Ús habitual | Intercanvi/serialització de registres | Anàlisi de columnes i emmagatzematge analític |
| Lectura d'un fitxer amb `cat` | No és text llegible directament | No és text llegible directament |

### 9.2. Importar en Avro

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_avro \
  --as-avrodatafile \
  --delete-target-dir
```

`--as-avrodatafile` demana que el resultat es codifiqui com a fitxers de dades Avro. El document explica que pot ser necessari ajustar les versions de les llibreries Avro de Sqoop i Hadoop; en la màquina virtual aquest pas **no està realitzat** segons el PDF.

### 9.3. Importar en Parquet

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_parquet \
  --as-parquetfile \
  --delete-target-dir
```

`--as-parquetfile` selecciona el format Parquet. En aquesta estructura de columnes, és habitual que una consulta que necessita només unes quantes columnes pugui llegir menys dades que amb un format orientat a files, encara que el resultat concret depèn del motor i del conjunt de dades.

### 9.4. Què ens indiquen les extensions?

A HDFS es poden crear fitxers `part-m-00000.avro` o fitxers `.parquet` amb noms generats. `_SUCCESS` és un marcador de finalització del job, **no un fitxer amb els registres importats**.

---

## 10. Eines per inspeccionar Avro i Parquet

### 10.1. Llistar fitxers Avro

```bash
hdfs dfs -ls /user/iabd/sqoop/professors_avro
```

Per llegir-los amb el convertidor de Hadoop presentat al PDF:

```bash
hdfs dfs -text /user/iabd/sqoop/professors_avro/part-m-00000.avro
```

La sortida pot mostrar una representació textual dels registres, amb els camps i tipus d'Avro. El document dona exemples de noms i edats de professors.

### 10.2. Per què `-tail` mostra caràcters estranys?

```bash
hdfs dfs -tail /user/iabd/sqoop/professors_avro/part-m-00000.avro
```

**Resposta de l'autoavaluació del PDF:** Avro guarda dades en format binari. `-tail` mostra els bytes finals, que no tenen per què correspondre a text llegible. Per interpretar el contingut correctament s'ha d'utilitzar una eina conscient del format.

### 10.3. `avro-tools`

El PDF descriu aquesta instal·lació de laboratori:

```bash
cd /tmp
wget https://repo1.maven.org/maven2/org/apache/avro/avro-tools/1.11.3/avro-tools-1.11.3.jar
sudo mkdir -p /opt/avro-tools
sudo mv avro-tools-1.11.3.jar /opt/avro-tools/
```

Crear l'script `/usr/local/bin/avro-tools`:

```bash
#!/bin/bash
java -jar /opt/avro-tools/avro-tools-1.11.3.jar "$@"
```

I donar-li permisos:

```bash
sudo chmod +x /usr/local/bin/avro-tools
```

Convertir els registres a JSON:

```bash
hdfs dfs -cat /user/iabd/sqoop/professors_avro/part-m-00000.avro | avro-tools tojson -
```

**Nota:** les instruccions són les del PDF i pressuposen Java, connectivitat i compatibilitat de versions amb aquest JAR. El subcomandament `tojson` serveix per mostrar els registres en una representació llegible.

### 10.4. Inspeccionar Parquet

```bash
hdfs dfs -ls /user/iabd/sqoop/professors_parquet
```

El document proposa `parquet-tools` en Python:

```bash
pip3 install parquet-tools
```

i una variant Java per inspeccionar dades en HDFS, amb comandes com:

```bash
hadoop jar parquet-tools-1.11.2.jar head -n5 hdfs://HOST:9000/RUTA/fitxer.parquet
hadoop jar parquet-tools-1.11.2.jar meta hdfs://HOST:9000/RUTA/fitxer.parquet
```

`head` consulta els primers registres; `meta` informa de l'esquema i les metadades del fitxer. **El PDF adverteix de problemes de compatibilitat** entre determinades versions de Sqoop i Parquet: l'eina concreta pot no funcionar en totes les instal·lacions.

---

## 11. Compressió de dades

### 11.1. Per què comprimir?

La compressió redueix l'espai consumit per les dades, especialment rellevant si les conservem durant anys. Hi ha un compromís entre mida, velocitat de compressió/descompressió i capacitat de dividir els fitxers per processar-los. El document il·lustra Gzip, Bzip2 i Snappy.

### 11.2. Gzip

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_gzip \
  --compress
```

Segons el PDF, `--compress` utilitza **gzip** per defecte en aquest exemple.

### 11.3. Bzip2

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_bzip \
  --compress --compression-codec bzip2
```

`--compression-codec` permet indicar quin compressor es vol emprar.

### 11.4. Snappy

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_snappy \
  --compress --compression-codec snappy
```

El PDF destaca Snappy com a biblioteca de compressió/descompressió d'alt rendiment utilitzada habitualment en Big Data.

### 11.5. Comparació conceptual

- **Gzip:** compressió habitual de propòsit general; no és l'opció més còmoda per dividir un sol fitxer comprimit en diverses tasques.
- **Bzip2:** sol buscar una compressió més alta, a canvi de cost computacional; ofereix propietats de divisió útils amb determinats formats i lectors.
- **Snappy:** prioritza la velocitat, molt útil en pipelines i formats analítics.

Aquesta comparació és una ampliació didàctica: el PDF presenta sobretot les opcions de comanda, no una prova quantitativa dels tres còdecs.

---

## 12. Importacions filtrades i consultes personalitzades

### 12.1. Filtrar files amb `--where`

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_materia_info \
  --where "materia='Informatica'"
```

`--where` introdueix una condició SQL que s'aplica a la base d'origen. Només es transfereixen les files que compleixen la condició.

**Atenció al joc de prova:** a la inserció inicial trobem `Informàtica` i `Informatica`. El resultat d'aquest filtre pot dependre de la col·lació, els accents i les files concretes.

### 12.2. Seleccionar columnes amb `--columns`

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_cols \
  --columns "nom,materia"
```

Només copia les dues columnes indicades. Això evita transferir camps que no necessitem. En algunes situacions, si l'operació té múltiples mappers, cal garantir una columna adequada per al particionat o ajustar `-m`.

### 12.3. Consulta personalitzada amb `--query`

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_query \
  --query "select * from professors where edat > 40 AND \$CONDITIONS" \
  --split-by id
```

Aquesta operació importa els professors de més de quaranta anys, deixant que Sqoop insereixi la condició de particionat al lloc de **`$CONDITIONS`**.

### 12.4. Per què s'escapa `$CONDITIONS`?

El símbol `$` té un significat especial per a Bash (expansió de variables). Si la consulta s'escriu entre cometes dobles, `\$CONDITIONS` evita que el shell intenti substituir-lo abans que Sqoop rebi el text. Una altra opció és formular les cometes adequadament perquè arribi el token literal.

### 12.5. El paper de `--split-by id`

Amb una consulta personalitzada, aquesta propietat indica quin camp serveix per definir els intervals dels diferents mappers. Cada tasca executa la consulta amb una condició de rang addicional. Les pàgines 24–25 del PDF mostren un exemple conceptual de rangs com `id >= 250 AND id < 500`.

### 12.6. `--where`, `--columns` i `--query`: comparació

| Necessitat | Opció adequada |
|---|---|
| Importar només unes files | `--where` |
| Importar només unes columnes | `--columns` |
| Fer una consulta SQL més elaborada | `--query` |
| Dividir explícitament la lectura per un camp | `--split-by` |

---

## 13. Importacions incrementals

### 13.1. El problema de repetir una càrrega completa

Suposa que dilluns importem els professors que tenen identificadors `1` a `4`. Dimarts se n'han afegit tres més. En lloc de tornar a importar tots els registres podem demanar **únicament els nous**.

### 13.2. Sintaxi del document

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --target-dir=/user/iabd/sqoop/professors_inc \
  --incremental append \
  --check-column id \
  --last-value 4
```

### 13.3. Què indica cada propietat?

- `--incremental append`: mode incremental basat en registres afegits.
- `--check-column id`: columna que indica l'ordre de creixement i permet detectar registres nous.
- `--last-value 4`: darrera marca de control processada anteriorment.

En aquest exemple, es recuperen els registres amb identificadors posteriors a `4`, subjecte a les condicions pròpies de Sqoop i del dataset.

### 13.4. Com preparar la següent execució?

El PDF mostra que, després de la importació, Sqoop suggereix els arguments de la següent càrrega, ara amb `--last-value 7`, després de recuperar els registres fins al setè identificador.

```text
Incremental import complete!
--incremental append
--check-column id
--last-value 7
```

Això permet actualitzar la marca de control (*watermark*) de les properes execucions. El document també suggereix conservar la definició mitjançant `sqoop job --create`.

### 13.5. Limitacions del mode append

**Molt important per entendre el concepte:** `append` funciona bé quan els nous registres tenen un valor de control creixent, per exemple una clau autoincremental. **No detecta modificacions fetes a files antigues** amb identificador inferior a l'últim valor processat. Tampoc no resol per si sol eliminacions a la base d'origen.

Aquesta distinció és una ampliació explicativa que ajuda a no confondre «importació incremental» amb «sincronització completa».

---

## 14. Sqoop i Apache Hive

### 14.1. Què aporta Hive?

HDFS emmagatzema fitxers, mentre que **Hive** permet definir taules i consultar els registres amb un llenguatge similar a SQL. La integració de Sqoop amb Hive evita fer la importació i, després, crear tota la càrrega en Hive manualment.

### 14.2. Importar a una taula Hive

```bash
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd --password=iabd \
  --table=professors --driver=com.mysql.jdbc.Driver \
  --hive-import --hive-database default \
  --create-hive-table --hive-table professors_mariadb
```

Paràmetres nous:

- `--hive-import`: activa la integració d'importació a Hive.
- `--hive-database default`: selecciona la base de dades Hive.
- `--create-hive-table`: demana crear la taula corresponent.
- `--hive-table professors_mariadb`: nom de la taula dins d'Hive.

El PDF remarca que, en aquest cas d'ús, **no s'indica `--target-dir`** a l'exemple.

### 14.3. Comprovar que existeix a Hive

```sql
DESCRIBE FORMATTED professors_mariadb;
SELECT * FROM professors_mariadb;
```

`DESCRIBE FORMATTED` mostra dades sobre l'esquema, la ubicació i altres propietats de la taula. També és útil comprovar que els tipus i els camps s'han interpretat correctament.

### 14.4. Exportar des de Hive mitjançant HCatalog

El PDF presenta un exemple d'exportació utilitzant el catàleg de Hive:

```bash
sqoop export --connect jdbc:mysql://localhost/sqoopCas2 \
  --username=iabd --password=iabd \
  --table=professors2 --driver=com.mysql.jdbc.Driver \
  --h-catalog-table professors_mariadb
```

**Nota de transcripció:** el document mostra `--h-catalog-table`. En distribucions de Sqoop 1.x és habitual trobar l'opció **`--hcatalog-table`** (sense els guions interiors). Cal revisar la sintaxi de la versió instal·lada (`sqoop help export`) abans d'executar-la. Aquest punt queda assenyalat perquè no es copiï una opció potencialment invàlida.

### 14.5. Relació amb Flume i Hive

```text
MariaDB  ── Sqoop ──► HDFS ──► Hive
                       ▲
Logs ──── Flume ───────┘
```

En un pipeline analític, Sqoop i Flume poden alimentar un magatzem distribuït des de fonts diferents; Hive proporciona una forma d'analitzar les dades un cop disponibles.

---

## 15. Paràmetres i comandes imprescindibles

| Comanda o opció | Per a què serveix? | Exemple curt |
|---|---|---|
| `sqoop list-databases` | Veure bases del servidor | `sqoop list-databases --connect jdbc:mysql://localhost ...` |
| `sqoop list-tables` | Veure taules d'una base | `sqoop list-tables --connect jdbc:mysql://localhost/sqoopCas1 ...` |
| `sqoop import` | Base de dades → HDFS | `sqoop import --table professors ...` |
| `sqoop export` | HDFS → base de dades | `sqoop export --table professors2 ...` |
| `sqoop import-all-tables` | Importar diverses taules | `--warehouse-dir /user/iabd/sqoop` |
| `--target-dir` | Ruta de destí a HDFS | `--target-dir /user/iabd/sqoop/professors_hdfs` |
| `--export-dir` | Ruta d'origen d'HDFS per exportar | `--export-dir /user/iabd/sqoop/professors_hdfs` |
| `--delete-target-dir` | Esborrar directori abans d'importar | `--delete-target-dir` |
| `--where` | Filtre de files | `--where "edat>40"` |
| `--columns` | Selecció de camps | `--columns "nom,materia"` |
| `--query` | Consulta personalitzada | `--query "SELECT ... AND \$CONDITIONS"` |
| `--as-avrodatafile` | Sortida Avro | `--as-avrodatafile` |
| `--as-parquetfile` | Sortida Parquet | `--as-parquetfile` |
| `--compress` | Compressió de la sortida | `--compress` |
| `--compression-codec` | Escollir el còdec | `--compression-codec snappy` |
| `--incremental append` | Carregar registres nous | `--incremental append` |
| `--check-column` | Columna de control | `--check-column id` |
| `--last-value` | Últim valor processat | `--last-value 4` |
| `--hive-import` | Importar a Hive | `--hive-import` |
| `--hive-table` | Nom de la taula Hive | `--hive-table professors_mariadb` |
| `hdfs dfs -ls` | Llistar fitxers HDFS | `hdfs dfs -ls /user/iabd/sqoop` |
| `hdfs dfs -cat` | Llegir un fitxer de text HDFS | `hdfs dfs -cat RUTA` |
| `hdfs dfs -getmerge` | Fusionar fragments en un fitxer local | `hdfs dfs -getmerge RUTA professors.csv` |

---

## 16. Errors freqüents i diagnòstic

### 16.1. No es pot connectar a MariaDB

**Símptoma:** `Communications link failure`, errors JDBC o missatges de connexió refusada.

**Comprovacions:** servei MariaDB actiu, host i port correctes, usuari i contrasenya, privilegis i presència del driver JDBC.

```bash
sudo systemctl status mariadb
mariadb -u iabd -p
```

### 16.2. `ClassNotFoundException` del connector

**Causa probable:** falta el JAR del driver o hi ha incompatibilitats entre biblioteques Java. Revisar `$SQOOP_HOME/lib` i els missatges complets del log.

### 16.3. El directori HDFS ja existeix

**Causa:** Sqoop intenta una nova importació completa a una ruta ja ocupada. Opcions: utilitzar una ruta nova o, només si es poden eliminar les dades, `--delete-target-dir`.

### 16.4. YARN no executa el job

**Causes possibles:** serveis aturats, poca memòria, manca d'espai o node no saludable.

```bash
jps
df -h
hdfs dfs -df -h /
```

### 16.5. Errors en exportar

Revisar, en aquest ordre: **existeix la taula?**, els camps tenen el mateix ordre? les dades estan delimitades com espera Sqoop? hi ha claus duplicades? l'usuari pot inserir o actualitzar? Recorda que l'exemple d'importació del PDF utilitza comes: exportar sense especificar el delimitador d'entrada pot generar errors.

### 16.6. `--query` falla

Comprovar que la consulta porta el token literal `$CONDITIONS` i que `--split-by` apunta a una columna existent i apta per al particionat. També cal revisar les cometes i les barres invertides del shell.

### 16.7. Es veuen bytes il·legibles amb Avro o Parquet

No és una prova de corrupció: són formats binaris. Utilitzar `avro-tools`, `parquet-tools` o un motor que entengui el format.

### 16.8. Problemes amb els noms i exemples del PDF

Hi ha diferències puntuals entre noms de taules (`professors` vs. `professors2`), nombre de mappers del log i l'opció `--h-catalog-table`. Cal diferenciar aquestes errades editorials del funcionament conceptual de Sqoop.

---

## 17. Bones pràctiques

1. **Verifica l'origen:** abans de copiar dades, consulta el nombre de files en la base SQL.
2. **Fes servir directoris separats:** una ruta d'HDFS per a cada prova, format o importació.
3. **No esborris sense comprovar:** `--delete-target-dir` pot eliminar dades importants.
4. **Evita exposar contrasenyes:** preferir `-P` o un mecanisme de credencials adequat a l'entorn.
5. **Revisa l'ordre dels camps en exportar:** la taula MariaDB i els fitxers han de ser compatibles.
6. **Tria el paral·lelisme amb criteri:** més mappers no garanteixen més velocitat.
7. **Guarda una marca de control:** en càrregues incrementals, registra el `last-value` utilitzat.
8. **Verifica també l'arribada:** consulta HDFS o Hive i compara files amb la font.
9. **Mantén controlada la compatibilitat:** versions de Sqoop, Hadoop, JDBC, Avro i Parquet.
10. **Diferencia l'objectiu docent del productiu:** el PDF utilitza credencials de prova i configuracions permissives que no s'han de copiar sense revisar en una infraestructura real.

---

## 18. Comparatives i esquemes per memoritzar

### 18.1. Import vs export

| Aspecte | `sqoop import` | `sqoop export` |
|---|---|---|
| Origen | MariaDB / base relacional | HDFS / dades de Hadoop |
| Destinació | HDFS / Hive | MariaDB / base relacional |
| Identificador de dades | `--table` de la font | `--table` de destinació |
| Carpeta | `--target-dir` | `--export-dir` |
| Necessita taula SQL? | La d'origen ja ha d'existir | La de destí ja ha d'existir |

### 18.2. Import completa vs incremental

```text
Càrrega completa:      [1, 2, 3, 4, 5, 6, 7]
Càrrega incremental:   últim valor = 4
                      [5, 6, 7]
Següent control:       últim valor = 7
```

### 18.3. Formats i compressors no són el mateix

**Format** = com s'organitzen i representen els registres (`text`, `Avro`, `Parquet`). **Compressió** = com es redueix la mida de les dades (`gzip`, `bzip2`, `snappy`). Una opció de format no s'ha de confondre amb un còdec.

### 18.4. Guia visual del flux complet

```text
                        ┌───────────────┐
                        │ MariaDB       │
                        │ sqoopCas1     │
                        │ professors    │
                        └──────┬────────┘
                               │ sqoop import
                               ▼
                        ┌───────────────┐
                        │ HDFS          │
                        │ professors_*  │
                        └──────┬────────┘
                         ┌─────┴───────┐
                         ▼             ▼
                    Sqoop export    Hive import
                         │             │
                         ▼             ▼
                    MariaDB        Taula Hive
                    sqoopCas2      professors_mariadb
```

---

## 19. Exercicis pràctics proposats

### Exercici 1. Importació bàsica

Crea la taula de professors del Cas 1, importa-la amb **un mapper** a `/user/iabd/sqoop/prova_m1` i comprova quants fitxers `part-m-*` obtens. Després repeteix amb dos mappers en una altra carpeta. **Objectiu:** relacionar `-m` amb el resultat a HDFS.

### Exercici 2. Selecció de columnes

Importa `nom` i `materia` a una ruta nova. Fes la comprovació a HDFS i explica per què el fitxer té menys columnes que la taula original.

### Exercici 3. Filtre d'edat

Importa només els professors amb edat superior a 40 anys utilitzant `--where`. Contrasta el resultat amb `SELECT * FROM professors WHERE edat > 40;` executat en MariaDB.

### Exercici 4. Consulta personalitzada

Fes servir `--query` amb `$CONDITIONS` i `--split-by id` per importar professors amb una edat inferior a 35 anys. Comprova el token escapant el símbol `$` en Bash.

### Exercici 5. Exportació

Crea una taula nova `professors2` a la segona base de dades. Exporta-hi els registres de text separats per comes i comprova el total amb `COUNT(*)`.

### Exercici 6. Incremental

Importa les files posteriors a l'identificador 4. Anota la marca de control que et proposa Sqoop en acabar i explica què passaria si després modifiquessis la matèria del professor amb identificador 2.

### Exercici 7. Formats

Importa la mateixa taula en Avro i Parquet. Llista els fitxers i justifica per què no convé inspeccionar-los amb `hdfs dfs -cat` pensant que són fitxers de text.

### Exercici 8. Hive

Importa `professors` directament a Hive com `professors_mariadb`; consulta'n l'esquema i els registres. Explica quina part del procés resol Sqoop i quina resol Hive.

---

## 20. Preguntes d'autoavaluació amb resposta

### Bloc A. Conceptes generals

**1. Què és Apache Sqoop?**  
Una eina per transferir dades estructurades entre bases de dades relacionals i l'ecosistema Hadoop.

**2. Què és una importació?**  
Una transferència que porta registres d'una base SQL cap a HDFS o Hive.

**3. Què és una exportació?**  
Una transferència de dades des d'HDFS cap a una base relacional.

**4. Quins sistemes apareixen als casos pràctics del document?**  
MariaDB, Apache Hadoop (HDFS i YARN) i Apache Hive.

**5. Per a què serveixen els connectors JDBC?**  
Per comunicar Sqoop amb sistemes relacionals i consultar-ne l'esquema i els registres.

**6. Quina relació hi ha entre Sqoop i MapReduce?**  
Sqoop utilitza tasques MapReduce per distribuir la lectura i escriptura de dades en el model del material.

**7. Què és un mapper?**  
Una tasca que processa una partició de la informació d'origen.

**8. Quants mappers utilitza Sqoop per defecte segons el PDF?**  
Quatre, si no s'especifica un altre nombre.

**9. Quina opció en controla el nombre?**  
`-m`, per exemple `-m 2`.

**10. Quatre mappers impliquen quatre servidors diferents?**  
No; són tasques i poden executar-se sobre menys nodes físics.

**11. Per què convé triar bé el nombre de mappers?**  
Per equilibrar el paral·lelisme, les connexions a la base SQL i el consum de recursos.

**12. Quin és l'estat de manteniment de Sqoop segons el document?**  
És un projecte a l'Apache Attic des de 2021.

### Bloc B. Configuració i primeres comandes

**13. Per què s'ha de revisar `/etc/hosts`?**  
Perquè el nom `master` resolgui a la IP que correspon a la màquina de Hadoop de classe.

**14. Per a què serveix `sqoop list-databases`?**  
Per enumerar les bases de dades accessibles al servidor relacional.

**15. Per a què serveix `sqoop list-tables`?**  
Per enumerar les taules d'una base de dades concreta.

**16. Què indica `--connect`?**  
La cadena JDBC de connexió, per exemple `jdbc:mysql://localhost/sqoopCas1`.

**17. Per què és preferible `-P` a `--password=...`?**  
Perquè evita escriure la contrasenya directament en la comanda visible.

**18. Per què necessitem el driver de MySQL?**  
Perquè Java/Sqoop pugui comunicar-se mitjançant JDBC amb la base SQL del laboratori.

**19. Quins serveis s'han d'engegar abans d'executar el job?**  
HDFS i YARN en la configuració docent descrita.

**20. Amb quina comanda es poden revisar processos Java?**  
`jps`.

**21. Per a què serveix `--target-dir`?**  
Per indicar la ruta d'arribada d'HDFS d'una importació.

**22. Quin perill té `--delete-target-dir`?**  
Elimina les dades existents en la destinació abans de carregar les noves.

### Bloc C. Casos pràctics i monitoratge

**23. Quina és la base de dades del Cas 1?**  
`sqoopCas1`.

**24. Com es diu la taula importada en el Cas 1?**  
`professors`.

**25. Quants registres s'insereixen inicialment?**  
Set.

**26. Quina funció té la columna `id`?**  
És la clau primària i facilita el particionat per rangs.

**27. Què representa `part-m-00000`?**  
Un dels fitxers de sortida escrits durant la tasca de map.

**28. Què indica `_SUCCESS`?**  
Que el job de Hadoop ha finalitzat amb èxit; no conté les files de la taula.

**29. Per a què es fa servir `hdfs dfs -ls`?**  
Per consultar fitxers i directoris d'HDFS.

**30. Què permet veure `hdfs dfs -cat`?**  
El contingut d'un fitxer, especialment útil quan és text pla.

**31. Per a què serveix `hdfs dfs -getmerge`?**  
Per combinar els fragments d'una carpeta d'HDFS en un fitxer local.

**32. Quin port utilitza la interfície YARN del document?**  
`8088`.

**33. Quin port utilitza la interfície HDFS NameNode del document?**  
`9870`.

**34. Què és `BoundingValsQuery` en els logs?**  
La consulta que obté els valors límit de la columna usada per repartir la lectura.

**35. Què significa `Retrieved 7 records`?**  
Que Sqoop ha recuperat set registres en l'execució mostrada.

**36. Un avís `WARN` implica obligatòriament un job fallit?**  
No; cal revisar si l'operació continua i finalitza correctament.

**37. Què pot causar `Unhealthy node`?**  
Per exemple, manca d'espai al disc o altres problemes de salut detectats per YARN.

**38. Per a què serveix `sqoop import-all-tables`?**  
Per importar les taules d'una base de dades en lloc de seleccionar-ne només una.

**39. Què indica `--warehouse-dir`?**  
La carpeta base d'HDFS en la qual es creen subcarpetes per a les taules importades.

**40. Quina és la base receptora del Cas 2?**  
`sqoopCas2`.

**41. Com es diu la taula receptora creada al Cas 2?**  
`professors2`.

**42. Cal crear prèviament la taula MariaDB abans d'exportar?**  
Sí, tal com es fa al cas pràctic.

**43. Per què pot fallar una exportació si hi ha duplicats?**  
Perquè poden vulnerar una clau primària o una restricció d'unicitat.

**44. Què aporta `--update-key id`?**  
Permet utilitzar el valor `id` per actualitzar registres en lloc de fer únicament insercions.

**45. Per a què s'utilitza `--update-mode allowinsert`?**  
Per permetre també insercions quan no hi ha una fila que coincideixi amb la clau d'actualització.

### Bloc D. Formats, filtres i incremental

**46. Avro és orientat a files o columnes?**  
A files.

**47. Parquet és orientat a files o columnes?**  
A columnes.

**48. Amb quina opció s'importa en Avro?**  
`--as-avrodatafile`.

**49. Amb quina opció s'importa en Parquet?**  
`--as-parquetfile`.

**50. Per què `hdfs dfs -tail` no mostra Avro com a text normal?**  
Perquè el fitxer està codificat en binari.

**51. Quina eina permet transformar Avro a JSON llegible?**  
`avro-tools tojson`.

**52. Per a què serveix `parquet-tools meta`?**  
Per inspeccionar l'esquema i les metadades d'un fitxer Parquet.

**53. Què fa `--compress` en els exemples del PDF?**  
Activa compressió, amb gzip com a format per defecte de l'exemple.

**54. Com es demana Bzip2?**  
`--compress --compression-codec bzip2`.

**55. Com es demana Snappy?**  
`--compress --compression-codec snappy`.

**56. Quina diferència hi ha entre format i compressió?**  
El format defineix la representació de dades; la compressió redueix la quantitat de bytes emmagatzemats.

**57. Per a què serveix `--where`?**  
Per limitar les files que compleixen una condició SQL.

**58. Per a què serveix `--columns`?**  
Per limitar les columnes importades.

**59. Quan s'utilitza `--query`?**  
Quan volem indicar una consulta SQL personalitzada en lloc d'importar una taula sencera.

**60. Per què és obligatori considerar `$CONDITIONS` amb `--query`?**  
Perquè Sqoop pugui incorporar les condicions de divisió dels mappers.

**61. Què és `--split-by`?**  
La columna utilitzada per dividir les dades en fragments de lectura.

**62. Què significa `--incremental append`?**  
Importar registres nous basant-se en una columna de control que creix.

**63. Què determina `--check-column id`?**  
Que la comparació incremental es fa amb l'identificador `id`.

**64. Què expressa `--last-value 4`?**  
Que l'última marca de control prèviament registrada era 4.

**65. La importació incremental `append` detecta actualitzacions de registres antics?**  
No; en general, no detecta canvis en files amb una clau anterior a la marca de control.

### Bloc E. Integració Hive i raonament

**66. Què fa `--hive-import`?**  
Activa la càrrega de dades a Hive dins del flux d'importació.

**67. Què indica `--hive-database default`?**  
La base de dades Hive en què volem crear o carregar la taula.

**68. Per a què serveix `--create-hive-table`?**  
Per demanar que Sqoop creï la taula de Hive.

**69. Què determina `--hive-table`?**  
El nom que ha de tenir la taula final a Hive.

**70. Quina ordre permet veure l'esquema i la ubicació d'una taula Hive?**  
`DESCRIBE FORMATTED nom_taula;`.

**71. Què és HCatalog en aquesta pràctica?**  
La capa de metadades/catàleg de Hive utilitzada per integrar dades entre eines.

**72. Per què no s'ha de confondre Flume amb Sqoop?**  
Flume està centrat en esdeveniments i logs; Sqoop en transferència de dades estructurades de bases relacionals.

**73. Quin tipus de dades encaixa especialment amb Sqoop?**  
Taules estructurades i registres accessibles mitjançant connectors de bases SQL.

**74. Si vols copiar només el nom i la matèria dels professors, quina opció utilitzaries?**  
`--columns "nom,materia"`.

**75. Si necessites carregar només professors de més de 40 anys, quina opció utilitzaries?**  
`--where "edat>40"`, o una consulta personalitzada equivalent.

**76. Si vols evitar que una exportació falli per dades ja existents, què pots revisar?**  
Les claus primàries i si convé un mecanisme d'actualització amb `--update-key`.

**77. Per què cal comprovar tant els logs com la destinació?**  
Perquè una finalització aparentment correcta no substitueix la verificació del volum i contingut de les dades carregades.

**78. Què recomanaries abans d'usar `--delete-target-dir`?**  
Confirmar la ruta exacta i disposar de còpia o d'una estratègia de recuperació si les dades són importants.

**79. Per què és útil Parquet en consultes analítiques?**  
Perquè està organitzat per columnes i alguns motors poden llegir únicament les columnes necessàries.

**80. Quina és la idea central que cal recordar de Sqoop?**  
**Importar i exportar dades estructurades entre el món SQL i Hadoop de forma automatitzada i paral·lela.**

---

## 21. Glossari

| Terme | Definició |
|---|---|
| **Apache Sqoop** | Eina d'intercanvi de dades estructurades entre bases SQL i Hadoop |
| **Apache Hadoop** | Ecosistema per a emmagatzematge i processament distribuït |
| **HDFS** | Sistema de fitxers distribuït de Hadoop |
| **YARN** | Gestor de recursos i planificació de tasques Hadoop |
| **MapReduce** | Model de processament distribuït emprat per Sqoop en el material |
| **Mapper** | Tasca de processament d'una partició de dades |
| **Split** | Fragment lògic de dades assignat a una tasca |
| **JDBC** | Interfície de connectivitat entre aplicacions Java i bases de dades |
| **Connector** | Component que permet Sqoop comunicar-se amb un sistema extern |
| **Importació** | Transferència de base relacional a Hadoop |
| **Exportació** | Transferència de Hadoop a base relacional |
| **Warehouse** | Carpeta o zona d'emmagatzematge de dades |
| **`--target-dir`** | Directori de destinació per a una importació |
| **`--export-dir`** | Directori de lectura per a una exportació |
| **`--split-by`** | Columna de particionat entre mappers |
| **Clau primària** | Identificador únic de files d'una taula |
| **`_SUCCESS`** | Marcador de finalització correcta d'un job Hadoop |
| **Avro** | Format binari orientat a files amb esquema |
| **Parquet** | Format binari orientat a columnes |
| **Còdec** | Algoritme/implementació de compressió i descompressió |
| **Gzip** | Sistema de compressió habitual |
| **Bzip2** | Sistema de compressió utilitzat en el document |
| **Snappy** | Biblioteca de compressió ràpida comuna a Big Data |
| **Incremental** | Càrrega que incorpora dades noves respecte a una execució anterior |
| **Watermark** | Valor de control fins al qual s'han processat registres |
| **Hive** | Sistema de consulta i gestió de dades sobre Hadoop mitjançant HiveQL |
| **HCatalog** | Component de catàleg i metadades de l'ecosistema Hive |
| **Metadades** | Informació que descriu camps, tipus, estructura i ubicació de les dades |
| **Data lake** | Repositori centralitzat de dades en diversos formats |
| **WARN** | Avís en el log, no necessàriament un error fatal |

---

## 22. Resum final d'examen

### Les deu idees que has de saber explicar

1. **Sqoop mou dades estructurades entre bases de dades relacionals i Hadoop.**
2. **Importació = SQL → HDFS; exportació = HDFS → SQL.**
3. **Utilitza JDBC i MapReduce**, amb mappers que treballen en paral·lel.
4. **`-m` determina el nombre de mappers; `--split-by` la columna de divisió.**
5. **`--target-dir` és per importar i `--export-dir` és per exportar.**
6. **La sortida es pot repartir en diversos fitxers**, que podem fusionar amb `hdfs dfs -getmerge`.
7. **Avro és orientat a files; Parquet a columnes.** Tots dos són formats binaris.
8. **`--where`, `--columns` i `--query` permeten controlar què es copia.**
9. **`--incremental append`, `--check-column` i `--last-value` permeten copiar registres nous.**
10. **`--hive-import` permet integrar la càrrega amb Hive**, per consultar-ne les dades amb un esquema de taula.

### Mini-xuleta de comandes

```bash
# Veure les bases de dades
sqoop list-databases --connect jdbc:mysql://localhost --username=iabd -P

# Veure les taules d'una base
sqoop list-tables --connect jdbc:mysql://localhost/sqoopCas1 --username=iabd -P

# Importar
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd -P --table professors \
  --target-dir /user/iabd/sqoop/professors_hdfs -m 2

# Exportar
sqoop export --connect jdbc:mysql://localhost/sqoopCas2 \
  --username=iabd -P --table professors2 \
  --export-dir /user/iabd/sqoop/professors_hdfs \
  --input-fields-terminated-by ','

# Comprovar i recuperar les dades
hdfs dfs -ls /user/iabd/sqoop/professors_hdfs
hdfs dfs -getmerge /user/iabd/sqoop/professors_hdfs professors.csv

# Importar incrementalment
sqoop import --connect jdbc:mysql://localhost/sqoopCas1 \
  --username=iabd -P --table professors \
  --target-dir /user/iabd/sqoop/professors_inc \
  --incremental append --check-column id --last-value 4
```

> **Consell final d'estudi:** abans de memoritzar una comanda sencera, identifica'n l'origen, la destinació, el nombre de mappers, el format i la política de càrrega (completa, filtrada o incremental). Si entens aquests cinc elements, et serà molt més fàcil explicar i adaptar les pràctiques.

---

## Fonts i criteri d'elaboració

- **Font principal:** *M5075_NF1_3_DOC00_Sqoop.pdf* (28 pàgines), Francesc Barragán Pascual, revisió del 04/02/2026.
- **Estructura:** se segueix la seqüència del material: introducció, instal·lació, importació, casos, Avro/Parquet, compressió, filtres, incremental i Hive.
- **Ampliacions didàctiques:** esquemes, taules comparatives, diagnòstic, exercicis i preguntes amb resposta.
- **Advertiments editorials:** es marquen els exemples del PDF amb incoherències de noms de taula, opcions o logs; els canvis als exemples pràctics s'indiquen expressament.
- **Abast:** aquests apunts resumeixen i desenvolupen el **document proporcionat**, no substitueixen una verificació de compatibilitat amb totes les versions actuals de Hadoop, Sqoop i Hive.
