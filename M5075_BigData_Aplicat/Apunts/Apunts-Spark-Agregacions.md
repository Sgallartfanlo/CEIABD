# Apunts extensos — PySpark: agregacions, JOIN, funcions i Pandas

## 1. Agregacions

Una **agregació** transforma un conjunt de files en un valor resum (o en un valor per cada grup). La guia utilitza un dataset de vendes amb camps com `Country`, `Zip`, `Units`, `Revenue` i `Date`.

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
spark = SparkSession.builder.appName('spark-agregacions').getOrCreate()
```

### `count` i `countDistinct`

```python
df.select(F.count('Country').alias('paisos_no_nuls')).show()
df.select(F.countDistinct('Country').alias('paisos_diferents')).show()
df.select(F.count('*').alias('totes_les_files')).show()
```

- `count('Country')`: compta els valors **no nuls** d'aquesta columna.
- `countDistinct('Country')` / `count_distinct`: valors únics no nuls.
- `count('*')`: totes les files, independentment de nuls d'altres columnes.
- `df.count()`: total de registres del DataFrame.

### `approx_count_distinct`

```python
df.select(F.approx_count_distinct('Zip').alias('codis_aprox')).show()
```

Aproxima la cardinalitat amb una estructura estadística més eficient en conjunts grans. El segon argument `rsd` controla l'error relatiu desitjat, **no és exactament una desviació estàndard general del dataset**. A la guia el resultat aproximat de `Zip` difereix del recompte exacte, cosa esperable.

## 2. Càlculs numèrics i estadística

```python
df.select(
    F.min('Units').alias('minim'),
    F.max('Units').alias('maxim'),
    F.sum('Revenue').alias('total'),
    F.avg('Revenue').alias('mitjana')
).show()
```

| Funció | Significat | Precaució |
|---|---|---|
| `min`, `max` | Mínim/màxim | ignoren valors nuls |
| `sum` | Suma | `NULL` si no hi ha valors agregables |
| `sum_distinct` | Suma de valors diferents | no és el mateix que `sum` |
| `avg` | Mitjana dels no nuls | `sum(x)/count(x)` si el conjunt és comparable |
| `stddev` / `stddev_pop` | desviació estàndard mostral/poblacional | diferent denominador |
| `variance` / `var_pop` | variància mostral/poblacional | diferent denominador |
| `skewness`, `kurtosis` | asimetria i curtosi | interpretació estadística |

**Exemple de diferència:** si `Units` és `[1, 1, 2]`, `sum` dona `4` i `sum_distinct` dona `3`.

## 3. Agrupar amb `groupBy` i `agg`

```python
df.groupBy('Country').count().show()
df.groupBy('Country').sum('Revenue').show()

resum = df.groupBy('Country').agg(
    F.count('*').alias('operacions'),
    F.sum('Revenue').alias('ingressos'),
    F.avg('Revenue').alias('tiquet_mitja')
)
resum.show()
```

`groupBy` **no** calcula encara el resultat; retorna una agrupació sobre la qual s'aplica una agregació. Podem agrupar per més d'una columna:

```python
df.groupBy('Country', 'Zip').agg(F.sum('Revenue').alias('total')).show()
```

També és possible:

```python
df.groupBy('Country').agg({'Zip': 'count', 'Revenue': 'avg'}).show()
```

**Ampliació:** `having` SQL equival a filtrar després d'una agregació:

```python
resum.filter(F.col('ingressos') > 1000).show()
```

## 4. Agregar col·leccions

La guia compara `collect_list` (pot conservar repetits) i `collect_set` (sense duplicats).

```python
df.filter(F.col('Units') > 5).groupBy('Country').agg(
    F.collect_list('Zip').alias('codis_amb_repeticions'),
    F.collect_set('Zip').alias('codis_unics')
).show(truncate=False)
```

L'ordre dels elements de les col·leccions després d'un shuffle pot no ser estable; si necessites un ordre determinista, utilitza `sort_array` sobre el resultat, quan sigui pertinent.

## 5. Taules pivot

Una taula **pivot** converteix valors d'una columna categòrica en columnes de sortida. El PDF mostra ingressos per any i país:

```python
from pyspark.sql.functions import year

df.groupBy(year('Date').alias('any')).pivot('Country').sum('Revenue').show()
```

Per calcular dues mesures:

```python
df.groupBy(F.year('Date')).pivot('Country').agg(
    F.sum('Revenue').alias('total'),
    F.sum('Units').alias('unitats')
).show()
```

**Ampliació:** quan coneixes els països possibles, indicar-los evita descobrir-los automàticament:

```python
df.groupBy('Date').pivot('Country', ['Canada','France','Germany','Mexico']).sum('Revenue')
```

Els `null` d'una pivot poden indicar combinacions sense registres, no necessàriament errors.

## 6. JOIN amb SQL

La guia utilitza dos fitxers: `departure_delays.csv` (vols: `date`, `delay`, `distance`, `origin`, `destination`) i `airport-codes-na.tsv` (aeroports: `City`, `State`, `Country`, `IATA`).

```python
vols = spark.read.option('header', True).option('inferSchema', True).csv('departure_delays.csv')
aeroports = spark.read.option('header', True).option('sep', '\t').csv('airport-codes-na.tsv')
vols.createOrReplaceTempView('vols')
aeroports.createOrReplaceTempView('aeroports')

resultat = spark.sql('''
SELECT v.origin, a.City AS ciutat_origen
FROM vols v
INNER JOIN aeroports a ON v.origin = a.IATA
''')
resultat.show(3)
```

Per obtenir origen i destinació en la mateixa fila, es fan **dues unions** amb la taula d'aeroports, usant dos àlies:

```python
consulta = spark.sql('''
SELECT v.*, a.City AS originCity, b.City AS destinationCity
FROM vols v
LEFT JOIN aeroports a ON v.origin = a.IATA
LEFT JOIN aeroports b ON v.destination = b.IATA
''')
```

**Per què `LEFT JOIN`?** Preserva els vols encara que algun codi IATA no sigui conegut; la ciutat corresponent apareix `NULL`. Si la taula d'aeroports té codis duplicats, el resultat podria multiplicar files.

## 7. JOIN amb l'API Python

```python
from pyspark.sql.functions import col

v = vols.alias('v')
a = aeroports.alias('a')
b = aeroports.alias('b')

unio = (v.join(a, col('v.origin') == col('a.IATA'), 'left')
         .join(b, col('v.destination') == col('b.IATA'), 'left')
         .select('v.*',
                 col('a.City').alias('originCity'),
                 col('b.City').alias('destinationCity')))
unio.show()
```

Quan la columna de join té el mateix nom als dos DataFrames, es pot indicar directament:

```python
df1.join(df2, 'user_id', 'inner')
```

## 8. Tipus de JOIN

| Tipus | Quines files reté? |
|---|---|
| `inner` | Només coincidències |
| `left` | Totes les de l'esquerra, i coincidències de la dreta |
| `right` | Totes les de la dreta, i coincidències de l'esquerra |
| `full` / `outer` | Totes de tots dos costats |
| `left_semi` | Files de l'esquerra amb coincidència; sense columnes dretes |
| `left_anti` | Files de l'esquerra **sense** coincidència |
| `cross` | Producte cartesià: pot créixer enormement |

```python
sense_aeroport = vols.join(aeroports, vols.origin == aeroports.IATA, 'left_anti')
sense_aeroport.count()
```

El document indica un recompte de **14.416** registres sense coincidència en l'exemple; és una dada del dataset docent, no un resultat universal.

**Diferència important:** `left_anti` és adequat per a detecció de codis desconeguts; `left_semi`, per comprovar existència de coincidència sense duplicar dades amb columnes dretes.

## 9. Funcions de dates

```python
from pyspark.sql import functions as F

df = df.withColumn('Date', F.to_date('Date', 'M/d/yyyy'))
df.select(
    'Date',
    F.date_format('Date', 'dd-MM-yyyy').alias('data_formatada'),
    F.next_day('Date', 'Sun').alias('proper_diumenge'),
    F.last_day('Date').alias('final_mes'),
    F.dayofmonth('Date').alias('dia'),
    F.dayofyear('Date').alias('dia_any'),
    F.month('Date').alias('mes'),
    F.year('Date').alias('any')
).show(3)
```

També hi ha `to_timestamp`, `unix_timestamp`, `from_unixtime`, `datediff`, `months_between`, `date_add` i `date_sub`. **Precaució:** els formats de data i les zones horàries afecten els resultats; comprova `printSchema()` abans de fer càlculs.

## 10. Funcions de cadenes

| Funció | Operació | Exemple |
|---|---|---|
| `trim`, `ltrim`, `rtrim` | elimina espais laterals | `F.trim('Country')` |
| `lower`, `upper`, `initcap` | majúscules/minúscules | `F.upper('Country')` |
| `length`, `reverse` | longitud/inverteix | `F.length('Zip')` |
| `substring` | extreu substring | `F.substring('Country',3,2)` |
| `split` | divideix en array | `F.split('Country','a')` |
| `locate` | busca una subcadena | `F.locate('a','Country')` |
| `concat`, `concat_ws` | concatena | `F.concat_ws('-', 'City','State')` |
| `translate` | substitucions caràcter a caràcter | `F.translate('Country','na','pe')` |
| `regexp_extract`, `regexp_replace` | expressió regular | neteja avançada |
| `levenshtein` | distància d'edició | similitud textual |

```python
df.select('Country', F.trim('Country').alias('net'),
          F.lower('Country').alias('minuscules'),
          F.substring('Country', 3, 2).alias('pos3_2')).show()
```

## 11. Arrays, structs i dades imbricades

La guia carrega un JSON de negocis de Yelp, amb `categories: array<string>` i un objecte `hours` imbricat.

```python
negocis = spark.read.json('yelp_academic_dataset_business.json')
negocis.printSchema()

negocis.select(
    'name',
    F.col('hours.Sunday').alias('horari_diumenge'),
    F.size('categories').alias('n_categories'),
    F.sort_array('categories').alias('categories_ordenades'),
    F.array_contains('categories', 'Restaurants').alias('es_restaurant')
).show(truncate=False)
```

`hours.Sunday` accedeix a una propietat d'un `struct`. `array_contains` retorna un booleà. `sort_array` ordena els elements d'un array.

### `explode`

```python
negocis.select('name', F.explode('categories').alias('categoria')).show(10)
```

Transforma cada element d'un array en una fila. **Consequència:** augmenta el nombre de files. Per conservar files amb array buit o nul pots estudiar `explode_outer` (ampliació).

## 12. JSON com a text i com a `struct`

El PDF construeix una cadena JSON amb un dia i una llista de tasques. Amb `from_json` i un esquema explícit la convertim en dades amb tipus.

```python
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

esquema = StructType([
    StructField('dia', StringType(), True),
    StructField('tareas', ArrayType(StringType()), True),
])

raw = spark.createDataFrame([
    ('{"dia":"Dilluns","tareas":["Estudiar","Entrenar"]}',)
], ['valor'])

parsed = raw.select(F.from_json('valor', esquema).alias('dades'))
parsed.select('dades.dia', F.col('dades.tareas')[0].alias('primera')).show()
parsed.select(F.to_json('dades').alias('json')).show(truncate=False)
```

- `from_json`: text JSON → estructura tipada.
- `to_json`: estructura → text JSON.
- `getItem` i `[0]`: accés a posicions d'array; indexació des de zero.

## 13. UDF (funcions d'usuari)

La guia crea una funció `bonus` que aplica una regla condicionada al nombre d'unitats.

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType

def bonus(units, revenue):
    if units is None or revenue is None:
        return None
    return 0.0 if units == 1 else units * revenue / 100

udf_bonus = udf(bonus, DoubleType())
df.select('Units','Revenue', udf_bonus('Units','Revenue').alias('bonus')).show()
```

**Aclariment important:** la formulació de càlcul anterior segueix l'operació `units * revenue / 100` del PDF, però això **no equival** a un simple 1% dels ingressos si `Revenue` és l'import total: el multiplicador `units` ho modifica. Per calcular exactament un 1% d'ingressos condicionat a més d'una unitat:

```python
df.withColumn('bonus_1pct', F.when(F.col('Units') > 1, F.col('Revenue') * 0.01).otherwise(0))
```

**Millor pràctica:** utilitza expressions natives (`when`, `col`, `expr`) quan sigui possible; acostumen a optimitzar-se millor que les UDF Python.

## 14. Cache i persistència

```python
df.cache()
df.count()          # força materialització del cache
df.unpersist()      # allibera recursos
```

Quan reutilitzes el mateix DataFrame moltes vegades, cachejar pot evitar recàlculs. La pestanya **Storage** de Spark UI (pàgina 25 del PDF) ajuda a comprovar-ho. `persist()` permet especificar nivells d'emmagatzematge. No s'ha de posar cache a tot: consumeix recursos, pot incrementar GC i perjudicar altres processos.

## 15. DataFrames i Pandas

```python
# Només si el resultat és petit i cap a la RAM del driver.
pdf = df.limit(1000).toPandas()
print(pdf.head())
```

`toPandas()` transfereix dades al driver: **pot causar OutOfMemory** amb datasets grans, advertència destacada a la pàgina 29. La guia també presenta l'API de pandas sobre Spark (segons la versió, `pyspark.pandas` o alternatives més modernes); no confondre-la amb un DataFrame Pandas local.

## 16. Pràctiques guiades (ampliació)

### Pràctica A. Vendes agregades

```python
vendes = spark.createDataFrame([
    ('Girona', 1, 100.0), ('Girona', 3, 200.0),
    ('Blanes', 2, 50.0), ('Blanes', 2, None)
], ['ciutat','unitats','ingressos'])

vendes.groupBy('ciutat').agg(
    F.count('*').alias('operacions'),
    F.sum('ingressos').alias('ingressos'),
    F.avg('ingressos').alias('mitjana')
).show()
```

### Pràctica B. Anti-join per identificar errors de referència

```python
comandes = spark.createDataFrame([(1,'A'),(2,'X'),(3,'B')], ['id','producte'])
cataleg = spark.createDataFrame([('A',),('B',)], ['producte'])
comandes.join(cataleg, 'producte', 'left_anti').show()  # X
```

### Pràctica C. Categories multilabel

```python
items = spark.createDataFrame([('A',['IA','Big Data']),('B',['Docker'])], ['nom','etiquetes'])
items.select('nom', F.explode('etiquetes').alias('etiqueta')).show()
```

## 17. Errors habituals

| Error | Per què passa | Solució |
|---|---|---|
| `AnalysisException` per nom de columna | columna mal escrita o duplicada després de JOIN | `printSchema`, `alias`, `select` |
| `Cannot resolve function` | funció no importada o versió incompatible | `from pyspark.sql import functions as F` |
| Data convertida a `string` | `inferSchema` insuficient o dades mixtes | esquema explícit, `cast` |
| Resultat JOIN massa gran | claus duplicades o cartesià accidental | comprovar `distinct`, claus i condicions |
| `NULL` en pivot | combinació absent | decidir si `fillna(0)` és adequat |
| `OutOfMemory` en Pandas | moltes files transferides al driver | agregació/mostra abans de `toPandas` |
| Cache no ajuda | només un ús o no materialitzat | mesurar temps i mirar Storage |
| UDF lenta | travessa frontera Python/JVM | funcions natives |

## 18. Glossari i resum

**Agregació:** resum de dades. **Cardinalitat:** nombre de valors diferents. **GroupBy:** agrupació. **Pivot:** categories convertides en columnes. **JOIN:** encreuament de datasets. **Anti-join:** files sense coincidència. **Array:** col·lecció. **Struct:** conjunt de camps imbricats. **Explode:** array → diverses files. **UDF:** funció definida per usuari. **Cache:** reutilització de resultats. **Pandas:** anàlisi local, diferent de PySpark distribuït.

Per a l'examen: recorda la diferència entre `count('*')` i `count(columna)`, entre `collect_list` i `collect_set`, entre `inner` i `left`, entre `left_anti` i `left_semi`, i entre `toPandas` i DataFrames distribuïts.

---

## Autoavaluació — 40 preguntes amb respostes

**1. Què calcula count(col)?**  
**Resposta:** El nombre de valors no nuls de la columna.

**2. Com es compten totes les files amb funcions SQL?**  
**Resposta:** Amb count("*").

**3. Què és count_distinct?**  
**Resposta:** El recompte exacte de valors diferents no nuls.

**4. Què és approx_count_distinct?**  
**Resposta:** Una estimació eficient de la cardinalitat.

**5. Quina diferència hi ha entre sum i sum_distinct?**  
**Resposta:** La segona només suma una vegada cada valor diferent.

**6. Què és avg?**  
**Resposta:** La mitjana dels valors no nuls.

**7. Quina diferència hi ha entre stddev i stddev_pop?**  
**Resposta:** Desviació mostral versus poblacional.

**8. Què retorna groupBy?**  
**Resposta:** Un objecte d’agrupació per aplicar-hi agregacions.

**9. Per què serveix agg?**  
**Resposta:** Per calcular una o diverses mesures sobre un grup.

**10. Què fa alias?**  
**Resposta:** Canvia el nom de visualització d’una expressió o columna.

**11. Quina diferència hi ha entre collect_list i collect_set?**  
**Resposta:** La llista pot conservar repetits; el set elimina duplicats.

**12. L’ordre de collect_list és sempre estable després de shuffle?**  
**Resposta:** No necessàriament.

**13. Què és una taula pivot?**  
**Resposta:** Un resum que converteix valors d’una categoria en columnes.

**14. Què és un inner join?**  
**Resposta:** Una unió que reté coincidències entre les dues bandes.

**15. Què és un left join?**  
**Resposta:** Conserva les files de l’esquerra encara que no coincideixin.

**16. Què és left_anti?**  
**Resposta:** Files de l’esquerra sense correspondència a la dreta.

**17. Què és left_semi?**  
**Resposta:** Files de l’esquerra amb coincidència, sense afegir columnes dretes.

**18. Quan serveix un doble join?**  
**Resposta:** Quan una taula de referència resol dos camps, com origen i destinació.

**19. Per què utilitzem alias a les unions?**  
**Resposta:** Per evitar ambigüitat de columnes.

**20. Què és cross join?**  
**Resposta:** Producte cartesià entre les files dels dos DataFrames.

**21. Per què un join pot duplicar files?**  
**Resposta:** Si les claus tenen diverses coincidències a l’altra taula.

**22. Què fa to_date?**  
**Resposta:** Converteix text a dada tipus data segons format.

**23. Què fa date_format?**  
**Resposta:** Formata una data com a cadena de text.

**24. Què fa last_day?**  
**Resposta:** Retorna l’últim dia del mes.

**25. Què fa trim?**  
**Resposta:** Elimina espais laterals d’una cadena.

**26. Què fa substring?**  
**Resposta:** Extreu una subcadena.

**27. Què fa split?**  
**Resposta:** Divideix una cadena en un array.

**28. Què fa regexp_replace?**  
**Resposta:** Substitueix coincidències d’una expressió regular.

**29. Què és un struct?**  
**Resposta:** Una columna estructurada amb camps interns.

**30. Què és un array?**  
**Resposta:** Una columna que conté múltiples elements.

**31. Què fa explode?**  
**Resposta:** Genera una fila per cada element d’un array.

**32. Què fa size?**  
**Resposta:** Retorna la mida d’una col·lecció.

**33. Què fa array_contains?**  
**Resposta:** Comprova si un element existeix dins d’un array.

**34. Què fa from_json?**  
**Resposta:** Analitza text JSON i el converteix a una estructura tipada.

**35. Què fa to_json?**  
**Resposta:** Converteix una estructura en cadena JSON.

**36. Què és una UDF?**  
**Resposta:** Una funció creada per l’usuari per estendre el processament.

**37. Per què preferir funcions natives abans de UDF Python?**  
**Resposta:** Perquè solen optimitzar-se millor i evitar conversions Python/JVM.

**38. Què fa cache?**  
**Resposta:** Marca dades per a persistència i reutilització.

**39. Què fa unpersist?**  
**Resposta:** Allibera les dades persistides.

**40. Quin risc presenta toPandas?**  
**Resposta:** Carrega totes les files seleccionades a la memòria del driver.

---

## Checklist final per estudiar

- [ ] Puc explicar sense mirar els apunts els conceptes principals.
- [ ] Sé escriure i executar els exemples sense copiar-los literalment.
- [ ] Entenc què passa a cada etapa de les comandes.
- [ ] Sé identificar els errors típics i resoldre'ls.
- [ ] He provat els exercicis en un entorn de pràctiques.
- [ ] He fet les preguntes d'autoavaluació sense mirar les respostes.

**Fonts:** document docent indicat a la capçalera. Els exercicis d'ampliació i les recomanacions són complementaris al material original. Per verificar les APIs d'una versió concreta, consulta la documentació oficial d'Apache Spark i dels connectors instal·lats.
