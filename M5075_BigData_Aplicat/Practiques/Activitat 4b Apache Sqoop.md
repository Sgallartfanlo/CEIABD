# APUNTS EXTENSOS — PRÀCTICA 4: INGESTA AMB APACHE SQOOP

## 1. Objectius i mapa de la pràctica [PRÀCTICA]

L'activitat té com a objectiu **traslladar dades estructurades des de MariaDB/MySQL a HDFS amb Apache Sqoop**, aplicant filtres, formats d'emmagatzematge, compressió i ingesta incremental. No és una pràctica d'exportació d'HDFS a MariaDB: els dos exercicis van de la base de dades relacional cap a HDFS.

| Cas | Taula | Filtre | Format | Compressió | Destí | Resultat acreditat |
|---|---|---|---|---|---|---|
| A | `orders` | `order_status='COMPLETE'` | Parquet | Snappy | `/user/iabd/sqoop/orders/dades_parquet` | **22.899 registres** |
| B | `customers` | `customer_state='CA'` i `customer_id > 99` | Avro | bzip2 | `/user/iabd/sqoop/customers/dades_avro` | **1.999 registres** |

**Idees essencials:** la font és MariaDB; Sqoop tradueix l'accés mitjançant JDBC i executa tasques de transferència; HDFS conserva els fitxers; el format dels fitxers no és el mateix que el motor de base de dades d'origen.

## 2. Arquitectura i recorregut de les dades [AMPLIACIÓ]

```text
MariaDB / MySQL                  Apache Sqoop / MapReduce                 HDFS
┌─────────────────┐             ┌──────────────────────────┐       ┌──────────────────────┐
│ retail_db       │ -- JDBC --> │ SELECT + WHERE + mappers │ ----> │ /user/iabd/sqoop/... │
│ orders          │             │ serialització / compressió│       │ fitxers .parquet/.avro│
│ customers       │             └──────────────────────────┘       └──────────────────────┘
└─────────────────┘
```

Sqoop és una eina de **transferència batch**, no un sistema d'streaming continu. En executar una importació, es llegeix una selecció de registres i es desen fitxers al destí. El nombre de fitxers de sortida pot dependre dels mappers i de la configuració.

## 3. Preparació de l'entorn [PRÀCTICA + AMPLIACIÓ]

La guia indica que la preparació de MariaDB ja estava feta a la màquina virtual. Abans de cada transferència cal comprovar que Hadoop és operatiu i que MariaDB admet connexions. La guia esmenta les ordres:

```bash
start-dfs.sh
start-yarn.sh
```

**Què fan?** `start-dfs.sh` arrenca serveis associats a HDFS; `start-yarn.sh` arrenca els serveis YARN. Són ordres per iniciar serveis, no simples tests d'estat. Abans de tornar-les a llançar, es pot comprovar:

```bash
jps
hdfs dfs -ls /
yarn node -list
```

**[AMPLIACIÓ]** Si `jps` no mostra tots els processos, això no demostra per si sol un error: el desplegament i els serveis actius depenen de la màquina i del mode utilitzat. És convenient consultar també els logs.

## 4. Base de dades `retail_db` [PRÀCTICA]

El conjunt de dades és d'una botiga i incorpora informació sobre clients, productes i comandes. La guia indica que es pot crear a partir de `create_db.sql`.

```bash
mariadb -u iabd -p
```

```sql
CREATE DATABASE IF NOT EXISTS retail_db;
USE retail_db;
SOURCE create_db.sql;
SHOW TABLES;
```

Explicació:

- `CREATE DATABASE IF NOT EXISTS`: evita fallar quan la base de dades ja existeix.
- `USE`: selecciona la base de dades activa.
- `SOURCE`: executa el contingut del fitxer SQL des del client de MariaDB; el fitxer ha de ser accessible des del directori corresponent.
- `SHOW TABLES`: enumera les taules importades.

**[AMPLIACIÓ]** Comprova els camps rellevants abans d'importar:

```sql
DESCRIBE orders;
DESCRIBE customers;
SELECT COUNT(*) FROM orders WHERE order_status = 'COMPLETE';
SELECT COUNT(*) FROM customers WHERE customer_state = 'CA' AND customer_id > 99;
```

Aquests recomptes són controls útils, però no apareixen com a captures verificades al PDF.

## 5. Comprovar la connexió Sqoop–MariaDB [PRÀCTICA]

```bash
sqoop list-tables \
  --connect jdbc:mysql://localhost/retail_db \
  --username iabd \
  -P
```

| Paràmetre | Funció |
|---|---|
| `list-tables` | Sol·licita la llista de taules de la BD |
| `--connect` | URL JDBC amb host i nom de la BD |
| `--username` | Usuari de MariaDB |
| `-P` | Demana la contrasenya interactivament |

La pràctica fa explícit que `-P` és preferible a escriure la contrasenya en clar a la línia d'ordres.

**No confondre:** `--password` espera un valor de contrasenya; `-P` obre una entrada interactiva. Si s'utilitza una URL amb `localhost`, s'assumeix que la BD és accessible des de l'entorn on s'executa Sqoop.

## 6. Cas A: importació filtrada de comandes [PRÀCTICA]

**Enunciat:** obtenir les files de la taula `orders` on `order_status` és `COMPLETE` i guardar-les en fitxers Parquet comprimits amb Snappy.

Requisits exactes:

```text
Taula:          retail_db.orders
Filtre:         order_status = 'COMPLETE'
Destinació:     /user/iabd/sqoop/orders/dades_parquet
Format:         Parquet
Compressió:     Snappy
Registres:      22.899
```

Una condició `WHERE` filtra les files a importar; no transforma els valors ni elimina files de la taula original.

## 7. Cas A: comanda completa i explicada [PRÀCTICA]

```bash
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username iabd \
  -P \
  --table orders \
  --where "order_status='COMPLETE'" \
  --target-dir /user/iabd/sqoop/orders/dades_parquet \
  --as-parquetfile \
  --compress \
  --compression-codec snappy \
  --delete-target-dir
```

Desglossament:

1. `sqoop import` inicia la transferència relacional → HDFS.
2. `--connect` identifica l'origen JDBC.
3. `--username` i `-P` proporcionen autenticació.
4. `--table orders` tria la taula.
5. `--where` limita la transferència a les comandes completades.
6. `--target-dir` indica la ruta HDFS exacta.
7. `--as-parquetfile` imposa el format de sortida.
8. `--compress --compression-codec snappy` indica compressió.
9. `--delete-target-dir` **esborra la ruta HDFS anterior si existeix**: és pràctic per repetir exercicis, però pot destruir dades existents.

**[AMPLIACIÓ]** Recomanació per comprovar abans de repetir:

```bash
hdfs dfs -ls /user/iabd/sqoop/orders/dades_parquet
```

Utilitza `--delete-target-dir` només quan la ruta és de proves i saps que el seu contingut es pot eliminar.

## 8. Parquet i Snappy [AMPLIACIÓ]

**Parquet** és un format **columnar**. Pot ser eficient quan una consulta necessita poques columnes d'una taula gran i permet emmagatzemar metadades sobre l'esquema. És un format binari: no s'ha d'intentar interpretar com si fos CSV.

**Snappy** és un algorisme de compressió orientat a velocitat. Sol ser una elecció habitual per a processos analítics en què interessa comprimir i descomprimir ràpidament. No garanteix sempre la màxima reducció de mida.

La pràctica remarca que **no té sentit `--fields-terminated-by` amb Parquet**, perquè no s'estan produint línies de text delimitades.

**Exemple de comprovació posterior amb Spark** (complementari, requereix PySpark configurat):

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("ValidacioSqoopParquet").getOrCreate()
path = "hdfs:///user/iabd/sqoop/orders/dades_parquet"
df = spark.read.parquet(path)
print(df.count())
df.groupBy("order_status").count().show()
```

El resultat esperat segons la pràctica és `22899`; l'exemple complementari no està executat aquí.

## 9. Cas A: resultat observat [PRÀCTICA]

A les captures de les pàgines 5–6 de contingut de la pràctica es mostra el missatge de Sqoop:

```text
Retrieved 22899 records
```

La comprovació de la interfície web d'HDFS mostra **quatre fitxers `.parquet`** i directoris auxiliars `.metadata` i `.signals` al destí. Aquests noms i aquesta estructura corresponen a l'execució documentada, no s'han de considerar universals per a qualsevol versió o configuració.

**Què acredita cada evidència?** El recompte del log dona el nombre de registres importats; la llista d'HDFS acredita l'existència dels fitxers; un control addicional sobre el contingut Parquet permetria verificar l'esquema i el filtre real.

## 10. Cas B: importació incremental de clients [PRÀCTICA]

La segona part sol·licita únicament clients de Califòrnia (`customer_state='CA'`) que tinguin `customer_id > 99`.

```text
Taula:          retail_db.customers
Columnes:       customer_id, customer_fname, customer_lname, customer_state
Filtre:         customer_state = 'CA'
Marc incremental inicial: customer_id = 99
Destí:          /user/iabd/sqoop/customers/dades_avro
Format:         Avro
Compressió:     bzip2
Resultat observat: 1.999 registres
```

Les columnes seleccionades no inclouen camps com el correu electrònic o la contrasenya que puguin existir a l'origen.

## 11. Cas B: comanda completa i explicada [PRÀCTICA]

```bash
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username iabd \
  -P \
  --table customers \
  --columns customer_id,customer_fname,customer_lname,customer_state \
  --where "customer_state='CA'" \
  --target-dir /user/iabd/sqoop/customers/dades_avro \
  --as-avrodatafile \
  --compress \
  --compression-codec bzip2 \
  --incremental append \
  --check-column customer_id \
  --last-value 99
```

Aquesta ordre combina **un filtre fix** (`customer_state='CA'`) amb **una condició incremental** (`customer_id > 99`). Són criteris complementaris; la importació només conté files que compleixen tots dos.

| Opció | Interpretació |
|---|---|
| `--columns` | Restringeix l'esquema de sortida a quatre camps |
| `--where` | Restringeix les files per estat |
| `--as-avrodatafile` | Escriu dades en contenidor Avro |
| `--compression-codec bzip2` | Sol·licita compressió bzip2 |
| `--incremental append` | Selecciona nous registres segons un camp creixent |
| `--check-column customer_id` | Identificador per comparar amb el límit |
| `--last-value 99` | Límit de la importació anterior; per aquesta execució, només valors superiors |

## 12. Com funciona `--incremental append` [AMPLIACIÓ]

Suposem que la taula conté identificadors `95, 99, 100, 101, 120`. Amb `--last-value 99` s'intenta importar `100, 101, 120` (sempre que els registres també compleixin el filtre d'estat). En la següent execució, cal utilitzar el **nou màxim** comunicat per Sqoop, no tornar a posar `99`.

```text
Execució 1: last-value = 99
           → importa registres nous fins al màxim detectat
Execució 2: last-value = màxim anterior
           → importa només els de valor superior
```

**Limitació important:** el mode `append` és apropiat per a identificadors creixents i registres nous. No és una solució general per detectar actualitzacions de files existents. És diferent d'un mode incremental basat en una marca temporal de modificació.

## 13. Avro i bzip2 [PRÀCTICA + AMPLIACIÓ]

**Avro** serialitza registres amb un esquema, i és habitual quan es prioritza una representació orientada a registres i un intercanvi consistent entre sistemes. **Parquet**, en canvi, s'organitza per columnes.

**bzip2** és un algorisme de compressió general; a diferència de Snappy, habitualment prioritza més la reducció de mida que la rapidesa. El resultat real depèn de les dades.

La guia esmenta la necessitat de verificar una dependència Avro a l'entorn del curs (`avro-1.8.1.jar`) i suggereix:

```bash
hdfs dfs -text /user/iabd/sqoop/customers/dades_avro/part-m-00000.avro
```

**[AMPLIACIÓ]** La possibilitat de visualitzar un fitxer Avro amb `-text` depèn del suport de formats disponible a l'entorn; per a una comprovació portable es pot utilitzar Spark o una utilitat Avro adequada. No s'ha d'assumir que `-cat` convertirà Avro binari en text llegible.

## 14. Cas B: resultats observats [PRÀCTICA]

La pàgina 8 de contingut de la pràctica mostra:

```text
Retrieved 1999 records
Incremental import complete!
--last-value 12429
```

La nova marca **12429** és la que Sqoop recomana per a una següent importació incremental en aquest escenari. Al directori HDFS es mostren **quatre fitxers `.avro`**. El resultat satisfà el requisit d'obtenir menys de 2.012 registres.

**Precaució:** els 1.999 registres no han de repetir-se com a resultat esperat en qualsevol base de dades; és el nombre acreditat per la còpia `retail_db` de la pràctica.

## 15. Comparació dels casos

| Aspecte | Cas A | Cas B |
|---|---|---|
| Tipus d'ingesta | Filtrada, no incremental | Incremental amb filtre |
| Taula | `orders` | `customers` |
| Selecció de columnes | Totes les columnes | Quatre columnes concretes |
| Selecció de files | Estat completat | Estat CA i ID creixent |
| Format | Parquet | Avro |
| Orientació | Columnar | Registres |
| Compressió | Snappy | bzip2 |
| Repetició | `--delete-target-dir` elimina la destinació anterior | Cal avançar el `--last-value` |
| Nombre observat | 22.899 | 1.999 |

## 16. Opcions de Sqoop més rellevants [AMPLIACIÓ]

```text
sqoop import                 importació des d'RDBMS
sqoop list-tables            llista taules de l'origen
--connect                    URL JDBC
--username                   usuari d'accés
-P                           sol·licita contrasenya interactiva
--table                      taula d'origen
--columns                    llista de columnes
--where                      condició SQL de filtre
--target-dir                 directori HDFS de destinació
--as-parquetfile             fitxers Parquet
--as-avrodatafile            fitxers Avro
--compress                   compressió habilitada
--compression-codec          algorisme de compressió
--incremental append         importació incremental per valor creixent
--check-column               camp de control
--last-value                  darrer valor importat
--delete-target-dir          elimina el destí abans d'importar
--num-mappers                fixa el paral·lelisme dels mappers
```

## 17. Mappers i sortides [AMPLIACIÓ]

Sqoop pot repartir el treball entre diversos **mappers** de Hadoop. La distribució eficient sol requerir una columna adequada per particionar la lectura. Si hi ha quatre mappers, és habitual observar diverses sortides `part-m-...`, però no és una equivalència absoluta entre mappers i fitxers finals en tots els formats i versions.

**Exemple de prova en entorn separat**:

```bash
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username iabd -P \
  --table customers \
  --target-dir /user/iabd/sqoop/prova_un_mapper \
  --num-mappers 1
```

Aquesta és una demostració complementària, no una execució documentada a la pràctica.

## 18. Diagnosi: què comprovar quan falla?

| Símptoma | Possibles causes | Comprovació |
|---|---|---|
| No connecta amb MariaDB | BD aturada, credencials, hostname o port | `mariadb -u iabd -p`; `sqoop list-tables` |
| No es troba el driver JDBC | Connector no disponible al classpath | Revisar llibreries i logs |
| Fallada MapReduce | YARN aturat, permisos, recursos | `jps`, logs de YARN |
| `File exists` | Directori HDFS ja existeix | `hdfs dfs -ls` abans de decidir si eliminar |
| Registres inesperats | Dades diferents o filtre erroni | `SELECT COUNT(*) ... WHERE ...` |
| Error de serialització | Versions Avro/Parquet o llibreries | Consultar stack trace complet |
| Importació incremental duplicada | Mateix `--last-value` en repetir | Recuperar el límit nou del log |
| Fitxer binari incomprensible amb `cat` | Formats Avro o Parquet | Lector del format corresponent |

## 19. Precaucions importants [AMPLIACIÓ]

**Evita contrasenyes en clar** en ordres compartides o captures. Per a exercicis, `-P` és una elecció raonable; en entorns reals, el sistema d'autenticació i els gestors de secrets han de seguir la política de l'organització.

**No confonguis reiniciar i repetir:** `--delete-target-dir` pot destruir fitxers HDFS; `--incremental append` no garanteix per si mateix que una segona execució amb la mateixa marca sigui idempotent.

**Les captures són evidència d'una execució**, no una garantia de compatibilitat futura entre versions de Sqoop, Java, Hadoop, drivers i formats.

## 20. Procediment de reconstrucció complet [AMPLIACIÓ]

1. Comprova HDFS/YARN/MariaDB.
2. Accedeix a MariaDB i verifica les dues taules.
3. Executa `sqoop list-tables` amb `-P`.
4. Consulta a MariaDB el recompte de `orders` amb `COMPLETE`.
5. Comprova si existeix el directori HDFS de `orders` i decideix si es pot substituir.
6. Executa el Cas A amb Parquet + Snappy.
7. Comprova el recompte retornat i la llista de fitxers a HDFS.
8. Consulta el recompte de clients `CA` amb ID superior a 99.
9. Executa el Cas B amb Avro + bzip2 i el límit inicial.
10. Desa el valor `--last-value` del log.
11. Llista els `.avro` i documenta el resultat.
12. Escriu una conclusió diferenciant formats, filtre i importació incremental.

Ordres de verificació HDFS:

```bash
hdfs dfs -ls /user/iabd/sqoop/orders/dades_parquet
hdfs dfs -ls /user/iabd/sqoop/customers/dades_avro
hdfs dfs -du -h /user/iabd/sqoop/orders/dades_parquet
hdfs dfs -du -h /user/iabd/sqoop/customers/dades_avro
```

## 21. Exercicis resolts [AMPLIACIÓ]

### Exercici 1. Quina part de la comanda A aplica el filtre?

**Resposta:** `--where "order_status='COMPLETE'"`. La taula continua intacta i només s'importa la selecció.

### Exercici 2. Com es limita la importació a una sola columna?

**Resposta:** amb `--columns nom_columna`, si la resta d'opcions del procediment són compatibles.

### Exercici 3. Volem afegir clients nous sense reimportar els anteriors. Què canvia?

**Resposta:** cal utilitzar el valor de `--last-value` que recomana l'última execució; en el registre documentat és `12429`.

### Exercici 4. Per què no serveix `--fields-terminated-by ','` per visualitzar Parquet?

**Resposta:** Parquet no és text CSV delimitat; és un format binari columnar amb esquema.

### Exercici 5. Quin destí utilitza el Cas B?

**Resposta:** `/user/iabd/sqoop/customers/dades_avro`.

### Exercici 6. Una nova importació A falla perquè la ruta existeix. Què fas?

**Resposta:** primer inspecciones el directori. Només si el seu contingut és prescindible, pots eliminar-lo o fer servir `--delete-target-dir`; alternativament, uses una ruta nova.

### Exercici 7. Has d'explicar 4 fitxers `.avro`. Què significa?

**Resposta:** l'execució documentada ha produït quatre fitxers de sortida Avro. No implica que hi hagi quatre registres.

### Exercici 8. Vols verificar les files abans de Sqoop. Quines consultes fas?

```sql
SELECT COUNT(*) FROM orders WHERE order_status='COMPLETE';
SELECT COUNT(*) FROM customers
WHERE customer_state='CA' AND customer_id>99;
```

## 22. Preguntes d'autoavaluació amb resposta [AMPLIACIÓ]

1. **Què és Sqoop?** Eina de transferència batch entre sistemes relacionals i Hadoop.
2. **Quin és l'origen d'aquesta pràctica?** MariaDB/MySQL.
3. **Quina base de dades s'utilitza?** `retail_db`.
4. **Quin és el destí?** HDFS.
5. **Quines taules apareixen?** `orders` i `customers`.
6. **Quina comanda comprova la connectivitat?** `sqoop list-tables`.
7. **Què és JDBC?** Interfície Java per connectar amb bases de dades.
8. **Què indica `--connect`?** URL JDBC.
9. **Què significa `-P`?** Preguntar la contrasenya interactivament.
10. **Què fa `--table`?** Selecciona la taula.
11. **Què fa `--where`?** Filtra registres.
12. **Quin filtre s'aplica a `orders`?** `order_status='COMPLETE'`.
13. **Quants registres s'importen al Cas A?** 22.899 segons la captura.
14. **Quin format té el Cas A?** Parquet.
15. **Quina compressió té el Cas A?** Snappy.
16. **Què significa columnar?** Organització per columnes en lloc de registres.
17. **Per què no cal delimitador de camps a Parquet?** Perquè no és text delimitat.
18. **Què fa `--delete-target-dir`?** Elimina la ruta de destinació existent.
19. **Quin risc té aquesta opció?** Pèrdua de dades existents al destí.
20. **Quin filtre d'estat usa el Cas B?** `customer_state='CA'`.
21. **Quina columna controla la incrementalitat?** `customer_id`.
22. **Quin límit inicial té?** 99.
23. **Quins ID s'importen?** Els superiors a 99, sota el filtre d'estat.
24. **Quantes columnes s'importen al Cas B?** Quatre.
25. **Quin format té el Cas B?** Avro.
26. **Quina compressió té?** bzip2.
27. **Què fa `--incremental append`?** Importa valors nous d'una columna creixent.
28. **Què fa `--check-column`?** Designa la columna de seguiment.
29. **Què fa `--last-value`?** Estableix el punt de referència anterior.
30. **Quants registres es recuperen al Cas B?** 1.999 segons la captura.
31. **Quina marca suggereix Sqoop després?** `12429`.
32. **Què passa si es repeteix la importació amb `99`?** Pot reimportar registres.
33. **Quina diferència bàsica hi ha entre Avro i Parquet?** Avro s'orienta a registres; Parquet, a columnes.
34. **Un fitxer `.parquet` es llegeix correctament amb `cat`?** No com a CSV de text.
35. **Què aporta el log `Retrieved ... records`?** Evidència del recompte transferit.
36. **On es veu la presència física dels fitxers?** A HDFS, per consola o interfície web.
37. **Quants fitxers es mostren en cada cas?** Quatre fitxers de dades, segons les captures.
38. **És la ingesta un procés en temps real?** No; és una transferència batch.
39. **L'append incremental detecta necessàriament canvis en files antigues?** No.
40. **Què s'ha de guardar per a la següent execució incremental?** El nou `--last-value`.

## 23. Glossari [AMPLIACIÓ]

| Terme | Definició curta |
|---|---|
| Sqoop | Eina d'ingesta/exportació de dades estructurades |
| HDFS | Sistema de fitxers distribuït de Hadoop |
| YARN | Gestor de recursos del clúster |
| JDBC | Protocol/API de connectivitat Java amb BD |
| Mapper | Tasca paral·lela que processa una partició |
| Parquet | Format columnar binari |
| Avro | Format binari orientat a registres i esquemes |
| Snappy | Compressió ràpida |
| bzip2 | Compressió general d'alta reducció relativa |
| Importació incremental | Transferència dels registres nous des d'una marca |
| Check column | Camp sobre el qual es comprova la novetat |
| Last value | Valor límit d'una execució anterior |
| Filter/WHERE | Condició de selecció de registres |
| Target dir | Ruta de sortida HDFS |
| Idempotència | Capacitat de repetir una operació sense duplicar-ne l'efecte |

## 24. Checklist final d'examen

- [ ] Sé descriure el flux MariaDB → Sqoop → HDFS.
- [ ] Puc explicar cada opció de les dues comandes.
- [ ] Recordo els formats i codecs de cada cas.
- [ ] Distingeixo filtre `WHERE` i importació incremental.
- [ ] Sé què significa `--last-value` i per què s'ha d'actualitzar.
- [ ] Sé interpretar els missatges `Retrieved 22899 records` i `Retrieved 1999 records`.
- [ ] Recordo les rutes HDFS de destinació.
- [ ] Sé comprovar l'existència dels fitxers i els seus formats.
- [ ] Conec el risc de `--delete-target-dir`.
- [ ] Puc comparar Avro i Parquet en dues frases.

---

### Resum de 30 segons

**Cas A:** `orders` + `COMPLETE` → **Parquet/Snappy** → **22.899** registres a HDFS.  
**Cas B:** `customers` + `CA` + `customer_id > 99` → **Avro/bzip2** → **1.999** registres; nova marca **12429**.  
**Clau conceptual:** Sqoop connecta una BD relacional amb Hadoop i executa ingesta batch; el format, la compressió i el filtre es defineixen amb opcions explícites.

*Apunts basats en la pràctica lliurada. Els fragments complementaris són explicacions i propostes d'estudi, no resultats addicionals que s'hagin comprovat sobre la teva màquina.*
