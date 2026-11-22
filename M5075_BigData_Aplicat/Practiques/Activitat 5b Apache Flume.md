# APUNTS EXTENSOS — PRÀCTICA 5b: APACHE FLUME

## 1. Què vol demostrar aquesta pràctica? [PRÀCTICA]

Després de treballar amb **Sqoop** per fer ingesta batch des de bases de dades relacionals, aquesta activitat aborda Apache Flume com a eina de **recollida i transport d'esdeveniments** cap a HDFS. El document implementa una progressió des d'un sol agent fins a la consolidació de diversos orígens.

| Apartat | Origen | Canals | Destinació | Comprovació |
|---|---|---|---|---|
| Cas 1a | SeqGen | MemChannel | HDFS | Números seqüencials a `seqgen_data` |
| Cas 1b | Netcat al port 44444 | FileChannel | HDFS | Frase amb nom complet a `net_data` |
| Cas 2 | Netcat → Avro | FileChannel + MemChannel | HDFS via segon agent | Frase nova a `avro_data` |
| Cas 3 | Faker/Spooldir + Netcat + Exec | 3 canals | AvroSink | Tres orígens enviats a un consolidador |
| Cas 4 | AvroSource al port 10003 | MemChannel | HDFS | Registres consolidats a `usuaris` |

Les comprovacions del PDF estan construïdes amb captures de terminals, fitxers `.conf`, dades d'origen i llistats de HDFS.

## 2. Arquitectura bàsica de Flume [PRÀCTICA + AMPLIACIÓ]

Flume és un servei per **capturar, agrupar i transportar esdeveniments**. Una configuració habitual combina una font, un canal i una destinació:

```text
Origen extern → [ SOURCE ] → [ CHANNEL ] → [ SINK ] → HDFS
                       └──────── AGENT ────────┘
```

- **Source:** converteix el que arriba de l'origen en esdeveniments de Flume.
- **Channel:** fa de cua intermèdia i evita que source i sink hagin de treballar a la mateixa velocitat.
- **Sink:** consumeix esdeveniments del channel i els entrega al destí.
- **Agent:** procés que defineix el conjunt de components i la seva configuració.

**Event:** unitat lògica transportada per Flume. Habitualment incorpora un `body` (contingut de l'esdeveniment) i uns `headers` (metadades). Les fonts i destinacions poden afegir o utilitzar capçaleres, però el text de cada registre és el contingut principal en aquesta pràctica.

## 3. Fonts, canals i sinks utilitzats [PRÀCTICA]

| Tipus | Què fa? | Ús a l'activitat |
|---|---|---|
| SeqGen Source | Genera esdeveniments seqüencials | Cas 1a |
| Netcat Source | Rep línies a través d'un socket TCP | Casos 1b, 2, 3 |
| Spooldir Source | Processa fitxers que apareixen a una carpeta | Cas 3, fitxers Faker |
| Exec Source | Llegeix la sortida d'una ordre externa | Cas 3, `usuaris.txt` |
| Avro Source | Rep esdeveniments d'altres agents | Casos 2 i 4 |
| Memory Channel | Cua en memòria | Cas 1a, receptor Cas 2 i consolidador |
| File Channel | Cua persistent en disc | Cas 1b i emissor Cas 2; una de les fonts Cas 3 |
| HDFS Sink | Escriu esdeveniments a HDFS | Casos 1a, 1b, 2 i 4 |
| Avro Sink | Envia esdeveniments a una Avro Source | Casos 2 i 3 |

**Distinció important:** una **Avro Source/Sink de Flume** és un mecanisme per comunicar agents; no és el mateix que desar fitxers en format Avro dins d'HDFS.

## 4. Comprovacions inicials [PRÀCTICA]

La pràctica comença verificant l'entorn amb:

```bash
jps
```

A la captura es veuen processos relacionats amb Hadoop, com **NameNode, DataNode, SecondaryNameNode, ResourceManager i NodeManager**. La finalitat és constatar que l'entorn del laboratori està preparat.

**[AMPLIACIÓ]** És pràctic complementar-ho amb:

```bash
hdfs dfs -ls /
hdfs dfs -ls /user/iabd
```

Si HDFS no respon, cal revisar abans la seva arrencada, el host configurat i la connectivitat. Flume no pot persistir a HDFS si el servei de destí és inabastable.

---

# BLOC I — AGENTS BÀSICS

## 5. Cas 1a: SeqGen → Memory → HDFS [PRÀCTICA]

**Objectiu:** generar nombres seqüencials de forma automàtica i enregistrar-los a HDFS.

```text
SeqGen Source → MemChannel → HdfsSink
                                  ↓
                  /user/iabd/flume/seqgen_data/
```

Primer es crea el directori de destinació:

```bash
hdfs dfs -mkdir -p /user/iabd/flume/seqgen_data
hdfs dfs -ls /user/iabd/flume/
```

`-mkdir -p` crea la ruta si no existeix i permet crear directoris intermedis. El resultat de `-ls` és una evidència de la presència de la ruta.

## 6. Cas 1a: configuració SeqGen [PRÀCTICA + AMPLIACIÓ]

El document configura un agent anomenat **`SeqGenAgent`**, amb els tres components citats. La captura mostra el fitxer de configuració; el següent exemple és una **reconstrucció didàctica** de la mateixa arquitectura. Les propietats de rotació i noms de fitxer poden variar respecte al fitxer utilitzat al laboratori:

```properties
# Exemple d'estudi; adaptar-lo a la instal·lació real
SeqGenAgent.sources = source1
SeqGenAgent.channels = channel1
SeqGenAgent.sinks = sink1

SeqGenAgent.sources.source1.type = seq
SeqGenAgent.sources.source1.channels = channel1

SeqGenAgent.channels.channel1.type = memory
SeqGenAgent.channels.channel1.capacity = 10000
SeqGenAgent.channels.channel1.transactionCapacity = 1000

SeqGenAgent.sinks.sink1.type = hdfs
SeqGenAgent.sinks.sink1.channel = channel1
SeqGenAgent.sinks.sink1.hdfs.path = hdfs://localhost:9000/user/iabd/flume/seqgen_data
SeqGenAgent.sinks.sink1.hdfs.fileType = DataStream
SeqGenAgent.sinks.sink1.hdfs.writeFormat = Text
```

**Atenció:** el valor `localhost:9000` és només orientatiu. Si l'HDFS del laboratori es resol amb un altre hostname o amb `fs.defaultFS`, s'ha d'utilitzar la configuració correcta de la màquina. Per al cas concret de `seq`, es recomana contrastar el tipus amb la versió de Flume instal·lada.

El canal en memòria és ràpid, però si l'agent falla abans de completar la transferència, els esdeveniments pendents a la cua RAM es poden perdre.

## 7. Cas 1a: iniciar l'agent i verificar-lo [PRÀCTICA]

La pràctica executa:

```bash
flume-ng agent \
  --conf /opt/flume/conf/ \
  --conf-file /opt/flume/conf/seqgen.conf \
  --name SeqGenAgent \
  -Dflume.root.logger=INFO,console
```

| Argument | Funció |
|---|---|
| `agent` | Executa un agent de Flume |
| `--conf` | Carpeta de configuració |
| `--conf-file` | Fitxer `.conf` a llegir |
| `--name` | Nom de l'agent definit dins del fitxer |
| `-Dflume.root.logger=INFO,console` | Missatges informatius al terminal |

Es comprova que han aparegut fitxers:

```bash
hdfs dfs -ls /user/iabd/flume/seqgen_data/ | head -15
```

Per llegir-ne el contingut:

```bash
hdfs dfs -cat /user/iabd/flume/seqgen_data/flumeData.* 2>/dev/null | head -20
```

**Resultat observat:** les captures mostren nombres **del 0 al 19**, la qual cosa confirma que l'agent està produint i enviant dades a HDFS. `2>/dev/null` oculta errors del procés i cal evitar-lo durant diagnosi d'errors reals; `head -20` limita la visualització a les primeres 20 línies.

**[AMPLIACIÓ]** SeqGen pot generar dades contínuament; cal aturar-lo després de la comprovació per evitar la creació indefinida de fitxers.

## 8. Cas 1b: Netcat → FileChannel → HDFS [PRÀCTICA]

El primer cas rebia dades internes; ara les dades s'introdueixen **des d'un client de xarxa**:

```text
Terminal / Client TCP → port 44444 → NetcatSource → FileChannel → HdfsSink
                                                              ↓
                                           /user/iabd/flume/net_data/
```

L'agent es diu **`NetcatAgent`** i el fitxer és **`netcat.conf`**.

El port 44444 és el punt d'entrada de missatges i **no** és el port de la interfície web Hadoop ni el port de comunicació Avro entre agents.

## 9. Cas 1b: preparar carpetes i FileChannel [PRÀCTICA]

```bash
hdfs dfs -mkdir -p /user/iabd/flume/net_data
mkdir -p /home/iabd/flume/data
mkdir -p /home/iabd/flume/checkpoint

hdfs dfs -ls /user/iabd/flume/
ls -ld /home/iabd/flume/data /home/iabd/flume/checkpoint
```

A FileChannel li calen directoris locals per mantenir informació del canal i permetre la seva recuperació:

- **`data`**: fitxers que contenen informació persistent de la cua.
- **`checkpoint`**: punts de control necessaris per reconstruir-ne l'estat.

**[AMPLIACIÓ]** Convindria que aquests directoris tinguessin permisos adequats per a l'usuari que executa Flume i estiguessin en un sistema de fitxers amb espai disponible. No han de compartir-se de manera arbitrària entre instàncies diferents de FileChannel.

## 10. Cas 1b: configuració i prova de missatge [PRÀCTICA]

**Configuració descrita al document:**

```text
Source:   Netcat / port 44444
Channel:  FileChannel (disc)
Sink:     HdfsSink
Destí:    /user/iabd/flume/net_data/
```

**[AMPLIACIÓ] Exemple de la part estructural** — noms orientatius, no còpia literal de la captura:

```properties
NetcatAgent.sources = netcat
NetcatAgent.channels = filechannel
NetcatAgent.sinks = hdfs

NetcatAgent.sources.netcat.type = netcat
NetcatAgent.sources.netcat.bind = 0.0.0.0
NetcatAgent.sources.netcat.port = 44444
NetcatAgent.sources.netcat.channels = filechannel

NetcatAgent.channels.filechannel.type = file
NetcatAgent.channels.filechannel.checkpointDir = /home/iabd/flume/checkpoint
NetcatAgent.channels.filechannel.dataDirs = /home/iabd/flume/data

NetcatAgent.sinks.hdfs.type = hdfs
NetcatAgent.sinks.hdfs.channel = filechannel
NetcatAgent.sinks.hdfs.hdfs.path = /user/iabd/flume/net_data/
NetcatAgent.sinks.hdfs.hdfs.fileType = DataStream
```

Arrencada:

```bash
flume-ng agent \
  --conf /opt/flume/conf/ \
  --conf-file /opt/flume/conf/netcat.conf \
  --name NetcatAgent \
  -Dflume.root.logger=INFO,console
```

En un altre terminal, es fa servir:

```bash
curl telnet://localhost:44444
```

L'usuari escriu una frase amb el nom complet i **Netcat contesta `OK`**. El document verifica també:

```bash
hdfs dfs -ls /user/iabd/flume/net_data/
hdfs dfs -cat /user/iabd/flume/net_data/flumeData.*
```

**Què demostra `OK`?** Que la font Netcat ha acceptat el missatge. Per acreditar la ingesta completa fins a HDFS cal fer la segona comprovació, que el document també aporta.

---

# BLOC II — FLUXOS ENCADENATS (MULTI-HOP)

## 11. Cas 2: per què encadenar agents? [PRÀCTICA + AMPLIACIÓ]

En comptes d'escriure directament des d'un únic agent a HDFS, s'utilitzen **dos agents**. El primer rep el missatge i l'envia al segon amb el protocol Avro utilitzat per Flume.

```text
                    AGENT A                                     AGENT B
Client TCP → Netcat Source → FileChannel → AvroSink ── TCP 10003 ──> AvroSource → MemChannel → HdfsSink
                                                                                           ↓
                                                                        /user/iabd/flume/avro_data/
```

**Aplicació:** separar un agent proper a les fonts d'un altre que concentra l'escriptura al sistema de destí. Permet desacoblar ubicacions i responsabilitats, i pot facilitar ampliacions amb més orígens.

## 12. Agent emissor: `NetcatAvroAgent` [PRÀCTICA]

La guia descriu el fitxer **`netcat-avro.conf`**:

- Netcat Source escolta a **44444**.
- FileChannel desa els esdeveniments temporalment en disc.
- AvroSink envia al port **10003** de l'agent receptor.

**[AMPLIACIÓ] Exemple d'esquelet:**

```properties
NetcatAvroAgent.sources = netcat
NetcatAvroAgent.channels = filech
NetcatAvroAgent.sinks = avro

NetcatAvroAgent.sources.netcat.type = netcat
NetcatAvroAgent.sources.netcat.bind = 0.0.0.0
NetcatAvroAgent.sources.netcat.port = 44444
NetcatAvroAgent.sources.netcat.channels = filech

NetcatAvroAgent.channels.filech.type = file
NetcatAvroAgent.channels.filech.checkpointDir = /home/iabd/flume/checkpoint-avro
NetcatAvroAgent.channels.filech.dataDirs = /home/iabd/flume/data-avro

NetcatAvroAgent.sinks.avro.type = avro
NetcatAvroAgent.sinks.avro.hostname = localhost
NetcatAvroAgent.sinks.avro.port = 10003
NetcatAvroAgent.sinks.avro.channel = filech
```

Els directoris `checkpoint-avro` i `data-avro` de l'exemple són una **proposta addicional** per evitar compartir estat del canal d'un altre agent. Cal crear-los abans de l'execució.

## 13. Agent receptor: `AvroHdfsAgent` [PRÀCTICA]

El document crea el destí:

```bash
hdfs dfs -mkdir -p /user/iabd/flume/avro_data
```

L'agent receptor està definit al fitxer **`avro-hdfs.conf`** i incorpora:

```text
AvroSource escoltant al port 10003
       ↓
MemChannel
       ↓
HdfsSink → /user/iabd/flume/avro_data/
```

**[AMPLIACIÓ] Exemple d'esquelet coherent amb el cas:**

```properties
AvroHdfsAgent.sources = avroin
AvroHdfsAgent.channels = mem
AvroHdfsAgent.sinks = hdfs

AvroHdfsAgent.sources.avroin.type = avro
AvroHdfsAgent.sources.avroin.bind = 0.0.0.0
AvroHdfsAgent.sources.avroin.port = 10003
AvroHdfsAgent.sources.avroin.channels = mem

AvroHdfsAgent.channels.mem.type = memory
AvroHdfsAgent.channels.mem.capacity = 10000
AvroHdfsAgent.channels.mem.transactionCapacity = 1000

AvroHdfsAgent.sinks.hdfs.type = hdfs
AvroHdfsAgent.sinks.hdfs.channel = mem
AvroHdfsAgent.sinks.hdfs.hdfs.path = /user/iabd/flume/avro_data/
AvroHdfsAgent.sinks.hdfs.hdfs.fileType = DataStream
```

## 14. Cas 2: ordre d'arrencada i comprovació [PRÀCTICA]

**Primer** el receptor, perquè estigui escoltant quan el primer agent intenti enviar:

```bash
flume-ng agent \
  --conf /opt/flume/conf/ \
  --conf-file /opt/flume/conf/avro-hdfs.conf \
  --name AvroHdfsAgent \
  -Dflume.root.logger=INFO,console
```

**Després** l'emissor, en un altre terminal:

```bash
flume-ng agent \
  --conf /opt/flume/conf/ \
  --conf-file /opt/flume/conf/netcat-avro.conf \
  --name NetcatAvroAgent \
  -Dflume.root.logger=INFO,console
```

**Finalment** s'envia una frase nova amb:

```bash
curl telnet://localhost:44444
```

Comprovacions:

```bash
hdfs dfs -ls /user/iabd/flume/avro_data/
hdfs dfs -cat /user/iabd/flume/avro_data/flumeData.*
```

Al PDF s'observa la frase amb el nom complet al fitxer HDFS. És una verificació **extrem a extrem**: l'entrada Netcat ha travessat els dos agents fins al sink HDFS.

---

# BLOC III — TRES FONTS D'INGESTA I CONSOLIDACIÓ

## 15. Cas 3: objectiu de la ingesta multi-agent [PRÀCTICA]

L'enunciat exigeix consolidar **tres tipus de font** per construir registres d'usuaris amb els camps:

```text
email; password; nom; professió
```

Les fonts concretes són:

1. **Faker + Spooldir:** fitxers CSV sintètics generats periòdicament.
2. **Netcat:** un usuari escrit manualment per TCP.
3. **Exec:** usuaris existents en un fitxer de text local.

Totes tres rutes es concentren posteriorment en **l'agent Avro receptor**, que les escriu a:

```text
/user/iabd/flume/usuaris/
```

**Molt important:** el resultat final es genera a HDFS, no a MariaDB. I les dades d'exemple són fictícies, no un sistema real de gestió de credencials.

## 16. Dades sintètiques amb Python i Faker [PRÀCTICA]

La pràctica crea la carpeta d'origen:

```bash
mkdir -p /home/iabd/flume/spool
hdfs dfs -mkdir -p /user/iabd/flume/usuaris
```

L'script `flume-faker.py` és el següent segons el document, presentat amb format normalitzat:

```python
from faker import Faker
import csv
import time

fake = Faker('es_ES')
num = 1

while True:
    output = open(f'spool/dadesFaker-{num}.csv', 'w')
    mywriter = csv.writer(output, delimiter=';')
    for r in range(100):
        mywriter.writerow([
            fake.free_email(),
            fake.password(),
            fake.name(),
            fake.job()
        ])
    output.close()
    num = num + 1
    time.sleep(20)
```

**Lectura detallada del codi:**

- `Faker('es_ES')` crea dades sintètiques amb convencions del locale indicat.
- `num` identifica seqüencialment els fitxers.
- `while True` repeteix indefinidament la generació.
- `csv.writer(..., delimiter=';')` escriu camps separats per punt i coma.
- `range(100)` crea **100 registres per fitxer**.
- `free_email`, `password`, `name` i `job` generen les quatre columnes.
- `time.sleep(20)` espera **20 segons** entre lots.

El nom `.csv` no implica que el separador sigui coma; en aquest exemple és `;`.

### Instal·lació de dependències [AMPLIACIÓ]

```bash
python3 --version
python3 -m pip show Faker
```

Si no s'ha instal·lat, es pot utilitzar un entorn virtual i després:

```bash
python3 -m venv ~/flume-env
source ~/flume-env/bin/activate
pip install Faker
```

El document indica explícitament que cal disposar de Python 3 i Faker, però no imposa aquesta forma concreta d'instal·lació.

## 17. Comprovacions de Faker [PRÀCTICA]

```bash
cd /home/iabd/flume
mkdir -p spool
python3 flume-faker.py
```

En un altre terminal:

```bash
ls -lh /home/iabd/flume/spool/
head -5 /home/iabd/flume/spool/dadesFaker-1.csv
```

Les captures mostren diversos fitxers `dadesFaker-N.csv` i registres amb els quatre camps separats per `;`. Els camps tenen significat diferent: `email` és un identificador de correu, `password` és una cadena generada per Faker, `nom` és una persona fictícia, i `professió` és la feina fictícia.

**[AMPLIACIÓ] Atenció a la generació de fitxers:** per a sistemes de producció, és recomanable crear el fitxer en una carpeta temporal i moure'l al directori `spool` **quan estigui complet**, perquè Spooldir no llegeixi un fitxer que encara s'està escrivint. La pràctica fa servir una versió simplificada per a l'exercici.

## 18. Spooldir, Netcat i Exec: què aporta cada font? [PRÀCTICA + AMPLIACIÓ]

### Spooldir

Vigila fitxers que apareixen dins d'una carpeta. La pràctica exigeix:

```properties
# Propietat de Spooldir indicada en el document
deletePolicy = immediate
```

En una configuració Flume real, aquesta propietat s'ha d'escriure amb el **prefix complet de la source**, per exemple:

```properties
MultiAgent.sources.spool.deletePolicy = immediate
```

La finalitat és que els fitxers llegits i processats **s'eliminin** en lloc de quedar renombrats. És un comportament destructiu respecte dels fitxers d'entrada, i per tant cal fer-ho sobre un directori de dades de prova o amb una estratègia d'arxiu adequada.

### Netcat

Permet inserir **un registre** teclejant-lo al port 44444:

```text
usuari@example.org;clau_ficticia;Nom Cognom;Professió
```

La resposta `OK` indica acceptació de la font, i el document comprova després la presència del registre a HDFS.

### Exec

Llegeix dades des de la sortida d'una ordre del sistema operatiu. A la pràctica s'utilitza un fitxer local de tres usuaris ficticis, a la ruta:

```text
/home/iabd/flume/dades/usuaris.txt
```

Preparació:

```bash
mkdir -p /home/iabd/flume/dades
nano /home/iabd/flume/dades/usuaris.txt
cat /home/iabd/flume/dades/usuaris.txt
```

**[AMPLIACIÓ]** Per llegir les files existents d'aquest fitxer, una font Exec podria executar `cat /home/iabd/flume/dades/usuaris.txt`. Si es necessités llegir línies noves, caldria un comportament diferent com `tail -F`, assumint-ne els riscos. La font Exec no té la mateixa garantia de lliurament que una font transaccional i s'ha de fer servir tenint en compte possibles pèrdues davant d'errors.

## 19. `MultiAgent`: emissor de tres fluxos cap a Avro [PRÀCTICA]

El document configura **`multiagent-avro.conf`** amb:

- **Tres sources**: `Netcat`, `Spooldir`, `Exec`.
- **Tres channels**: `FileChannel`, `MemChannel1`, `MemChannel2`.
- **Tres sinks Avro** enviant al port **10003**.
- Connexió de cada source amb el seu channel i sink.

Representació de la mateixa estructura:

```text
        ┌── Netcat (TCP 44444) ──→ FileChannel ───→ AvroSink ──┐
        │                                                      │
        ├── Spooldir (CSV Faker) → MemChannel1 → AvroSink ─────┼──→ port 10003
        │                                                      │
        └── Exec (usuaris.txt) ───→ MemChannel2 → AvroSink ────┘
                                      MultiAgent
```

**[AMPLIACIÓ]** L'associació concreta entre cadascuna de les tres sources i els tres canals ha de coincidir amb el fitxer real; el diagrama anterior agrupa components segons la descripció, però no substitueix la captura del `.conf` quan es vol reproduir-lo exactament.

### Esquelet didàctic del fitxer `multiagent-avro.conf`

```properties
MultiAgent.sources = netcat spool exec
MultiAgent.channels = file1 mem1 mem2
MultiAgent.sinks = avro1 avro2 avro3

# Sources
MultiAgent.sources.netcat.type = netcat
MultiAgent.sources.netcat.bind = 0.0.0.0
MultiAgent.sources.netcat.port = 44444
MultiAgent.sources.netcat.channels = file1

MultiAgent.sources.spool.type = spooldir
MultiAgent.sources.spool.spoolDir = /home/iabd/flume/spool
MultiAgent.sources.spool.deletePolicy = immediate
MultiAgent.sources.spool.channels = mem1

MultiAgent.sources.exec.type = exec
MultiAgent.sources.exec.command = cat /home/iabd/flume/dades/usuaris.txt
MultiAgent.sources.exec.channels = mem2

# Canals
MultiAgent.channels.file1.type = file
MultiAgent.channels.file1.checkpointDir = /home/iabd/flume/ck-multi
MultiAgent.channels.file1.dataDirs = /home/iabd/flume/data-multi
MultiAgent.channels.mem1.type = memory
MultiAgent.channels.mem2.type = memory

# Sinks Avro (mateix receptor)
MultiAgent.sinks.avro1.type = avro
MultiAgent.sinks.avro1.hostname = localhost
MultiAgent.sinks.avro1.port = 10003
MultiAgent.sinks.avro1.channel = file1

MultiAgent.sinks.avro2.type = avro
MultiAgent.sinks.avro2.hostname = localhost
MultiAgent.sinks.avro2.port = 10003
MultiAgent.sinks.avro2.channel = mem1

MultiAgent.sinks.avro3.type = avro
MultiAgent.sinks.avro3.hostname = localhost
MultiAgent.sinks.avro3.port = 10003
MultiAgent.sinks.avro3.channel = mem2
```

Aquest és **un exemple d'estudi reconstruït**, no una transcripció literal del document. Abans d'executar-lo cal crear les carpetes de FileChannel, comprovar els paràmetres amb la versió de Flume instal·lada i garantir que cap altre agent ocupi els mateixos ports.

## 20. Cas 4: agent consolidador [PRÀCTICA]

Per completar l'activitat es modifica **`avro-hdfs.conf`** perquè **`AvroHdfsAgent`** guardi dades a:

```text
/user/iabd/flume/usuaris/
```

La seva arquitectura és:

```text
Sources Netcat + Spooldir + Exec
             ↓
      MultiAgent (3 AvroSinks)
             ↓ port 10003
      AvroHdfsAgent (AvroSource)
             ↓
         MemChannel
             ↓
          HdfsSink
             ↓
  /user/iabd/flume/usuaris/
```

L'agent receptor s'ha d'iniciar abans de l'emissor perquè el port 10003 estigui disponible.

Ordres documentades:

```bash
flume-ng agent \
  --conf /opt/flume/conf/ \
  --conf-file /opt/flume/conf/avro-hdfs.conf \
  --name AvroHdfsAgent \
  -Dflume.root.logger=INFO,console
```

En un segon terminal:

```bash
flume-ng agent \
  --conf /opt/flume/conf/ \
  --conf-file /opt/flume/conf/multiagent-avro.conf \
  --name MultiAgent \
  -Dflume.root.logger=INFO,console
```

I el generador Faker s'executa des d'un terminal addicional mentre s'estudia la ingesta dinàmica.

## 21. Verificació dels tres fluxos [PRÀCTICA]

### 21.1. Verificació de Spooldir

```bash
ls -lh /home/iabd/flume/spool/
```

La carpeta apareix **buida** en la captura després del processament, fet coherent amb `deletePolicy = immediate`. Després, es comprova que a HDFS han aparegut fitxers nous:

```bash
hdfs dfs -ls /user/iabd/flume/usuaris/
hdfs dfs -ls -t /user/iabd/flume/usuaris/ | head -12
```

L'opció `-t` ordena per temps de modificació i `head -12` limita la sortida. Els fitxers nous i el contingut de registres ficticis són la prova de la ingesta de Faker.

### 21.2. Verificació de Netcat

```bash
curl telnet://localhost:44444
```

S'envia un registre manual separat per punt i coma; la font contesta `OK`. Després s'utilitzen comandes de lectura de fitxers HDFS amb `grep` per trobar l'usuari concret.

**[AMPLIACIÓ] Patró possible per cercar un camp de prova** (ajusta la ruta/patró als fitxers reals):

```bash
hdfs dfs -cat '/user/iabd/flume/usuaris/*' 2>/dev/null | grep 'usuari@example.org'
```

### 21.3. Verificació d'Exec

La pràctica busca un dels noms del fitxer `usuaris.txt`, per exemple **`Anna Garcia`**:

```bash
hdfs dfs -cat '/user/iabd/flume/usuaris/*' 2>/dev/null | grep 'Anna Garcia'
```

La captura mostra que el nom s'ha recuperat del directori HDFS, acreditant la font Exec.

### 21.4. Lectura de dades a HDFS

```bash
hdfs dfs -ls /user/iabd/flume/usuaris/
hdfs dfs -cat '/user/iabd/flume/usuaris/*' 2>/dev/null | head -20
```

És possible que es mostrin diversos fitxers, perquè el sink pot fer rotació de sortides segons la configuració. L'ordre de línies **no és necessàriament el mateix que l'ordre cronològic d'entrada de totes les fonts**.

## 22. Comandes bàsiques de tota l'activitat

| Comanda | Què comprova o executa |
|---|---|
| `jps` | Processos Java visibles al sistema |
| `hdfs dfs -mkdir -p RUTA` | Crea una carpeta HDFS |
| `hdfs dfs -ls RUTA` | Llista fitxers HDFS |
| `hdfs dfs -cat RUTA` | Mostra el contingut d'un fitxer de text HDFS |
| `hdfs dfs -ls -t RUTA` | Llista fitxers ordenats per modificació |
| `mkdir -p RUTA` | Crea directoris locals |
| `ls -ld RUTA` | Mostra informació sobre un directori local |
| `ls -lh RUTA` | Llista fitxers locals amb mides llegibles |
| `head -5 FITXER` | Mostra les primeres cinc línies |
| `cat FITXER` | Mostra contingut de text local |
| `python3 flume-faker.py` | Genera lots sintètics |
| `flume-ng agent ...` | Inicia un agent |
| `curl telnet://localhost:44444` | Interacciona amb Netcat Source |
| `grep 'TEXT'` | Cerca un patró dins del flux de sortida |

## 23. Ports i directoris: taula de memorització

| Recurs | Ús |
|---|---|
| TCP `44444` | Source Netcat |
| TCP `10003` | Connexió entre agents mitjançant Avro |
| `/opt/flume/conf/` | Fitxers de configuració de Flume |
| `/user/iabd/flume/seqgen_data/` | Fitxers del Cas 1a |
| `/user/iabd/flume/net_data/` | Fitxers del Cas 1b |
| `/user/iabd/flume/avro_data/` | Fitxers del Cas 2 |
| `/user/iabd/flume/usuaris/` | Fitxers dels Casos 3–4 |
| `/home/iabd/flume/spool/` | Fitxers CSV de Faker |
| `/home/iabd/flume/dades/usuaris.txt` | Registres de la font Exec |
| `/home/iabd/flume/data/` | Directoris del FileChannel del Cas 1b |
| `/home/iabd/flume/checkpoint/` | Checkpoints del FileChannel del Cas 1b |

## 24. Canals, recuperació i garanties [AMPLIACIÓ]

### MemoryChannel

Una cua resident en memòria; útil per simplificar proves i quan es prioritza baixa latència, però no ofereix la persistència del canal en disc.

### FileChannel

Una cua persistent basada en fitxers i checkpoints. És més adequada quan és important conservar esdeveniments pendents davant d'una fallada del procés, tot i que pot tenir un cost d'E/S de disc més alt.

### Què significa l'èxit d'una transacció?

Flume utilitza canals amb transaccions entre la font i el canal, i entre el canal i el sink. Això permet reintents i desacoblament. Tanmateix, **no equival a garantir exactament un únic registre a HDFS davant de qualsevol fallada de tota una cadena distribuïda**. La configuració, les fonts i els sinks determinen la fiabilitat pràctica.

### Per què `OK` de Netcat no és una prova final?

Perquè `OK` acredita la recepció de la source. El fitxer HDFS pot aparèixer després d'un retard de processament o rotació del sink. El test complet és **entrada → recepció → fitxer de sortida → contingut**.

## 25. Errors habituals i solucions [AMPLIACIÓ]

| Problema | Possibles causes | Comprovació o acció |
|---|---|---|
| Flume no arrenca | Nom d'agent erroni, sintaxi `.conf`, biblioteques | Revisar el log des del primer error |
| Port 44444 ocupat | Ja hi ha un NetcatAgent actiu | Comprovar el procés/port abans d'arrencar un segon agent |
| Port 10003 no disponible | AvroHdfsAgent no està arrencat o configuració de host errònia | Iniciar receptor primer i comprovar escolta |
| Hi ha `OK` però no hi ha fitxer | Sink pendent, rotació o error HDFS | Comprovar logs del sink i HDFS |
| FileChannel falla | Directoris inexistents, permisos o espai | Revisar `checkpointDir`, `dataDirs`, permisos i disc |
| Spooldir no elimina CSV | `deletePolicy` no configurat o errors de processament | Revisar atribut complet i logs |
| Les dades de Faker no arriben | Script no en execució, carpeta incorrecta, fitxer incomplet | `ls -lh`, paths i logs de source |
| Exec no envia registres | Ordre incorrecta, fitxer buit, permisos | Executar l'ordre manualment |
| SLF4J informa de duplicats | Diverses implementacions al classpath | No confondre un avís amb una fallada efectiva |
| `grep` no troba el nom | Encara no s'ha escrit o patró equivocat | Comprovar fitxers nous i contingut |

**SLF4J:** les captures de la pràctica mostren avisos sobre biblioteques de logging duplicades, però en aquestes execucions els agents continuen i processen dades. L'impacte real sempre s'ha de valorar mirant si hi ha errors fatals o pèrdua de funcionalitat.

## 26. Seguretat i qualitat de dades [AMPLIACIÓ]

1. **Contrassenyes de prova:** l'enunciat genera un camp anomenat `password` i l'emmagatzema en text dins de fitxers d'aprenentatge. Això és **només acceptable com a simulació amb dades fictícies**. En sistemes reals no s'han de recopilar i guardar contrasenyes en clar en pipelines d'ingesta.
2. **Netcat sense autenticació:** exposar un port que accepta registres de xarxa pot permetre entrades inesperades. Restringeix-ne l'abast a l'entorn de laboratori.
3. **Spooldir amb eliminació immediata:** conserva una còpia si necessites traçabilitat o capacitat de reprocessar els fitxers.
4. **Format consistent:** la cadena `email;password;nom;professió` requereix que tots els registres tinguin camps i separadors coherents; els salts de línia i caràcters especials poden complicar-ne el consum posterior.
5. **Traçabilitat d'origen:** la consolidació a un únic directori facilita l'accés, però si s'ha de saber quin agent ha produït cada esdeveniment convé afegir metadades d'origen o particions a les sortides.

## 27. Reconstrucció ordenada de la pràctica [AMPLIACIÓ]

### Part A — SeqGen

1. Verifica Hadoop amb `jps`.
2. Crea la ruta HDFS `seqgen_data`.
3. Prepara el `.conf` amb SeqGen, MemoryChannel i HdfsSink.
4. Inicia `SeqGenAgent`.
5. Llista els fitxers HDFS i llegeix les primeres línies.
6. Atura l'agent després de comprovar els nombres.

### Part B — Netcat

1. Crea `net_data` a HDFS.
2. Crea `data` i `checkpoint` locals.
3. Prepara `netcat.conf`.
4. Inicia `NetcatAgent`.
5. Escriu un missatge en el port 44444.
6. Comprova `OK`, el fitxer HDFS i el contingut.

### Part C — Multi-hop

1. Crea `avro_data` a HDFS.
2. Prepara `netcat-avro.conf` i `avro-hdfs.conf`.
3. Inicia primer `AvroHdfsAgent`.
4. Inicia `NetcatAvroAgent`.
5. Envia un missatge nou al port 44444.
6. Comprova el contingut final d'`avro_data`.

### Part D — Multi-font i consolidador

1. Crea `spool`, `dades` i el directori `usuaris` a HDFS.
2. Instal·la o comprova Faker.
3. Crea i executa `flume-faker.py`.
4. Verifica els CSV generats.
5. Crea `usuaris.txt` amb dades fictícies.
6. Configura el `MultiAgent` amb tres sources/channels/sinks.
7. Afegeix `deletePolicy = immediate` al Spooldir amb prefix complet.
8. Configura el receptor per escriure a `/user/iabd/flume/usuaris/`.
9. Inicia primer `AvroHdfsAgent`, després `MultiAgent`.
10. Comprova dades de Faker, Exec i Netcat per separat.
11. Llista els fitxers més recents i revisa el contingut final.

## 28. Exercicis resolts [AMPLIACIÓ]

### Exercici 1. Dibuixa el Cas 1a

**Solució:** `SeqGen → MemoryChannel → HDFS Sink → seqgen_data`.

### Exercici 2. Quin component permet llegir per TCP al port 44444?

**Solució:** la Netcat Source.

### Exercici 3. Per què es creen carpetes `checkpoint` i `data`?

**Solució:** per mantenir l'estat persistent de FileChannel.

### Exercici 4. Quina diferència hi ha entre els ports 44444 i 10003?

**Solució:** 44444 és l'entrada TCP de missatges Netcat; 10003 és la comunicació Avro entre agents Flume.

### Exercici 5. Envia un usuari fictici i comprova'l

```bash
curl telnet://localhost:44444
# Escriu: prova@example.org;clau-falsa;Persona Prova;Analista

hdfs dfs -cat '/user/iabd/flume/usuaris/*' 2>/dev/null | grep 'prova@example.org'
```

**Interpretació:** ha d'aparèixer la fila al fitxer HDFS per donar per acreditada la ingesta completa.

### Exercici 6. Quin és el paper del `deletePolicy`?

**Solució:** amb valor `immediate`, l'agent elimina el fitxer Spooldir després de processar-lo, en lloc de conservar-lo renombrat.

### Exercici 7. Es generen 100 registres cada 20 segons. Quina mitjana teòrica d'entrada és?

**Solució:** **5 registres per segon** en termes de taxa mitjana de generació, si no hi ha pauses addicionals ni retards. No és una mesura de throughput real de Flume.

### Exercici 8. Quines comprovacions acrediten Exec?

**Solució:** primer visualitzar `usuaris.txt`, després verificar que un dels seus noms apareix en els fitxers de HDFS del consolidador.

### Exercici 9. Què implica un FileChannel persistent?

**Solució:** esdeveniments pendents poden recuperar-se després de determinades fallades; calen fitxers de dades i checkpoints locals.

### Exercici 10. Què diferencia Flume i Sqoop?

**Solució:** Sqoop s'orienta a transferències batch de dades estructurades entre RDBMS i Hadoop; Flume, a ingestes contínues d'esdeveniments des de diverses fonts.

## 29. Preguntes d'autoavaluació amb resposta [AMPLIACIÓ]

1. **Què és Flume?** Una eina distribuïda per recollir i transportar esdeveniments.
2. **Quins tres components formen un agent?** Source, Channel i Sink.
3. **Què és una source?** Entrada d'esdeveniments.
4. **Què és un channel?** Cua temporal d'esdeveniments.
5. **Què és un sink?** Component que envia al destí.
6. **Quina és la destinació general de la pràctica?** HDFS.
7. **Quina diferència bàsica hi ha respecte a Sqoop?** Flume transporta esdeveniments; Sqoop transfereix dades relacionals en batch.
8. **Quina source genera nombres automàticament?** SeqGen.
9. **Quin agent s'utilitza al Cas 1a?** `SeqGenAgent`.
10. **Quin channel s'hi utilitza?** MemChannel.
11. **Quins valors es comproven a l'HDFS del Cas 1a?** Nombres del 0 al 19 a la captura.
12. **Quina comanda mostra els processos Hadoop?** `jps`.
13. **Què fa `hdfs dfs -mkdir -p`?** Crea una ruta HDFS, incloent directoris intermedis.
14. **Què indica `--conf-file`?** El fitxer de configuració Flume.
15. **Què indica `--name`?** El nom de l'agent.
16. **Què fa el logger `INFO,console`?** Mostra registres informatius al terminal.
17. **Què és Netcat?** Source que accepta línies via TCP.
18. **Quin port utilitza Netcat a la pràctica?** 44444.
19. **Quina comanda s'utilitza per escriure-hi?** `curl telnet://localhost:44444`.
20. **Què vol dir la resposta `OK`?** Que la source ha acceptat el missatge.
21. **`OK` garanteix escriptura final a HDFS?** No; cal comprovar la sortida.
22. **Quin canal utilitza el Cas 1b?** FileChannel.
23. **Quines dues carpetes locals apareixen per FileChannel?** `data` i `checkpoint`.
24. **Quina és la ruta HDFS del Cas 1b?** `/user/iabd/flume/net_data/`.
25. **Què és multi-hop?** Encadenar agents Flume.
26. **Quin és l'agent emissor del Cas 2?** `NetcatAvroAgent`.
27. **Quin és el receptor?** `AvroHdfsAgent`.
28. **Quin port utilitza la connexió Avro?** 10003.
29. **Quina és la ruta de sortida del Cas 2?** `/user/iabd/flume/avro_data/`.
30. **En quin ordre s'han d'iniciar els agents?** Primer receptor, després emissor.
31. **Quina source rep esdeveniments d'un altre agent?** AvroSource.
32. **Quin sink envia a un altre agent?** AvroSink.
33. **Avro entre agents implica que HDFS desa fitxers Avro?** No necessàriament.
34. **Quines tres fonts s'utilitzen al Cas 3?** Spooldir, Netcat i Exec.
35. **Quina llibreria Python genera dades fictícies?** Faker.
36. **Quin locale utilitza l'script?** `es_ES`.
37. **Quants registres genera per CSV?** 100.
38. **Cada quant genera un fitxer?** Cada 20 segons, segons l'script.
39. **Quin separador utilitza el CSV?** Punt i coma `;`.
40. **Quins camps té cada usuari?** Email, contrasenya, nom, professió.
41. **Quina ruta local rep els CSV?** `/home/iabd/flume/spool/`.
42. **Què fa Spooldir?** Processa fitxers nous d'una carpeta.
43. **Quina propietat elimina els fitxers processats?** `deletePolicy = immediate`.
44. **Quin risc té eliminar-los?** Perdre els fitxers d'origen per reprocessar-los.
45. **Quina font llegeix un fitxer local via comanda?** Exec.
46. **Quin fitxer s'usa per Exec?** `/home/iabd/flume/dades/usuaris.txt`.
47. **Quantes fonts i canals s'empren a MultiAgent?** Tres fonts i tres canals.
48. **Quantes destinacions Avro descriu la pràctica a MultiAgent?** Tres.
49. **Quina és la ruta consolidada?** `/user/iabd/flume/usuaris/`.
50. **Per què es diu consolidador?** Rep fluxos de diferents orígens i els desa en una ubicació final.
51. **Què fa `head -5`?** Mostra les cinc primeres línies.
52. **Què fa `grep`?** Cerca patrons al text.
53. **Què fa `hdfs dfs -ls -t`?** Ordena per data de modificació.
54. **Per què pot haver-hi molts fitxers a HDFS?** Rotació de sortides i ingesta contínua.
55. **Què és un MemoryChannel?** Cua en memòria no persistent.
56. **Què és un FileChannel?** Cua amb estat persistent en disc.
57. **Què és un checkpoint?** Informació de control per reconstruir l'estat de FileChannel.
58. **Què significa un missatge de SLF4J duplicat?** Avís de dependències de logging duplicades, no sempre una fallada fatal.
59. **Per què les dades d'exemple han de ser fictícies?** Perquè no s'han d'ingestar contrasenyes reals en text pla.
60. **Com acredites l'èxit de tota la cadena?** Comproves l'entrada i el contingut final a HDFS.

## 30. Glossari [AMPLIACIÓ]

| Terme | Definició curta |
|---|---|
| Agent | Procés Flume que agrupa sources, channels i sinks |
| Event | Cos de dades i capçaleres transportats per Flume |
| Source | Component que rep o genera events |
| Channel | Cua intermèdia d'esdeveniments |
| Sink | Component que entrega events al destí |
| SeqGen | Source de generació seqüencial |
| Netcat | Source TCP de missatges de text |
| Spooldir | Source de fitxers afegits a una carpeta |
| Exec | Source basada en la sortida d'una comanda |
| Avro Sink | Sink de transmissió a una Avro Source |
| Avro Source | Source receptora d'un agent Flume |
| HdfsSink | Sink que persisteix a HDFS |
| MemChannel | Canal en memòria |
| FileChannel | Canal persistent en disc |
| Checkpoint | Punt de control de l'estat del canal |
| Multi-hop | Cadena de diversos agents |
| Consolidador | Agent receptor que reuneix diferents fluxos |
| Faker | Llibreria de generació de dades fictícies |
| `deletePolicy` | Política de gestió de fitxers Spooldir processats |
| `grep` | Eina de cerca de patrons en text |
| `jps` | Llista de processos Java accessibles |

## Checklist final d'examen

- [ ] Puc dibuixar Source → Channel → Sink.
- [ ] Diferencio els cinc tipus de source de la pràctica.
- [ ] Sé explicar FileChannel vs MemChannel.
- [ ] Recordo el port Netcat 44444 i el port Avro 10003.
- [ ] Sé explicar el Cas 1a sense consultar els apunts.
- [ ] Sé reproduir conceptualment el Cas 1b.
- [ ] Sé dibuixar els dos agents del Cas 2.
- [ ] Sé explicar per què s'inicia el receptor Avro abans de l'emissor.
- [ ] Entenc Faker, Spooldir i `deletePolicy = immediate`.
- [ ] Distingeixo les tres fonts del Cas 3.
- [ ] Sé demostrar que cada font ha arribat a HDFS.
- [ ] Conec les rutes HDFS dels quatre casos.
- [ ] Entenc per què `OK` no és suficient com a prova final.
- [ ] Sé identificar avisos SLF4J i errors reals.
- [ ] Puc explicar les precaucions de seguretat sobre contrasenyes i ports.

---

### Resum ultra ràpid

- **Cas 1a:** `SeqGen → MemChannel → HDFS` → `/user/iabd/flume/seqgen_data/`.
- **Cas 1b:** `Netcat:44444 → FileChannel → HDFS` → `/user/iabd/flume/net_data/`.
- **Cas 2:** `Netcat → FileChannel → AvroSink:10003 → AvroSource → MemChannel → HDFS` → `/user/iabd/flume/avro_data/`.
- **Casos 3–4:** `Faker/Spooldir + Netcat + Exec → MultiAgent → Avro:10003 → AvroHdfsAgent → HDFS` → `/user/iabd/flume/usuaris/`.
- **Evidència real:** fitxers i continguts comprovats a HDFS; la pràctica verifica separadament les tres fonts consolidades.

*Aquest document segueix l'activitat lliurada i afegeix ampliacions identificades per facilitar l'estudi. Les configuracions completes reconstruïdes són exemples didàctics que s'han d'adaptar abans d'executar-los; no són còpies verificades dels fitxers de la teva màquina.*
