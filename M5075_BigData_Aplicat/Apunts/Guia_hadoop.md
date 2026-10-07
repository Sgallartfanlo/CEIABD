# Guia d'Instal·lació de Hadoop (Pseudo-Distributed Mode)

Aquesta guia recull els passos essencials per instal·lar i configurar Apache Hadoop en un entorn de desenvolupament o prova (mode pseudo-distribuït) sobre un sistema operatiu Linux (Ubuntu/Debian).

---

## 1. Requisits Previs

Abans de començar amb Hadoop, cal assegurar-se de tenir el sistema preparat:
* **Sistema Operatiu:** Ubuntu 20.04 / 22.04 LTS (o similar).
* **Usuari dedicat:** Es recomana crear un usuari específic per a Hadoop (p. ex., `hadoop`).
* **Java:** Hadoop requereix Java Runtime Environment (JRE) i Java Development Kit (JDK).

### Creació de l'usuari Hadoop
```bash
sudo adduser hadoop
su - hadoop
```

---

## 2. Instal·lació de Java (OpenJDK)

Hadoop està escrit en Java, per la qual cosa cal instal·lar el JDK.

1. Actualitza els repositoris i instal·la Java (per exemple, Java 11 o 8):
   ```bash
   sudo apt update
   sudo apt install openjdk-11-jdk -y
   ```

2. Comprova la versió instal·lada:
   ```bash
   java -version
   ```

3. Configura la variable d'entorn `JAVA_HOME`. Afegeix la línia següent al final del fitxer `~/.bashrc`:
   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
   export PATH=$PATH:$JAVA_HOME/bin
   ```
   Després, aplica els canvis:
   ```bash
   source ~/.bashrc
   ```

---

## 3. Configuració d'accés SSH sense contrasenya

Hadoop utilitza SSH per gestionar els seus nodes (fins i tot en mode pseudo-distribuït).

1. Genera les claus SSH:
   ```bash
   ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
   ```

2. Autoritza la clau per accedir localment:
   ```bash
   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
   chmod 0600 ~/.ssh/authorized_keys
   ```

3. Comprova que funciona sense demanar contrasenya:
   ```bash
   ssh localhost
   ```

---

## 4. Descarregar i Descomprimir Hadoop

1. Descarrega una versió estable d'Apache Hadoop (p. ex., 3.3.6) des del lloc web oficial o via `wget`:
   ```bash
   wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
   ```

2. Descomprimeix el fitxer al directori desitjat (per exemple, `/usr/local` o al directori personal):
   ```bash
   tar -xzvf hadoop-3.3.6.tar.gz
   sudo mv hadoop-3.3.6 /usr/local/hadoop
   sudo chown -R hadoop:hadoop /usr/local/hadoop
   ```

---

## 5. Configuració de les Variables d'Entorn de Hadoop

Afegeix les rutes de Hadoop al fitxer `~/.bashrc`:

```bash
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

Aplica els canvis:
```bash
source ~/.bashrc
```

---

## 6. Modificació dels Fitxers de Configuració de Hadoop

Els fitxers de configuració es troben a `$HADOOP_HOME/etc/hadoop/`.

### A. `hadoop-env.sh`
Defineix la variable `JAVA_HOME` per a Hadoop. Edita el fitxer i assegura't de descomentar o afegir:
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### B. `core-site.xml`
Defineix el directori temporal i l'URI predeterminat del sistema de fitxers (HDFS).
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

### C. `hdfs-site.xml`
Defineix el factor de rèplica i els directoris de dades per al NameNode i DataNode.
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/usr/local/hadoop/data/dfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/usr/local/hadoop/data/dfs/datanode</value>
    </property>
</configuration>
```

### D. `mapred-site.xml`
Configura el framework MapReduce (YARN).
```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
```

### E. `yarn-site.xml`
Configura els serveis de YARN.
```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

---

## 7. Format del NameNode

Abans d'iniciar els serveis per primera vegada, cal formatar el sistema de fitxers HDFS:

```bash
hdfs namenode -format
```

---

## 8. Execució i Verificació dels Serveis

### Iniciar Hadoop (HDFS i YARN)
```bash
start-dfs.sh
start-yarn.sh
```
*(Alternativament, pots utilitzar `start-all.sh`)*

### Comprovació de processos actius
Executa la comanda `jps` per veure els processos de Java en execució. Hauries de veure:
* `NameNode`
* `DataNode`
* `ResourceManager`
* `NodeManager`
* `SecondaryNameNode`

### Interfícies Web
Pots accedir als panells de control a través del navegador:
* **HDFS NameNode:** `http://localhost:9870/`
* **YARN ResourceManager:** `http://localhost:8088/`

### Aturar els serveis
```bash
stop-yarn.sh
stop-dfs.sh