# Apache Hadoop HDFS — Apunts extensos i guia d'administració

> **M5075 · Big Data Aplicat · NF1**  
> **Documents de base:** *M5075_NF1_1_DOC01_HDFS* (26 pàgines; revisió 29/01/2026) i *M5075_NF1_1_DOC02_Comandes bàsiques administració HDFS* (2 pàgines).  
> **Objectiu:** entendre l'arquitectura i el funcionament d'HDFS i saber utilitzar i interpretar les comandes del temari.  
> **Convenció:** els apartats «Ampliació» afegeixen explicacions didàctiques; els apartats «Nota de revisió» identifiquen detalls dels documents que cal comprovar abans de copiar-los a la pràctica.

---

## Índex

1. Què és HDFS i per a què serveix
2. Arquitectura i components: NameNode, DataNode i Secondary NameNode
3. Comandes i sistemes de fitxers: `hdfs dfs` i `hadoop fs`
4. Rutes, permisos i operacions bàsiques
5. Metadades, FsImage, EditLog i checkpoints
6. Blocs, mida i replicació
7. Procés de lectura detallat
8. Procés d'escriptura detallat
9. Integritat, errors i recuperació
10. Administració del clúster i diagnòstic
11. Instantànies o snapshots
12. Interfície web HDFS i permisos
13. Accés a HDFS des de Python
14. Hue i altres interfícies
15. Guia completa de comandes, per categories
16. Pràctica guiada: administració bàsica
17. Pràctica guiada: blocs i FSCK
18. Pràctica guiada: snapshots i recuperació
19. Errors habituals, bones pràctiques i precaucions
20. Comparatives per memoritzar
21. Glossari
22. Preguntes d'autoavaluació amb resposta
23. Exercicis pràctics resolts
24. Checklist d'estudi i resum exprés

---

## 1. Què és HDFS i per a què serveix

**HDFS** (*Hadoop Distributed File System*) és el sistema de fitxers distribuït de l'ecosistema Apache Hadoop. La seva finalitat és emmagatzemar fitxers grans en diversos equips d'un clúster i fer que l'usuari els pugui gestionar com si formessin un sistema de fitxers únic. Un fitxer lògic pot estar físicament repartit en diversos **blocs** guardats en diferents **DataNodes**.

### Idees clau

- **Distribuït:** l'emmagatzematge físic no és en un únic disc; els blocs es distribueixen entre equips.
- **Escalable:** podem ampliar capacitat afegint DataNodes.
- **Tolerant a fallades:** la replicació permet conservar l'accés a les dades si falla un node, sempre que quedin còpies vàlides.
- **Orientat a grans volums:** és molt adequat per a fitxers grans i lectures seqüencials.
- **Model de dades predominant:** *write once, read many*; no està pensat per modificar arbitràriament bytes del mig d'un fitxer.
- **Separació de responsabilitats:** el NameNode gestiona metadades i els DataNodes emmagatzemen dades reals.

**Exemple conceptual:** un CSV de diversos centenars de megabytes es fragmenta en blocs. El NameNode registra quin fitxer correspon a quins blocs i on es troben; els DataNodes emmagatzemen els bytes de cada bloc. El client consulta al NameNode per saber on llegir, però llegeix les dades directament dels DataNodes.

### Quan no és la millor opció?

No és adequat quan una aplicació necessita latències molt baixes, milions de fitxers minúsculs, múltiples escriptors simultanis sobre el mateix fitxer o modificacions freqüents de registres individuals. Per a accés a registres i altres patrons, l'ecosistema disposa de tecnologies com HBase; per a consultes analítiques, Hive i altres motors.

### Esquema general

```text
                       CONSULTES DE METADADES
 Client ────────────────────────► NameNode
    │                                 │
    │                                 └── Metadades:
    │                                      fitxers, rutes, blocs,
    │                                      permisos, ubicacions
    │
    ├──────── lectura/escriptura ──────► DataNode A
    ├──────── lectura/escriptura ──────► DataNode B
    └──────── lectura/escriptura ──────► DataNode C
                                          (blocs i rèpliques)
```

**Important per a l'examen:** el **NameNode no transmet les dades dels fitxers** al client. Li facilita les ubicacions dels blocs i gestiona el sistema de fitxers.

---

## 2. Arquitectura i components

### 2.1 NameNode

És el servei que administra l'**espai de noms** (*namespace*) d'HDFS. Aquest espai inclou l'arbre de directoris, fitxers, propietaris, grups, permisos, identificadors de blocs i informació sobre la localització de les rèpliques. Les metadades actives es mantenen en memòria per accelerar l'accés, i hi ha mecanismes de persistència en disc.

**Tasques principals:**

1. Rebre peticions del client per obrir, crear, canviar el nom o eliminar fitxers.
2. Comprovar permisos i existència de rutes.
3. Informar de quins DataNodes tenen les rèpliques d'un bloc.
4. Seguir l'estat dels DataNodes i dels blocs a partir dels seus informes.
5. Coordinar el factor de replicació i la recuperació de blocs davant de fallades.

El NameNode és crític. En un desplegament senzill pot haver-hi un únic NameNode actiu i, si falla, el servei HDFS deixa d'estar disponible fins que es recupera. **Ampliació:** en desplegaments de producció es pot configurar *High Availability* amb NameNodes actiu i en espera; per això la formulació «només n'hi ha un» dels apunts és pròpia de l'arquitectura simplificada que s'estudia.

### 2.2 DataNode

Els DataNodes són els serveis que guarden i serveixen els **blocs reals**. Cada DataNode pot utilitzar diversos discos o directoris físics.

Funcions:

- Escriure blocs que envia un client o un altre DataNode.
- Llegir blocs i enviar-los directament al client.
- Mantenir i verificar sumes de comprovació (*checksums*).
- Informar periòdicament el NameNode que està operatiu (*heartbeat*).
- Enviar informes de blocs (*block reports*), que permeten identificar quines rèpliques té.
- Participar en la replicació quan HDFS ho requereix.

### 2.3 Secondary NameNode

El nom és enganyós: **no és un NameNode secundari que substitueix automàticament el principal**. El seu paper tradicional és ajudar a fer **checkpoints** de les metadades, combinant la imatge del sistema de fitxers amb les modificacions acumulades.

No s'ha de confondre una **snapshot HDFS d'un directori** amb el **checkpoint de metadades** que es realitza per al NameNode: tenen objectius diferents.

### 2.4 Comparativa

| Component | Funció principal | Què gestiona? | Té dades dels fitxers? |
|---|---|---|---|
| NameNode | Control del sistema de fitxers | Rutes, permisos, metadades i blocs | No, no en serveix el contingut |
| DataNode | Emmagatzematge i transferència | Blocs, rèpliques, checksums | Sí |
| Secondary NameNode | Checkpoints | Imatge i canvis de metadades | No |
| Client HDFS | Operar amb els fitxers | Peticions a NameNode i connexions amb DataNodes | Llegeix/escriu directament |

---

## 3. `hdfs dfs`, `hadoop fs` i sistemes de fitxers

El PDF diferencia dues famílies de comandes:

- `hdfs dfs`: shell del sistema de fitxers HDFS.
- `hadoop fs`: shell genèric que pot treballar amb diferents sistemes de fitxers segons la URI i la configuració, incloent HDFS i altres connectors.

```bash
hdfs dfs -ls /
hadoop fs -ls /
```

En un entorn on `fs.defaultFS` apunta a HDFS, les dues instruccions poden consultar el mateix sistema distribuït.

### `core-site.xml` i `fs.defaultFS`

El document mostra una configuració de l'estil:

```xml
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://hadoopsrv:9000</value>
</property>
```

La clau `fs.defaultFS` estableix el sistema de fitxers per defecte. El nom del servidor i el port **depenen del teu entorn**: a les pràctiques del curs apareixen noms com `hadoopsrv`, `iabd-virtualbox` o `master`.

**Nota:** `hadoop dfs` és una sintaxi històrica; per a les pràctiques del material es fa servir `hdfs dfs`.

### Distingir Linux local i HDFS

```bash
ls /home/hadoop                   # Fitxers del Linux local
hdfs dfs -ls /user/hadoop         # Fitxers dins d'HDFS
pwd                               # Directori actual de Linux
hdfs dfs -ls /                    # Arrel d'HDFS
```

Encara que totes dues estructures utilitzin rutes amb `/`, **no són el mateix sistema**. Una ruta `/user/hadoop/dades` dins d'HDFS no equival a `/user/hadoop/dades` del disc local.

---

## 4. Rutes, permisos i operacions bàsiques

### 4.1 Crear un directori

```bash
hdfs dfs -mkdir -p /user/iabd/dades
```

`-mkdir` crea una carpeta i `-p` permet crear directoris pare inexistents. Sense `-p`, si el pare no existeix, apareixerà un error.

### 4.2 Pujar un fitxer

```bash
hdfs dfs -put textos/exemple.txt /user/iabd/dades/
```

L'origen és un fitxer local i la destinació és una ruta HDFS. `-copyFromLocal` també s'utilitza per a aquesta operació.

Per donar un altre nom al fitxer dins d'HDFS:

```bash
hdfs dfs -put exemple.txt /user/iabd/dades/exempleNomNou.txt
```

### 4.3 Llistar i comptar

```bash
hdfs dfs -ls /user/iabd/dades
hdfs dfs -count /user/iabd/dades
hdfs dfs -du -h /user/iabd/dades
```

`-ls` mostra entrades del directori; `-count` resumeix nombre de directoris, fitxers i volum; `-du -h` ajuda a estudiar l'espai que ocupen els fitxers.

### 4.4 Llegir

```bash
hdfs dfs -cat /user/iabd/dades/exemple.txt
hdfs dfs -head /user/iabd/dades/exemple.txt
hdfs dfs -tail /user/iabd/dades/exemple.txt
```

`cat` presenta el contingut del fitxer; `head` permet consultar-ne el començament; `tail`, el final. Per a formats codificats o comprimits, `-text` pot ser útil quan el format és reconegut.

### 4.5 Baixar

```bash
hdfs dfs -get /user/iabd/dades/exemple.txt /tmp/
hdfs dfs -copyToLocal /user/iabd/dades/exemple.txt /tmp/
```

Per a una còpia amb informació de checksum CRC local:

```bash
hdfs dfs -get -crc /user/iabd/dades/exemple.txt ./exemple.txt
```

### 4.6 Canviar el nom, moure, copiar i esborrar

```bash
hdfs dfs -mv /user/iabd/dades/exemple.txt /user/iabd/dades/exemple2.txt
hdfs dfs -cp /user/iabd/dades/exemple2.txt /user/iabd/copia.txt
hdfs dfs -rm /user/iabd/dades/exemple2.txt
hdfs dfs -rm -r /user/iabd/dades
```

**Atenció:** `-rm -r` elimina recursivament el directori i tot el seu contingut. Revisa sempre la ruta abans d'executar-lo.

### 4.7 Permisos

HDFS utilitza conceptes de propietari, grup i permisos d'estil POSIX:

```bash
hdfs dfs -ls /user/iabd
hdfs dfs -chmod 750 /user/iabd/dades
hdfs dfs -chown iabd:supergroup /user/iabd/dades
```

La primera posició numèrica és per al propietari, la segona per al grup i la tercera per a altres usuaris. `7 = rwx`, `5 = r-x`, `0 = ---`.

**Ampliació:** a més de permisos bàsics, HDFS pot utilitzar ACLs. No totes les operacions ni els permisos es comporten exactament com els del sistema Linux local.

---

## 5. Metadades: FsImage, EditLog i checkpoints

El PDF explica com el NameNode manté l'estat del sistema de fitxers mitjançant fitxers de metadades dins de la ruta que tingui configurada, per exemple a `hdfs-site.xml`.

### 5.1 FsImage

La **FsImage** és una representació persistent de l'estat de l'espai de noms d'HDFS en un moment determinat. No conté el contingut de tots els fitxers; conté informació administrativa sobre l'estructura del sistema.

### 5.2 EditLog

L'**EditLog** registra modificacions posteriors: altes, baixes, canvis de nom, permisos i altres operacions del namespace.

### 5.3 Recuperació del NameNode

Quan es posa en marxa, la informació persistent permet reconstruir l'estat conegut del sistema de fitxers:

```text
                FsImage (estat persistent)
                           +
                EditLog (canvis posteriors)
                           ↓
              Estat actual del namespace
                           ↓
                   NameNode operatiu
```

Els checkpoints serveixen per evitar que els registres de modificacions creixin indefinidament i facilitin la reconstrucció de l'estat.

### 5.4 Fitxers habituals

Al document es descriuen prefixos similars a:

- `fsimage_...`: imatges de metadades.
- `edits_...`: registres de canvis tancats.
- `edits_inprogress_...`: segment d'edicions actiu.

**Nota de revisió:** el PDF presenta també formes com `fsimagen` i una clau antiga `dfs.name.dir`. En configuracions recents és habitual trobar `dfs.namenode.name.dir`. Consulta el `hdfs-site.xml` real i no copiïs rutes a cegues.

**Molt important:** mai no eliminis ni modifiquis manualment fitxers `fsimage`, `edits` o blocs físics d'un NameNode/DataNode en producció. Per inspeccionar metadades, utilitza eines administratives, no un editor binari.

---

## 6. Blocs, mida i replicació

### 6.1 Què és un bloc?

És la unitat lògica en què HDFS organitza l'emmagatzematge d'un fitxer. El material utilitza **128 MiB** com a mida típica de bloc:

```text
128 MiB = 128 × 1024 × 1024 = 134.217.728 bytes
```

Si el fitxer supera aquesta mida, es divideix en més d'un bloc. Un fitxer petit ocupa igualment una unitat lògica de bloc, però no reserva necessàriament físicament tots els 128 MiB.

### 6.2 Exemple del PDF: `ratings.csv`

El fitxer té **678.260.987 bytes** i la sortida de `fsck` del document indica **6 blocs** amb factor de replicació **1**. Els cinc primers tenen 134.217.728 bytes i l'últim és més petit, aproximadament 7,17 milions de bytes.

```bash
hdfs dfs -mkdir -p /user/hadoop/prova-hdfs
hdfs dfs -put ./ml-25m/ratings.csv /user/hadoop/prova-hdfs
hdfs fsck /user/hadoop/prova-hdfs -files -blocks
```

El document mostra com relacionar els identificadors de blocs de `fsck` amb els directoris físics del DataNode. Aquesta inspecció és diagnòstica: **no s'han de moure ni editar manualment** els fitxers `blk_...`.

### 6.3 Replicació

El factor de replicació indica el nombre de còpies de cadascun dels blocs. El valor habitual en un clúster distribuït és 3, mentre que al sistema de prova amb un únic DataNode sovint s'utilitza 1.

| Factor | Interpretació | Conseqüència |
|---|---|---|
| 1 | Una còpia de cada bloc | Sense redundància de rèpliques |
| 2 | Dues còpies | Major tolerància a fallades, més espai |
| 3 | Tres còpies | Redundància superior, encara més espai |

**Exemple:** un fitxer de 600 MiB necessita 5 blocs lògics si la mida és 128 MiB. Amb replicació 3, hi haurà fins a 15 rèpliques físiques de blocs repartides pel clúster. L'espai real aproximat és tres vegades la mida de les dades, sense comptar metadades i altres despeses.

### 6.4 Replicació i racks

En desplegaments grans, Hadoop té en compte la topologia de xarxa i la disposició en **racks** per distribuir rèpliques. Així no totes les còpies han de dependre d'una única màquina ni del mateix armari.

---

## 7. Procés de lectura detallat

El PDF descriu les etapes de lectura d'un fitxer HDFS. És una de les parts fonamentals del tema.

1. El client demana **obrir** el fitxer (`open()`).
2. El `DistributedFileSystem` consulta el NameNode per RPC.
3. El NameNode respon amb els blocs del fitxer i les ubicacions dels DataNodes que en tenen còpies.
4. El client obté un `FSDataInputStream` i llegeix directament del DataNode més adient o més proper.
5. En acabar un bloc, el flux continua amb un DataNode apropiat per al següent bloc, sense que el programa hagi de gestionar manualment els fragments.
6. En finalitzar, el client tanca el flux (`close()`).

```text
Client                     NameNode                      DataNodes
  | -- open(fitxer) --------> |                              |
  | <-- ubicacions blocs --- |                              |
  |                                                         |
  | ---------------- read(bloc 1) -------------------------> DN A
  | <---------------- dades -------------------------------- |
  | ---------------- read(bloc 2) -------------------------> DN B
  | <---------------- dades -------------------------------- |
  | -- close() --                                         
```

### Què passa si falla una lectura?

Si el DataNode no respon o el bloc falla una comprovació d'integritat, el client pot provar una altra rèplica i informar del problema. Aquesta és una de les raons per les quals HDFS guarda rèpliques i checksums.

**Pregunta típica d'examen:** les dades passen pel NameNode? **No.** El NameNode dona metadades i ubicacions, i el client es connecta directament als DataNodes.

**Ampliació:** el client pot beneficiar-se de la *localitat de dades*, i intentar prioritzar una rèplica propera per reduir latència i trànsit de xarxa.

---

## 8. Procés d'escriptura detallat

El procés d'escriptura funciona amb un **pipeline** de DataNodes. Segons el PDF:

1. El client crida `create()` al `DistributedFileSystem`.
2. Es consulta el NameNode, que verifica permisos i que la ruta es pot crear.
3. El client rep un `FSDataOutputStream`.
4. El NameNode facilita els DataNodes candidats per a les rèpliques del bloc.
5. El client envia paquets al primer DataNode; aquest desa i reenvia al segon, i successivament als altres del pipeline.
6. Les confirmacions (*acknowledgements*, ACK) tornen quan s'han processat els paquets.
7. En tancar el flux (`close()`), es buiden els paquets pendents, es confirmen i es finalitza l'operació de creació.

```text
Client ── create ──► NameNode
   │                  │
   │ ◄── autorització i nodes
   │
   └── paquets ──► DataNode A ──► DataNode B ──► DataNode C
                      │               │               │
                      └──────── ACK ◄─┴──────── ACK ◄─┘
```

En un clúster d'una única màquina i replicació 1 només cal una rèplica. En un clúster amb replicació 3, tres DataNodes participen en el pipeline d'aquest bloc.

### Lectura vs escriptura

| Característica | Lectura | Escriptura |
|---|---|---|
| Primera petició | `open()` | `create()` |
| Comunicació amb NameNode | Localització de blocs | Validació i destinacions |
| Flux | `FSDataInputStream` | `FSDataOutputStream` |
| Transferència principal | DataNode → client | Client → DataNode(s) |
| Protecció | Rèpliques, checksum | Pipeline, rèpliques i ACK |
| Finalització | `close()` | `close()` i confirmació final |

---

## 9. Integritat i recuperació

HDFS protegeix la disponibilitat mitjançant **replicació**, i comprova la integritat amb **checksums**. Aquestes dues idees són diferents:

- **Replicació:** disposar de còpies addicionals si un node o un disc falla.
- **Checksum:** detectar que els bytes llegits no corresponen amb els esperats.

### CRC local quan baixem un fitxer

El document explica que es pot recuperar una còpia amb fitxer de checksum:

```bash
hdfs dfs -get -crc /user/iabd/dades/arxiu ./arxiuLocal
```

Això pot crear un fitxer auxiliar ocult `.arxiuLocal.crc` amb metadades de verificació. No confonguis un fitxer CRC local amb el resultat de `hdfs dfs -checksum`, que consulta la suma de comprovació d'un fitxer a HDFS.

### Si un DataNode desapareix

El NameNode detecta absència de comunicació i reavalua la disponibilitat dels blocs. Si hi ha una còpia vàlida i nodes amb capacitat, el sistema pot restaurar la replicació necessària. Amb factor 1 i un únic DataNode, la caiguda del node deixa les dades inaccessibles mentre no es recuperi.

### Ordres de diagnòstic

```bash
hdfs dfsadmin -report
hdfs fsck /user/hadoop/prova-hdfs -files -blocks -locations
hdfs dfs -checksum /user/hadoop/prova-hdfs/ratings.csv
```

---

## 10. Administració del clúster i diagnòstic

El PDF recull diverses ordres essencials per administrar HDFS:

```bash
hdfs dfsadmin -report
hdfs fsck /
hdfs dfsadmin -printTopology
hdfs dfsadmin -listOpenFiles
hdfs dfsadmin -safemode enter
hdfs dfsadmin -safemode leave
```

### `dfsadmin -report`

Mostra informació general del clúster: capacitat, ús, nodes vius i morts, recursos i altres detalls. És una primera comprovació útil quan hi ha problemes d'emmagatzematge.

### `fsck`

Realitza una comprovació de la salut del sistema de fitxers o d'una ruta. Amb `-files -blocks` permet revisar arxius i blocs. Interpreta especialment:

- `HEALTHY`: la comprovació no ha detectat corrupció sota la ruta.
- `Missing blocks`: blocs sense rèpliques accessibles.
- `Corrupt blocks`: blocs detectats com a corruptes.
- `Under-replicated`: blocs amb menys rèpliques que les sol·licitades.

### `-printTopology`

Mostra la topologia de nodes/racks, útil per estudiar distribució i resiliència.

### Mode segur (*safe mode*)

```bash
hdfs dfsadmin -safemode enter
hdfs dfsadmin -safemode get
hdfs dfsadmin -safemode leave
```

És un estat de NameNode en què es restringeixen canvis sobre el sistema de fitxers, útil durant determinades operacions de posada en marxa o manteniment. **No el facis servir per solucionar un error sense entendre'n el motiu.**

### Fitxers oberts

```bash
hdfs dfsadmin -listOpenFiles
```

Pot ajudar a identificar fitxers encara oberts per escriptura o altres situacions operatives.

---

## 11. Instantànies HDFS (*snapshots*)

Una snapshot captura l'estat d'un directori HDFS en un moment concret. Permet recuperar fitxers o versions lògiques anteriors sense haver de copiar inicialment tot el contingut del directori. El PDF en mostra un cicle complet.

### 11.1 Crear carpeta i habilitar snapshots

```bash
hdfs dfs -mkdir -p /user/hadoop/dades
hdfs dfsadmin -allowSnapshot /user/hadoop/dades
```

### 11.2 Pujar dades i crear la instantània

```bash
hdfs dfs -put tirantloblanc.txt /user/hadoop/dades/
hdfs dfs -createSnapshot /user/hadoop/dades snapshot1
```

La instantània serà accessible de forma lògica a:

```text
/user/hadoop/dades/.snapshot/snapshot1/
```

### 11.3 Simular una eliminació i recuperar

```bash
hdfs dfs -rm /user/hadoop/dades/tirantloblanc.txt
hdfs dfs -ls /user/hadoop/dades
hdfs dfs -cp \
  /user/hadoop/dades/.snapshot/snapshot1/tirantloblanc.txt \
  /user/hadoop/dades/tirantloblanc.txt
```

El resultat esperat és que el fitxer torni a existir a la ruta original.

### 11.4 Consultar i eliminar instantànies

```bash
hdfs lsSnapshottableDir
hdfs dfs -deleteSnapshot /user/hadoop/dades snapshot1
hdfs dfsadmin -disallowSnapshot /user/hadoop/dades
```

**Precaució:** en general cal eliminar prèviament les snapshots associades abans de deshabilitar-les. També poden conservar blocs que aparentment s'han esborrat del directori visible i, per això, mantenir espai ocupat.

### Snapshots no equivalen a còpia fora del clúster

**Ampliació:** una snapshot és una eina de recuperació lògica dins d'HDFS, però no substitueix una política de còpies de seguretat externes. Davant una pèrdua completa del clúster o un problema greu de metadades, no n'hi ha prou amb tenir snapshots al mateix sistema.

---

## 12. Interfície web HDFS i permisos

El material presenta la interfície del NameNode a:

```text
http://IP_SERVIDOR:9870/explorer.html#/
```

Des d'aquesta interfície podem visualitzar directoris i fitxers, consultar blocs, propietaris i altres dades del sistema.

### L'usuari `dr.who`

El PDF explica un error habitual: les operacions de la UI es poden associar a l'usuari estàtic `dr.who` i, si no té permisos, fallaran en crear, editar o eliminar fitxers.

La guia mostra com a exemple donar permisos globals a una carpeta de proves:

```bash
hdfs dfs -mkdir -p /user/hadoop/proves
hdfs dfs -chmod -R 777 /user/hadoop/proves
```

**Advertiment:** `777` concedeix lectura, escriptura i execució a tothom. És acceptable, com a màxim, en un laboratori aïllat i sense dades sensibles; no s'ha d'aplicar indiscriminadament en producció.

L'altre exemple modifica una propietat de `core-site.xml`:

```xml
<property>
    <name>hadoop.http.staticuser.user</name>
    <value>iabd</value>
</property>
```

**Ampliació:** aquesta configuració depèn del model de seguretat i només s'ha de considerar en un laboratori sense autenticació forta. No és un substitut d'una configuració correcta d'autenticació i autorització.

---

## 13. HDFS i Python

El PDF presenta **HdfsCLI** com una manera de treballar amb HDFS a través de Python, en concret fent servir `InsecureClient` en un entorn docent sense Kerberos.

### 13.1 Preparar entorn virtual

```bash
python3 --version
sudo apt update
sudo apt install python3-venv
python3 -m venv ~/hadoop_env
source ~/hadoop_env/bin/activate
pip install hdfs
```

**Nota de revisió:** la guia proposa `python3.12-venv`; aquest paquet concret només és adequat si la màquina utilitza Python 3.12. A Ubuntu 22.04 pot haver-hi una altra versió de Python per defecte, per això és preferible començar comprovant-la.

### 13.2 Connectar amb WebHDFS

```python
from hdfs import InsecureClient

HOST = 'iabd-virtualbox'
PORT = 9870
client = InsecureClient(f'http://{HOST}:{PORT}', user='hadoop')

print(client.list('/user/hadoop'))
```

La URL apunta al servei HTTP/WebHDFS, no al port RPC habitual de HDFS. El nom del host i l'usuari s'han d'adaptar al teu laboratori.

### 13.3 Llegir un fitxer

```python
ruta = '/user/hadoop/textos/tirantloblanc.txt'

with client.read(ruta, encoding='utf-8') as reader:
    text = reader.read()

print(text[:500])
```

El document llegeix el contingut en bytes i el presenta per pantalla; aquí hi afegim `encoding='utf-8'` perquè l'exemple sigui més senzill de treballar com a text.

### 13.4 Escriure dades

```python
csv = 'nom,cognoms\nJoan,Pou\nFrancesc,Barragan\n'
client.write('/user/hadoop/dades/dades.csv', data=csv, encoding='utf-8', overwrite=True)
```

**Nota de revisió:** al document original, l'exemple textual del CSV no separa de forma consistent tots els valors amb comes. En aquesta versió didàctica l'hem normalitzat i afegit salts de línia, per obtenir un CSV coherent.

### 13.5 Snakebite i altres llibreries

El PDF cita `snakebite-py3` i un exemple de `Client('iabd-virtualbox', 9000)` per llistar rutes i llegir fitxers. També indica que Snakebite ja no es manté i que no ofereix escriptura. És important recordar que **Snakebite i HdfsCLI no utilitzen necessàriament el mateix protocol ni port de connexió**.

```python
from snakebite.client import Client

sb_client = Client('iabd-virtualbox', 9000)
for entrada in sb_client.ls(['/user/hadoop']):
    print(entrada)
```

La guia també esmenta **mrjob** (MapReduce des de Python), **Pydoop** (API HDFS i MapReduce) i l'ús freqüent de **Pandas** quan les dades es consumeixen en formats analítics com Parquet o Avro.

---

## 14. Hue

**Hue (Hadoop User Experience)** és una interfície web per accedir i treballar amb serveis de l'ecosistema Hadoop sense fer totes les operacions des del terminal. Al document s'indica que ja es troba instal·lat a la màquina virtual de pràctiques.

### Arrencada segons el material

```bash
cd /opt/hue-4.10.0
./build/env/bin/hue runserver
```

El document també mostra una alternativa amb Docker:

```bash
docker run -it -p 8888:8888 gethue/hue:latest
```

**Nota:** si Hue està en local s'indica una URL de l'estil `http://IP_SERVIDOR:8000/`; si el contenidor publica `8888:8888`, el port d'accés de la màquina amfitriona serà 8888. No barregis els dos modes d'arrencada.

### Per a què és útil?

- Navegar per directoris i fitxers HDFS.
- Visualitzar o carregar fitxers.
- Fer consultes a Hive quan estigui integrat.
- Evitar errors de sintaxi en operacions senzilles.

**Recorda:** Hue és una interfície; no substitueix HDFS ni el NameNode.

---

## 15. Guia completa de comandes HDFS

Aquesta secció integra **totes les ordres del PDF de dues pàgines** i les ordres bàsiques que apareixen en la guia llarga. Les rutes entre `<...>` són marcadors, no les has d'escriure literalment.

### 15.1 Transferència de fitxers

| Comanda | Què fa | Exemple |
|---|---|---|
| `-put` | Copia local → HDFS | `hdfs dfs -put dades.csv /user/iabd/` |
| `-copyFromLocal` | Copia local → HDFS | `hdfs dfs -copyFromLocal dades.csv /user/iabd/` |
| `-moveFromLocal` | Mou local → HDFS | `hdfs dfs -moveFromLocal dades.csv /user/iabd/` |
| `-get` | Copia HDFS → local | `hdfs dfs -get /user/iabd/dades.csv ./` |
| `-copyToLocal` | Copia HDFS → local | `hdfs dfs -copyToLocal /user/iabd/dades.csv ./` |
| `-getmerge` | Uneix fitxers d'HDFS en un fitxer local | `hdfs dfs -getmerge /user/iabd/parts ./total.txt` |
| `-appendToFile` | Afegeix contingut local al final d'un fitxer HDFS | `hdfs dfs -appendToFile noves.txt /user/iabd/log.txt` |

**Diferència fonamental:** `-put` deixa intacte el fitxer local; `-moveFromLocal` té la finalitat de moure'l, no només copiar-lo. Comprova sempre que la transferència s'ha completat.

### 15.2 Visualització i navegació

| Comanda | Descripció |
|---|---|
| `hdfs dfs -ls /ruta` | Llista fitxers i carpetes |
| `hdfs dfs -cat /ruta/f` | Mostra el contingut d'un fitxer |
| `hdfs dfs -head /ruta/f` | Mostra el començament |
| `hdfs dfs -tail /ruta/f` | Mostra el final |
| `hdfs dfs -text /ruta/f` | Prova de mostrar contingut llegible de formats compatibles |
| `hdfs dfs -count /ruta` | Compta directoris, fitxers i espai |
| `hdfs dfs -find /ruta -name '*.csv'` | Cerca fitxers per expressió |
| `hdfs dfs -stat '%b - %F - %n - %r' /ruta/f` | Mostra propietats seleccionades |

El format `-stat` del PDF utilitza `%b` (mida del fitxer en bytes), `%F` (tipus), `%n` (nom) i `%r` (factor de replicació).

### 15.3 Espai, integritat i diagnòstic

```bash
hdfs dfs -df -h /
hdfs dfs -checksum /user/iabd/dades.csv
hdfs fsck /user/iabd
hdfs dfsadmin -report
hdfs dfsadmin -printTopology
```

- `-df -h`: capacitat/espai disponible del sistema de fitxers.
- `-checksum`: consulta checksum del fitxer HDFS.
- `fsck`: comprova l'estat dels fitxers/blocs.
- `-report`: informa del clúster i dels DataNodes.
- `-printTopology`: mostra organització de nodes i racks.

### 15.4 Snapshots

```bash
hdfs dfsadmin -allowSnapshot /user/iabd/dades
hdfs dfs -createSnapshot /user/iabd/dades s1
hdfs lsSnapshottableDir
hdfs dfs -deleteSnapshot /user/iabd/dades s1
hdfs dfsadmin -disallowSnapshot /user/iabd/dades
```

### 15.5 Administració de fitxers i espai de noms

```bash
hdfs dfs -mkdir -p /user/iabd/proves
hdfs dfs -cp /user/iabd/a.txt /user/iabd/b.txt
hdfs dfs -mv /user/iabd/b.txt /user/iabd/c.txt
hdfs dfs -rm /user/iabd/c.txt
hdfs dfs -rm -r /user/iabd/proves
```

### 15.6 Inspecció dels fitxers interns del NameNode

La fitxa de comandes del material indica:

```bash
hdfs oev -i /dades/namenode/current/edits_... -o ~/edits.txt
```

**Nota de revisió important:** `hdfs oev` és per visualitzar **EditLog**. Per inspeccionar **FsImage** es fa servir `hdfs oiv`, no `hdfs oev`.

```bash
# EditLog (exemple d'inspecció)
hdfs oev -i /ruta/namenode/current/edits_... -o /tmp/edits.xml

# FsImage (exemple conceptual)
hdfs oiv -i /ruta/namenode/current/fsimage_... -o /tmp/fsimage.xml
```

Les opcions i el processador de sortida poden variar segons la versió; revisa l'ajuda de `hdfs oev -help` i `hdfs oiv -help`. Fes-ho només en fitxers de metadades coneguts i evita editar la font original.

---

## 16. Pràctica guiada 1: administració bàsica

**Objectiu:** dominar les comandes de creació, transferència, consulta i eliminació de fitxers, sense modificar informació important.

```bash
# 1. Preparar un fitxer de prova al Linux local
printf 'primera línia\nsegona línia\n' > /tmp/hdfs_prova.txt

# 2. Crear directori a HDFS
hdfs dfs -mkdir -p /user/iabd/proves-hdfs

# 3. Pujar el fitxer
hdfs dfs -put /tmp/hdfs_prova.txt /user/iabd/proves-hdfs/

# 4. Consultar-lo
hdfs dfs -ls /user/iabd/proves-hdfs
hdfs dfs -cat /user/iabd/proves-hdfs/hdfs_prova.txt

# 5. Comprovar recompte
hdfs dfs -count /user/iabd/proves-hdfs

# 6. Baixar-lo a una altra ruta local
hdfs dfs -get /user/iabd/proves-hdfs/hdfs_prova.txt /tmp/hdfs_recuperat.txt

# 7. Verificar que el local és igual
cmp /tmp/hdfs_prova.txt /tmp/hdfs_recuperat.txt

# 8. Neteja, NOMÉS del directori de proves
hdfs dfs -rm -r /user/iabd/proves-hdfs
```

**Resultat esperat:** el fitxer s'ha pogut pujar, llegir, recuperar i comparar correctament. `cmp` no imprimeix res si els fitxers comparats són idèntics.

**Preguntes de comprensió:** Quina ruta era local? Quina ruta era HDFS? Què succeiria si `-put` apunta a un directori que no existeix? Què passa amb el fitxer local després de `-get`?

---

## 17. Pràctica guiada 2: blocs i FSCK

**Objectiu:** inspeccionar la fragmentació i l'estat d'un fitxer HDFS sense manipular físicament els blocs.

```bash
hdfs dfs -ls /user/hadoop/prova-hdfs
hdfs fsck /user/hadoop/prova-hdfs -files -blocks
hdfs dfs -stat '%b - %F - %n - %r' /user/hadoop/prova-hdfs/ratings.csv
hdfs dfsadmin -report
```

### Què has d'identificar?

1. **Mida** del fitxer.
2. **Nombre de blocs** del fitxer.
3. **Mida de cada bloc**, especialment de l'últim.
4. **Factor de replicació**.
5. **Estat de salut** del directori.
6. **Nombre de DataNodes** disponibles.

En l'exemple del PDF, el fitxer `ratings.csv` té 678.260.987 bytes, sis blocs, un DataNode i una rèplica per bloc. Un `fsck` amb `HEALTHY` mostra que el conjunt inspeccionat no presenta blocs corruptes ni absents segons aquella comprovació.

**Ampliació:** si el sistema té un sol DataNode, no és possible mantenir tres rèpliques independents en tres DataNodes. Això explica que la configuració d'un laboratori pseudo-distribuït acostumi a tenir `dfs.replication=1`.

---

## 18. Pràctica guiada 3: snapshots

**Objectiu:** comprovar que es pot recuperar un fitxer després d'eliminar-lo de la vista principal.

```bash
# Preparació local
printf 'versió original\n' > /tmp/snap_test.txt

# Preparació HDFS
hdfs dfs -mkdir -p /user/iabd/snap-lab
hdfs dfsadmin -allowSnapshot /user/iabd/snap-lab
hdfs dfs -put /tmp/snap_test.txt /user/iabd/snap-lab/

# Fer snapshot
hdfs dfs -createSnapshot /user/iabd/snap-lab abans_esborrat

# Esborrar el fitxer visible
hdfs dfs -rm /user/iabd/snap-lab/snap_test.txt

# Recuperar-lo des de la snapshot
hdfs dfs -cp \
  /user/iabd/snap-lab/.snapshot/abans_esborrat/snap_test.txt \
  /user/iabd/snap-lab/snap_test.txt

# Comprovar-lo
hdfs dfs -cat /user/iabd/snap-lab/snap_test.txt

# Netejar snapshot i configuració de prova
hdfs dfs -deleteSnapshot /user/iabd/snap-lab abans_esborrat
hdfs dfsadmin -disallowSnapshot /user/iabd/snap-lab
hdfs dfs -rm -r /user/iabd/snap-lab
```

**Resultat esperat:** després de la recuperació tornaràs a veure `versió original`.

---

## 19. Errors habituals i precaucions

### 19.1 `Permission denied`

**Possibles causes:** usuari incorrecte, directori HDFS sense permisos, propietari o grup diferents, o operació des de la UI amb un usuari genèric.

```bash
hdfs dfs -ls /user/iabd
hdfs dfs -ls /user/iabd/dades
```

**Solució recomanada:** corregir propietari, grup o permisos necessaris. Evita `chmod 777` com a solució universal.

### 19.2 `File exists`

Ja hi ha un fitxer amb la ruta triada. Pots canviar el nom o gestionar explícitament una substitució quan l'ordre la permeti. No eliminis el fitxer previ sense revisar si és valuós.

### 19.3 `No such file or directory`

Revisa l'ortografia, el sistema de fitxers i els directoris pare. És freqüent confondre `/home/hadoop` local amb `/user/hadoop` d'HDFS.

### 19.4 `Safe mode` actiu

Si HDFS està en mode segur, es poden bloquejar operacions d'escriptura. Comprova l'estat:

```bash
hdfs dfsadmin -safemode get
```

No forcis la sortida del mode segur si no coneixes el problema que l'ha provocat.

### 19.5 `Under-replicated blocks`

La replicació efectiva és inferior a la configurada. Pot ser degut a manca de DataNodes, espai o problemes de comunicació. Comprova `dfsadmin -report`, `fsck` i l'estat dels serveis.

### 19.6 HDFS no respon

Comprova que el NameNode està en marxa i que la resolució de noms és correcta:

```bash
jps
hdfs dfsadmin -report
```

La interfície web pot ser `http://localhost:9870` o `http://IP_SERVIDOR:9870`, segons el desplegament.

### 19.7 Problemes en Python

Un error de connexió amb `InsecureClient` pot provenir de WebHDFS desactivat, port incorrecte, usuari sense permisos o host no resoluble. Revisa la URL HTTP abans de culpar la llibreria.

### 19.8 Precaucions que has de recordar

- No editis fitxers interns del NameNode ni blocs físics dels DataNodes.
- No executis `hdfs namenode -format` en un clúster que conté dades que vols conservar.
- No utilitzis `hdfs dfs -rm -r` sobre rutes no verificades.
- No confonguis snapshot interna amb backup extern.
- No pressuposis que tots els exemples del PDF utilitzen el mateix hostname o la mateixa versió.

---

## 20. Comparatives imprescindibles

### `hdfs dfs` vs `hadoop fs`

| `hdfs dfs` | `hadoop fs` |
|---|---|
| Orientat a HDFS | Interfície genèrica de sistemes de fitxers |
| Molt utilitzat per a ordres HDFS | Pot operar sobre HDFS o altres sistemes compatibles |
| `hdfs dfs -ls /` | `hadoop fs -ls /` |

### `-put` vs `-get` vs `-getmerge`

| Operació | Direcció | Resultat |
|---|---|---|
| `-put` | Local → HDFS | Copia un fitxer cap a HDFS |
| `-get` | HDFS → local | Copia un fitxer o directori cap al sistema local |
| `-getmerge` | HDFS → local | Combina fitxers en un únic resultat local |

### FsImage vs EditLog vs Snapshot

| Concepte | Propòsit |
|---|---|
| FsImage | Estat persistent de metadades del NameNode |
| EditLog | Operacions que modifiquen les metadades |
| Checkpoint | Consolidar metadades per facilitar recuperació |
| Snapshot HDFS | Conservar una vista d'un directori en un moment |

### `fsck` vs `checksum`

`fsck` és una eina de diagnòstic de la salut de blocs i fitxers. `-checksum` és una consulta de suma de comprovació d'un fitxer específic. No són equivalents.

### `NameNode` vs `DataNode`

El NameNode sap **on** hi ha els blocs i **què** representen; el DataNode guarda i envia els **bytes** dels blocs.

---

## 21. Glossari

| Terme | Significat |
|---|---|
| HDFS | Sistema de fitxers distribuït de Hadoop |
| NameNode | Servei responsable de l'espai de noms i les metadades |
| DataNode | Servei que desa i serveix blocs de dades |
| Namespace | Arbre lògic de fitxers i directoris HDFS |
| Bloc | Fragment lògic d'un fitxer HDFS |
| Replicació | Còpies físiques addicionals d'un bloc |
| Rack | Agrupació física o lògica de nodes en la xarxa |
| FsImage | Imatge persistent de l'espai de noms |
| EditLog | Historial de canvis de metadades |
| Checkpoint | Consolidació de metadades |
| RPC | Crida a procediment remot |
| Checksum | Valor per detectar alteracions de dades |
| CRC | Família de comprovacions per redundància cíclica |
| Heartbeat | Senyal periòdic per anunciar que un node està actiu |
| Block report | Informe dels blocs emmagatzemats en un DataNode |
| Pipeline | Cadena de DataNodes per escriure rèpliques |
| ACK | Confirmació que s'ha processat una operació |
| Snapshot | Vista conservada d'un directori HDFS en un moment |
| Safe mode | Estat restrictiu del NameNode |
| WebHDFS | API HTTP per interactuar amb HDFS |
| HdfsCLI | Llibreria Python client d'HDFS/WebHDFS |
| Hue | Interfície web per a Hadoop i serveis associats |
| `fsck` | Eina de comprovació de consistència del sistema |
| `dfsadmin` | Comandes administratives HDFS |
| `oiv` | Visualitzador de FsImage |
| `oev` | Visualitzador d'EditLog |

---

## 22. Autoavaluació: 60 preguntes amb resposta

### Fonaments i arquitectura

1. **Què vol dir HDFS?** Hadoop Distributed File System.
2. **Quina funció té HDFS?** Emmagatzemar fitxers de manera distribuïda.
3. **Què és un NameNode?** El gestor de l'espai de noms i les metadades d'HDFS.
4. **Què és un DataNode?** Un servei que emmagatzema i serveix blocs.
5. **Les dades passen pel NameNode?** No, van entre client i DataNodes.
6. **Què conserva el NameNode sobre un fitxer?** Ruta, permisos i metadades dels blocs.
7. **Què és un heartbeat?** Senyal periòdic per indicar que un node segueix actiu.
8. **Què és un block report?** Informe dels blocs que té un DataNode.
9. **Què fa el Secondary NameNode?** Participa en els checkpoints de metadades.
10. **És un substitut automàtic del NameNode?** No.
11. **Què és el namespace?** L'arbre de directoris i fitxers lògics.
12. **Per què és crític el NameNode?** Perquè controla l'accés al sistema de fitxers.
13. **Què és un clúster?** Un conjunt de màquines que col·laboren.
14. **Què és un rack?** Una agrupació física o lògica de servidors.
15. **Què aporta la localitat de dades?** Redueix transferències innecessàries per xarxa.

### Blocs i integritat

16. **Quina mida de bloc s'utilitza als exemples?** 128 MiB.
17. **Quants bytes són 128 MiB?** 134.217.728 bytes.
18. **Què passa si un fitxer és més gran que un bloc?** Es divideix en diversos blocs.
19. **Un fitxer petit ocupa físicament 128 MiB?** No necessàriament; ocupa els bytes reals.
20. **Què és el factor de replicació?** Nombre de còpies dels blocs.
21. **Quin factor s'utilitza al laboratori d'un node?** 1.
22. **Quin factor és habitual en clústers distribuïts?** 3, segons el material.
23. **Què succeeix si falla un DataNode amb rèpliques disponibles?** Es pot continuar llegint des d'una altra rèplica.
24. **Què detecta un checksum?** Alteracions en el contingut.
25. **Què vol dir `HEALTHY` a fsck?** Que la ruta analitzada no presenta problemes detectats per aquella comprovació.
26. **Quants blocs tenia `ratings.csv` al PDF?** Sis.
27. **Quina mida tenia `ratings.csv` a l'exemple?** 678.260.987 bytes.
28. **Què vol dir `Under-replicated`?** Que falten còpies respecte del factor demanat.
29. **Què és un `blk_...`?** Un fitxer físic de dades de bloc.
30. **Es recomana editar manualment blocs físics?** No.

### Lectura, escriptura i metadades

31. **Quin mètode inicia la lectura?** `open()`.
32. **Quin mètode inicia una creació?** `create()`.
33. **Quin flux serveix per llegir?** `FSDataInputStream`.
34. **Quin flux serveix per escriure?** `FSDataOutputStream`.
35. **Què consulta el client abans de llegir?** Ubicacions de blocs al NameNode.
36. **Qui lliura els bytes del fitxer?** Els DataNodes.
37. **Què és el pipeline d'escriptura?** Cadena de DataNodes que rep i replica paquets.
38. **Què és un ACK?** Una confirmació de recepció/procés.
39. **Què és FsImage?** Imatge persistent de les metadades.
40. **Què és EditLog?** Registre de canvis en les metadades.
41. **Per a què serveix un checkpoint?** Per consolidar i facilitar la gestió de metadades.
42. **En què es diferencia una snapshot de FsImage?** La primera conserva una vista d'un directori; la segona descriu metadades del NameNode.

### Comandes i administració

43. **Com llistes l'arrel HDFS?** `hdfs dfs -ls /`.
44. **Com crees `/user/iabd/prova`?** `hdfs dfs -mkdir -p /user/iabd/prova`.
45. **Com puges un fitxer local?** `hdfs dfs -put fitxer /user/iabd/`.
46. **Com baixes un fitxer d'HDFS?** `hdfs dfs -get /user/iabd/fitxer ./`.
47. **Com llegeixes un fitxer HDFS?** `hdfs dfs -cat /ruta/fitxer`.
48. **Com mostres la part final?** `hdfs dfs -tail /ruta/fitxer`.
49. **Què fa `-getmerge`?** Reuneix fitxers HDFS en un de local.
50. **Què fa `-appendToFile`?** Afegeix dades al final d'un fitxer HDFS.
51. **Com obtens un report del clúster?** `hdfs dfsadmin -report`.
52. **Com comproves blocs i fitxers?** `hdfs fsck /ruta -files -blocks`.
53. **Com veus la topologia?** `hdfs dfsadmin -printTopology`.
54. **Com consultes l'espai lliure?** `hdfs dfs -df -h /`.
55. **Com consultes un checksum?** `hdfs dfs -checksum /ruta/fitxer`.
56. **Com habilites snapshots?** `hdfs dfsadmin -allowSnapshot /ruta`.
57. **Com en crees una?** `hdfs dfs -createSnapshot /ruta nom`.
58. **Com recuperes un fitxer de snapshot?** Amb `hdfs dfs -cp` des de `.snapshot/nom/...`.
59. **Quina eina llegeix EditLog?** `hdfs oev`.
60. **Quina eina llegeix FsImage?** `hdfs oiv`.

---

## 23. Exercicis pràctics resolts

### Exercici A. Pujar i recuperar un fitxer

**Enunciat:** crea `/user/iabd/examen`, puja `notes.txt`, visualitza'l i recupera'l a `/tmp`.

```bash
hdfs dfs -mkdir -p /user/iabd/examen
hdfs dfs -put notes.txt /user/iabd/examen/
hdfs dfs -cat /user/iabd/examen/notes.txt
hdfs dfs -get /user/iabd/examen/notes.txt /tmp/notes.txt
```

### Exercici B. Cercar CSV en un directori

```bash
hdfs dfs -find /user/iabd/dades -name '*.csv'
```

### Exercici C. Obtenir mida, tipus, nom i rèpliques

```bash
hdfs dfs -stat '%b - %F - %n - %r' /user/iabd/dades/clients.csv
```

### Exercici D. Unir les parts d'una sortida MapReduce

```bash
hdfs dfs -getmerge /user/iabd/resultats /tmp/resultat_total.txt
```

El resultat és un fitxer **local** amb la concatenació dels fitxers de la ruta HDFS. Revisa si al directori també hi ha fitxers auxiliars i si cal un ordre concret de concatenació.

### Exercici E. Comprovar que un directori està sa

```bash
hdfs fsck /user/iabd/dades -files -blocks
```

Cal revisar `Status`, blocs absents, corruptes i insuficientment replicats. Un directori existent no garanteix per si sol que els seus blocs siguin accessibles.

### Exercici F. Saber quins nodes hi ha

```bash
hdfs dfsadmin -report
hdfs dfsadmin -printTopology
```

La primera dona estat i capacitats; la segona mostra l'estructura de nodes i racks.

### Exercici G. Crear una snapshot i després eliminar-la

```bash
hdfs dfsadmin -allowSnapshot /user/iabd/dades
hdfs dfs -createSnapshot /user/iabd/dades examen
hdfs lsSnapshottableDir
hdfs dfs -deleteSnapshot /user/iabd/dades examen
hdfs dfsadmin -disallowSnapshot /user/iabd/dades
```

### Exercici H. Inspeccionar el final d'un log d'HDFS

```bash
hdfs dfs -tail /user/iabd/logs/app.log
```

No cal descarregar tot el fitxer per consultar-ne el final.

### Exercici I. Recuperar el diagnòstic de metadades

```bash
hdfs dfsadmin -safemode get
hdfs dfsadmin -listOpenFiles
```

La primera consulta detecta si el NameNode està en mode segur; la segona serveix per revisar fitxers oberts.

### Exercici J. Explicar per què un PDF diu que `dr.who` no pot escriure

L'usuari HTTP assignat per defecte no té permisos de creació a la ruta HDFS consultada. No és un error de sintaxi de `mkdir`, sinó de **propietari i autorització**. La solució és definir correctament la identitat d'usuari i els permisos d'accés, sense obrir tot HDFS a `777`.

---

## 24. Checklist final per preparar l'examen

- [ ] Puc explicar què és HDFS i per què treballa amb blocs.
- [ ] Puc distingir clarament NameNode, DataNode i Secondary NameNode.
- [ ] Sé per què el NameNode no participa en el trànsit de bytes.
- [ ] Sé què contenen `fsimage` i `edits`.
- [ ] Puc explicar la lectura amb `open()`, `FSDataInputStream` i rèpliques.
- [ ] Puc explicar l'escriptura amb `create()`, pipeline i ACK.
- [ ] Sé calcular el nombre de blocs d'un fitxer.
- [ ] Entenc què significa un factor de replicació 1 o 3.
- [ ] Distingeixo fitxers locals i fitxers HDFS.
- [ ] Domino `-put`, `-get`, `-ls`, `-cat`, `-mv`, `-rm` i `-getmerge`.
- [ ] Sé consultar `dfsadmin -report` i `fsck`.
- [ ] Puc interpretar `HEALTHY`, `Under-replicated` i `Missing blocks`.
- [ ] Sé activar, crear, recuperar i eliminar snapshots.
- [ ] Entenc les limitacions de la UI HDFS i dels permisos `dr.who`.
- [ ] Sé què és WebHDFS i per què HdfsCLI utilitza HTTP.
- [ ] Conec Hue i la diferència entre una interfície i el servei HDFS.
- [ ] Recordo que `hdfs oev` consulta EditLog i `hdfs oiv` FsImage.
- [ ] Identifico quines ordres poden esborrar dades i requereixen precaució.

### Resum exprés

**HDFS distribueix fitxers en blocs.** El **NameNode** controla les metadades i els **DataNodes** guarden els blocs. La lectura passa per una consulta inicial de metadades i després una connexió directa als DataNodes. L'escriptura utilitza un pipeline amb rèpliques i confirmacions. **FsImage + EditLog** permeten reconstruir l'estat administratiu del sistema; les **snapshots** serveixen per recuperar versions de directoris. Per operar des del terminal utilitzem `hdfs dfs`; per diagnosticar, `hdfs fsck` i `hdfs dfsadmin`; per accedir des de Python, WebHDFS i HdfsCLI; per treballar visualment, la UI del NameNode i Hue.

---

## Referències dels documents utilitzats

- **M5075_NF1_1_DOC01_HDFS.docx.pdf** — *Hadoop/HDFS*, Francesc Barragán Pascual, revisió 29/01/2026. Seccions: treballant amb HDFS, NameNodes/DataNodes, lectura, escriptura, blocs, administració, snapshots, HDFS UI, HDFS i Python, Hue.
- **M5075_NF1_1_DOC02_Comandes bàsiques administració HDFS.pdf** — fitxa de comandes de dues pàgines. Comandes de transferència, exploració, snapshots, diagnòstic i metadades.

**Criteri d'edició:** s'ha seguit l'estructura i el contingut dels dos PDFs. Les ampliacions explicatives, les notes de prudència, les comparatives i els exercicis addicionals són material didàctic complementari. Alguns exemples han estat normalitzats per coherència i s'han marcat les diferències importants respecte del text original.
