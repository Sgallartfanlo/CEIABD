# M05075 - BigData Aplicat
## Activitat 2: Primers passos amb Hadoop

* **Nom de l'alumnat:** Sergi Gallart Fanlo
* **Professor:** Joan Pou
* **Curs:** 2026/2027
* **Centre:** Institut Sa Palomera (CE IA&BD)

---

## Taula de Continguts
1. [Estimació del número Pi amb MapReduce](#1-estimació-del-número-pi-amb-mapreduce)
2. [Comptador de paraules de "Tirant lo Blanc" amb Python i Hadoop Streaming](#2-comptador-de-paraules-de-tirant-lo-blanc-amb-python-i-hadoop-streaming)
   - [2.1 Script del Mapper (`mapper.py`)](#21-script-del-mapper-mapperpy)
   - [2.2 Script del Reducer (`reducer.py`)](#22-script-del-reducer-reducerpy)
   - [2.3 Prova de funcionament en local](#23-prova-de-funcionament-en-local)
   - [2.4 Execució del Job a Hadoop Streaming](#24-execució-del-job-a-hadoop-streaming)
   - [2.5 Verificació dels resultats a HDFS](#25-verificació-dels-resultats-a-hdfs)
3. [Monitorització i Administració amb Hadoop UI, YARN i JobHistoryServer](#3-monitorització-i-administració-amb-hadoop-ui-yarn-i-jobhistoryserver)

---

## 1. Estimació del número Pi amb MapReduce

### Comanda executada:
```bash
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.4.3.jar pi 8 24
```

### Resultat obtingut:
```text
Executem l'exemple inclòs en la distribució de Hadoop per estimar el valor de pi
mitjançant el mètode de Montecarlo
Job Finished in 42.974 seconds
Estimated value of Pi is 3.08333333333333333333
```

### Explicació del procés:
Es llança un job de MapReduce que utilitza el mètode de Montecarlo per calcular una aproximació del número $\pi$. S'executen **8 tasques Mapper** en paral·lel i cadascuna genera **24 mostres**. El resultat final obtingut és `3.0833333333333333`.

#### Pregunta: En canviar els valors de 8 i de 24, què estem canviant realment? El resultat varia?
* **8:** Modifiquem el nombre de tasques *Mapper* que s'executen en paral·lel.
* **24:** Modifiquem el nombre de mostres (punts aleatoris) que genera cada *Mapper*.
* **Variació del resultat:** Sí que varia el resultat. En tractar-se d'un mètode d'estimació probabilístic basat en punts aleatoris, com més gran sigui el nombre total de mostres (`Mappers × Mostres`), més precisa serà l'aproximació al valor real de $\pi$.

---

## 2. Comptador de paraules de "Tirant lo Blanc" amb Python i Hadoop Streaming

L'objectiu és comptar les paraules del text *Tirant lo Blanc* aplicant les següents regles de neteja:
1. El procés de mapatge ha de netejar les paraules de signes ortogràfics (punts, comes, parèntesis, etc.).
2. Les paraules en majúscules i minúscules s'han de tractar com la mateixa paraula.

### 2.1 Script del Mapper (`mapper.py`)

```python
#!/usr/bin/env python3
import sys
import string

for line in sys.stdin:
    # Convertim la línia a minúscules
    line = line.lower()
    # Eliminem els signes de puntuació
    line = line.translate(str.maketrans('', '', string.punctuation))
    # Separem les paraules
    words = line.strip().split()
    # Emetem parells (paraula, 1)
    for word in words:
        if word:
            print(f"{word}\t1")
```

> **Descripció:** El *Mapper* rep el text per l'entrada estàndard (`stdin`), el converteix a minúscules, elimina la puntuació mitjançant `translate()` i `string.punctuation`, separa les paraules i n'emet cadascuna amb un valor inicial de 1.

---

### 2.2 Script del Reducer (`reducer.py`)

```python
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        word, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        continue

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

if current_word == word and current_word is not None:
    print(f"{current_word}\t{current_count}")
```

> **Descripció:** El *Reducer* rep les parelles clau-valor ordenades per la clau (paraula), acumula la quantitat d'aparicions de cada paraula i en mostra el total.

---

### 2.3 Prova de funcionament en local

Concedim permisos d'execució als dos scripts i fem una prova mitjançant canonades (`pipes`):

```bash
chmod +x mapper.py reducer.py
echo "Hola, Hola!" | ./mapper.py | sort | ./reducer.py
```

**Sortida obtinguda:**
```text
hola	2
```
> **Conclusió:** Es confirma que la conversió a minúscules, l'eliminació de puntuació i l'acumulació de freqüències funcionen correctament.

---

### 2.4 Execució del Job a Hadoop Streaming

Llançament del procés MapReduce distribuït sobre el clúster d'Hadoop:

```bash
mapred streaming \
  -files mapper.py,reducer.py \
  -input /user/hadoop/textos/tirantloblanc.txt \
  -output /user/hadoop/sortidaPy \
  -mapper mapper.py \
  -reducer reducer.py
```

**Sortida del terminal:**
```text
2026-10-13 17:09:57,224 INFO mapreduce.Job: Job job_1791909911314_0004 completed successfully
2026-10-13 17:09:57,286 INFO mapreduce.Job: Counters: 54
2026-10-13 17:09:57,292 INFO streaming.StreamJob: Output directory: /user/hadoop/sortidaPy
```

---

### 2.5 Verificació dels resultats a HDFS

#### Llistat del directori de sortida:
```bash
hdfs dfs -ls /user/hadoop/sortidaPy
```
```text
Found 2 items
-rw-r--r--   1 hadoop supergroup          0 2026-10-13 17:09 /user/hadoop/sortidaPy/_SUCCESS
-rw-r--r--   1 hadoop supergroup      89269 2026-10-13 17:09 /user/hadoop/sortidaPy/part-00000
```

#### Visualització de les primeres línies del fitxer resultat:
```bash
hdfs dfs -cat /user/hadoop/sortidaPy/part-00000 | head -n 25
```
```text
07042	1
1	14
10	2
100	1
1000	1
11	1
12	8
125	1
13	1
130	1
14	4
14th	1
15	4
1500	2
16	3
17228	1
18	4
1812	1
1856	2
1860	4
1861	1
1864	7
1865	7
1866	36
1867	1
```

---

## 3. Monitorització i Administració amb Hadoop UI, YARN i JobHistoryServer

### Exploració d'HDFS des de la interfície Web (Hadoop UI - Port 9870)
A través del navegador web hem accedit a l'eina **Browse Directory**:
* **Directori principal:** Es comprova la presència de les carpetes `/user/hadoop/textos` i `/user/hadoop/sortida_wordcount`.
* **Detalls del bloc (`part-00000`):**
  * **Block ID:** `1073741988`
  * **Block Pool ID:** `BP-1710563444-127.0.1.1-1790847296867`
  * **Mida del fitxer:** `236680 bytes` (231.15 KB)
  * **Node d'emmagatzematge:** `hadoop-server`
* **Previsualització del fitxer (*Head the file*):** S'observa la correcta estructuració de les paraules ordenades alfabèticament (`capfica 1`, `capficada 1`, `capficat 4`, etc.).

### Visualització de treballs a YARN Resource Manager (Port 8088)
A la interfície de YARN es mostren tots els treballs (*Jobs*) executats correctament:
* **`QuasiMonteCarlo`:** Execució corresponent a l'estimació del número $\pi$.
* **`streamjob...jar`:** Diverses execucions de tasques MapReduce mitjançant Hadoop Streaming i Python.

Per a cada aplicació es registren les mètriques següents: `Application ID`, `User`, `Name`, `Application Type (MAPREDUCE)`, `Queue`, `StartTime`, `LaunchTime` i l'estat final (`FINISHED/SUCCEEDED`).