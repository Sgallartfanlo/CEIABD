# Apunts extensos — Instal·lació d'Apache Hadoop 3.4.3 a Ubuntu 22.04

## 1. Objectius i mapa general de la instal·lació

La guia planteja desplegar **Hadoop 3.4.3 sobre Ubuntu 22.04**, en una única màquina que simula un entorn distribuït. En acabar, aquesta màquina executarà diversos dimonis Java independents que ofereixen emmagatzematge distribuït (HDFS) i gestió de recursos (YARN).

### Resultats esperats

- Java funciona i es coneix la ruta `JAVA_HOME`.
- Existeix un usuari Linux `hadoop` amb el seu directori personal.
- L'usuari pot establir una sessió SSH a `localhost` sense introduir la seva contrasenya d'usuari.
- Hadoop es troba a `/usr/local/hadoop` i les variables d'entorn apunten al directori.
- HDFS té un **NameNode** i un **DataNode** en funcionament.
- YARN té un **ResourceManager** i un **NodeManager** en funcionament.
- Es poden obrir les interfícies web dels serveis i executar ordres de prova.

### Visió del sistema

```text
                     Ubuntu 22.04 (una màquina)
┌─────────────────────────────────────────────────────────┐
│ Java / JVM                                              │
│                                                         │
│ HDFS                            YARN                    │
│ ┌───────────────┐               ┌──────────────────┐   │
│ │ NameNode      │               │ ResourceManager  │   │
│ │ Metadades     │               │ Planificació     │   │
│ └───────┬───────┘               └────────┬─────────┘   │
│         │                                │             │
│ ┌───────▼───────┐               ┌────────▼─────────┐   │
│ │ DataNode      │               │ NodeManager       │   │
│ │ Blocs de dades│               │ Execució recursos │   │
│ └───────────────┘               └──────────────────┘   │
│                                                         │
│             MapReduce executa treballs amb YARN         │
└─────────────────────────────────────────────────────────┘
```

**Idea clau:** una màquina física no equival necessàriament a un únic procés. En el mode pseudodistribuït, diversos processos col·laboren com si fossin peces d'un clúster.

---

## 2. Què és Apache Hadoop?

**Apache Hadoop** és un conjunt de tecnologies de codi obert pensades per emmagatzemar i processar grans volums de dades amb recursos repartits entre màquines. La seva arquitectura permet dividir tasques i fitxers per treballar en paral·lel i créixer afegint nodes.

La guia destaca que Hadoop serveix tant per a dades estructurades com per a dades no estructurades. Dins d'un sistema Big Data, separa dues funcions essencials:

1. **Emmagatzemar:** HDFS distribueix el contingut dels fitxers.
2. **Processar:** MapReduce executa càlculs paral·lels i YARN distribueix els recursos computacionals.

**Exemple:** si disposem de registres de milions de visites web, HDFS pot guardar-los en diferents blocs i MapReduce pot comptar les visites en paral·lel. El nostre entorn de laboratori només té un node, però manté la mateixa divisió lògica de components.

### Conceptes vinculats

- **Clúster:** conjunt de nodes que actuen coordinadament.
- **Node:** ordinador o instància que participa en el sistema.
- **Dimoni (*daemon*):** procés que s'executa com a servei.
- **Escalabilitat horitzontal:** augmentar la capacitat incorporant nodes nous.
- **Tolerància a fallades:** continuar operant o recuperar dades davant incidències; en la nostra instal·lació amb una sola rèplica aquesta tolerància és limitada.

---

## 3. Els quatre components fonamentals

| Component | Funció | Recordatori |
|---|---|---|
| **Hadoop Common** | Biblioteques, utilitats i elements compartits | Base comuna |
| **HDFS** | Sistema de fitxers distribuït | Guarda dades |
| **YARN** | Administració i assignació de recursos del clúster | Decideix on executar |
| **MapReduce** | Model i motor de processament paral·lel | Processa dades |

### 3.1 Hadoop Common

Inclou les biblioteques i eines que utilitzen els altres components. Sense aquest conjunt comú, HDFS, MapReduce i YARN no compartirien les mateixes eines bàsiques d'execució i configuració.

### 3.2 HDFS

HDFS (*Hadoop Distributed File System*) distribueix l'emmagatzematge en blocs i gestiona on es troben. Els seus protagonistes són:

- **NameNode:** manté l'espai de noms i les metadades: carpetes, fitxers, permisos i ubicació dels blocs.
- **DataNode:** emmagatzema blocs físics i respon a les operacions de lectura/escriptura.

**No confonguis:** el NameNode no és, en general, el servidor que guarda tot el contingut dels fitxers; aquesta tasca correspon als DataNodes. En un únic ordinador hi conviuen els dos processos.

### 3.3 YARN

YARN (*Yet Another Resource Negotiator*) fa possible repartir recursos per executar aplicacions:

- **ResourceManager:** coordina els recursos del clúster i la planificació.
- **NodeManager:** gestiona els recursos i processos d'un node.

YARN no substitueix HDFS: **HDFS emmagatzema; YARN gestiona execució i recursos**.

### 3.4 MapReduce

Model basat en dividir una operació en fases:

```text
Dades d'entrada → MAP (transformacions) → SHUFFLE/SORT → REDUCE (agregacions)
```

**Ampliació:** algunes feines de MapReduce poden tenir zero reducers, depenent de la tasca. En aquest laboratori, la configuració `mapreduce.framework.name=yarn` permet executar les tasques amb YARN.

---

## 4. Modes de funcionament de Hadoop

| Mode | Nombre de màquines | Processos | Ús habitual |
|---|---:|---|---|
| **Local / Standalone** | 1 | Sense desplegament distribuït de dimonis HDFS/YARN | Desenvolupament i proves senzilles |
| **Pseudodistribuït** | 1 | Diversos dimonis Java separats | Aprenentatge i laboratori |
| **Totalment distribuït** | Diverses | Serveis repartits entre múltiples nodes | Entorns de clúster |

La **guia instal·la el mode pseudodistribuït**. És important memoritzar que no és sinònim de producció ni proporciona automàticament redundància física: un error del servidor pot afectar tots els components.

---

## 5. Requisits previs i planificació

### Segons la guia (p. 4)

- Ubuntu **22.04**.
- Nom de servidor d'exemple: `hadoop`.
- Adreça IP d'exemple: `192.168.56.104`.
- Usuari amb permisos `sudo`.
- Una instal·lació en una única màquina.

### Informació que convé comprovar abans de començar (ampliació)

```bash
lsb_release -a
hostname
hostname -I
whoami
id
ip -br addr
df -h
free -h
```

**Què revisa cada ordre?** `lsb_release -a` identifica Ubuntu; `hostname` mostra el nom del servidor; `hostname -I` informa de les adreces; `whoami` mostra l'usuari actiu; `id` indica grups i identificadors; `df -h` comprova disc; `free -h` mostra memòria RAM.

**Atenció:** `192.168.56.104` és una IP del document i **no** té per què ser la del teu ordinador. Cal substituir-la sempre que la xarxa sigui diferent. El nom `hadoop`, el nom `master` i `localhost` no són intercanviables si no resolen correctament al mateix servidor.

---

## 6. Instal·lació de Java/OpenJDK

### Per què cal Java?

Hadoop està escrit principalment en Java. Els dimonis i diverses eines s'executen sobre la JVM (*Java Virtual Machine*). Per això, Java és un requisit abans de configurar Hadoop.

### Segons la guia (p. 4–5)

```bash
sudo apt update
sudo apt install default-jdk
java -version
```

**Explicació:**

1. `sudo apt update` actualitza la informació disponible dels repositoris; no és el mateix que actualitzar tots els paquets instal·lats.
2. `sudo apt install default-jdk` instal·la el JDK per defecte del sistema configurat.
3. `java -version` mostra la versió que realment s'executarà quan invoquem Java.

La guia pretén treballar amb **OpenJDK 11** i mostra la ruta `/usr/lib/jvm/java-11-openjdk-amd64`.

### Precaució: no pressuposar la versió instal·lada

`default-jdk` no identifica per si mateix una versió fixa en totes les distribucions i repositoris. Per garantir que el laboratori segueix les indicacions del PDF, pots instal·lar explícitament el paquet si és disponible:

```bash
sudo apt install openjdk-11-jdk
java -version
```

Aquesta és una **ampliació pràctica**, no una substitució silenciosa del procediment original. Les compatibilitats exactes de Java poden dependre de la versió i la configuració de Hadoop.

### Localitzar el Java instal·lat

```bash
readlink -f "$(which java)"
```

Possible resultat:

```text
/usr/lib/jvm/java-11-openjdk-amd64/bin/java
```

La variable `JAVA_HOME` ha d'apuntar al directori pare del subdirectori `bin`, és a dir:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

**Pregunta d'examen:** què passarà si `JAVA_HOME` apunta a un directori que no existeix? Hadoop pot fallar en arrencar els seus serveis perquè no trobarà l'entorn Java esperat.

---

## 7. Creació de l'usuari Hadoop i autenticació SSH

### 7.1 Per què un usuari dedicat?

La guia utilitza `hadoop` com a usuari de Linux per executar els serveis i posseir els fitxers d'instal·lació. Separar aquest usuari de `root` redueix la necessitat d'executar processos amb privilegis administratius.

### 7.2 Instal·lar SSH i pdsh (p. 6)

```bash
sudo apt install openssh-server openssh-client pdsh
```

- **OpenSSH Server:** accepta connexions SSH entrants.
- **OpenSSH Client:** inicia connexions SSH.
- **pdsh:** eina per executar ordres en hosts en paral·lel; pot ser utilitzada per scripts d'administració.

### 7.3 Crear l'usuari (p. 7)

```bash
sudo useradd -m -s /bin/bash hadoop
sudo passwd hadoop
sudo usermod -aG sudo hadoop
su - hadoop
```

| Fragment | Funció |
|---|---|
| `useradd` | Crea un usuari |
| `-m` | Crea el directori personal |
| `-s /bin/bash` | Assigna Bash com a shell |
| `passwd` | Defineix la contrasenya |
| `usermod -aG sudo` | Afegeix l'usuari al grup sudo |
| `su - hadoop` | Canvia a l'usuari amb el seu entorn de sessió |

**Precaució:** el grup `sudo` no és imprescindible per al funcionament normal dels dimonis Hadoop. La guia l'afegeix per facilitar l'administració del laboratori; en producció s'han de limitar els privilegis.

### 7.4 Crear les claus SSH (p. 8)

```bash
ssh-keygen -t rsa
ls ~/.ssh/
```

El document utilitza RSA i indica prémer `Enter` sense configurar frase de pas per a les proves automatitzades. En una instal·lació actual es poden considerar alternatives més modernes, com Ed25519, segons la compatibilitat i la política de seguretat.

Fitxers habituals:

- `~/.ssh/id_rsa`: **clau privada**, no s'ha de compartir.
- `~/.ssh/id_rsa.pub`: **clau pública**, es pot autoritzar al servidor.

### 7.5 Autoritzar la clau i comprovar-ne els permisos (p. 9)

```bash
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
ssh localhost
```

El símbol `>>` **afegeix** contingut sense eliminar el que ja hi havia. La configuració `chmod 600` permet que el propietari llegeixi i escrigui l'arxiu, però no els altres usuaris.

**Ampliació recomanada:**

```bash
chmod 700 ~/.ssh
```

Els permisos restrictius sobre el directori `.ssh` poden evitar que OpenSSH rebutgi les claus.

**Resultat esperat:** en executar `ssh localhost`, pot demanar confirmació de la identitat de l'amfitrió la primera vegada, però **no** hauria de sol·licitar la contrasenya de l'usuari un cop autoritzada la clau.

### Diagnòstic d'SSH

```bash
sudo systemctl status ssh
ssh -v localhost
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

Si demana contrasenya, cal revisar que estiguis operant com a `hadoop`, que el servei SSH estigui actiu, que la clau autoritzada sigui la correcta i que els permisos siguin acceptables.

---

## 8. Descarregar i instal·lar Hadoop 3.4.3

### Segons la guia (p. 10–11)

```bash
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.4.3/hadoop-3.4.3.tar.gz
tar -xvzf hadoop-3.4.3.tar.gz
sudo mv hadoop-3.4.3 /usr/local/hadoop
sudo chown -R hadoop:hadoop /usr/local/hadoop
```

### Explicació detallada

1. **`wget`** descarrega el fitxer comprimit des de l'arxiu d'Apache.
2. **`tar -xvzf`** n'extreu el contingut: `x` extreure, `v` sortida detallada, `z` gestionar gzip, `f` indicar el fitxer.
3. **`sudo mv`** mou i reanomena el directori dins de `/usr/local/`.
4. **`chown -R`** estableix propietari i grup de manera recursiva.

L'estructura principal quedarà així:

```text
/usr/local/hadoop/
├── bin/                 # Executables Hadoop
├── sbin/                # Scripts d'inici i aturada
├── etc/hadoop/          # Configuracions
├── lib/                 # Biblioteques
├── share/               # Recursos i JARs
└── ...
```

### Verificacions útils (ampliació)

```bash
ls -ld /usr/local/hadoop
ls /usr/local/hadoop/bin
ls /usr/local/hadoop/etc/hadoop
```

**Precaució:** abans d'executar `mv`, comprova que la destinació no contingui una instal·lació que vulguis conservar. No la sobreescriguis inadvertidament.

### Verificació d'integritat (ampliació)

En entorns administrats és bona pràctica comparar la suma SHA-512 de l'arxiu descarregat amb la publicada per Apache per detectar descàrregues corruptes o manipulades. La guia no desenvolupa aquest pas.

---

## 9. Variables d'entorn d'Hadoop

### 9.1 Editar `~/.bashrc` (p. 12)

Amb la sessió de l'usuari `hadoop`:

```bash
nano ~/.bashrc
```

Afegir el bloc de la guia:

```bash
# Variables d'entorn d'Hadoop
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```

### 9.2 Què significa cada variable?

| Variable | Significat |
|---|---|
| `JAVA_HOME` | Ruta del JDK |
| `HADOOP_HOME` | Directori principal d'Hadoop |
| `HADOOP_INSTALL` | Ruta utilitzada per alguns scripts |
| `HADOOP_MAPRED_HOME` | Components MapReduce |
| `HADOOP_COMMON_HOME` | Components Hadoop Common |
| `HADOOP_HDFS_HOME` | Components HDFS |
| `HADOOP_YARN_HOME` | Components YARN |
| `HADOOP_COMMON_LIB_NATIVE_DIR` | Biblioteca nativa |
| `PATH` | Cerca executables `hadoop`, `hdfs`, `start-dfs.sh`, etc. |
| `HADOOP_OPTS` | Opcions addicionals de JVM |

### 9.3 Aplicar els canvis (p. 13)

```bash
source ~/.bashrc
```

`source` executa les instruccions del fitxer a la sessió de shell actual. Si no es fa, els canvis poden no estar disponibles fins a obrir una sessió nova.

### 9.4 Comprovar variables

```bash
echo "$JAVA_HOME"
echo "$HADOOP_HOME"
echo "$HADOOP_OPTS"
which hadoop
which hdfs
```

No confonguis `PATH` (llista de rutes de cerca) amb `HADOOP_HOME` (ruta d'instal·lació).

### 9.5 Configurar `hadoop-env.sh` (p. 13)

```bash
nano "$HADOOP_HOME/etc/hadoop/hadoop-env.sh"
```

Afegir o ajustar una línia **sense `#` inicial**:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

**Atenció:** el signe `#` al començament d'una línia en un script shell normalment la converteix en un comentari; si la deixes comentada, no configurarà Java.

### 9.6 Verificar Hadoop (p. 14)

```bash
$HADOOP_HOME/bin/hadoop version
```

Hauries d'observar la versió **3.4.3**. Si funciona aquesta ordre però no `hadoop version`, probablement tens un problema de `PATH`.

---

## 10. Els quatre fitxers XML de configuració

A la secció de mode pseudodistribuït (p. 16), la guia enumera:

| Fitxer | Què defineix? | Paràmetres principals de la guia |
|---|---|---|
| `core-site.xml` | Propietats comunes i sistema de fitxers predeterminat | `fs.defaultFS` |
| `hdfs-site.xml` | Emmagatzematge HDFS | `dfs.replication`, `dfs.namenode.name.dir`, `dfs.datanode.data.dir` |
| `mapred-site.xml` | Motor d'execució MapReduce | `mapreduce.framework.name`, `mapreduce.application.classpath` |
| `yarn-site.xml` | Recursos i serveis auxiliars YARN | `yarn.nodemanager.aux-services`, `yarn.nodemanager.env-whitelist` |

Els trobem a:

```text
$HADOOP_HOME/etc/hadoop/
```

### Sintaxi XML general

```xml
<configuration>
  <property>
    <name>nom.de.la.propietat</name>
    <value>valor</value>
  </property>
</configuration>
```

**Errors comuns:** duplicar `<configuration>`, oblidar un tancament `</property>`, escriure malament el nom d'una propietat o utilitzar una ruta/port incorrecte.

---

## 11. Configuració de `core-site.xml`

### Segons la guia (p. 17)

```bash
nano "$HADOOP_HOME/etc/hadoop/core-site.xml"
```

```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://192.168.56.104:9000</value>
  </property>
</configuration>
```

### Interpretació

- `fs.defaultFS`: URI predeterminada del sistema de fitxers utilitzat pel client Hadoop.
- `hdfs://`: indica que s'utilitza HDFS.
- `192.168.56.104`: IP del NameNode a la guia.
- `9000`: port RPC configurat per a la comunicació amb HDFS.

Quan una ordre HDFS no inclou cap URI completa, el client pot utilitzar la configuració d'aquest fitxer.

**Precaució important:** el PDF suggereix `0.0.0.0` com a substitució de la IP. Cal distingir **adreça d'escolta** de **destinació de connexió**: `0.0.0.0` és útil com a *bind address* d'un servei, però no és una destinació adequada per recomanar als clients com a valor de `fs.defaultFS`. És millor emprar una IP real o un nom DNS resoluble.

**Ampliació:** en una màquina que resol bé el nom `hadoop`, es podria utilitzar `hdfs://hadoop:9000`, però això requereix configuració correcta de DNS o `/etc/hosts`.

---

## 12. Directoris NameNode i DataNode

### Segons la guia (p. 17)

```bash
sudo mkdir -p /home/hadoop/hdfs/{namenode,datanode}
sudo chown hadoop:hadoop /home/hadoop/hdfs
```

### Què representa cada carpeta?

```text
/home/hadoop/hdfs/
├── namenode/   # Metadades del sistema de fitxers HDFS
└── datanode/   # Dades i blocs locals d'HDFS
```

`mkdir -p` crea directoris intermedis si cal. L'expansió `{namenode,datanode}` és una funcionalitat de Bash que crea les dues rutes.

**Ampliació preventiva:** per assegurar que el propietari de totes les carpetes acabades de crear sigui `hadoop`, pots comprovar i, si és necessari, corregir recursivament:

```bash
sudo chown -R hadoop:hadoop /home/hadoop/hdfs
ls -ld /home/hadoop/hdfs /home/hadoop/hdfs/*
```

Aquesta comprovació és útil perquè canviar el propietari **només del directori pare** no garanteix modificar els subdirectoris si ja existien.

---

## 13. Configuració de `hdfs-site.xml`

### Segons la guia (p. 18)

```bash
nano "$HADOOP_HOME/etc/hadoop/hdfs-site.xml"
```

```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/home/hadoop/hdfs/namenode</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/home/hadoop/hdfs/datanode</value>
  </property>
</configuration>
```

### Explicació de les propietats

**`dfs.replication=1`** defineix un factor de replicació d'una sola còpia per defecte. Com que el laboratori té un únic DataNode, no pot mantenir tres rèpliques en tres servidors diferents. **Una rèplica no és una còpia de seguretat.**

**`dfs.namenode.name.dir`** indica on el NameNode manté localment les dades persistents de metadades. Cal protegir aquesta carpeta: perdre-la pot impedir recuperar l'estructura del sistema HDFS.

**`dfs.datanode.data.dir`** indica on s'emmagatzemen localment els blocs HDFS que gestiona el DataNode.

### Comparació visual

```text
NameNode                                      DataNode
/home/hadoop/hdfs/namenode                    /home/hadoop/hdfs/datanode

«Quin fitxer existeix i on?»                  «Aquí hi ha els bytes del bloc»
```

**Pregunta típica:** posar `dfs.replication=1` vol dir que Hadoop deixa de ser distribuït? No: continua utilitzant l'arquitectura HDFS, però en aquest laboratori només disposa d'una còpia de cada bloc.

---

## 14. Formatatge inicial del NameNode

### Ordre de la guia (p. 18)

```bash
hdfs namenode -format
```

### Què fa?

Inicialitza les estructures persistents del NameNode necessàries per a un nou HDFS: informació d'identificació del clúster i metadades inicials.

### Precaució crítica

**Fes aquest pas només quan estiguis inicialitzant un clúster nou i buit.** No l'executis cada vegada que arranquis Hadoop. Reformatejar un NameNode que ja contenia dades pot fer que es perdin les metadades anteriors i deixar les dades existents d'HDFS inaccessibles o inconsistents.

### Com distingir instal·lació d'arrencada?

- **Instal·lació inicial:** configurar carpetes i fitxers XML i formatar una sola vegada el NameNode nou.
- **Arrencada habitual:** iniciar els serveis amb `start-dfs.sh`, **sense tornar a formatar**.

**Ampliació:** abans d'actuar sobre un sistema preexistent, examina l'estat i la necessitat de preservar les metadades del NameNode. No esborris carpetes d'HDFS per resoldre errors sense un diagnòstic.

---

## 15. Arrencada i comprovació d'HDFS

### Arrencar HDFS (p. 19)

```bash
start-dfs.sh
```

La guia inicia NameNode i DataNode; en instal·lacions habituals també es poden gestionar processos auxiliars segons la configuració del clúster.

### Validar els processos amb Java (ampliació)

```bash
jps
```

El resultat esperat en aquest laboratori hauria d'incloure com a mínim:

```text
NameNode
DataNode
Jps
```

`jps` informa dels processos Java. **No substitueix** un control funcional complet: un procés pot existir i, tot i així, tenir problemes de configuració.

### Accés web al NameNode (p. 20–21)

```text
http://192.168.56.104:9870/
```

A la interfície es pot consultar l'estat d'HDFS i, al menú **DataNodes**, els nodes que serveixen blocs. La guia mostra captures d'aquests panells.

### Interfície del DataNode (p. 21–23)

```text
http://192.168.56.104:9864/
```

La guia mostra una pàgina del DataNode amb informació sobre el volum de dades, l'estat del servei i els seus directoris locals.

### Comprovar HDFS per línia d'ordres (ampliació)

```bash
hdfs dfs -ls /
hdfs dfsadmin -report
```

- `hdfs dfs -ls /`: intenta consultar l'arrel d'HDFS.
- `hdfs dfsadmin -report`: mostra un informe sobre la capacitat i els DataNodes coneguts.

**Diferència essencial:** `/home/hadoop/hdfs/datanode` és una ruta del **sistema de fitxers Linux local**; `/user/hadoop` és una ruta **lògica dins d'HDFS**. No s'han d'utilitzar com si fossin equivalents.

---

## 16. Configurar MapReduce per executar-se amb YARN

### Segons la guia (p. 24)

```bash
nano "$HADOOP_HOME/etc/hadoop/mapred-site.xml"
```

```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapreduce.application.classpath</name>
    <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
  </property>
</configuration>
```

### Explicació

- **`mapreduce.framework.name=yarn`** indica que els treballs MapReduce s'executaran utilitzant YARN en lloc d'un mode local.
- **`mapreduce.application.classpath`** indica rutes on trobar els recursos necessaris per iniciar aplicacions MapReduce.

**Nota:** hem reconstruït en una sola línia el valor `classpath`, que al PDF apareix partit visualment entre dues línies. Si copies un salt de línia accidental dins d'una ruta, pots provocar errors difícils de localitzar.

### Diferència entre MapReduce i YARN

MapReduce defineix i executa el model de processament. YARN gestiona l'assignació de recursos i el llançament de tasques. Podem recordar-ho així:

```text
MapReduce: QUINA feina cal fer?
YARN:      AMB QUINS recursos i EN QUIN node s'executa?
```

---

## 17. Configurar `yarn-site.xml` i iniciar YARN

### Segons la guia (p. 24–25)

```bash
nano "$HADOOP_HOME/etc/hadoop/yarn-site.xml"
```

```xml
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.env-whitelist</name>
    <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
  </property>
</configuration>
```

### Significat

**`yarn.nodemanager.aux-services=mapreduce_shuffle`** activa el servei auxiliar necessari per al procés de *shuffle* dels treballs MapReduce.

**`yarn.nodemanager.env-whitelist`** identifica variables de l'entorn que es poden propagar als contenidors de YARN; la llista inclou les rutes dels diferents components Hadoop.

### Arrencada (p. 25)

```bash
start-yarn.sh
```

### Comprovació de processos (ampliació)

```bash
jps
```

S'espera veure, entre altres:

```text
ResourceManager
NodeManager
```

### Interfície web de YARN

```text
http://192.168.56.104:8088/
```

A la interfície es pot observar el ResourceManager, les aplicacions enviades, els seus estats i els nodes registrats. La pàgina 26 del PDF inclou captures d'**All Applications** i **Nodes**.

---

## 18. Taula de ports i interfícies

| Port | Servei en aquesta guia | Per a què serveix? |
|---:|---|---|
| `22` | SSH | Connexió i scripts remots |
| `9000` | RPC del NameNode configurat | Accés dels clients a HDFS |
| `9870` | NameNode Web UI | Supervisar HDFS |
| `9864` | DataNode Web UI | Consultar el node de dades |
| `8088` | ResourceManager Web UI | Supervisar aplicacions i nodes YARN |

**Cal recordar:** `9000` no és la interfície web del NameNode. La interfície web que mostra la guia és `9870`.

Per comprovar quins processos escolten ports (ampliació):

```bash
ss -lnt
```

Si la interfície no s'obre des del navegador, comprova la IP, la xarxa entre l'ordinador i la màquina virtual, el servei, la resolució del nom i les regles del tallafoc.

---

## 19. Proves pràctiques després d'instal·lar Hadoop (ampliació)

La guia acaba mostrant la instal·lació en marxa i les pàgines web; les proves següents són una **ampliació** per verificar funcionalment HDFS i MapReduce.

### 19.1 Crear una carpeta HDFS

```bash
hdfs dfs -mkdir -p /user/hadoop/proves
hdfs dfs -ls /user/hadoop
```

L'opció `-p` permet crear els directoris pare necessaris.

### 19.2 Crear un fitxer local

```bash
printf 'hola hadoop\nhola big data\n' > /tmp/prova-hadoop.txt
cat /tmp/prova-hadoop.txt
```

### 19.3 Pujar-lo a HDFS

```bash
hdfs dfs -put /tmp/prova-hadoop.txt /user/hadoop/proves/
hdfs dfs -ls /user/hadoop/proves/
```

### 19.4 Llegir-lo des d'HDFS

```bash
hdfs dfs -cat /user/hadoop/proves/prova-hadoop.txt
```

**Sortida esperada:**

```text
hola hadoop
hola big data
```

### 19.5 Descarregar-lo

```bash
hdfs dfs -get /user/hadoop/proves/prova-hadoop.txt /tmp/prova-hadoop-recuperada.txt
cat /tmp/prova-hadoop-recuperada.txt
```

### 19.6 Consultar la salut del sistema

```bash
hdfs dfsadmin -report
```

Un resultat correcte hauria de mostrar el DataNode actiu. Un laboratori amb un node i replicació 1 no té redundància física.

### 19.7 Prova d'execució MapReduce

Pots localitzar els exemples inclosos a la distribució i executar-ne un de tipus `wordcount` després d'haver preparat les dades d'entrada:

```bash
ls "$HADOOP_HOME/share/hadoop/mapreduce/"*examples*.jar
```

**Exemple orientatiu** (la ruta exacta del JAR pot variar):

```bash
hadoop jar "$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.4.3.jar" \
  wordcount /user/hadoop/proves /user/hadoop/wordcount-sortida

hdfs dfs -cat /user/hadoop/wordcount-sortida/part-r-00000
```

**Important:** el directori de sortida no ha d'existir abans d'executar `wordcount`. Si ja existeix, tria una ruta nova o elimina-la només si n'has comprovat el contingut i no necessites les dades.

---

## 20. Errors habituals i resolució d'incidències

### 20.1 `Permission denied` en arrencar HDFS amb `pdsh`

La guia (p. 19–20) indica afegir a `.bashrc`:

```bash
export PDSH_RCMD_TYPE=ssh
source ~/.bashrc
```

Això obliga `pdsh` a utilitzar SSH com a mètode de connexió remota.

La guia també proposa, com a alternativa, desinstal·lar `pdsh`:

```bash
sudo apt-get remove pdsh
```

**Diagnòstic recomanat:** abans de desinstal·lar res, comprova `ssh localhost`, permisos de `.ssh`, usuari actiu i la variable `PDSH_RCMD_TYPE`. La desinstal·lació no és una solució universal per a qualsevol error de permisos.

### 20.2 `JAVA_HOME is not set`

**Causa possible:** manca la variable o apunta a una ruta incorrecta.

```bash
echo "$JAVA_HOME"
readlink -f "$(which java)"
grep JAVA_HOME "$HADOOP_HOME/etc/hadoop/hadoop-env.sh"
```

**Solució:** revisar `.bashrc` i `hadoop-env.sh`, adaptar la ruta i carregar l'entorn. Recorda que una línia comentada amb `#` no defineix la variable.

### 20.3 `hadoop: command not found`

**Causa probable:** `PATH` no inclou `$HADOOP_HOME/bin`.

```bash
echo "$HADOOP_HOME"
echo "$PATH"
source ~/.bashrc
```

### 20.4 `Connection refused` en executar `hdfs dfs -ls /`

Possibles causes:

- El NameNode no està arrencat.
- `fs.defaultFS` apunta a una IP o un port equivocat.
- Un tallafoc bloqueja la comunicació.
- El procés ha fallat durant l'arrencada.

```bash
jps
hdfs getconf -confKey fs.defaultFS
```

### 20.5 El NameNode funciona però el DataNode no apareix

Revisa permisos i les rutes de `dfs.datanode.data.dir`, l'espai disponible, els registres de l'aplicació i si s'ha reinicialitzat indegudament el NameNode.

```bash
ls -ld /home/hadoop/hdfs /home/hadoop/hdfs/*
df -h
hdfs dfsadmin -report
```

### 20.6 La pàgina `:9870` o `:8088` no funciona

1. Identifica la IP correcta (`hostname -I`).
2. Revisa que el servei corresponent aparegui a `jps`.
3. Comprova els ports (`ss -lnt`).
4. Revisa la configuració de xarxa de la màquina virtual.
5. Verifica la resolució DNS i el tallafoc si accedeixes des d'un altre ordinador.

### 20.7 `NameNode is not formatted`

Això pot passar en una **instal·lació nova** en què encara no s'ha inicialitzat HDFS. Abans de fer `hdfs namenode -format`, assegura't que realment es tracta d'un clúster nou i que no s'han perdut o desconfigurat simplement les rutes de metadades d'un sistema existent.

### 20.8 Errors de sintaxi XML

Una etiqueta incorrecta pot impedir llegir la configuració. Verifica que hi hagi un únic element arrel `<configuration>`, que cada `<property>` contingui `name` i `value`, i que les etiquetes estiguin tancades.

### 20.9 Fallades de YARN per memòria insuficient

En una màquina virtual, diversos dimonis competeixen per la RAM. Si el ResourceManager s'obre però no s'executen les aplicacions, comprova els recursos del sistema i els logs abans de modificar la configuració.

```bash
free -h
jps
```

### 20.10 El fitxer existeix en Linux però no a HDFS

**Motiu:** són sistemes de fitxers diferents. `ls /tmp` consulta Linux; `hdfs dfs -ls /tmp` consulta HDFS. Cal `-put` o un altre mecanisme d'ingesta per copiar el fitxer al sistema distribuït.

---

## 21. Ordre correcte de totes les operacions

### Instal·lació inicial (una única vegada)

1. Preparar Ubuntu i l'accés administratiu.
2. Instal·lar Java.
3. Instal·lar SSH, crear l'usuari `hadoop` i configurar les claus.
4. Descarregar i instal·lar Hadoop 3.4.3.
5. Definir les variables `.bashrc` i `JAVA_HOME`.
6. Configurar `core-site.xml`.
7. Crear els directoris locals del NameNode i DataNode.
8. Configurar `hdfs-site.xml`.
9. **Formatar el NameNode nou una sola vegada.**
10. Arrencar HDFS i verificar-lo.
11. Configurar `mapred-site.xml` i `yarn-site.xml`.
12. Arrencar YARN i verificar-lo.

### Arrencada habitual (sense formatatge)

```bash
start-dfs.sh
start-yarn.sh
jps
```

### Aturada habitual (ampliació)

```bash
stop-yarn.sh
stop-dfs.sh
```

Aturar ordenadament ajuda a evitar interrupcions de tasques i facilita el manteniment. No cal eliminar els directoris de dades per apagar Hadoop.

---

## 22. Seguretat i bones pràctiques

Aquest és un entorn de **laboratori**, no una configuració de producció. Per això cal entendre les seves limitacions:

- No exposar a Internet les interfícies web ni els ports interns sense controls d'accés.
- Fer servir un usuari de servei amb els permisos necessaris, no `root` per a tot.
- Protegir la clau SSH privada; l'accés sense frase de pas simplifica l'automatització però implica riscos si es roba la clau.
- No utilitzar la IP d'exemple de la guia sense comprovar la teva xarxa.
- Conservar còpies de seguretat de les metadades i dades importants.
- No executar `namenode -format` per solucionar errors sense comprovar l'estat previ.
- No assumir que `dfs.replication=1` protegeix davant la pèrdua del disc.
- Evitar donar permisos oberts o desactivar proteccions de sistema sense necessitat.
- Comprovar els fitxers descarregats abans d'utilitzar-los en entorns reals.

---

## 23. Taules comparatives per memoritzar

### 23.1 NameNode, DataNode, ResourceManager i NodeManager

| Dimoni | Subsistema | Responsabilitat |
|---|---|---|
| NameNode | HDFS | Metadades i espai de noms |
| DataNode | HDFS | Blocs reals de dades |
| ResourceManager | YARN | Planificació i gestió de recursos del clúster |
| NodeManager | YARN | Recursos i contenidors del node |

### 23.2 Directoris Linux i HDFS

| Ruta | Tipus | Funció |
|---|---|---|
| `/usr/local/hadoop` | Linux | Aplicació instal·lada |
| `/home/hadoop/.ssh` | Linux | Claus SSH |
| `/home/hadoop/hdfs/namenode` | Linux | Dades internes persistents del NameNode |
| `/home/hadoop/hdfs/datanode` | Linux | Blocs locals del DataNode |
| `/user/hadoop/proves` | HDFS | Carpeta lògica dins del sistema distribuït |

### 23.3 Comandes bàsiques

| Comanda | Propòsit |
|---|---|
| `java -version` | Consultar Java |
| `ssh localhost` | Provar autenticació SSH |
| `hadoop version` | Consultar versió Hadoop |
| `hdfs namenode -format` | Inicialitzar un NameNode **nou** |
| `start-dfs.sh` | Arrencar HDFS |
| `start-yarn.sh` | Arrencar YARN |
| `jps` | Mostrar processos Java |
| `hdfs dfs -ls /` | Llistar l'arrel HDFS |
| `hdfs dfsadmin -report` | Consultar estat dels nodes HDFS |
| `stop-yarn.sh` | Aturar YARN |
| `stop-dfs.sh` | Aturar HDFS |

---

## 24. Exercici pràctic complet amb verificació

**Enunciat:** desplega Hadoop en mode pseudodistribuït seguint la guia i presenta evidències que funcionen les capes HDFS i YARN.

### Evidències recomanades

1. **Java:** captura de `java -version`.
2. **Usuari:** captura de `whoami` mostrant `hadoop`.
3. **SSH:** captura de `ssh localhost` sense demanda de contrasenya d'usuari.
4. **Hadoop:** captura de `hadoop version`.
5. **Configuració:** fragments dels quatre XML amb les propietats rellevants.
6. **Processos:** captura de `jps` amb NameNode, DataNode, ResourceManager i NodeManager.
7. **HDFS:** captura del port `9870`, amb DataNode actiu.
8. **YARN:** captura del port `8088`, amb NodeManager registrat.
9. **Funcionament:** creació de carpeta i pujada d'un fitxer amb `hdfs dfs -put`.
10. **Lectura:** captura de `hdfs dfs -cat` mostrant el contingut.

### Com redactar una explicació de pràctica

> Hem configurat un clúster Hadoop 3.4.3 en mode pseudodistribuït sobre Ubuntu 22.04. Després d'instal·lar Java i configurar l'autenticació SSH de l'usuari `hadoop`, hem establert les variables d'entorn i els fitxers XML d'HDFS i YARN. Un cop inicialitzat el NameNode nou, hem arrencat els serveis, verificat els processos i comprovat les interfícies web. Finalment, hem provat operacions de lectura i escriptura a HDFS.

**Nota:** aquest text és un model de redacció, no una afirmació que les comandes s'hagin executat realment.

---

## 25. Autoavaluació — 60 preguntes amb resposta

### Fonaments (1–12)

1. **Què és Hadoop?** Un ecosistema de codi obert per emmagatzemar i processar grans conjunts de dades.
2. **Quins són els quatre components principals?** Common, HDFS, YARN i MapReduce.
3. **Què fa Hadoop Common?** Aporta biblioteques i serveis comuns.
4. **Per a què serveix HDFS?** Per gestionar un sistema de fitxers distribuït.
5. **Per a què serveix YARN?** Per administrar recursos i planificar aplicacions.
6. **Què fa MapReduce?** Processa dades amb tasques paral·leles.
7. **Què és un clúster?** Un conjunt de nodes que actuen coordinadament.
8. **Què és un node?** Una màquina que forma part del clúster.
9. **Què significa pseudodistribuït?** Diversos serveis distribuïts lògicament en una sola màquina.
10. **Quins són els tres modes?** Local, pseudodistribuït i totalment distribuït.
11. **És un entorn de producció aquesta guia?** No; és una instal·lació de laboratori.
12. **Quin Ubuntu s'utilitza?** Ubuntu 22.04.

### Java, usuaris i SSH (13–24)

13. **Quina versió Hadoop instal·la la guia?** Hadoop 3.4.3.
14. **Quina versió de Java s'espera utilitzar?** OpenJDK 11.
15. **Com consultes la versió Java?** `java -version`.
16. **Per què necessita Java Hadoop?** Perquè els seus components i dimonis s'executen amb JVM.
17. **Per què es crea `hadoop`?** Per executar i administrar els serveis amb un usuari específic.
18. **Què fa `useradd -m`?** Crea l'usuari i el seu directori personal.
19. **Què fa `su - hadoop`?** Inicia una sessió com a usuari `hadoop`.
20. **Per què es necessita SSH?** Per a scripts de gestió remota i arrencada de serveis.
21. **Quina comanda genera claus RSA?** `ssh-keygen -t rsa`.
22. **Quin fitxer conté la clau pública?** `id_rsa.pub`.
23. **Quin fitxer guarda claus públiques autoritzades?** `authorized_keys`.
24. **Com es comprova l'accés local SSH?** `ssh localhost`.

### Instal·lació i entorn (25–34)

25. **Quina ordre descarrega Hadoop?** `wget` amb la URL de l'arxiu Apache.
26. **Què fa `tar -xvzf`?** Descomprimeix i extreu un arxiu `.tar.gz`.
27. **On s'instal·la Hadoop?** `/usr/local/hadoop`.
28. **Què fa `chown -R`?** Canvia el propietari i grup recursivament.
29. **Què defineix `HADOOP_HOME`?** El directori principal d'Hadoop.
30. **Què defineix `JAVA_HOME`?** El directori del JDK.
31. **Per què es modifica `PATH`?** Per executar comandes Hadoop sense la ruta completa.
32. **Què fa `source ~/.bashrc`?** Recarrega la configuració a la sessió actual.
33. **On es configura `JAVA_HOME` també?** A `etc/hadoop/hadoop-env.sh`.
34. **Com verifiques la versió Hadoop?** `hadoop version`.

### HDFS i fitxers XML (35–46)

35. **Quina propietat de `core-site.xml` configura el sistema per defecte?** `fs.defaultFS`.
36. **Quin port RPC utilitza la guia?** 9000.
37. **Què fa el NameNode?** Manté metadades i l'espai de noms d'HDFS.
38. **Què fa el DataNode?** Guarda i serveix blocs de dades.
39. **Quina propietat defineix les rèpliques?** `dfs.replication`.
40. **Quin valor té al laboratori?** 1.
41. **On es guarden les metadades locals del NameNode?** `/home/hadoop/hdfs/namenode`.
42. **On es guarden els blocs locals del DataNode?** `/home/hadoop/hdfs/datanode`.
43. **Per què no s'ha de repetir `namenode -format`?** Perquè pot destruir metadades d'un HDFS existent.
44. **Com s'arrenca HDFS?** `start-dfs.sh`.
45. **Quin port mostra el NameNode Web UI?** 9870.
46. **Quin port mostra el DataNode Web UI?** 9864.

### YARN, verificació i incidències (47–60)

47. **Quina propietat activa YARN com a motor de MapReduce?** `mapreduce.framework.name=yarn`.
48. **Què fa ResourceManager?** Gestiona la disponibilitat i assignació de recursos del clúster.
49. **Què fa NodeManager?** Administra recursos i execució local al node.
50. **Per a què serveix `mapreduce_shuffle`?** Servei auxiliar per a l'intercanvi de dades entre tasques MapReduce.
51. **Com s'arrenca YARN?** `start-yarn.sh`.
52. **Quin port utilitza ResourceManager Web UI?** 8088.
53. **Quina ordre mostra els processos Java?** `jps`.
54. **Quina ordre llista fitxers de l'arrel d'HDFS?** `hdfs dfs -ls /`.
55. **Quina ordre puja un fitxer a HDFS?** `hdfs dfs -put origen desti`.
56. **Quina ordre llegeix un fitxer HDFS?** `hdfs dfs -cat ruta`.
57. **Quina ordre mostra informació de DataNodes i capacitat?** `hdfs dfsadmin -report`.
58. **Com es configura `pdsh` perquè utilitzi SSH?** `export PDSH_RCMD_TYPE=ssh`.
59. **Quina diferència hi ha entre `9000` i `9870`?** `9000` és RPC HDFS de la guia; `9870` és la interfície web del NameNode.
60. **Per què `dfs.replication=1` no és una còpia de seguretat?** Perquè una única còpia es pot perdre amb el node o disc que la conté.

---

## 26. Glossari essencial

| Terme | Definició curta |
|---|---|
| Apache Hadoop | Ecosistema de processament i emmagatzematge distribuït |
| Big Data | Dades que requereixen enfocaments escalables per volum, velocitat o varietat |
| HDFS | Sistema de fitxers distribuït de Hadoop |
| YARN | Gestor de recursos per a aplicacions del clúster |
| MapReduce | Model de processament paral·lel de dades |
| NameNode | Servei de metadades d'HDFS |
| DataNode | Servei que emmagatzema els blocs d'HDFS |
| ResourceManager | Coordinador de recursos YARN |
| NodeManager | Administrador de recursos en cada node YARN |
| JVM | Màquina virtual Java |
| JDK | Kit de desenvolupament Java |
| SSH | Protocol per establir connexions remotes segures |
| Clau privada | Secret d'autenticació que no s'ha de compartir |
| Clau pública | Material que es pot autoritzar en un servidor SSH |
| `authorized_keys` | Llista de claus SSH autoritzades per un usuari |
| `JAVA_HOME` | Ruta d'instal·lació Java |
| `HADOOP_HOME` | Ruta d'instal·lació d'Hadoop |
| HDFS URI | Adreça com `hdfs://host:9000` |
| RPC | Comunicació entre processos/serveis |
| `dfs.replication` | Nombre predeterminat de còpies dels blocs HDFS |
| XML | Format de configuració estructurat en etiquetes |
| Pseudodistribuït | Serveis separats executant-se en una màquina |
| Dimoni | Procés de servei executat en segon pla |
| *Shuffle* | Redistribució de dades entre fases Map i Reduce |
| `jps` | Eina Java per inspeccionar processos locals |
| `pdsh` | Eina de shell remota en paral·lel |
| `localhost` | Nom que acostuma a referir-se al mateix ordinador |
| `fs.defaultFS` | Sistema de fitxers per defecte dels clients Hadoop |

---

## 27. Repàs exprés i checklist final

### Els 10 conceptes que has de saber explicar sense mirar

1. Hadoop = **Common + HDFS + YARN + MapReduce**.
2. **NameNode** gestiona metadades; **DataNode** emmagatzema blocs.
3. **ResourceManager** coordina recursos; **NodeManager** gestiona un node.
4. Mode **pseudodistribuït** = una màquina, diversos dimonis.
5. Hadoop necessita **Java** i la ruta `JAVA_HOME` correcta.
6. Els scripts d'arrencada utilitzen **SSH** per gestionar serveis.
7. Les configuracions principals són **core-site, hdfs-site, mapred-site i yarn-site**.
8. `dfs.replication=1` és coherent amb un laboratori d'un sol DataNode, però no proporciona redundància.
9. **`hdfs namenode -format` només per a un NameNode nou.**
10. Els ports principals de la guia són **9000, 9870, 9864 i 8088**.

### Checklist d'instal·lació

- [ ] Ubuntu 22.04 i IP comprovats.
- [ ] Java correctament instal·lat i verificat.
- [ ] Usuari `hadoop` creat i sessió activa.
- [ ] SSH a `localhost` sense contrasenya d'usuari.
- [ ] Hadoop 3.4.3 instal·lat a `/usr/local/hadoop`.
- [ ] Variables d'entorn correctes i recarregades.
- [ ] `hadoop-env.sh` amb `JAVA_HOME` correcte.
- [ ] `core-site.xml` amb IP o nom real del NameNode.
- [ ] `hdfs-site.xml` amb directoris i replicació 1.
- [ ] NameNode nou formatat una sola vegada.
- [ ] HDFS iniciat i DataNode visible.
- [ ] `mapred-site.xml` configurat per a YARN.
- [ ] `yarn-site.xml` configurat per a `mapreduce_shuffle`.
- [ ] YARN iniciat i NodeManager visible.
- [ ] Panells web 9870 i 8088 accessibles.
- [ ] Lectura i escriptura a HDFS provades.

---

## 28. Referències i notes sobre la guia

**Font principal:** *M5075_NF1_1_Activitat 1_Com instal·lar_HADOOP3_4_3_Ubuntu22_04_v02.pdf*, 27 pàgines, material de M5075 Big Data Aplicat de l'Institut Sa Palomera. La pàgina 27 remet a un tutorial de **HowtoForge** sobre instal·lació d'Hadoop a Ubuntu 22.04.

**Distribució temàtica del PDF:**

- **Pàgines 3–4:** Hadoop, components i requisits previs.
- **Pàgines 4–6:** instal·lació Java.
- **Pàgines 6–10:** usuari Hadoop i configuració SSH.
- **Pàgines 10–14:** instal·lació i variables d'entorn.
- **Pàgines 16–18:** mode pseudodistribuït, `core-site.xml` i `hdfs-site.xml`.
- **Pàgines 18–23:** formatatge, arrencada HDFS i interfícies de NameNode/DataNode.
- **Pàgines 24–26:** configuració de MapReduce i YARN, interfície del ResourceManager.

### Detalls que convé tenir en compte

- La guia alterna una referència històrica a **Hadoop 3.4.1** quan explica Java i la instal·lació real de **Hadoop 3.4.3**. Aquests apunts mantenen **3.4.3** com a versió objectiu de l'activitat.
- Les ordres del document de vegades apareixen precedides per `#`, que en una captura representa el prompt d'un usuari privilegiat. **No has de copiar aquest `#` com a part d'una comanda de shell**, perquè en Bash indica comentari.
- La IP `192.168.56.104` és un **exemple**. L'entorn de cada alumne pot tenir-ne una altra.
- Les proves de fitxers HDFS, `jps`, les indicacions de seguretat i els exercicis d'autoavaluació són **ampliacions didàctiques** i no s'han de presentar com a passos textuals del PDF.
- En els blocs XML s'han normalitzat els salts de línia llargs per evitar errors de còpia i enganxada.

**Recomanació d'estudi:** primer memoritza el propòsit de cada servei i fitxer de configuració; després repassa el procediment d'instal·lació i practica explicar què fa cadascuna de les comandes. Per acabar, resol les 60 preguntes sense consultar les respostes.
