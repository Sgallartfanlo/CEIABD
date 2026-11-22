# Apunts extensos — Apache Spark: fonaments, desplegament i arquitectura

## 1. Què és Apache Spark i per què serveix?

**Apache Spark** és un motor de processament de dades distribuït. Permet executar càlculs sobre conjunts de dades que poden estar repartits entre diverses màquines. No és un llenguatge de programació, ni un sistema de fitxers, ni una base de dades. La lògica es pot escriure en Python (PySpark), Scala, Java, SQL i R.

La guia emmarca Spark dins del cicle d'analítica de dades: ingestió, neteja, validació, transformació, agregació, exploració, anàlisi i generació de resultats. Spark pot treballar en un ordinador únic, en un clúster o en serveis gestionats.

**Diferencia essencial:** Spark executa la computació; les dades es poden emmagatzemar a HDFS, S3, bases de dades o altres sistemes. Per això Hadoop i Spark són complementaris.

### Exemple conceptual de pipeline

```text
CSV / JSON / HDFS / S3 / JDBC
             │
             ▼
       Spark DataFrame
             │
   netejar → filtrar → unir
             │
         agrupar
             │
        persistir
             ▼
       Parquet / taula
```

## 2. Spark i Hadoop: similituds i diferències

| Aspecte | Hadoop MapReduce | Apache Spark |
|---|---|---|
| Funció | Model/motor de processament batch | Motor de computació general |
| Resultats intermedis | Sovint materialitzats a disc entre fases | Pot reutilitzar dades en memòria amb cache/persist |
| Interactivitat | Menys convenient | API interactiva i SQL |
| Algorismes iteratius | Poden repetir costoses E/S | Pot accelerar iteracions si es reutilitzen dades |
| Emmagatzematge | Normalment HDFS | HDFS, fitxers locals, S3, JDBC, etc. |
| Gestió de recursos | YARN per a MapReduce modern | Standalone, YARN, Kubernetes i altres segons versió |

La guia destaca la rapidesa de Spark, les estructures en memòria i l'avaluació diferida (*lazy*). **Matís important:** Spark no guarda automàticament *totes* les dades ni *tots* els resultats en RAM; utilitza memòria i disc segons el pla d'execució, la mida de les dades i si es fa `cache()` o `persist()`.

## 3. Característiques clau

### 3.1 Velocitat
Spark optimitza les operacions amb un pla d'execució. Les transformacions formen un **DAG** (*Directed Acyclic Graph*, graf dirigit acíclic); el planificador l'organitza en treballs, etapes i tasques. La guia esmenta també Tungsten i les optimitzacions del motor.

### 3.2 Facilitat d'ús
L'API permet expressar transformacions d'alt nivell com `select`, `filter`, `groupBy`, `join` i accions com `count`, `show`, `collect` o `write`.

### 3.3 Modularitat
Spark inclou SQL/DataFrames, streaming, eines de machine learning i biblioteques per a grafs.

### 3.4 Flexibilitat
Funciona amb dades tabulars, textos, fitxers estructurats i múltiples orígens, tant en batch com en flux.

## 4. Stack unificat de Spark

La figura de components de la **pàgina 5** situa Spark Core sota les API de Python, R, Scala, SQL i Java i els mòduls de processament.

| Mòdul | Què resol | Exemple |
|---|---|---|
| Spark Core | Execució distribuïda, planificació i tolerància a fallades | `sc.parallelize(...)` |
| Spark SQL | SQL, DataFrames i formats estructurats | `spark.sql(...)` |
| Structured Streaming | Processar fluxos de dades | lectura contínua de Kafka |
| MLlib | Machine learning | classificació, regressió, pipelines |
| GraphX | Algorismes sobre grafs (principalment Scala/Java) | relacions entre entitats |

### Exemple del document: JSON i vista temporal

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('consulta-zips').getOrCreate()
df_zips = spark.read.json('zips.json')
df_zips.createOrReplaceTempView('zips')
df_resultat = spark.sql('''
    SELECT city, state
    FROM zips
    WHERE pop > 10000
    ORDER BY pop DESC
''')
df_resultat.show()
```

**Explicació:** `read.json` construeix un DataFrame; `createOrReplaceTempView` registra un nom de consulta dins de la sessió; `spark.sql` construeix un altre DataFrame; `show` activa l'execució. La vista temporal no és una taula persistent.

## 5. API, formats i connectors

**RDD:** abstracció distribuïda de baix nivell, útil per a certes operacions amb `SparkContext`. **DataFrame:** dades distribuïdes amb columnes i esquema; permet optimització SQL. **Dataset:** abstracció tipada disponible especialment a Scala/Java; en PySpark s'utilitza habitualment DataFrame.

Formats treballats o esmentats al PDF: text, CSV, JSON, Parquet, ORC i Avro. Fonts de dades: HDFS, S3, emmagatzematge local, Hive, bases relacionals JDBC i ecosistemes com Kafka i Cassandra (amb connectors adequats).

## 6. PySpark i Jupyter

En l'entorn docent la comanda `pyspark` està preparada per obrir un notebook; en una instal·lació ordinària, sovint obre una consola interactiva PySpark.

```bash
pyspark
```

Per iniciar Jupyter automàticament des de PySpark, al `~/.bashrc`:

```bash
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS=notebook
source ~/.bashrc
```

Per generar la configuració de Jupyter:

```bash
jupyter notebook --generate-config
```

El material de classe indica l'opció `c.ServerApp.ip` al fitxer de configuració. **Ampliació de seguretat:** evitar exposar Jupyter o Spark UI directament a Internet; preferir `127.0.0.1`, túnels SSH i autenticació. El token que apareix a la consola és secret d'accés temporal i no s'ha de compartir.

**Qui calcula què?** Jupyter és la interfície de codi i visualització; les operacions de dades les executa Spark (driver i executors).

## 7. Execució amb Docker

La guia presenta les imatges `jupyter/pyspark-notebook` de Jupyter Docker Stacks. Exemple adaptat:

```bash
docker run -d --name pyspark \
  -v "${PWD}:/home/jovyan/work" \
  -p 127.0.0.1:8888:8888 \
  -p 127.0.0.1:4040:4040 \
  jupyter/pyspark-notebook
```

- `-d`: contenidor en segon pla.
- `--name`: nom identificable.
- `-v`: bind mount de la carpeta actual.
- `-p`: exposició de ports. El port 8888 és del notebook i el 4040, habitualment, de la Spark UI.

```bash
docker logs pyspark
docker exec -it pyspark bash
docker stop pyspark
docker start pyspark
```

**Ampliació:** la imatge sense etiqueta fixa canvia amb el temps. Per reproduir les pràctiques convé fixar una versió compatible amb Java/Python.

## 8. Clúster Standalone

La guia diferencia un node amb servei **master** i altres nodes que executen **workers**:

```bash
$SPARK_HOME/sbin/start-master.sh -h 0.0.0.0
$SPARK_HOME/sbin/start-worker.sh spark://IP_DEL_MASTER:7077
```

Per limitar CPU i RAM disponibles d'un worker:

```bash
$SPARK_HOME/sbin/start-worker.sh -c 8 -m 16G spark://IP_DEL_MASTER:7077
```

El navegador del master acostuma a mostrar la interfície a `http://IP_DEL_MASTER:8080`. **No confondre:** el *master* del gestor Standalone no és necessàriament el *driver* de cada aplicació. Els workers ofereixen recursos; els **executors** són processos llançats per executar tasques d'una aplicació.

## 9. Spark al núvol

### Google Colab
El PDF mostra una instal·lació manual de Spark dins d'un notebook. Per estudiar és important retenir el patró: preparar Java/Python, instal·lar dependències, inicialitzar `SparkSession` i executar codi. **Les versions concretes Java/Spark/PySpark de l'exemple poden ser incompatibles** si es barregen; no s'ha d'aplicar cegament el bloc de la guia.

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[*]').appName('colab').getOrCreate()
```

`local[*]` utilitza els nuclis disponibles a la màquina virtual de Colab, no un clúster extern per defecte.

### Databricks
La guia descriu notebooks, workspace, catàlegs i execució gestionada. Exemple basat en el material:

```python
numbers_df = spark.range(101)  # del 0 al 100
resultat = numbers_df.selectExpr('sum(id) AS total').collect()[0]['total']
print(resultat)  # 5050
```

**Diferència clau:** Spark és el motor de codi obert; Databricks és una plataforma de treball i serveis gestionats. El document també presenta Delta Lake i el concepte *lakehouse*.

## 10. SparkContext i SparkSession

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('m5075').getOrCreate()
sc = spark.sparkContext
```

| Objecte | Funció | API típica |
|---|---|---|
| `SparkContext` (`sc`) | Accés de baix nivell al motor i RDD | `sc.parallelize` |
| `SparkSession` (`spark`) | Punt d'entrada recomanat per a DataFrames i SQL | `spark.read`, `spark.sql` |

Evita crear diversos `SparkContext` independents en el mateix procés. `getOrCreate()` recupera la sessió existent o en crea una.

## 11. Hola Spark i `spark-submit`

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('hola-spark').getOrCreate()
sc = spark.sparkContext
rdd = sc.parallelize(range(101))
print('Suma:', rdd.sum())   # 5050
spark.stop()
```

Desa com `holaSpark.py` i executa:

```bash
spark-submit holaSpark.py
```

Contra un master Standalone:

```bash
spark-submit --master spark://IP_DEL_MASTER:7077 holaSpark.py
```

La pàgina 23 del PDF alterna els noms `holaSpark.py` i `holaMundo.py`; utilitza **el nom real del teu fitxer**. Si les variables de Jupyter interfereixen amb l'execució de scripts, comprova `PYSPARK_DRIVER_PYTHON` i l'entorn.

## 12. Spark i S3 (AWS)

Per llegir amb `s3a://`, el PDF mostra l'ús de biblioteques `hadoop-aws` i AWS SDK i de credencials. La compatibilitat entre les versions dels `.jar` de Hadoop, l'SDK i Spark és imprescindible.

```python
# Suposa connector S3A i credencials ja configurats de forma segura.
df = spark.read.option('header', True).csv('s3a://EL_TEU_BUCKET/dades.csv')
```

**Ampliació de seguretat:** no incrustis claus AWS en notebooks o fitxers que publicaràs; utilitza rols, perfils o mecanismes gestionats de credencials.

## 13. Arquitectura d'una aplicació Spark

```text
Usuari / Notebook / spark-submit
              │
              ▼
         DRIVER (SparkSession)
              │ petició de recursos
              ▼
       CLUSTER MANAGER
              │
      ┌───────┴────────┐
      ▼                ▼
   WORKER A         WORKER B
   Executor 1       Executor 2
   tasca A, B       tasca C, D
   cache local      cache local
```

La figura de la **pàgina 26** separa driver, gestor del clúster i executors. El **driver** crea el pla, coordina les tasques i pot recollir resultats; el **gestor del clúster** assigna recursos; els **executors** processen particions i poden desar dades en cache.

Els executors no són màquines físiques: són processos que s'executen als workers. Una aplicació pot utilitzar diversos executors i cada executor pot executar diverses tasques simultàniament, segons nuclis disponibles.

## 14. DAG → Job → Stage → Task

- **Job:** execució desencadenada per una acció com `count()`, `collect()` o una escriptura.
- **Stage:** grup de tasques que poden executar-se sense creuar certes dependències de dades; un *shuffle* sol introduir límits entre stages.
- **Task:** operació concreta sobre una partició en un executor.
- **Partició:** fragment lògic de dades utilitzat per paral·lelitzar.

```text
read CSV ── filter ── select ── groupBy ── count
    │         transformacions lazy      │
    └─── pla de càlcul (DAG) ────────────┘
                                         ↓ acció
                                   Job / Stages / Tasks
```

**Matís per a l'examen:** `filter()` no executa necessàriament res immediatament. Una acció activa el càlcul necessari; poden existir excepcions per operacions que requereixen inspeccions o metadades.

## 15. DataFrames i primera transformació

Exemple de la guia a partir d'un text del Quixot:

```python
text = spark.read.text('el_quijote.txt')
text.printSchema()              # value: string
text.first()                    # primera fila
amb_quixot = text.filter(text.value.contains('Quijote'))
print(amb_quixot.count())       # activa el càlcul
```

**No memoritzis els recomptes com a constants:** depenen de la versió del fitxer. `count()` compta files; `first()` obté la primera fila; `filter()` produeix un DataFrame derivat.

### Transformació vs acció

| Transformacions | Accions |
|---|---|
| `filter`, `select`, `withColumn`, `groupBy`, `join` | `count`, `show`, `collect`, `first`, `write` |
| Retornen una descripció de dades derivades | Demanen un resultat o provoquen escriptura |

## 16. Spark UI

En una aplicació local activa, habitualment `http://localhost:4040`; el port pot variar si ja està ocupat. Les pàgines 29–30 del PDF mostren dades de monitoratge.

| Pestanya | Què mirar |
|---|---|
| Jobs | Treballs executats, durada i estat |
| Stages | Etapes i temps de tasques |
| Storage | DataFrames/RDD persistits |
| Executors | Recursos, errors i rendiment |
| SQL | Pla de consultes DataFrame/SQL quan està disponible |

## 17. Pràctica completa guiada (ampliació)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

spark = SparkSession.builder.appName('practica-intro-spark').getOrCreate()
dades = [('Girona', 10), ('Blanes', 20), ('Girona', 12), ('Blanes', None)]
df = spark.createDataFrame(dades, ['ciutat', 'vendes'])
df.printSchema()
df.show()

net = df.filter(col('vendes').isNotNull())
resum = net.groupBy('ciutat').agg(count('*').alias('operacions'))
resum.show()
resum.explain(True)
spark.stop()
```

**Preguntes sobre la pràctica:** per què el nombre de files canvia després de `filter`? Per què l'agregació fa un agrupament? Quines accions activen jobs? Com ho mostraries a Spark UI?

## 18. Errors habituals i precaucions

| Símptoma | Possible causa | Com comprovar-ho |
|---|---|---|
| `ModuleNotFoundError: pyspark` | PySpark fora de l'entorn Python | `python -m pip show pyspark` |
| Jupyter no es connecta | URL/token/port o bind incorrecte | logs de Jupyter i port 8888 |
| `JAVA_HOME` incorrecte | Java no localitzat o incompatible | `java -version`, `echo "$JAVA_HOME"` |
| `FileNotFoundException` | Ruta local diferent de la ruta visible als executors | ruta del notebook, `pwd`, HDFS o volum |
| Spark UI no accessible | Aplicació finalitzada / port diferent / xarxa | logs del driver |
| Error `OutOfMemory` | `collect()` de massa registres o memòria insuficient | evitar portar tot al driver |
| `spark-submit` no troba el script | Ruta o nom incoherent | `ls -l`, ruta absoluta |

**Versions:** el PDF barreja captures i exemples de diverses versions. Revisa la documentació del teu entorn abans de copiar instruccions de Colab o dependències AWS. Les afirmacions de rendiment no són garanties universals.

## 19. Glossari i esquema d'examen

- **PySpark:** API Python de Spark.
- **Driver:** procés que coordina l'aplicació.
- **Executor:** procés que executa tasques i emmagatzema partitions/cache.
- **Worker:** node/servei que ofereix recursos de càlcul.
- **Cluster manager:** assigna recursos.
- **DAG:** graf de dependències de les operacions.
- **Job:** conjunt de treball activat per una acció.
- **Stage:** conjunt de tasques d'una fase del job.
- **Task:** unitat de computació per partició.
- **RDD:** col·lecció distribuïda de baix nivell.
- **DataFrame:** taula distribuïda amb esquema.
- **Lazy evaluation:** diferiment de transformacions.
- **Cache:** persistència per reutilitzar dades.
- **Spark UI:** interfície de monitoratge.

**Per memoritzar:** `SparkSession` és la porta d'entrada habitual; Spark processa, HDFS/S3 emmagatzemen, YARN o Standalone administren recursos; una acció dona lloc a computació distribuïda.

---

## Autoavaluació — 40 preguntes amb respostes

**1. Què és Spark?**  
**Resposta:** Un motor de processament distribuït de dades, no un llenguatge ni un sistema de fitxers.

**2. Què és PySpark?**  
**Resposta:** L’API Python d’Apache Spark.

**3. Per què Spark i Hadoop es complementen?**  
**Resposta:** Spark calcula; Hadoop pot aportar HDFS per guardar dades i YARN per gestionar recursos.

**4. Què representa un DAG?**  
**Resposta:** Un graf dirigit acíclic amb les dependències de les operacions.

**5. Per a què serveix Spark SQL?**  
**Resposta:** Per treballar amb DataFrames i executar consultes SQL.

**6. Què fa MLlib?**  
**Resposta:** Aporta algorismes i pipelines de machine learning.

**7. Què és Structured Streaming?**  
**Resposta:** L’API de processament incremental de dades en flux.

**8. Quina diferència hi ha entre Spark i Databricks?**  
**Resposta:** Spark és el motor obert; Databricks és una plataforma gestionada sobre aquesta tecnologia i altres components.

**9. Què és SparkSession?**  
**Resposta:** El punt d’entrada principal per a DataFrames i SQL.

**10. Què és SparkContext?**  
**Resposta:** Un context de baix nivell per a RDD i funcionalitats del motor.

**11. Com s’accedeix al SparkContext des d’una sessió?**  
**Resposta:** Amb spark.sparkContext.

**12. Què retorna spark.range(101)?**  
**Resposta:** Un DataFrame amb els valors del 0 al 100.

**13. Quina és la suma dels nombres del 0 al 100?**  
**Resposta:** 5050.

**14. Què fa local[*]?**  
**Resposta:** Executa Spark en mode local utilitzant els nuclis disponibles.

**15. Quina és la funció del driver?**  
**Resposta:** Crear plans, coordinar tasques i interactuar amb el gestor del clúster.

**16. Què és un executor?**  
**Resposta:** Un procés que executa tasques i pot mantenir particions en cache.

**17. Què és un worker?**  
**Resposta:** Un node o servei que ofereix recursos al gestor de clúster.

**18. Què fa un cluster manager?**  
**Resposta:** Assigna recursos als processos de les aplicacions.

**19. Què és un job?**  
**Resposta:** Una unitat de computació desencadenada per una acció.

**20. Què és un stage?**  
**Resposta:** Una part d’un job formada per tasques paral·lelitzables.

**21. Què és una task?**  
**Resposta:** La unitat més petita de càlcul que s’envia a un executor.

**22. Què és una partició?**  
**Resposta:** Una divisió lògica de dades sobre la qual es pot treballar en paral·lel.

**23. Què és lazy evaluation?**  
**Resposta:** Les transformacions defineixen un pla, i el càlcul s’executa en demanar una acció.

**24. És filter una transformació?**  
**Resposta:** Sí.

**25. És count una acció?**  
**Resposta:** Sí.

**26. Què fa createOrReplaceTempView?**  
**Resposta:** Registra una vista SQL temporal de sessió.

**27. Què fa spark-submit?**  
**Resposta:** Envia una aplicació Spark per executar-la amb la configuració del clúster.

**28. Quin port és habitual per Spark UI local?**  
**Resposta:** 4040, si està disponible.

**29. Quin port és habitual del master Standalone UI?**  
**Resposta:** 8080.

**30. Quin port de master Standalone s’usa als exemples?**  
**Resposta:** 7077.

**31. Què fa `docker -v`?**  
**Resposta:** Munta un volum o una carpeta host al contenidor.

**32. Quina diferència hi ha entre Jupyter i Spark?**  
**Resposta:** Jupyter és la interfície; Spark executa les transformacions.

**33. Per què no s’ha de fer collect() sobre dades enormes?**  
**Resposta:** Pot portar massa dades a la RAM del driver.

**34. Què és S3A?**  
**Resposta:** El connector Hadoop per accedir a dades d’Amazon S3.

**35. Què és un RDD?**  
**Resposta:** Una col·lecció distribuïda de baix nivell.

**36. Per què usar DataFrames?**  
**Resposta:** Ofereixen esquema i optimització per al motor Spark SQL.

**37. Què mostra la pestanya Jobs?**  
**Resposta:** Estat i durada dels treballs.

**38. Què mostra la pestanya Storage?**  
**Resposta:** Informació sobre dades persistides en memòria/disc.

**39. On es poden mirar errors de les tasques?**  
**Resposta:** Als logs d’executors i a les pestanyes Stages/Executors.

**40. Quin és un avantatge del processament en memòria?**  
**Resposta:** Pot reduir lectures i escriptures intermèdies repetides.

---

## Checklist final per estudiar

- [ ] Puc explicar sense mirar els apunts els conceptes principals.
- [ ] Sé escriure i executar els exemples sense copiar-los literalment.
- [ ] Entenc què passa a cada etapa de les comandes.
- [ ] Sé identificar els errors típics i resoldre'ls.
- [ ] He provat els exercicis en un entorn de pràctiques.
- [ ] He fet les preguntes d'autoavaluació sense mirar les respostes.

**Fonts:** document docent indicat a la capçalera. Els exercicis d'ampliació i les recomanacions són complementaris al material original. Per verificar les APIs d'una versió concreta, consulta la documentació oficial d'Apache Spark i dels connectors instal·lats.
