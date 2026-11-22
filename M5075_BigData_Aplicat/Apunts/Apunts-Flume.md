# APUNTS EXTENSOS — APACHE FLUME

---
# 1. Introducció a Apache Flume

## 1.1. Què és?

**Apache Flume** és una eina destinada a la **recollida, ingesta i transport de grans quantitats de dades**, especialment esdeveniments i registres (*logs*). Permet construir fluxos continus des dels productors fins als sistemes que emmagatzemen o processen les dades.

Segons el dossier, Flume va ser presentat per **Cloudera cap al 2010** i posteriorment va passar a formar part de l'ecosistema Apache. Inicialment es va dissenyar per recollir els logs de nombrosos servidors web i traslladar-ne els esdeveniments a **HDFS** per al processament posterior.

La idea clau és separar **qui genera les dades** de **qui les rep i emmagatzema**.

```text
Servidors / Aplicacions / Usuaris
               |
               v
        APACHE FLUME
   (recull, encua i envia)
               |
               v
        HDFS / HBase / ...
```

### Conceptes essencials

- **Ingesta:** introducció de dades en un sistema per al seu ús posterior.
- **Streaming:** tractament de dades a mesura que van arribant, en comptes d'esperar que tots els fitxers estiguin disponibles.
- **Pipeline:** conjunt de passos connectats pels quals passen les dades.
- **Log:** registre d'accions, esdeveniments o errors d'una aplicació o servidor.
- **Buffer:** zona temporal que absorbeix diferències de velocitat entre emissor i receptor.

## 1.2. Per què utilitzar un buffer?

El PDF remarca que Flume fa de **buffer entre productors i destinacions**. Això permet que una font que produeix dades ràpidament no saturi immediatament el consumidor, i ajuda a suportar interrupcions temporals del destí.

Exemple conceptual:

```text
FONT: genera 300 missatges/s
          |
          v
CANAL: cua temporal d'esdeveniments
          |
          v
DESTÍ: processa 200 missatges/s
```

Mentre la font produeix més ràpid del que el sink consumeix, la cua pot acumular missatges **fins al límit de la capacitat configurada**. El buffer no és infinit: una saturació sostinguda també requereix capacitat suficient o mesures de control de flux.

Si HDFS no està disponible, els esdeveniments pendents poden mantenir-se al canal. **La durabilitat real depèn del tipus de canal**: un FileChannel persisteix en disc; un Memory Channel no protegeix davant de la pèrdua de la RAM.

## 1.3. Situació del projecte

El dossier indica que Apache Logging Services va marcar Flume com a projecte **adormit (*dormant*) el 10 d'octubre de 2024** i assenyala **1.11.0** com a darrera versió disponible en el moment de la seva revisió. Aquestes dades es recullen del material docent i no constitueixen una comprovació en temps real de la pàgina oficial.

**Idea d'examen:** la utilitat de Flume és principalment **transportar/ingerir esdeveniments**; no s'ha de confondre amb el motor encarregat d'analitzar-los.

---

# 2. Alternatives a Flume

El document distingeix alternatives **de codi obert** i **serveis al núvol o comercials**.

## 2.1. Open source

| Eina | Funció destacada al dossier |
|---|---|
| **Apache Kafka** | Missatgeria distribuïda i processament d'esdeveniments en temps real. |
| **Apache NiFi** | Moviment i processament de dades mitjançant una interfície visual. |
| **Logstash** | Processament i ingesta de dades, especialment cap a Elasticsearch. |
| **Apache Flink** | Processament d'esdeveniments en temps real. |
| **Apache Pulsar** | Streaming i missatgeria distribuïda; alternativa en l'àmbit de Kafka. |

## 2.2. Solucions cloud i comercials

| Servei | Funció destacada |
|---|---|
| **AWS Kinesis** | Ingesta i anàlisi de dades en streaming com a servei gestionat. |
| **Google Cloud Pub/Sub** | Sistema de missatgeria al núvol. |
| **Azure Event Hubs** | Ingesta i streaming d'esdeveniments a Azure. |
| **IBM MQ** | Missatgeria per a entorns empresarials. |

**Nota d'estudi:** no totes aquestes eines són equivalents en totes les seves funcions. Algunes se centren en el transport i la missatgeria i d'altres en el processament, l'orquestració o la integració. El dossier les inclou com a alternatives tecnològiques relacionades.

---

# 3. Instal·lació i entorn de treball

## 3.1. Entorn del document

A la màquina virtual de classe **Flume ja està instal·lat**. El PDF indica:

```bash
FLUME_HOME=/opt/flume-1.11.0
```

Aquesta variable d'entorn apunta al directori base del programari.

El document també facilita un enllaç de descàrrega de la versió 1.11.0:

```text
https://dlcdn.apache.org/flume/1.11.0/apache-flume-1.11.0-bin.tar.gz
```

A les ordres d'exemple es fa servir habitualment `/opt/flume/conf/` i els fitxers situats dins de `./conf/`. Per tant, **comprova on es troba realment la instal·lació i quin és el directori de treball** abans d'executar-les. La ruta exacta del dossier és pròpia de la màquina virtual docent.

## 3.2. Comprovacions útils

```bash
echo "$FLUME_HOME"
ls "$FLUME_HOME"
ls "$FLUME_HOME/conf"
which flume-ng
```

Interpretació:

- `echo`: mostra el valor configurat de `FLUME_HOME`.
- `ls`: verifica si existeixen carpetes i configuracions.
- `which flume-ng`: comprova si el comandament es troba al `PATH`.

Si el fitxer de configuració s'ha desat a `$FLUME_HOME/conf/seqgen.conf`, és pràctic canviar prèviament de directori:

```bash
cd "$FLUME_HOME"
```

## 3.3. Característiques descrites al PDF

1. **Disseny flexible** basat en fluxos de dades.
2. **Robustesa i resistència davant de fallades**, segons la configuració.
3. **Possibilitat de moure dades** a destinacions com **HDFS** i **HBase**.
4. **Execució distribuïda** amb diversos agents connectats.

---

# 4. Arquitectura de Flume

L'arquitectura fonamental consta de **tres components** dins de cada agent:

```text
+---------------------------------------------------+
|                  AGENT FLUME                      |
|                                                   |
|   +----------+    +-----------+    +----------+   |
|   |  SOURCE  | -> |  CHANNEL  | -> |   SINK   |   |
|   |  Origen  |    |   Cua     |    |   Destí  |   |
|   +----------+    +-----------+    +----------+   |
|                                                   |
+---------------------------------------------------+
```

**Regla imprescindible:** `SOURCE → CHANNEL → SINK`.

## 4.1. Source (font)

És el component que **rep, llegeix o genera esdeveniments** i els introdueix en un o més canals.

Exemples del material:

- **Exec Source:** executa una ordre del sistema.
- **NetCat Source:** escolta missatges en un port TCP.
- **Spooling Directory Source:** observa una carpeta i ingereix els fitxers nous.
- **Avro Source:** rep esdeveniments d'un altre agent per Avro.
- **Sequence Generator Source:** genera nombres per a proves.
- Altres fonts de la llista del PDF: Kafka, HTTP, JMS, syslog i Thrift.

Una font pot escriure en **múltiples channels**. Això és important quan es vol distribuir o replicar un flux.

## 4.2. Channel (canal)

És el component que **emmagatzema temporalment els esdeveniments** abans que siguin consumits per un sink. Es comporta com una cua.

- Les sources **afegeixen** esdeveniments.
- Els sinks **consumeixen** esdeveniments.
- Diverses sources poden escriure al mateix canal.
- Diversos sinks poden llegir d'un mateix canal, però **cada esdeveniment del canal és consumit per un dels sinks**, no copiat automàticament a tots.
- Un sink queda associat a **un sol canal**.

### Memory Channel

Desa temporalment els esdeveniments **en memòria RAM**.

**Avantatge:** ràpid.  
**Inconvenient:** les dades pendents es poden perdre si cau el procés o la màquina.

### File Channel

Desa els esdeveniments i els punts de control **en disc local**.

**Avantatge:** ofereix persistència i recuperació davant de fallades, segons la integritat del disc i la configuració.  
**Inconvenient:** en general, més operacions de disc i una gestió més complexa que el canal de memòria.

## 4.3. Sink (destí)

És el component que **extreu esdeveniments del canal** i els envia al següent sistema o agent.

Exemples:

- **Logger Sink:** mostra els esdeveniments al registre de Flume.
- **HDFS Sink:** desa esdeveniments a Hadoop Distributed File System.
- **Avro Sink:** envia esdeveniments a un altre agent mitjançant Avro RPC.
- Altres sinks esmentats: Hive, Kafka, HBase, Thrift, File Roll, Null, etc.

El dossier subratlla el **commit transaccional**: quan el sink completa correctament l'enviament, confirma l'operació i l'esdeveniment pot sortir definitivament del canal.

## 4.4. Seqüència d'un esdeveniment

1. Un productor genera una línia de dades.
2. La source la converteix en un esdeveniment.
3. La source l'afegeix al channel.
4. El channel el manté en espera.
5. El sink el recupera.
6. El sink intenta lliurar-lo al destí.
7. Quan l'operació té èxit, es confirma la transacció i l'esdeveniment es retira del canal.

```text
MISSATGE
   |
   v
[Source] --escriptura--> [Channel] --lectura--> [Sink]
                            ^                      |
                            |------ confirmació ---|
                                                   |
                                                   v
                                                  HDFS
```

**Nota d'estudi:** l'ús de transaccions i cues redueix pèrdues en situacions habituals de fallada, però no s'ha d'interpretar com una garantia universal que mai hi haurà duplicats o pèrdues en qualsevol configuració.

---

# 5. Agents i esdeveniments

## 5.1. Agent

Un **agent** és la unitat bàsica d'execució de Flume. Conté les fonts, canals i destins necessaris per moure dades.

Es poden desplegar diferents agents a diferents màquines i **encadenar-los** per transportar informació des de l'origen fins al repositori final.

Exemple:

```text
Servidor web A ---> Agent A --+
                              |
Servidor web B ---> Agent B --+--> Agent central --> HDFS
                              |
Servidor web C ---> Agent C --+
```

Els agents pròxims als productors recullen dades; els agents centrals poden agrupar-les o reenviar-les.

## 5.2. Esdeveniment (*event*)

És la **unitat mínima de dades** que processa Flume. El dossier presenta la lectura d'una línia delimitada per salt de línia com un cas habitual de creació d'esdeveniments.

Un event té dues parts:

| Element | Què conté? | Utilitat |
|---|---|---|
| **Header** (capçalera) | Metadades clau–valor. | Classificar, enrutar, identificar orígens, dates, prioritats. |
| **Body / payload** (cos) | Matriu de bytes amb les dades reals. | Transportar el missatge o registre. |

Exemple conceptual:

```text
Event {
  headers: {
    "timestamp": "...",
    "ip_origen": "192.168.1.15"
  },
  body: "Usuari autenticat correctament"
}
```

Al `LoggerSink`, el contingut del body es pot mostrar en hexadecimal acompanyat d'una representació llegible.

### Exemple del PDF

```text
Event: { headers:{} body: 44 6F 63 75 6D 65 6E 74 73 Documents }
```

- `headers:{}`: capçalera buida.
- `44 6F 63...`: bytes representats en hexadecimal.
- `Documents`: contingut interpretat com a text.

**Per memoritzar:** un esdeveniment = **capçalera + cos**.

---

# 6. Tipus de components més importants

Aquesta selecció reordena els tipus que apareixen a la taula de la pàgina 5 del PDF.

| Sources | Channels | Sinks |
|---|---|---|
| Avro | Memory | HDFS |
| Thrift | JDBC | Hive |
| Exec | Kafka | Logger |
| JMS | File | Avro |
| Spooling Directory | Spillable Memory | Thrift |
| Kafka | Pseudo Transaction | Kafka |
| NetCat | | File Roll |
| Sequence Generator | | Null |
| Syslog | | HBase / AsyncHBase |
| HTTP | | Elasticsearch / altres |

El document també enumera fonts de Twitter, variants de syslog i sinks orientats a Solr o Kite Dataset. Per saber si un component determinat és usable en una instal·lació, cal consultar la guia de la versió corresponent.

### Què convé saber explicar a l'examen?

- **Netcat vs Exec:** Netcat rep text per xarxa; Exec obté sortida d'una comanda.
- **Spooldir vs Netcat:** Spooldir ingereix fitxers d'un directori; Netcat rep línies de connexions.
- **Avro Source vs Avro Sink:** la primera rep connexions Avro; el segon les envia.
- **Memory vs File Channel:** RAM ràpida però volàtil davant de fallades; disc més durador.
- **Logger vs HDFS Sink:** Logger és útil per observar les dades; HDFS les persisteix.

---

# 7. Configuració d'agents amb `.conf`

## 7.1. Estructura general

Els fitxers de configuració utilitzen parelles **propietat = valor**. El nom de l'agent encapçala les propietats.

```properties
# Components de l'agent
ElMeuAgent.sources = Source1
ElMeuAgent.channels = Channel1
ElMeuAgent.sinks = Sink1

# Configuració de la source
ElMeuAgent.sources.Source1.type = ...

# Configuració del channel
ElMeuAgent.channels.Channel1.type = ...

# Configuració del sink
ElMeuAgent.sinks.Sink1.type = ...

# Enllaços
ElMeuAgent.sources.Source1.channels = Channel1
ElMeuAgent.sinks.Sink1.channel = Channel1
```

## 7.2. Les quatre parts de la configuració

1. **Declarar** les fonts, els canals i els destins.
2. **Definir** el tipus i les propietats de les fonts.
3. **Definir** els tipus i les propietats dels canals i destins.
4. **Enllaçar** les fonts i els destins amb els canals.

L'ordre exacte de les línies es pot organitzar per llegibilitat, però cal que totes les referències a noms de components coincideixin.

## 7.3. `channels` (plural) i `channel` (singular)

Aquesta diferència és molt important:

```properties
# Source: pot enviar a més d'un canal
Agent.sources.Source1.channels = CanalA CanalB

# Sink: queda connectat a un únic canal
Agent.sinks.Sink1.channel = CanalA
```

**Motiu:** una font pot fer *fan-out*, mentre que cada sink consumeix d'un sol canal. Si dos sinks consumeixen el mateix canal, competeixen pels esdeveniments; això **no és el mateix** que duplicar el flux.

## 7.4. Ordre d'execució bàsica

```bash
flume-ng agent \
  --conf conf/ \
  --conf-file conf/agent.conf \
  --name ElMeuAgent \
  -Dflume.root.logger=INFO,console
```

| Paràmetre | Significat |
|---|---|
| `flume-ng agent` | Inicia un agent de Flume. |
| `--conf` | Indica el directori general de configuració. |
| `--conf-file` | Indica el fitxer `.conf` de l'agent. |
| `--name` / `-n` | Indica quin agent s'ha d'executar. |
| `-Dflume.root.logger=INFO,console` | Configura la sortida de registre utilitzada als exemples del PDF. |

El nom de `--name` **ha de coincidir amb el prefix definit al `.conf`**.

### Com aturar l'agent

Normalment s'executa en primer pla (*foreground*). Per interrompre'l s'utilitza:

```text
Ctrl + C
```

El PDF també esmenta `Ctrl + Z`, però aquest últim **suspèn el procés** en lloc de finalitzar-lo de manera ordinària. Per aturar l'agent, prefereix `Ctrl + C`.

---

# 8. Pràctica inicial: ExecLoggerAgent (pàgines 7–9)

## 8.1. Objectiu

Executar una ordre Linux (`ls /home/iabd/`), convertir la sortida en esdeveniments i mostrar-los al log de Flume.

```text
Exec Source ---> Memory Channel ---> Logger Sink
     |                 |                 |
  comanda ls          RAM            missatges
```

## 8.2. Fitxer `agent.conf`

Ruta proposada pel document: `/home/iabd/conf/agent.conf`.

```properties
# Noms dels components de l'agent
ExecLoggerAgent.sources = Exec
ExecLoggerAgent.channels = MemChannel
ExecLoggerAgent.sinks = LoggerSink

# Source: executa una ordre
ExecLoggerAgent.sources.Exec.type = exec
ExecLoggerAgent.sources.Exec.command = ls /home/iabd/

# Sink: registra els esdeveniments
ExecLoggerAgent.sinks.LoggerSink.type = logger

# Channel: cua temporal en RAM
ExecLoggerAgent.channels.MemChannel.type = memory
ExecLoggerAgent.channels.MemChannel.capacity = 1000
ExecLoggerAgent.channels.MemChannel.transactionCapacity = 100

# Enllaços de components
ExecLoggerAgent.sources.Exec.channels = MemChannel
ExecLoggerAgent.sinks.LoggerSink.channel = MemChannel
```

## 8.3. Explicació línia per línia

- `sources = Exec`: crea una source identificada com a `Exec`.
- `channels = MemChannel`: declara el canal.
- `sinks = LoggerSink`: declara la destinació.
- `type = exec`: la font obté dades de l'execució d'una ordre.
- `command = ls /home/iabd/`: mostra el contingut del directori.
- `type = logger`: imprimeix events al registre.
- `type = memory`: desa temporalment els events a RAM.
- `capacity = 1000`: capacitat màxima configurada de la cua en esdeveniments.
- `transactionCapacity = 100`: límit configurat d'esdeveniments en una transacció del canal.
- `sources.Exec.channels`: indica on publica l'origen.
- `sinks.LoggerSink.channel`: indica des de quin canal consumeix el destí.

**Nota d'estudi:** `capacity` i `transactionCapacity` no indiquen el mateix: la primera és la capacitat total de la cua, i la segona limita el nombre d'events per transacció.

## 8.4. Execució

Des de `/home/iabd`, segons el dossier:

```bash
flume-ng agent \
  --name ExecLoggerAgent \
  --conf /opt/flume/conf/ \
  --conf-file ./conf/agent.conf
```

## 8.5. Què apareix al log?

El PDF descriu tres fases:

1. Flume **crea** el canal, la source i el sink.
2. Flume **inicialitza i arrenca** els components.
3. La comanda s'executa i el LoggerSink registra cada línia retornada com a esdeveniment.

Un fragment de sortida recollit al material és:

```text
Event: { headers:{} body: 64 65 72 62 79 2E 6C 6F 67 derby.log }
```

La comanda `ls` finalitza després de retornar la llista; això **no implica necessàriament que el procés Flume finalitzi automàticament**.

### Preguntes típiques

**Quin origen utilitza?** Exec Source.  
**Quin canal utilitza?** Memory Channel.  
**On acaben les dades?** Al log, via LoggerSink.  
**S'han enviat a HDFS?** No.  
**Per què hi ha `headers:{}`?** No s'han afegit metadades a la capçalera.

---

# 9. Cas 1a — Emmagatzematge a HDFS (pàgines 12–14)

## 9.1. Objectiu

Generar dades seqüencials i emmagatzemar-les en HDFS.

```text
Sequence Generator ---> Memory Channel ---> HDFS Sink
   0, 1, 2, 3...             RAM             fitxers HDFS
```

**Agent:** `SeqGenAgent`.  
**Fitxer:** `seqgen.conf`.

## 9.2. Configuració completa

```properties
# Components
SeqGenAgent.sources = SeqSource
SeqGenAgent.channels = MemChannel
SeqGenAgent.sinks = HDFS

# Font seqüencial
SeqGenAgent.sources.SeqSource.type = seq

# Destí HDFS
SeqGenAgent.sinks.HDFS.type = hdfs
SeqGenAgent.sinks.HDFS.hdfs.path = hdfs://master:9000/user/iabd/flume/seqgen_data/
SeqGenAgent.sinks.HDFS.hdfs.filePrefix = flume-cas1a-seqgen
SeqGenAgent.sinks.HDFS.hdfs.rollInterval = 0
SeqGenAgent.sinks.HDFS.hdfs.rollCount = 1000
SeqGenAgent.sinks.HDFS.hdfs.fileType = DataStream

# Canal de memòria
SeqGenAgent.channels.MemChannel.type = memory
SeqGenAgent.channels.MemChannel.capacity = 1000
SeqGenAgent.channels.MemChannel.transactionCapacity = 100

# Connexions
SeqGenAgent.sources.SeqSource.channels = MemChannel
SeqGenAgent.sinks.HDFS.channel = MemChannel
```

## 9.3. Propietats principals

| Propietat | Explicació |
|---|---|
| `type = seq` | Font que genera una seqüència de nombres per a proves. |
| `type = hdfs` | Destí que escriu a HDFS. |
| `hdfs.path` | Ruta de destinació dins del sistema distribuït. |
| `hdfs.filePrefix` | Prefix dels noms dels fitxers creats. |
| `hdfs.rollInterval = 0` | Desactiva el tancament per interval de temps. |
| `hdfs.rollCount = 1000` | Criteri de rotació quan s'han escrit 1.000 events. |
| `hdfs.fileType = DataStream` | Escriptura com a flux de dades. |
| `capacity = 1000` | Capacitat del canal de memòria. |
| `transactionCapacity = 100` | Límit d'events per transacció. |

**Important:** fixar `rollInterval = 0` no desactiva necessàriament la resta de criteris de rotació; poden continuar aplicant-se altres paràmetres.

## 9.4. Preparació de Hadoop i HDFS

El document indica que cal tenir **Hadoop i YARN iniciats** abans de començar i proposa:

```bash
start-all.sh
```

També recorda que s'ha de crear el directori HDFS necessari. Una ordre pràctica coherent amb aquesta instrucció és:

```bash
hdfs dfs -mkdir -p /user/iabd/flume/seqgen_data
```

*Nota d'estudi:* aquesta ordre `-mkdir -p` explicita el pas de creació que el PDF indica, però no escriu literalment.

## 9.5. Executar l'agent

Des de `$FLUME_HOME`:

```bash
flume-ng agent --conf conf/ --conf-file conf/seqgen.conf \
  --name SeqGenAgent \
  -Dflume.root.logger=INFO,console
```

El generador continua produint valors. El dossier recomana aturar-lo després d'uns segons amb **Ctrl + C** per evitar generar massa fitxers.

## 9.6. Comprovar les dades

```bash
hdfs dfs -ls /user/iabd/flume/seqgen_data
```

Aquesta ordre enumera els fitxers generats. Per veure el contingut d'un fitxer concret:

```bash
hdfs dfs -cat /user/iabd/flume/seqgen_data/NOM_DEL_FITXER
```

El contingut esperat és similar a:

```text
0
1
2
3
...
```

Per eliminar els fitxers i la carpeta de la pràctica:

```bash
hdfs dfs -rm -r /user/iabd/flume/seqgen_data
```

**Atenció:** aquesta última ordre **esborra** el directori i el contingut. Confirma'n la ruta abans d'executar-la.

## 9.7. Què hem après?

- La source pot **generar** dades sense una entrada externa.
- HDFS pot ser un **destí directe** del sink.
- Les dades es poden agrupar en fitxers segons criteris de rotació.
- Les comandes `hdfs dfs -ls` i `hdfs dfs -cat` permeten verificar la ingesta.

---

# 10. Cas 1b — De Netcat a HDFS (pàgines 15–17)

## 10.1. Objectiu

Enviar línies de text per un port local, convertir cada línia en un esdeveniment i persistir-les a HDFS, fent servir un **FileChannel**.

```text
Terminal (curl telnet)
         |
   localhost:44444
         |
         v
  Netcat Source ---> File Channel ---> HDFS Sink
                         |
                  disc local
                         |
                         v
                /user/iabd/flume/net_data/
```

**Agent:** `NetcatAgent`.  
**Fitxer:** `netcat.conf`.

## 10.2. Configuració completa

```properties
# Components
NetcatAgent.sources = Netcat
NetcatAgent.channels = FileChannel
NetcatAgent.sinks = HdfsSink

# Netcat Source
NetcatAgent.sources.Netcat.type = netcat
NetcatAgent.sources.Netcat.bind = localhost
NetcatAgent.sources.Netcat.port = 44444
NetcatAgent.sources.Netcat.channels = FileChannel

# HDFS Sink
NetcatAgent.sinks.HdfsSink.type = hdfs
NetcatAgent.sinks.HdfsSink.hdfs.path = hdfs://master:9000/user/iabd/flume/net_data/
NetcatAgent.sinks.HdfsSink.hdfs.writeFormat = Text
NetcatAgent.sinks.HdfsSink.hdfs.fileType = DataStream
NetcatAgent.sinks.HdfsSink.channel = FileChannel

# FileChannel
NetcatAgent.channels.FileChannel.type = file
NetcatAgent.channels.FileChannel.dataDir = /home/iabd/flume/data
NetcatAgent.channels.FileChannel.checkpointDir = /home/iabd/flume/checkpoint
```

## 10.3. Propietats de Netcat

```properties
NetcatAgent.sources.Netcat.bind = localhost
NetcatAgent.sources.Netcat.port = 44444
```

`bind` especifica la interfície/adreça d'escolta i `port` indica el port utilitzat. Amb `localhost`, les connexions de prova es fan a la mateixa màquina.

Cada cop que s'introdueix una línia completa amb **Enter**, Netcat la transmet com a esdeveniment. Al PDF, el client rep una resposta `OK` per les línies enviades.

## 10.4. Propietats del FileChannel

```properties
NetcatAgent.channels.FileChannel.type = file
NetcatAgent.channels.FileChannel.dataDir = /home/iabd/flume/data
NetcatAgent.channels.FileChannel.checkpointDir = /home/iabd/flume/checkpoint
```

- `type = file`: canal persistent en disc.
- `dataDir`: fitxers locals amb dades del canal.
- `checkpointDir`: metadades i punts de control per recuperar l'estat.

Aquests camins són **carpetes del Linux local, no carpetes HDFS**.

## 10.5. Execució

Terminal 1:

```bash
flume-ng agent --conf /opt/flume/conf/ --conf-file ./conf/netcat.conf \
  --name NetcatAgent \
  -Dflume.root.logger=INFO,console
```

Terminal 2:

```bash
curl telnet://localhost:44444
```

Missatges de prova:

```text
Provant Netcat
OK
Això sembla que més o menys funciona
OK
```

L'`OK` és la resposta del servei, no una nova línia de dades que calgui escriure manualment.

## 10.6. Comprovació a HDFS

El dossier consulta el navegador web d'HDFS:

```text
http://master:9870/explorer.html#/user/iabd/flume/net_data
```

També pots comprovar la ruta des del terminal:

```bash
hdfs dfs -ls /user/iabd/flume/net_data
hdfs dfs -cat /user/iabd/flume/net_data/NOM_DEL_FITXER
```

La captura de la pàgina 17 mostra el resultat d'aquest flux a l'explorador d'HDFS.

## 10.7. Per què aquest cas és important?

A diferència del cas 1a, aquí hi ha **entrada manual per xarxa** i el buffer és **persistent al disc**. És un bon exemple per explicar la diferència entre una prova amb Memory Channel i una ingesta que ha de tolerar millor les interrupcions.

---

# 11. Esdeveniments, fitxers HDFS i rotació

El document explica que el sink HDFS no ha d'obrir i tancar necessàriament un fitxer per cada event; pot **agrupar-ne molts** en un mateix fitxer.

## 11.1. Criteris de rotació

| Propietat | Què controla? | Valor per defecte indicat al PDF |
|---|---|---|
| `hdfs.rollInterval` | Temps abans de rotar el fitxer. | 30 segons. |
| `hdfs.rollSize` | Mida abans de rotar el fitxer. | 1024 bytes. |
| `hdfs.rollCount` | Nombre d'esdeveniments abans de rotar. | 10 esdeveniments. |

*Els valors d'aquesta taula són els que presenta el dossier; en un entorn diferent és recomanable consultar la configuració i la versió instal·lada.*

### Exemple

Si el fitxer arriba al límit de temps, de mida o d'esdeveniments que estigui habilitat, pot tancar-se i començar-ne un de nou.

```text
Arriben events
     |
     v
Fitxer HDFS obert i temporal
     |
     +---- Temps esgotat? -------+
     |                           |
     +---- Mida assolida? -------+--> Tancar/rotar
     |                           |         |
     +---- Nombre assolit? ------+         v
                                  Fitxer definitiu
                                        |
                                        v
                                   Fitxer nou
```

## 11.2. Fitxers `.tmp`

Mentre el sink escriu, el fitxer pot aparèixer amb **nom temporal**, amb prefix `_` i sufix `.tmp`, tal com explica el dossier. En acabar el cicle de rotació es tanca i adopta el nom final.

**Idea important:** veure un `.tmp` mentre l'agent està funcionant **no implica necessàriament un error**.

---

# 12. Cas 2 — Fluxos encadenats amb Avro (pàgines 18–20)

## 12.1. Què és un flux *multi-hop*?

És un pipeline on **la sortida d'un agent alimenta l'entrada d'un altre**. En els exemples del PDF la connexió es fa amb una parella **Avro Sink → Avro Source**.

```text
                    AGENT 1                         AGENT 2

Text TCP ---> [Netcat] -> [FileChannel] -> [AvroSink]
                                            |
                                      localhost:10003
                                            |
                                            v
                                        [AvroSource] -> [MemChannel] -> [HdfsSink] -> HDFS
```

La connexió Avro fa possible dividir el sistema en dues etapes. Cada etapa pot tenir el seu propi canal i configuració.

## 12.2. Primer agent: `NetcatAvroAgent`

**Fitxer:** `netcat-avro.conf`.

```properties
# Components
NetcatAvroAgent.sources = Netcat
NetcatAvroAgent.channels = FileChannel
NetcatAvroAgent.sinks = AvroSink

# Netcat: rep dades al port 44444
NetcatAvroAgent.sources.Netcat.type = netcat
NetcatAvroAgent.sources.Netcat.bind = localhost
NetcatAvroAgent.sources.Netcat.port = 44444

# Avro: envia dades al port 10003
NetcatAvroAgent.sinks.AvroSink.type = avro
NetcatAvroAgent.sinks.AvroSink.hostname = localhost
NetcatAvroAgent.sinks.AvroSink.port = 10003

# FileChannel i connexions
NetcatAvroAgent.sources.Netcat.channels = FileChannel
NetcatAvroAgent.sinks.AvroSink.channel = FileChannel
NetcatAvroAgent.channels.FileChannel.type = file
NetcatAvroAgent.channels.FileChannel.dataDir = /home/iabd/flume/data
NetcatAvroAgent.channels.FileChannel.checkpointDir = /home/iabd/flume/checkpoint
```

### Funció de cada component

1. **Netcat** rep missatges a `localhost:44444`.
2. **FileChannel** desa els esdeveniments al disc local.
3. **AvroSink** els envia cap a `localhost:10003`.

**Important:** el primer agent **no desa directament en HDFS**.

## 12.3. Segon agent: `AvroHdfsAgent`

**Fitxer:** `avro-hdfs.conf`.

```properties
# Components
AvroHdfsAgent.sources = AvroSource
AvroHdfsAgent.channels = MemChannel
AvroHdfsAgent.sinks = HdfsSink

# Avro: rep del primer agent
AvroHdfsAgent.sources.AvroSource.type = avro
AvroHdfsAgent.sources.AvroSource.bind = localhost
AvroHdfsAgent.sources.AvroSource.port = 10003

# HDFS: destinació final
AvroHdfsAgent.sinks.HdfsSink.type = hdfs
AvroHdfsAgent.sinks.HdfsSink.hdfs.path = /user/iabd/flume/avro_data/
AvroHdfsAgent.sinks.HdfsSink.hdfs.fileType = DataStream
AvroHdfsAgent.sinks.HdfsSink.hdfs.writeFormat = Text

# Memory Channel i connexions
AvroHdfsAgent.sources.AvroSource.channels = MemChannel
AvroHdfsAgent.sinks.HdfsSink.channel = MemChannel
AvroHdfsAgent.channels.MemChannel.type = memory
```

### Funció de cada component

1. **AvroSource** obre un servidor Avro RPC al port `10003`.
2. **MemChannel** manté temporalment les dades en RAM.
3. **HdfsSink** les escriu a `/user/iabd/flume/avro_data/`.

## 12.4. Relació entre els dos agents

| Agent emissor | Agent receptor |
|---|---|
| `AvroSink` | `AvroSource` |
| `hostname = localhost` | `bind = localhost` |
| `port = 10003` | `port = 10003` |
| Envia esdeveniments | Els rep |

**Regla:** el destí Avro del primer agent ha de poder contactar amb l'origen Avro del segon agent. En el dossier, tots dos estan a `localhost:10003`.

## 12.5. Ordre correcte d'arrencada

**Primer: l'agent receptor/consolidador.**

```bash
flume-ng agent --conf /opt/flume/conf/ --conf-file ./conf/avro-hdfs.conf \
  --name AvroHdfsAgent \
  -Dflume.root.logger=INFO,console
```

**Després: l'agent emissor.**

```bash
flume-ng agent --conf ./conf/ --conf-file ./conf/netcat-avro.conf \
  --name NetcatAvroAgent \
  -Dflume.root.logger=INFO,console
```

**Finalment: enviar missatges.**

```bash
curl telnet://localhost:44444
```

A continuació es comproven els fitxers a:

```text
/user/iabd/flume/avro_data/
```

## 12.6. Per què s'arrenca primer el receptor?

Perquè el segon agent ha de posar el servidor Avro a l'escolta al port `10003` abans que el primer agent intenti enviar-li dades. Això evita intents inicials de connexió fallits i facilita comprovar tot el pipeline.

## 12.7. Pregunta típica

**Per què es fa servir Avro?** Per **connectar agents** i transportar esdeveniments entre les dues etapes del flux.

---

# 13. Cas 3 — Flux multi-agent i consolidació (pàgines 21–24)

## 13.1. Objectiu

Unificar **tres fonts heterogènies** i enviar-les a un mateix receptor:

1. **Netcat:** text per un port TCP.
2. **Spooldir:** fitxers nous dins d'una carpeta vigilada.
3. **Exec:** resultat d'executar una ordre Linux.

Es reutilitza l'agent `AvroHdfsAgent` del cas 2 com a **consolidador**.

```text
                            MultiAgent

Netcat:44444 --> FileChannel ----> AvroSink1 ---+
                                                |
Spooldir ------> MemChannel1 ---> AvroSink2 ---+--> AvroSource:10003
                                                |           |
Exec:cat ------> MemChannel2 ---> AvroSink3 ---+           v
                                                        MemChannel
                                                            |
                                                            v
                                                          HDFS
```

## 13.2. Fitxer `multiagent-avro.conf`

```properties
# Tres fonts, tres canals, tres sinks
MultiAgent.sources = Netcat Spooldir Exec
MultiAgent.channels = FileChannel MemChannel1 MemChannel2
MultiAgent.sinks = AvroSink1 AvroSink2 AvroSink3

# Source 1: Netcat
MultiAgent.sources.Netcat.type = netcat
MultiAgent.sources.Netcat.bind = localhost
MultiAgent.sources.Netcat.port = 44444

# Source 2: Spooldir
MultiAgent.sources.Spooldir.type = spooldir
MultiAgent.sources.Spooldir.spoolDir = /home/iabd/flume/spoolDir

# Source 3: Exec
MultiAgent.sources.Exec.type = exec
MultiAgent.sources.Exec.command = cat /home/iabd/das/empleats.txt

# Tres sinks Avro al mateix receptor
MultiAgent.sinks.AvroSink1.type = avro
MultiAgent.sinks.AvroSink1.hostname = localhost
MultiAgent.sinks.AvroSink1.port = 10003

MultiAgent.sinks.AvroSink2.type = avro
MultiAgent.sinks.AvroSink2.hostname = localhost
MultiAgent.sinks.AvroSink2.port = 10003

MultiAgent.sinks.AvroSink3.type = avro
MultiAgent.sinks.AvroSink3.hostname = localhost
MultiAgent.sinks.AvroSink3.port = 10003

# Canals
MultiAgent.channels.FileChannel.type = file
MultiAgent.channels.FileChannel.dataDir = /home/iabd/flume/data
MultiAgent.channels.FileChannel.checkpointDir = /home/iabd/flume/checkpoint
MultiAgent.channels.MemChannel1.type = memory
MultiAgent.channels.MemChannel2.type = memory

# Connexions de cada flux
MultiAgent.sources.Netcat.channels = FileChannel
MultiAgent.sources.Spooldir.channels = MemChannel1
MultiAgent.sources.Exec.channels = MemChannel2

MultiAgent.sinks.AvroSink1.channel = FileChannel
MultiAgent.sinks.AvroSink2.channel = MemChannel1
MultiAgent.sinks.AvroSink3.channel = MemChannel2
```

## 13.3. Relació entre els components

| Source | Channel | Sink | Destinació |
|---|---|---|---|
| Netcat | FileChannel | AvroSink1 | AvroSource:10003 |
| Spooldir | MemChannel1 | AvroSink2 | AvroSource:10003 |
| Exec | MemChannel2 | AvroSink3 | AvroSource:10003 |

### Netcat

Escolta el port `44444` i rep línies de text. Utilitza un **canal de fitxer**, que permet mantenir les dades pendents en disc.

### Spooldir

Vigila la carpeta:

```text
/home/iabd/flume/spoolDir
```

Quan s'hi incorpora un fitxer nou, Flume el processa. El dossier explica que, després de la ingesta, el fitxer és marcat amb el sufix **`.COMPLETED`**.

**Nota d'estudi:** Spooldir és especialment interessant per integrar fitxers de text o CSV que una altra aplicació deixa periòdicament en un directori. Cal tractar els fitxers d'entrada com a nous i complets en dipositar-los a la carpeta vigilada.

### Exec

Executa una ordre per llegir el contingut d'un fitxer:

```bash
cat /home/iabd/das/empleats.txt
```

**Atenció a una incoherència del PDF:** en el fitxer de configuració apareix `/home/iabd/das/empleats.txt`, però a l'apartat de preparació es demana tenir `/home/iabd/dades/empleats.txt`. Abans d'executar el cas, cal **unificar aquestes rutes** segons el fitxer real. No són automàticament equivalents.

## 13.4. Preparació

El PDF indica que cal disposar de:

```text
/home/iabd/flume/spoolDir
/home/iabd/dades/empleats.txt
```

Una preparació possible és:

```bash
mkdir -p /home/iabd/flume/spoolDir
ls -l /home/iabd/dades/empleats.txt
```

Si el fitxer és a `dades`, corregeix la propietat `MultiAgent.sources.Exec.command` per apuntar-hi.

## 13.5. Execució del multi-agent

Primer, arrenca **AvroHdfsAgent**:

```bash
flume-ng agent --conf /opt/flume/conf/ --conf-file ./conf/avro-hdfs.conf \
  --name AvroHdfsAgent \
  -Dflume.root.logger=INFO,console
```

Després, arrenca **MultiAgent**:

```bash
flume-ng agent --conf /opt/flume/conf/ --conf-file ./conf/multiagent-avro.conf \
  --name MultiAgent \
  -Dflume.root.logger=INFO,console
```

Per provar l'origen Netcat:

```bash
curl telnet://localhost:44444
```

Per provar Spooldir, col·loca **un fitxer de text o CSV nou** a `/home/iabd/flume/spoolDir` i comprova que s'ingereix. Per verificar el resultat final, consulta HDFS:

```bash
hdfs dfs -ls /user/iabd/flume/avro_data
```

## 13.6. Què ens demostra aquest exemple?

- Una mateixa configuració d'agent pot declarar **diverses fonts**.
- Les fonts poden utilitzar **canals diferents**.
- Cada canal pot alimentar el seu propi sink.
- Diversos **AvroSinks** poden transmetre a un únic **AvroSource**.
- Un agent central pot **consolidar** diversos fluxos per escriure'ls a HDFS.

---

# 14. Directoris `dataDir` i `checkpointDir`

La pàgina 24 dedica un apartat específic a les carpetes locals del **FileChannel**.

## 14.1. `dataDir`

Exemple:

```text
/home/iabd/flume/data
```

És el directori local on el FileChannel desa dades temporals dels esdeveniments que encara han de ser lliurats al sink.

```text
Arriba event -> FileChannel/dataDir -> Sink -> Confirmació
```

Després de completar correctament l'operació, el canal pot marcar l'esdeveniment com a consumit i gestionar-ne la retirada de l'emmagatzematge.

## 14.2. `checkpointDir`

Exemple:

```text
/home/iabd/flume/checkpoint
```

Guarda **metadades i punts de control** que ajuden a reconstruir l'estat del canal quan es reinicia Flume.

Entre aquesta informació hi ha l'estat dels esdeveniments i les transaccions pendents.

## 14.3. Comparació

| `dataDir` | `checkpointDir` |
|---|---|
| Dades persistides pel FileChannel. | Metadades i punts de control. |
| Contribueix a conservar events pendents. | Contribueix a recuperar l'estat de la cua. |
| És una ruta del disc local. | També és una ruta del disc local. |
| No equival a la destinació final HDFS. | No equival a la destinació final HDFS. |

**Recordatori clau:** la ruta `hdfs.path` és **la destinació HDFS**, mentre que `dataDir` i `checkpointDir` pertanyen **al buffer local**.

---

# 15. Interceptors (pàgines 24–26)

## 15.1. Què és un interceptor?

És un component que actua sobre els esdeveniments **entre la source i el channel**, abans que es desin al canal.

Permet:

- **Enriquir** capçaleres amb informació extra.
- **Modificar** determinades dades o metadades.
- **Filtrar** missatges i descartar els que no interessen.

```text
Source ---> [Interceptor(s)] ---> Channel ---> Sink
                |
                +-- afegeix timestamp
                +-- afegeix IP
                +-- filtra per regex
```

## 15.2. Timestamp Interceptor

Afegeix informació temporal als headers de l'event.

Configuració del dossier per a `MultiAgent`:

```properties
MultiAgent.sources.Netcat.interceptors = tsInterceptor hostInterceptor

MultiAgent.sources.Netcat.interceptors.tsInterceptor.type = timestamp
```

El nom `tsInterceptor` és una **etiqueta definida per nosaltres**; el que determina el tipus és `type = timestamp`.

## 15.3. Host Interceptor

Permet incorporar l'adreça del host d'origen a la capçalera:

```properties
MultiAgent.sources.Netcat.interceptors.hostInterceptor.type = host
MultiAgent.sources.Netcat.interceptors.hostInterceptor.useIP = true
MultiAgent.sources.Netcat.interceptors.hostInterceptor.hostHeader = ip_origen
```

- `type = host`: interceptor de host.
- `useIP = true`: utilitza una IP.
- `hostHeader = ip_origen`: clau de capçalera on es desa la informació.

### Com queden junts?

```properties
# Llista d'interceptors associats a la font Netcat
MultiAgent.sources.Netcat.interceptors = tsInterceptor hostInterceptor

# Timestamp
MultiAgent.sources.Netcat.interceptors.tsInterceptor.type = timestamp

# Host
MultiAgent.sources.Netcat.interceptors.hostInterceptor.type = host
MultiAgent.sources.Netcat.interceptors.hostInterceptor.useIP = true
MultiAgent.sources.Netcat.interceptors.hostInterceptor.hostHeader = ip_origen
```

**Nota important:** per aplicar-los a `NetcatAvroAgent` en lloc de `MultiAgent`, s'ha de canviar el prefix de totes les línies.

## 15.4. Carpetes HDFS dinàmiques segons IP i data

El dossier proposa aprofitar aquestes metadades modificant el sink HDFS del consolidador:

```properties
AvroHdfsAgent.sinks.HdfsSink.hdfs.path = /user/iabd/flume/avro_data/%{ip_origen}/%Y-%m-%d/
AvroHdfsAgent.sinks.HdfsSink.hdfs.useLocalTimeStamp = true
```

Això permet organitzar les dades en carpetes que separen **IP i data**.

Exemple il·lustratiu:

```text
/user/iabd/flume/avro_data/
    192.168.1.15/
        2026-11-22/
            fitxer_dades
```

La IP i la data de l'exemple són il·lustratives.

**Matís:** `useLocalTimeStamp = true` fa servir l'hora local per a les expressions temporals del sink; si es vol aprofitar específicament el timestamp afegit a la capçalera, cal revisar aquesta opció i la configuració apropiada per a la versió de Flume. El PDF combina les dues idees en l'exemple.

## 15.5. Regex Filter Interceptor

Un **filtre amb expressió regular** determina quins missatges poden continuar pel pipeline.

Exemple del PDF: **descartar els events que continguin `TEST`**.

```properties
# Interceptor associat a la font Netcat
MultiAgent.sources.Netcat.interceptors = filterInterceptor

# Filtre regex
MultiAgent.sources.Netcat.interceptors.filterInterceptor.type = regex_filter
MultiAgent.sources.Netcat.interceptors.filterInterceptor.regex = .*TEST.*
MultiAgent.sources.Netcat.interceptors.filterInterceptor.excludeEvents = true
```

### Interpretació de la regex

```regex
.*TEST.*
```

- `.*` inicial: qualsevol seqüència de caràcters abans de `TEST`.
- `TEST`: text concret que es busca.
- `.*` final: qualsevol seqüència de caràcters després de `TEST`.
- `excludeEvents = true`: els events que coincideixen amb el patró s'exclouen.

| Missatge | Conté `TEST`? | Amb `excludeEvents = true` |
|---|---|---|
| `Hola` | No | Es conserva. |
| `Això és un TEST` | Sí | Es descarta. |
| `TEST inicial` | Sí | Es descarta. |
| `Producció correcta` | No | Es conserva. |

### Incoherència que convé tenir present

El text introductori del PDF esmenta altres possibles criteris, com missatges que continguin `OK` o no continguin `IGNORE`, però la **configuració final que realment mostra filtra `TEST`**. Per estudiar aquest exemple, pren com a referència la configuració concreta.

## 15.6. Interceptors encadenats

Es poden declarar múltiples interceptors en una única source, separant els noms amb espais:

```properties
MultiAgent.sources.Netcat.interceptors = tsInterceptor hostInterceptor
```

Quan treballen en cadena, l'event travessa successivament les transformacions definides. Un interceptor de filtratge pot descartar-lo abans que arribi al canal.

---

# 16. Comandes essencials

## 16.1. Linux i entorn

```bash
# Mostrar variable de l'entorn
echo "$FLUME_HOME"

# Canviar al directori base
cd "$FLUME_HOME"

# Llistar fitxers d'un directori
ls /home/iabd/

# Mostrar el contingut d'un fitxer
cat /home/iabd/dades/empleats.txt

# Crear carpeta local
mkdir -p /home/iabd/flume/spoolDir
```

## 16.2. Hadoop / HDFS

```bash
# Iniciar serveis de Hadoop segons l'entorn docent
start-all.sh

# Crear directori HDFS
hdfs dfs -mkdir -p /user/iabd/flume/seqgen_data

# Llistar fitxers HDFS
hdfs dfs -ls /user/iabd/flume/seqgen_data

# Mostrar un fitxer HDFS
hdfs dfs -cat /user/iabd/flume/seqgen_data/NOM_DEL_FITXER

# Eliminar un directori HDFS (destructiu)
hdfs dfs -rm -r /user/iabd/flume/seqgen_data
```

## 16.3. Executar un agent

```bash
flume-ng agent --conf conf/ --conf-file conf/agent.conf \
  --name NOM_AGENT \
  -Dflume.root.logger=INFO,console
```

Substitueix `NOM_AGENT` per l'agent definit dins del `.conf`.

## 16.4. Enviar esdeveniments amb Netcat

```bash
curl telnet://localhost:44444
```

Escriu una línia de text i prem **Enter**. L'agent haurà d'estar iniciat i escoltant al port corresponent.

## 16.5. Consultar HDFS al navegador

```text
http://master:9870/explorer.html#/user/iabd/flume/net_data
```

La disponibilitat de l'adreça depèn de la configuració i la resolució del nom `master` en la màquina docent.

---

# 17. Taula comparativa dels casos pràctics

| Pràctica | Source(s) | Channel(s) | Sink(s) | Resultat |
|---|---|---|---|---|
| Inicial | Exec | Memory | Logger | Sortida d'una ordre al log. |
| Cas 1a | Sequence Generator | Memory | HDFS | Nombres desats a HDFS. |
| Cas 1b | Netcat | File | HDFS | Missatges TCP desats a HDFS. |
| Cas 2, agent 1 | Netcat | File | Avro | Missatges enviats a un altre agent. |
| Cas 2, agent 2 | Avro | Memory | HDFS | Esdeveniments Avro persistits a HDFS. |
| Cas 3, MultiAgent | Netcat, Spooldir, Exec | File, Memory, Memory | Tres Avro | Tres fluxos cap al consolidador. |
| Cas 3, consolidador | Avro | Memory | HDFS | Fluxos unificats a HDFS. |

### Evolució pedagògica del dossier

**Pràctica inicial:** entendre els tres components.  
**Cas 1a:** canviar el destí a HDFS.  
**Cas 1b:** canviar la source a Netcat i el canal a fitxer.  
**Cas 2:** introduir diversos agents i Avro.  
**Cas 3:** afegir múltiples sources i consolidació.  
**Interceptors:** enriquir i filtrar els esdeveniments abans d'encuar-los.

---

# 18. Errors habituals i diagnòstic

Aquest apartat afegeix pautes de comprovació per treballar amb els exemples del PDF.

## 18.1. El nom de l'agent no coincideix

**Símptoma:** Flume no carrega els components previstos.

Comprova que:

```text
--name NetcatAgent
```

coincideixi amb:

```properties
NetcatAgent.sources = ...
NetcatAgent.channels = ...
NetcatAgent.sinks = ...
```

## 18.2. `channel` i `channels` intercanviats

**Símptoma:** la source o el sink no queda connectat.

Correcte:

```properties
Agent.sources.Font.channels = Canal
Agent.sinks.Desti.channel = Canal
```

## 18.3. La source Netcat no respon

Comprova:

1. Que l'agent està executant-se.
2. Que `bind` i `port` coincideixen amb l'adreça de connexió.
3. Que no hi ha un altre procés utilitzant el port `44444`.
4. Que s'està connectant des de la màquina adequada.

Ordre de prova:

```bash
curl telnet://localhost:44444
```

## 18.4. Avro no pot connectar

Comprova:

- Que **AvroHdfsAgent** s'ha arrencat primer.
- Que `AvroSink.hostname` apunta al host adequat.
- Que `AvroSink.port` i `AvroSource.port` coincideixen (`10003`).
- Que el receptor pot escoltar i acceptar connexions.

## 18.5. HDFS no rep dades

Comprova:

- Que HDFS està en marxa.
- Que la ruta `hdfs.path` és correcta.
- Que l'usuari té permisos.
- Que no hi ha missatges d'error al log de Flume.
- Que el fitxer no continua en estat temporal a l'espera de rotació.

Ordre útil:

```bash
hdfs dfs -ls /user/iabd/flume/avro_data
```

## 18.6. El FileChannel no pot iniciar-se

Verifica que les carpetes locals de `dataDir` i `checkpointDir` són vàlides, que hi ha espai disponible al disc i que l'usuari pot escriure-hi. No reutilitzis els mateixos directoris actius per a dos FileChannels independents: fes servir rutes diferenciades si han de funcionar simultàniament.

## 18.7. `Exec` no pot llegir `empleats.txt`

Revisa la discrepància:

```text
/home/iabd/das/empleats.txt
/home/iabd/dades/empleats.txt
```

Escull la ruta que realment existeix i assegura't que `cat` la pot llegir.

## 18.8. El fitxer `.conf` conté propietats incorrectes

A la pàgina 10–11, el dossier presenta una plantilla genèrica amb algunes **errades de nomenclatura**. La sintaxi que s'ha de seguir és:

```properties
Agent.sources.Source.propietat = valor
Agent.channels.Channel.propietat = valor
Agent.sinks.Sink.propietat = valor
```

No copiïs les formes genèriques errònies que fan servir `channel` en singular com a categoria o `sources` per configurar un sink.

---

# 19. Preguntes de repàs amb respostes

## Fonaments

**1. Què és Apache Flume?**  
Una eina per ingerir, transportar i canalitzar esdeveniments des de les fonts cap a les destinacions.

**2. Quin ús històric tenia?**  
Recollir logs de servidors web i desar-los a HDFS.

**3. Quins són els tres components principals?**  
Source, Channel i Sink.

**4. Quina és la funció del channel?**  
Actuar com a cua o buffer entre l'origen i el destí.

**5. Quina diferència hi ha entre un agent i un event?**  
Un agent és un conjunt de components que executa un flux; un event és la unitat individual de dades transportada.

**6. Què conté la capçalera d'un event?**  
Metadades clau–valor.

**7. Què conté el payload?**  
Les dades reals en forma de bytes.

**8. Per què una source usa `channels` i un sink usa `channel`?**  
Perquè una source pot publicar en més d'un canal, mentre que cada sink consumeix d'un canal.

**9. Dos sinks que consumeixen el mateix canal dupliquen tots els missatges?**  
No. Competeixen per consumir els events; això és diferent de replicar-los en dos canals.

**10. Què és el commit transaccional?**  
La confirmació que permet donar per consumida una operació després del lliurament correcte al destí.

## Components

**11. Què fa Exec Source?**  
Executa una ordre i ingereix la seva sortida.

**12. Què fa Netcat Source?**  
Escolta un port i converteix línies rebudes en events.

**13. Què fa Spooldir?**  
Vigila un directori i processa nous fitxers.

**14. Què fa LoggerSink?**  
Mostra els events al log.

**15. Què fa HdfsSink?**  
Escriu dades en HDFS.

**16. Què fa AvroSink?**  
Envia events a un receptor Avro.

**17. Què fa AvroSource?**  
Rep events enviats per un sink Avro.

**18. Quin canal és més ràpid en termes generals, Memory o File?**  
Memory Channel, perquè utilitza la RAM.

**19. Quin canal ofereix persistència local?**  
FileChannel.

**20. On es guarda el FileChannel?**  
En directoris del sistema de fitxers local, no en la destinació final HDFS.

## Configuració

**21. Per a què serveix `--name`?**  
Per indicar el nom de l'agent que s'ha de carregar.

**22. Per a què serveix `--conf-file`?**  
Per indicar el fitxer de configuració de l'agent.

**23. Què vol dir `capacity = 1000`?**  
Capacitat configurada de fins a 1.000 events al canal de memòria.

**24. Què vol dir `transactionCapacity = 100`?**  
Límit d'esdeveniments per transacció del canal.

**25. Quin port utilitza Netcat als exemples?**  
`44444`.

**26. Quin port utilitza Avro als exemples?**  
`10003`.

**27. Quina ordre permet veure arxius HDFS?**  
`hdfs dfs -ls RUTA`.

**28. Quina ordre permet llegir el contingut d'un fitxer HDFS?**  
`hdfs dfs -cat FITXER`.

**29. Què significa `rollCount`?**  
Nombre d'esdeveniments que pot desencadenar la rotació d'un fitxer HDFS.

**30. Què indica `rollInterval = 0`?**  
Que la rotació per interval temporal queda desactivada.

## Casos pràctics

**31. Què genera SeqGenAgent?**  
Una seqüència numèrica.

**32. On desa les dades SeqGenAgent?**  
A `/user/iabd/flume/seqgen_data/`.

**33. Quin canal utilitza NetcatAgent en el cas 1b?**  
FileChannel.

**34. Quants agents intervenen al cas 2?**  
Dos: `NetcatAvroAgent` i `AvroHdfsAgent`.

**35. Quin s'ha d'arrencar primer al cas 2?**  
`AvroHdfsAgent`, el receptor.

**36. Quines tres fonts s'utilitzen al cas 3?**  
Netcat, Spooldir i Exec.

**37. Per què hi ha tres AvroSinks al cas 3?**  
Perquè cadascun dels tres fluxos té el seu propi canal i sink, però tots envien cap al mateix receptor Avro.

**38. Què és la consolidació?**  
Reunir dades de diferents fonts en un flux o destí central.

**39. Quin és el destí final del cas 3?**  
HDFS mitjançant el sink de `AvroHdfsAgent`.

**40. Quina diferència hi ha entre multi-hop i multi-agent?**  
En el material, multi-hop destaca **l'encadenament d'etapes**, mentre que el cas multi-agent destaca **la consolidació de diversos orígens** en un receptor comú. Ambdues arquitectures utilitzen més d'un agent.

## Interceptors i recuperació

**41. On se situa un interceptor?**  
Entre la source i el channel.

**42. Per a què serveix TimestampInterceptor?**  
Per afegir una marca temporal als headers.

**43. Per a què serveix HostInterceptor?**  
Per afegir informació del host o IP d'origen.

**44. Què fa RegexFilter?**  
Conserva o exclou events segons un patró regular.

**45. Què fa `regex = .*TEST.*`?**  
Detecta línies que contenen `TEST`.

**46. Què implica `excludeEvents = true`?**  
Que els events coincidents es descarten.

**47. Per a què serveix `dataDir`?**  
Per desar dades persistides del FileChannel.

**48. Per a què serveix `checkpointDir`?**  
Per desar punts de control i metadades que ajuden a recuperar l'estat del canal.

**49. Per què es poden crear carpetes HDFS per IP i data?**  
Perquè els interceptors aporten metadades als headers i el sink pot utilitzar-les en la ruta HDFS.

**50. Què passa si no arrenca HDFS?**  
El sink no podrà persistir correctament al destí. Els missatges poden quedar pendents al canal fins que es restableixi, sempre dins dels límits de capacitat i durabilitat del canal configurat.

---

# 20. Resum final i glossari

## 20.1. Esquema global

```text
                    APACHE FLUME
                         |
                  Un o més AGENTS
                         |
           +-------------+-------------+
           |             |             |
         SOURCE ------> CHANNEL -----> SINK
           |             |             |
    rep / genera    emmagatzema     envia / desa
      events        temporalment      events
           |             |             |
    Netcat, Exec     Memory, File   Logger, HDFS,
    Spooldir, Avro                Avro, etc.
                         |
                      EVENT
                    /       \
                 Header     Body
               (metadades) (bytes)
```

## 20.2. Glossari essencial

| Terme | Definició breu |
|---|---|
| **Agent** | Unitat d'execució que conté els components d'un flux de Flume. |
| **Source** | Component d'entrada que rep o genera events. |
| **Channel** | Cua temporal d'esdeveniments. |
| **Sink** | Component que consumeix events i els transmet al destí. |
| **Event** | Unitat mínima de transport de dades a Flume. |
| **Header** | Metadades clau–valor de l'event. |
| **Payload / Body** | Dades de l'event en bytes. |
| **Ingesta** | Entrada de dades cap a un sistema. |
| **Streaming** | Flux continu de dades/esdeveniments. |
| **Buffer** | Emmagatzematge intermedi. |
| **Memory Channel** | Canal en memòria RAM. |
| **FileChannel** | Canal amb emmagatzematge local en disc. |
| **HDFS** | Sistema distribuït de fitxers de Hadoop. |
| **Avro** | Mecanisme de comunicació entre agents als casos del document. |
| **Netcat** | Font que rep línies de text per un port de xarxa. |
| **Spooldir** | Font que processa fitxers que arriben a un directori. |
| **Multi-hop** | Encadenament de diversos agents o etapes. |
| **Consolidació** | Agrupació de fluxos procedents d'orígens diferents. |
| **Commit** | Confirmació transaccional d'una operació. |
| **Checkpoint** | Punt de control per restaurar l'estat. |
| **Interceptor** | Component que modifica, enriqueix o filtra events abans del canal. |
| **Regex** | Expressió regular per identificar patrons de text. |
| **Rotació** | Tancament d'un fitxer i obertura d'un altre segons criteris configurats. |

## 20.3. Les 12 idees que més convé retenir

1. L'arquitectura de Flume és **Source → Channel → Sink**.
2. **Un agent** agrupa els components que executen un flux.
3. **Un event** conté **header** i **body**.
4. **Memory Channel** utilitza RAM; **FileChannel** utilitza disc local.
5. Una source es vincula amb **`.channels`**, un sink amb **`.channel`**.
6. **LoggerSink** mostra esdeveniments; **HdfsSink** els desa a HDFS.
7. **Seq Source** genera dades per a proves.
8. **Netcat Source** escolta al port `44444` en els casos del PDF.
9. Un **AvroSink** es connecta amb una **AvroSource** al port `10003` en els exemples.
10. En fluxos encadenats, convé **arrencar primer el receptor**.
11. **Spooldir** ingereix fitxers nous i **Exec** treballa amb la sortida d'una ordre.
12. Els **interceptors** permeten afegir timestamps, IP i aplicar filtres regex.

---

# 21. Referències i observacions sobre el material

**Font principal:** Francesc Barragán Pascual, *Flume*, M5075 BigData Aplicat, Institut Sa Palomera / Departament d'Educació i FP, revisió del **04/02/2026**, 26 pàgines.

**Enllaços recollits al dossier:**

- Projecte Apache Flume: https://flume.apache.org/
- Guia d'usuari d'Apache Flume: disponible des del lloc oficial.
- Interceptors: https://data-flair.training/blogs/flume-interceptors/

**Precisió sobre el contingut:** els valors, els noms dels agents, els ports, les configuracions i els fluxos principals s'han extret del PDF. Els diagrames ASCII, algunes comprovacions operatives i les preguntes de repàs s'han redactat per facilitar l'estudi. No s'ha fet cap verificació externa de les versions o de l'estat actual dels projectes.

**Diferències o errades detectades al mateix document:**

- La ruta del fitxer `empleats.txt` apareix com a `/home/iabd/das/...` en una configuració i com a `/home/iabd/dades/...` en la preparació.
- La plantilla genèrica de propietats de les pàgines 10–11 presenta errades de prefix; als apunts s'utilitza la forma coherent `sources`, `channels` i `sinks`.
- El text de filtratge esmenta exemples amb `OK` o `IGNORE`, però el codi definitiu fa servir el patró `TEST`.
- Hi ha variacions tipogràfiques en els noms dels fitxers d'exemple (`cas1a` / `caso1a`); en una execució real s'ha de consultar el nom que efectivament generi HDFS.

---

**Final dels apunts — Apache Flume · M5075 Big Data Aplicat**
