# Apache Hive 3.1.3 — Instal·lació i configuració a Hadoop

## 1. Objectius i context de la instal·lació

**[GUIA]** L'activitat ensenya a instal·lar Apache Hive 3.1.3 i integrar-lo amb un entorn Hadoop ja existent, configurar els serveis, emmagatzemar les metadades en una base de dades MySQL/MariaDB i connectar-hi clients. També inclou la integració amb Sqoop i la configuració de Hue, amb opció de desplegar-lo en un contenidor Docker.

**[AMPLIACIÓ]** Un cop acabada la pràctica, hauríem de ser capaços de respondre quatre preguntes: (1) on són els fitxers de dades?, (2) qui recorda l'esquema de les taules?, (3) qui rep les consultes SQL?, i (4) des d'on s'executen aquestes consultes? La resposta breu és: les dades poden residir a **HDFS**; les metadades, al **Metastore**; el servei de consultes és **HiveServer2**; i els usuaris hi accedeixen, per exemple, des de **Beeline** o **Hue**.

Cal distingir **instal·lació** (copiar binaris), **configuració** (definir rutes, dependències i connexions), **inicialització** (preparar l'esquema del Metastore) i **execució** (engegar serveis i fer consultes). Que la comanda `hive --version` respongui només confirma una part de la instal·lació, no que el sistema complet funcioni.

## 2. Què és Hive i on encaixa dins de Hadoop

**[AMPLIACIÓ]** Apache Hive és una capa que permet definir taules i llançar consultes amb un llenguatge semblant a SQL sobre conjunts de dades gestionats en l'ecosistema Hadoop. Hive no substitueix HDFS: proporciona una manera estructurada d'accedir a la informació. Tampoc no és equivalent a una base de dades relacional tradicional pensada principalment per a transaccions curtes.

```text
                       Usuari / aplicació
                              |
                     Beeline / Hue / JDBC
                              |
                       HiveServer2
                         /        \
                    Metastore    Motor de consulta
                       |               |
                    MariaDB        Hadoop / YARN
                                       |
                                      HDFS
```

**Què representa cada capa?** MariaDB emmagatzema *metadades*, com noms de taules, columnes, ubicacions i particions. HDFS emmagatzema els *fitxers de dades* quan les taules utilitzen aquest sistema d'arxius. HiveServer2 coordina consultes de clients remots i utilitza un motor d'execució compatible amb la configuració de Hive.

**Exemple conceptual:** si creem `CREATE TABLE alumnes (nom STRING, edat INT);`, el Metastore registra què és `alumnes` i quines columnes té. Les files no es converteixen automàticament en registres dins de MariaDB: les dades de la taula s'emmagatzemen a la ubicació que correspongui segons la definició de Hive.

## 3. Components: Hive CLI, Metastore, HiveServer2 i Beeline

**[GUIA]** Les darreres pàgines del document dediquen un bloc específic a les tres comandes `hive`, `hive --service metastore` i `hive --service hiveserver2`, i a la connexió `beeline -u jdbc:hive2://localhost:10000`.

| Component | Funció principal | Comanda habitual | Port habitual |
|---|---|---|---|
| Hive CLI | Consola tradicional per interactuar amb Hive | `hive` | No és un servidor JDBC |
| Metastore Server | Servei de consulta de metadades | `hive --service metastore` | 9083 (Thrift) |
| HiveServer2 | Servei que rep consultes de clients JDBC/ODBC | `hive --service hiveserver2` | 10000 (JDBC/Thrift) |
| Beeline | Client que envia instruccions a HiveServer2 | `beeline -u jdbc:hive2://localhost:10000` | Es connecta al 10000 |
| MariaDB/MySQL | Base de dades que persisteix el catàleg | Servei de MariaDB | 3306 |
| Hue | Interfície web per a usuaris | Instal·lació local o Docker | 8000/8888 segons desplegament |

**[AMPLIACIÓ]** La distinció clau és que **Metastore no és Beeline** i **MariaDB no és HiveServer2**. Beeline és el client; HiveServer2 accepta la consulta; el Metastore ofereix informació de l'esquema; MariaDB guarda aquesta informació de manera persistent. En un desplegament amb Metastore remot, el servei Metastore i HiveServer2 poden tenir processos independents.

⚠️ **[PRECAUCIÓ]** La guia presenta el Metastore remot al port 9083. Perquè HiveServer2 l'utilitzi, la configuració del desplegament ha de ser coherent (per exemple, `hive.metastore.uris=thrift://localhost:9083`). Arrencar el procés no garanteix per si sol que tots els clients el consultin: la configuració efectiva ha de coincidir.

## 4. Visió general del procediment

```text
1. Comprovar Java, Hadoop, HDFS, YARN i usuari
2. Descarregar i descomprimir Hive 3.1.3
3. Definir HIVE_HOME i altres variables
4. Preparar fitxers de configuració
5. Preparar HDFS i compatibilitat de dependències
6. Configurar Hadoop proxyuser i Hue
7. Configurar hive-site.xml
8. Preparar base de dades i connector JDBC
9. Inicialitzar Metastore amb schematool
10. Arrencar serveis i connectar Beeline
11. Provar SHOW DATABASES i consultes
```

Aquesta seqüència evita un error típic: intentar connectar Beeline abans d'arrencar HiveServer2 o abans de configurar el magatzem de metadades.

## 5. Preparació de l'entorn i comprovacions prèvies

**[GUIA]** Es comença situant l'usuari al seu directori personal:

```bash
cd ~
pwd
```

`cd ~` entra al directori personal de l'usuari actual; `pwd` permet comprovar que realment treballem a la ruta esperada. En la guia es pressuposa l'usuari `hadoop`, per tant `~` hauria de ser `/home/hadoop`.

**[AMPLIACIÓ]** Abans d'instal·lar convé comprovar l'estat de les dependències:

```bash
whoami
java -version
hadoop version
hdfs dfs -ls /
which wget
which tar
echo "$HADOOP_HOME"
echo "$SQOOP_HOME"
```

Si `hdfs dfs -ls /` falla, no sempre vol dir que Hive estigui malament: pot ser un problema previ d'HDFS, de permisos o de la configuració `fs.defaultFS`. Si `SQOOP_HOME` no està definit, la còpia del JAR de Hive a Sqoop fallarà encara que Hive s'hagi instal·lat correctament.

> **Nota d'entorn:** la guia fa servir `/home/hadoop/hadoop`. En altres pràctiques del curs pots trobar `/usr/local/hadoop`, `/opt/hadoop` o `/opt/hadoop-3.3.1`. No barregis rutes d'instal·lacions diferents: adapta-les al teu sistema.

## 6. Descàrrega de Hive 3.1.3

**[GUIA]** La guia inclou un enllaç al servidor de descàrregues i un d'alternatiu a l'arxiu històric d'Apache:

```bash
wget https://dlcdn.apache.org/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz
```

Alternativa que també apareix:

```bash
wget https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz
```

L'opció `wget` descarrega el fitxer en el directori de treball. Un nom acabat en `.tar.gz` indica un conjunt de fitxers empaquetats amb `tar` i comprimits amb gzip.

**[AMPLIACIÓ]** Comprova que la descàrrega existeix abans de continuar:

```bash
ls -lh apache-hive-3.1.3-bin.tar.gz
file apache-hive-3.1.3-bin.tar.gz
```

⚠️ **[PRECAUCIÓ]** Els miralls actius poden deixar d'oferir versions antigues; per això la guia proporciona l'URL de `archive.apache.org`. Si es tracta d'una instal·lació sensible, convé verificar els checksums o signatures des de fonts oficials. No assumim que els dos URLs sempre estiguin disponibles.

## 7. Descompressió i organització de directoris

**[GUIA]**

```bash
tar zxvf apache-hive-3.1.3-bin.tar.gz
mv apache-hive-3.1.3-bin hive
rm apache-hive-3.1.3-bin.tar.gz
```

| Ordre | Significat |
|---|---|
| `tar` | Treballa amb un arxiu empaquetat |
| `z` | Descomprimeix gzip |
| `x` | Extreu contingut |
| `v` | Mostra fitxers a mesura que els extreu |
| `f` | Indica el fitxer sobre el qual opera |
| `mv ... hive` | Reanomena la carpeta extreta |
| `rm ...tar.gz` | Elimina el fitxer comprimit, no la carpeta extreta |

La ruta final prevista és `/home/hadoop/hive` si totes les ordres es fan des de `/home/hadoop`. Si s'ha executat `tar` en una altra carpeta, `HIVE_HOME` no apuntarà correctament a Hive.

**[AMPLIACIÓ]** Verificació:

```bash
ls -ld ~/hive
ls ~/hive/bin
ls ~/hive/conf
```

⚠️ `rm` és destructiu: elimina només l'arxiu indicat, però no el pots recuperar amb facilitat si no tens còpia. Mantén l'arxiu comprimit fins a haver verificat la instal·lació si vols poder repetir-la sense tornar-lo a descarregar.

## 8. Variables d'entorn del terminal

**[GUIA]** Obrim el fitxer de configuració del shell:

```bash
sudo nano ~/.bashrc
```

I afegim:

```bash
export HIVE_HOME=/home/hadoop/hive
export HIVE_CONF_DIR=$HIVE_HOME/conf
export HCAT_HOME=$HIVE_HOME/hcatalog
export PATH=$PATH:$HIVE_HOME/bin
export CLASSPATH=$CLASSPATH:/home/hadoop/hadoop/lib/*:.
export CLASSPATH=$CLASSPATH:/home/hadoop/hive/lib/*:.
```

Finalment:

```bash
source ~/.bashrc
```

**Explicació de les variables:**

- `HIVE_HOME`: carpeta principal de Hive.
- `HIVE_CONF_DIR`: carpeta que conté la configuració de Hive.
- `HCAT_HOME`: carpeta del component HCatalog, quan forma part del paquet.
- `PATH`: permet executar `hive`, `beeline` o `schematool` sense indicar-ne la ruta completa.
- `CLASSPATH`: defineix localitzacions on Java cerca classes i dependències; és sensible a versions i conflictes de JARs.

**[AMPLIACIÓ]** La comanda `source` aplica les modificacions al shell actual sense haver de tancar i tornar a obrir la sessió. Després:

```bash
printf '%s\n' "$HIVE_HOME" "$HIVE_CONF_DIR"
command -v hive
command -v beeline
```

⚠️ **[PRECAUCIÓ]** Normalment no cal `sudo` per editar el `~/.bashrc` de l'usuari propietari. Si s'executa amb `sudo`, verifica que realment s'està modificant el fitxer correcte. Les entrades de `CLASSPATH` són les de la guia, però afegir massa biblioteques globalment pot provocar conflictes entre Hadoop i Hive; no ho generalitzis a qualsevol entorn.

## 9. Fitxers de configuració de Hive

**[GUIA]** Entrem al directori de configuració i copiem les plantilles:

```bash
cd "$HIVE_HOME/conf"
cp hive-default.xml.template hive-site.xml
cp hive-env.sh.template hive-env.sh
cp hive-exec-log4j2.properties.template hive-exec-log4j2.properties
cp hive-log4j2.properties.template hive-log4j2.properties
```

| Fitxer | Finalitat |
|---|---|
| `hive-site.xml` | Propietats funcionals de Hive, del Metastore i de connexió JDBC |
| `hive-env.sh` | Variables d'entorn del procés Hive |
| `hive-exec-log4j2.properties` | Configuració de logging associada a execució |
| `hive-log4j2.properties` | Configuració general del logging de Hive |

**[AMPLIACIÓ]** Les ordres `cp` fallen si una plantilla no existeix a la versió instal·lada. És recomanable revisar primer `ls -1 "$HIVE_HOME/conf"`. No convé sobrescriure configuracions que ja funcionen: fes una còpia prèvia de `hive-site.xml` en entorns reutilitzats.

## 10. Configuració de `hive-env.sh`

**[GUIA]** La guia obre:

```bash
sudo nano "$HIVE_HOME/conf/hive-env.sh"
```

I incorpora:

```bash
export HADOOP_HOME=/home/hadoop/hadoop
export HIVE_CONF_DIR=/home/hadoop/hive/conf
```

**Què resol?** Els scripts d'arrencada de Hive han de localitzar Hadoop i els fitxers de configuració. `HADOOP_HOME` assenyala la instal·lació de Hadoop i `HIVE_CONF_DIR` el directori de paràmetres de Hive.

**[AMPLIACIÓ]** Revisa que les carpetes existeixen:

```bash
test -d "$HADOOP_HOME" && echo 'Hadoop localitzat'
test -f "$HIVE_CONF_DIR/hive-site.xml" && echo 'Configuració localitzada'
```

> **Errada de nom:** al text de la guia hi ha una referència a `hive.env.sh`, però el fitxer que edita la comanda és **`hive-env.sh`**, amb guió, no punt.

## 11. Integració amb Sqoop

**[GUIA]**

```bash
cp "$HIVE_HOME/lib/hive-common-3.1.3.jar" "$SQOOP_HOME/lib"
```

Aquesta còpia busca que Sqoop disposi d'una biblioteca de Hive necessària per a determinades funcionalitats d'importació a Hive de l'entorn docent.

**[AMPLIACIÓ]** Abans d'executar-la:

```bash
echo "$SQOOP_HOME"
ls "$HIVE_HOME/lib/hive-common-3.1.3.jar"
ls "$SQOOP_HOME/lib" | grep -i hive
```

⚠️ **[PRECAUCIÓ]** Sqoop és un projecte antic i els seus JAR poden tenir dependències incompatibles amb altres versions de Hive/Hadoop. La guia pressuposa una combinació concreta; no copiïs biblioteques a cegues en un sistema de producció. Per depurar una importació, comprova sempre que les versions de Sqoop, Hive, Hadoop i els connectors són coherents.

## 12. Preparació dels directoris HDFS

**[GUIA]**

```bash
hdfs dfs -mkdir /tmp
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chmod g+w /tmp
hdfs dfs -chmod g+w /user/hive/warehouse
```

`/tmp` s'utilitza per a operacions temporals de diverses eines Hadoop. `/user/hive/warehouse` és una ubicació habitual per a dades de taules gestionades en configuracions d'aquest tipus. `-mkdir -p` crea els directoris pares quan cal. `chmod g+w` afegeix permís d'escriptura al grup corresponent.

**[AMPLIACIÓ]** Comprovació dels permisos:

```bash
hdfs dfs -ls -d /tmp
hdfs dfs -ls -d /user/hive/warehouse
hdfs dfs -stat '%n %u %g %a' /user/hive/warehouse
```

⚠️ **[PRECAUCIÓ]** Si `/tmp` ja existeix, `hdfs dfs -mkdir /tmp` pot mostrar un error perquè la carpeta existeix. Una alternativa reexecutable és `hdfs dfs -mkdir -p /tmp`. El permís `g+w` només habilita escriptura per al grup propietari; si Hive s'executa amb un usuari o grup diferent, cal revisar propietaris i permisos. No és convenient substituir-ho per un `chmod 777` indiscriminat.

## 13. Compatibilitat de llibreries: Guava

**[GUIA]** La guia proposa eliminar un JAR antic de Hive i copiar-hi un altre des de Hadoop:

```bash
rm "$HIVE_HOME/lib/guava-19.0.jar"
cp "$HADOOP_HOME/share/hadoop/hdfs/lib/guava-27.0-jre.jar" "$HIVE_HOME/lib"
```

**[AMPLIACIÓ]** Guava és una biblioteca de Java utilitzada per projectes de l'ecosistema Hadoop. Quan existeixen versions incompatibles de les mateixes classes, poden aparèixer errors d'execució com `NoSuchMethodError`, `NoClassDefFoundError` o altres fallades d'enllaç. El problema no és que Guava sigui incorrecta, sinó que una aplicació pot requerir una versió específica.

**Procediment prudent de diagnòstic:**

```bash
find "$HIVE_HOME/lib" -maxdepth 1 -iname '*guava*' -print
find "$HADOOP_HOME" -iname '*guava*' -print
```

⚠️ **[PRECAUCIÓ IMPORTANT]** El pas de la guia és **específic de la seva combinació de versions**. No eliminis una biblioteca sense confirmar que els JAR esmentats existeixen i que realment hi ha un conflicte. Per poder tornar enrere, resulta preferible moure l'antic JAR a una carpeta de còpies *fora de `lib`* abans de provar el canvi. Si els noms del JAR són diferents, adapta la comanda després d'inspeccionar-los.

## 14. Configuració de proxyusers a Hadoop

**[GUIA]** Es demana editar `$HADOOP_HOME/etc/hadoop/core-site.xml` i afegir aquestes propietats si el compte és `iabd`:

```xml
<property>
  <name>hadoop.proxyuser.iabd.hosts</name>
  <value>*</value>
</property>
<property>
  <name>hadoop.proxyuser.iabd.groups</name>
  <value>*</value>
</property>
```

Després s'indica que cal reiniciar Hadoop perquè els processos carreguin els canvis.

**[AMPLIACIÓ]** Una identitat configurada com a *proxyuser* pot actuar en nom d'altres usuaris en les condicions autoritzades. Les propietats `.hosts` i `.groups` delimiten, respectivament, orígens autoritzats i grups d'usuaris sobre els quals és possible impersonar.

⚠️ **[PRECAUCIÓ DE SEGURETAT]** Els valors `*` autoritzen un abast molt ampli i només s'han de considerar en un laboratori controlat si realment són necessaris. En entorns reals s'han de restringir hosts i grups. A més, si el servei és executat per `hive` i no per `iabd`, la propietat que caldria revisar podria ser `hadoop.proxyuser.hive.*`, no `iabd.*`: depèn de quin usuari fa d'intermediari.

## 15. Configuració de Hue

**[GUIA]** El document demana revisar el fitxer `~/hue-overrides.ini`:

```bash
nano ~/hue-overrides.ini
```

Fragment de configuració del document, amb `IP_HOST` com a valor a substituir:

```ini
[beeswax]
hive_server_host=IP_HOST
hive_server_port=10000
hive_conf_dir=/home/hadoop/hive/conf

[hadoop]
[[hdfs_clusters]]
[[[default]]]
fs_defaultfs=hdfs://IP_HOST:9000
webhdfs_url=http://IP_HOST:9870/webhdfs/v1

[desktop]
[[database]]
engine=mysql
host=IP_HOST
port=3306
user=iabd
password=iabd
name=hue
```

**Què controla cada apartat?**

| Secció | Per a què serveix |
|---|---|
| `[beeswax]` | Indica el servidor Hive i el port de consultes |
| `[hadoop]` / HDFS | Configura l'accés al sistema de fitxers i a WebHDFS |
| `[desktop]` / `[[database]]` | Configura la base de dades interna que utilitza Hue |

**[AMPLIACIÓ]** Hi ha dues bases de dades conceptualment diferents: la **base del Metastore** de Hive (amb noms de taules i esquemes) i la **base de dades interna de Hue** (amb informació de la pròpia aplicació). Poden estar en la mateixa instància MariaDB, però no són el mateix esquema ni tenen la mateixa finalitat.

⚠️ **[PRECAUCIÓ]** La guia presenta un espai en `hdfs:// IP_HOST:9000` i `http:// IP_HOST:9870/...` per motius de maquetació. En un fitxer real **no hi ha d'haver espais després de `//`**. També cal substituir `IP_HOST` per una adreça o nom DNS real accessible *des del contenidor Hue*, no necessàriament `localhost`.

## 16. Execució de Hue amb Docker

**[GUIA]** La guia indica recrear el contenidor:

```bash
docker stop hue
docker rm hue

docker run -d --restart unless-stopped -p 8888:8888 \
  --add-host=nom-host:IP_HOST \
  -v ~/hue-overrides.ini:/usr/share/hue/desktop/conf/z-hue-overrides.ini \
  --name hue \
  gethue/hue:latest
```

**Explicació:** `stop` deté un contenidor; `rm` elimina el contenidor (no necessàriament els volums); `run` crea una nova instància; `-d` la deixa en segon pla; `--restart unless-stopped` gestiona reinicis; `-p 8888:8888` publica el port; `--add-host` crea una resolució de nom; `-v` munta el fitxer local de configuració.

**[AMPLIACIÓ]** Abans de fer `rm`, inspecciona l'estat:

```bash
docker ps -a --filter name=hue
docker logs --tail 60 hue
```

Després de recrear-lo:

```bash
docker ps
docker logs --tail 60 hue
```

⚠️ **[PRECAUCIÓ]** La comanda de la guia falla si el contenidor `hue` encara no existeix (això no és necessàriament un problema greu). `gethue/hue:latest` pot canviar amb el temps, per això és preferible fixar una etiqueta compatible quan es busca una pràctica reproduïble. Comprova que `~/hue-overrides.ini` existeix i és un fitxer, perquè un muntatge incorrecte pot provocar problemes. Substitueix `IP_HOST` i `nom-host` pels valors reals.

## 17. Configuració del fitxer `hive-site.xml`

**[GUIA]**

```bash
sudo nano "$HIVE_HOME/conf/hive-site.xml"
```

A continuació es defineixen les propietats que apareixen al document:

```xml
<!-- Noves propietats indicades a la guia -->
<property>
  <name>system:java.io.tmpdir</name>
  <value>/tmp/hive/java</value>
</property>
<property>
  <name>system:user.name</name>
  <value>${user.name}</value>
</property>
<property>
  <name>datanucleus.schema.autoCreateAll</name>
  <value>true</value>
</property>

<!-- Connexió JDBC al Metastore -->
<property>
  <name>javax.jdo.option.ConnectionURL</name>
  <value>jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true</value>
</property>
<property>
  <name>javax.jdo.option.ConnectionDriverName</name>
  <value>com.mysql.jdbc.Driver</value>
</property>
<property>
  <name>javax.jdo.option.ConnectionUserName</name>
  <value>iabd</value>
</property>
<property>
  <name>javax.jdo.option.ConnectionPassword</name>
  <value>iabd</value>
</property>
<property>
  <name>hive.metastore.event.db.notification.api.auth</name>
  <value>false</value>
</property>
```

**Interpretació dels paràmetres més importants:**

- `ConnectionURL`: indica on és MariaDB/MySQL i quin esquema (`hive`) ha d'utilitzar.
- `ConnectionDriverName`: classifica el connector JDBC que farà servir Java.
- `ConnectionUserName` i `ConnectionPassword`: credencials de la base de dades del Metastore.
- `datanucleus.schema.autoCreateAll`: controla aspectes de creació d'esquema segons la configuració/versió.
- `hive.metastore.event.db.notification.api.auth`: ajust d'autorització de notificacions del Metastore que figura a la guia.

**[AMPLIACIÓ]** Un fitxer XML requereix una única arrel `<configuration>` i cada `<property>` ha de quedar dins d'aquesta arrel. **No copiïs un segon bloc `<configuration>` dins del primer.** Busca cada propietat abans d'afegir-la; tenir duplicats pot complicar el diagnòstic. Si utilitzes el `hive-site.xml` generat a partir d'una plantilla llarga, revisa les línies que la guia diu que poden contenir caràcters estranys; el número concret de línia pot canviar segons el paquet.

⚠️ **[PRECAUCIÓ]** `com.mysql.jdbc.Driver` correspon al connector antic que usa la guia. Els connectors moderns solen utilitzar `com.mysql.cj.jdbc.Driver`. No canviïs el nom sense revisar la versió del JAR. Les credencials `iabd/iabd` són un exemple docent: no són adequades com a credencials de producció. La desactivació d'autoritzacions i la creació automàtica d'esquemes s'han de valorar segons l'entorn.

## 18. Preparació de MariaDB com a Metastore

**[GUIA]**

```bash
sudo mysql -u root -p
```

Un cop dins de la consola SQL:

```sql
CREATE DATABASE hive;
GRANT ALL PRIVILEGES ON hive.* TO 'iabd'@'localhost';
QUIT;
```

La base `hive` és l'esquema persistent on el Metastore desarà taules de metadades. El privilegi sobre `hive.*` fa referència a tots els objectes de la **base de dades `hive`**, no a totes les bases de dades del servidor.

**[AMPLIACIÓ]** Comprovacions:

```bash
sudo systemctl status mariadb
mysql -u iabd -p -e 'SHOW DATABASES;'
```

Si l'usuari `iabd` no existeix encara, el `GRANT` pot fallar segons la versió i les polítiques de MariaDB/MySQL. En aquest cas cal crear abans l'usuari amb una contrasenya apropiada i posteriorment concedir els privilegis mínims. Si l'esquema `hive` ja existeix, `CREATE DATABASE hive` retorna un error; `CREATE DATABASE IF NOT EXISTS hive` evita això en una preparació reexecutable.

## 19. Connector JDBC MySQL

**[GUIA]** Es descarrega un connector antic i es mou a la carpeta de biblioteques de Hive:

```bash
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.49/mysql-connector-java-5.1.49.jar
mv mysql-connector-java-5.1.49.jar "$HIVE_HOME/lib/"
```

Sense un driver JDBC adequat, el Metastore no pot obrir la connexió configurada amb `jdbc:mysql://...`. Java necessita la classe del driver dins del classpath del procés.

**[AMPLIACIÓ]** Verificació:

```bash
ls -lh "$HIVE_HOME/lib/"*mysql* 2>/dev/null
```

⚠️ **[PRECAUCIÓ]** La versió 5.1.49 està lligada a l'exemple del document. Alguns connectors i bases modernes poden requerir una altra versió i un altre nom de classe. Si apareix `ClassNotFoundException` o `No suitable driver`, el primer diagnòstic és verificar tant la presència del JAR com la coincidència entre el driver i `ConnectionDriverName`.

## 20. Inicialització de l'esquema amb `schematool`

**[GUIA]**

```bash
schematool -dbType mysql -initSchema
```

**Què fa?** Crea l'estructura interna de taules i objectes que Hive necessita a la base de metadades. És diferent de crear simplement `CREATE DATABASE hive;` a MariaDB. La base buida existeix, però encara no conté necessàriament l'esquema que el servei Metastore espera.

**[AMPLIACIÓ]** Opcions de comprovació que poden estar disponibles segons la versió:

```bash
schematool -dbType mysql -info
```

⚠️ **[PRECAUCIÓ]** `-initSchema` és una operació d'inicialització, no una ordre que cal executar a cada arrencada. Si la base ja està inicialitzada, repetir-la pot generar errors. Les actualitzacions d'esquema entre versions de Hive segueixen procediments diferents dels d'una instal·lació nova.

## 21. Arrencada del Metastore

**[GUIA]**

```bash
hive --service metastore
```

Aquesta ordre inicia el servei de metadades. En la configuració habitual que descriu la guia, el port del servei és `9083`. El servei s'ha de mantenir actiu mentre els clients que utilitzin un Metastore remot facin consultes.

**[AMPLIACIÓ]** Des d'un altre terminal:

```bash
jps
ss -ltn | grep 9083
```

⚠️ L'absència del port pot indicar que el servei no ha arrencat o que està configurat en un altre port. La presència del port no garanteix que la connexió amb MariaDB sigui correcta; revisa també els logs.

## 22. Hive CLI: ús i limitacions

**[GUIA]** El document explica que, en una altra sessió, podem entrar a Hive amb:

```bash
hive
```

I treballar amb ordres SQL:

```sql
SHOW DATABASES;
-- Exemple conceptual del document:
SELECT * FROM alumnes;
```

**[AMPLIACIÓ]** Hive CLI és un client tradicional que executa consultes dins del procés del client i té limitacions en comparació amb la via HiveServer2. Per això el document acaba recomanant HiveServer2 més Beeline com a seqüència d'ús habitual. La taula `alumnes` no existirà fins que s'hagi creat; el `SELECT` que apareix a la guia és un exemple de sintaxi.

## 23. Arrencada de HiveServer2

**[GUIA]**

```bash
hive --service hiveserver2
```

HiveServer2 és el servei que permet que programes externs s'hi connectin utilitzant protocols i connectors JDBC/ODBC. El port habitual del document és `10000`.

**[AMPLIACIÓ]** Comprovacions bàsiques:

```bash
jps
ss -ltn | grep 10000
```

**Exemple d'error:** si `beeline` indica `Connection refused`, comprova si HiveServer2 és en execució, si està escoltant a l'adreça esperada i si existeix un tallafoc o problema de DNS. Si la connexió s'estableix però les consultes fallen, el problema pot ser de Metastore, permisos o execució.

## 24. Connexió amb Beeline

**[GUIA]** En una tercera sessió:

```bash
beeline -u jdbc:hive2://localhost:10000
```

La guia planteja aquesta seqüència típica:

```bash
# Terminal 1
hive --service metastore

# Terminal 2
hive --service hiveserver2

# Terminal 3
beeline -u jdbc:hive2://localhost:10000
```

**[AMPLIACIÓ]** Una vegada connectat:

```sql
SHOW DATABASES;
CREATE DATABASE IF NOT EXISTS prova_hive;
USE prova_hive;
SHOW TABLES;
```

`localhost` significa la màquina des de la qual s'executa Beeline. Si Beeline s'executa des d'un altre ordinador o dins d'un contenidor, cal utilitzar el nom DNS o la IP del servidor HiveServer2 accessible per aquell client. Els noms d'usuari i la forma d'autenticació depenen de la configuració del servidor.

## 25. Flux complet d'una consulta

**[GUIA + AMPLIACIÓ]** La darrera secció de la guia presenta un esquema amb Beeline, HiveServer2, Metastore i HDFS. Despleguem-lo pas a pas:

1. Un usuari escriu `SELECT * FROM alumnes;` des de Beeline.
2. Beeline envia la consulta a HiveServer2 a través de JDBC.
3. HiveServer2 interpreta la consulta i consulta informació de taules i columnes al Metastore.
4. El Metastore obté la informació del catàleg de MariaDB i la retorna al servidor.
5. Hive prepara i executa el pla necessari; segons la consulta i el motor, això pot implicar YARN i processos distribuïts.
6. Es llegeixen els fitxers a HDFS si la taula es basa en aquesta ubicació.
7. HiveServer2 retorna el resultat a Beeline.

```text
[Usuari] -> [Beeline] --JDBC:10000--> [HiveServer2]
                                          |
                                          +--Metastore:9083--> [MariaDB:3306]
                                          |
                                          +--Motor de consulta--> [HDFS / YARN]
                                          |
[Usuari] <- [Beeline] <-------------------+ (resultat)
```

**Idea d'examen:** el Metastore no desa les files de la taula com a dades de negoci; desa les definicions i metadades necessàries perquè els motors sàpiguen interpretar i localitzar els fitxers.

## 26. Pràctica de comprovació de la instal·lació

**[AMPLIACIÓ]** Aquesta pràctica final no apareix com una activitat completa al document original, però ajuda a verificar que tot el recorregut funciona.

**Pas 1.** Comprovar HDFS i els serveis:

```bash
hdfs dfs -ls /
jps
```

**Pas 2.** Entrar per Beeline després d'haver arrencat els dos serveis:

```bash
beeline -u jdbc:hive2://localhost:10000
```

**Pas 3.** Crear una base i una taula petites:

```sql
CREATE DATABASE IF NOT EXISTS proves_installacio;
USE proves_installacio;
CREATE TABLE IF NOT EXISTS salut_hive (
    id INT,
    missatge STRING
);
SHOW TABLES;
DESCRIBE salut_hive;
```

**Pas 4.** Inserir un exemple i consultar-lo (si l'entorn admet aquesta operació):

```sql
INSERT INTO salut_hive VALUES (1, 'Hive funciona');
SELECT * FROM salut_hive;
```

**Pas 5.** Inspeccionar metadades:

```sql
DESCRIBE FORMATTED salut_hive;
```

**Què cal observar?** La taula ha de figurar en el catàleg, la consulta ha de retornar el registre i `DESCRIBE FORMATTED` ha de mostrar-ne propietats, inclosa la ubicació de les dades. Si `SHOW TABLES` funciona però l'`INSERT` falla, el problema podria ser l'execució de consultes, els permisos o el motor, no necessàriament el Metastore.

## 27. Ports, processos i fitxers clau

### Ports

| Port | Servei | Funció |
|---|---|---|
| 3306 | MariaDB/MySQL | Persistència de metadades |
| 9083 | Metastore Server | API de metadades de Hive |
| 10000 | HiveServer2 | Connexions de Beeline/JDBC |
| 9000 | HDFS (segons configuració del curs) | Accés a HDFS |
| 9870 | NameNode UI / WebHDFS | Interfície web i API HTTP |
| 8888 | Hue Docker (guia) | Interfície Hue publicada al host |

### Fitxers

| Fitxer | Propòsit |
|---|---|
| `~/.bashrc` | Variables de terminal |
| `$HIVE_HOME/conf/hive-env.sh` | Variables per als processos de Hive |
| `$HIVE_HOME/conf/hive-site.xml` | Connexions i paràmetres de Hive |
| `$HADOOP_HOME/etc/hadoop/core-site.xml` | Configuració general de Hadoop, proxyuser i FS |
| `~/hue-overrides.ini` | Configuració particular de Hue |
| `$HIVE_HOME/lib/*.jar` | Dependències Java de Hive |

**Recorda:** aquests són ports i rutes de la **configuració explicada a la guia**, no valors invariables per a tots els desplegaments.

## 28. Problemes freqüents i diagnòstic

| Símptoma | Causes possibles | Comprovació inicial |
|---|---|---|
| `hive: command not found` | `PATH` mal definit o carpeta errònia | `echo "$HIVE_HOME"; command -v hive` |
| `JAVA_HOME is not set` | Java no localitzat pel procés | `java -version; echo "$JAVA_HOME"` |
| `Connection refused` des de Beeline | HiveServer2 aturat, port/host incorrecte | `jps; ss -ltn` |
| Error `ClassNotFoundException` del driver | Falta el JAR JDBC o no coincideix classe/versió | `ls "$HIVE_HOME/lib"/*mysql*` |
| `Access denied` a MySQL | Usuari, contrasenya o privilegis incorrectes | `mysql -u iabd -p` |
| Metastore schema no inicialitzat | Falta `schematool -initSchema` | `schematool -dbType mysql -info` |
| Error de biblioteca Guava | Versions de JAR incompatibles | `find "$HIVE_HOME/lib" -iname '*guava*'` |
| Hue no mostra les taules | HiveServer2 no accessible des del contenidor | Revisar `hue-overrides.ini` i `docker logs hue` |
| Hue no accedeix a HDFS | WebHDFS/host/port/permisos incorrectes | Revisar URL i serveis HDFS |
| `Permission denied` a warehouse | Falta permís per al compte que executa Hive | `hdfs dfs -ls -d /user/hive/warehouse` |
| Error en arrencar el Metastore | Configuració JDBC, base no accessible o port ocupat | Logs, port 9083 i credencials |
| XML invàlid | Propietat duplicada, caràcter estrany, etiqueta mal tancada | Revisar sintaxi de `hive-site.xml` |

**Procediment ordenat de diagnòstic:**

1. Comprova la ruta i la versió de Java i Hadoop.
2. Comprova l'existència dels fitxers de Hive.
3. Comprova MariaDB i les credencials.
4. Revisa la configuració XML i el driver JDBC.
5. Comprova que `schematool` reconegui l'esquema.
6. Arrenca Metastore i confirma el servei.
7. Arrenca HiveServer2 i confirma el servei.
8. Connecta Beeline, i només després revisa Hue.

Aquest ordre és útil perquè evita investigar l'última capa abans de verificar les dependències inferiors.

## 29. Seguretat, permisos i precaucions

**[AMPLIACIÓ CRÍTICA]** El material docent busca facilitar una instal·lació reproduïble en un laboratori, però determinades decisions no són adequades per a entorns compartits o de producció.

- **Credencials planes:** la guia utilitza `iabd/iabd` al XML i a Hue. En una instal·lació real cal gestionar secrets amb mecanismes apropiats i restringir l'accés als fitxers.
- **Proxyuser amb `*`:** permet una autorització excessivament àmplia; limita l'abast d'usuaris/grups i hosts.
- **Versions de dependències:** substituir JAR manualment pot solucionar una incompatibilitat concreta però trencar-ne una altra; documenta cada canvi.
- **Permisos d'HDFS:** concedir `g+w` pressuposa que el grup del servei és el correcte; revisa propietaris i permisos abans de modificar-los.
- **MariaDB al port 3306:** no cal exposar-lo a Internet; només hauria de ser accessible des dels serveis que el necessiten.
- **Ports de Hive i Hue:** restringeix l'accés de xarxa i defineix mecanismes d'autenticació; evita confiar només en un entorn sense seguretat.
- **Docker:** elimina el contenidor `hue` només quan entenguis on es persisteixen les dades i la configuració.
- **Esquema del Metastore:** `schematool -initSchema` és d'instal·lació inicial; no el repeteixis de manera indiscriminada.
- **Compatibilitat temporal:** la guia utilitza Hive 3.1.3 i Hadoop 3.4.3; no s'ha verificat aquí que totes les dependències de qualsevol instal·lació nova siguin compatibles. Utilitza els passos com a referència de l'entorn docent.

## 30. Checklist i seqüència recomanada

### Checklist abans d'arrencar

- [ ] L'usuari i les rutes coincideixen amb els de la màquina.
- [ ] Java i Hadoop responen correctament.
- [ ] HDFS està disponible.
- [ ] `HIVE_HOME` apunta a la carpeta real de Hive.
- [ ] Els fitxers `hive-env.sh` i `hive-site.xml` existeixen.
- [ ] El driver JDBC de MySQL és present i compatible.
- [ ] La base de dades `hive` està creada i l'usuari hi té accés.
- [ ] L'esquema del Metastore està inicialitzat.
- [ ] Els directoris HDFS tenen els permisos necessaris.
- [ ] No s'han barrejat JAR incompatibles.
- [ ] Les variables de Hue tenen adreces i ports correctes.

### Seqüència de terminals

```bash
# Terminal A: iniciar el Metastore, si la configuració l'utilitza remot
hive --service metastore
```

```bash
# Terminal B: iniciar HiveServer2
hive --service hiveserver2
```

```bash
# Terminal C: connectar el client
beeline -u jdbc:hive2://localhost:10000
```

El document també mostra comandes en segon pla amb `&`, però en una pràctica d'aprenentatge resulta més fàcil diagnosticar incidències mantenint inicialment els processos en terminals diferents. La disponibilitat del port i els logs serveixen per verificar l'arrencada.

---

## 31. 55 preguntes d'autoavaluació resoltes

**1. Quina és la finalitat de Hive?** Permetre definir estructures de taules i consultar dades dins de l'ecosistema Hadoop amb llenguatge semblant a SQL.

**2. Hive substitueix HDFS?** No. Pot utilitzar HDFS com a capa de dades.

**3. Què és el Metastore?** El repositori de metadades de bases de dades, taules, columnes i localitzacions.

**4. On es persisteixen les metadades en aquesta guia?** En un esquema `hive` de MariaDB/MySQL.

**5. Què és HiveServer2?** El servei que rep consultes de clients com Beeline i clients JDBC/ODBC.

**6. Què és Beeline?** Un client de línia d'ordres que es connecta a HiveServer2.

**7. Què fa `cd ~`?** Entra al directori personal de l'usuari actual.

**8. Quin paquet es descarrega?** `apache-hive-3.1.3-bin.tar.gz`.

**9. Què fa `wget`?** Descarrega un recurs des d'una URL.

**10. Per què hi ha dues URLs de descàrrega?** Per disposar d'una alternativa a l'arxiu històric d'Apache.

**11. Què significa `tar zxvf`?** Descomprimir gzip, extreure, mostrar fitxers i indicar un arxiu.

**12. Per què es reanomena la carpeta?** Per disposar de la ruta estable `/home/hadoop/hive`.

**13. Què significa `HIVE_HOME`?** La carpeta principal de la instal·lació de Hive.

**14. Què significa `HIVE_CONF_DIR`?** El directori dels fitxers de configuració.

**15. Què indica `HCAT_HOME`?** La ruta de HCatalog dins de la instal·lació.

**16. Per què s'amplia `PATH`?** Per executar els programes de Hive sense posar-ne la ruta completa.

**17. Què és `CLASSPATH`?** Un conjunt de rutes que Java pot utilitzar per trobar classes i biblioteques.

**18. Què fa `source ~/.bashrc`?** Recarrega les variables al shell actual.

**19. Què és `hive-site.xml`?** Un fitxer de propietats de Hive i els serveis associats.

**20. Què és `hive-env.sh`?** L'script de variables d'entorn dels processos Hive.

**21. Quin fitxer porta les variables per a l'arrencada del procés?** `hive-env.sh`, no `hive.env.sh`.

**22. Per què es copia un JAR a Sqoop?** Per aportar una dependència necessària a la integració concreta descrita a la guia.

**23. Quin directori HDFS és el warehouse?** `/user/hive/warehouse` en aquesta configuració.

**24. Què fa `hdfs dfs -mkdir -p`?** Crea el directori i també els pares necessaris.

**25. Què fa `chmod g+w`?** Afegeix permís d'escriptura al grup propietari.

**26. Què és Guava?** Una biblioteca Java utilitzada per diversos components Hadoop/Hive.

**27. Quin risc té substituir Guava?** Provocar o resoldre conflictes de dependències segons les versions instal·lades.

**28. On es configuren els proxyusers Hadoop?** A `core-site.xml`.

**29. Què vol dir `hosts=*`?** Autoritzar qualsevol host segons aquella propietat; és massa permissiu fora d'un laboratori.

**30. Per què cal reiniciar Hadoop després de canviar `core-site.xml`?** Perquè els processos hagin de carregar la nova configuració.

**31. Quin fitxer de Hue edita la guia?** `~/hue-overrides.ini`.

**32. Quin port utilitza HiveServer2 a la guia?** `10000`.

**33. Quin port utilitza el Metastore remot habitual?** `9083`.

**34. Quin port utilitza MariaDB/MySQL?** Habitualment `3306`.

**35. Què és WebHDFS?** Una interfície HTTP per operar amb HDFS.

**36. Quin port web del NameNode apareix?** `9870`.

**37. Quin port Docker de Hue exposa la guia?** `8888` al host i al contenidor.

**38. Què fa `docker stop hue`?** Atura el contenidor amb aquell nom.

**39. Què fa `docker rm hue`?** Elimina el contenidor, no necessàriament els volums.

**40. Què fa `--restart unless-stopped`?** Configura una política de reinici del contenidor.

**41. Què fa `--add-host`?** Afegeix una entrada de resolució de nom al contenidor.

**42. Què fa `-v` a Docker?** Munta fitxers o directoris entre host i contenidor.

**43. Per què `localhost` pot fallar dins de Hue?** Perquè fa referència al contenidor, no automàticament al host de Hadoop.

**44. Què identifica `ConnectionURL` a `hive-site.xml`?** La URL JDBC de la base del Metastore.

**45. Per a què serveix `ConnectionDriverName`?** Per identificar la classe del driver JDBC que Java carregarà.

**46. Quina base de dades es crea a la guia?** `hive`.

**47. Què fa `GRANT ALL PRIVILEGES ON hive.*`?** Dona privilegis sobre els objectes de l'esquema `hive` a l'usuari indicat.

**48. Què fa `schematool -dbType mysql -initSchema`?** Inicialitza les taules internes requerides pel Metastore.

**49. Cal executar `-initSchema` a cada arrencada?** No, és una operació inicial d'esquema.

**50. Quina ordre arrenca el Metastore?** `hive --service metastore`.

**51. Quina ordre arrenca HiveServer2?** `hive --service hiveserver2`.

**52. Quina ordre obre Hive CLI?** `hive`.

**53. Quina ordre connecta Beeline local?** `beeline -u jdbc:hive2://localhost:10000`.

**54. Quina diferència hi ha entre Metastore i HiveServer2?** El primer proporciona metadades; el segon rep i processa consultes de clients.

**55. Quina és la prova mínima del client?** Connectar Beeline i executar `SHOW DATABASES;`.

---

## 32. Exercicis pràctics amb solució

### Exercici 1 — Ruta d'instal·lació incorrecta

**Enunciat:** `HIVE_HOME=/home/hadoop/hive`, però el directori extret és `/home/hadoop/apache-hive-3.1.3-bin`. Què falla?

**Solució:** Hive no està a la ruta indicada. Cal reanomenar la carpeta o modificar `HIVE_HOME` i recarregar `.bashrc`:

```bash
mv ~/apache-hive-3.1.3-bin ~/hive
source ~/.bashrc
```

### Exercici 2 — No es troba `beeline`

**Solució:** comprova `PATH` i `$HIVE_HOME/bin`:

```bash
echo "$PATH"
ls "$HIVE_HOME/bin/beeline"
command -v beeline
```

### Exercici 3 — Beeline mostra `Connection refused`

**Solució:** primer verifica el servei HiveServer2, no reinstal·lis Hive d'entrada:

```bash
jps
ss -ltn | grep 10000
```

### Exercici 4 — MariaDB rebutja l'usuari

**Solució:** comprova la connexió amb credencials reals i el dret d'accés a `hive`:

```bash
mysql -u iabd -p -e 'SHOW DATABASES;'
```

Si no connecta, revisa usuari, contrasenya i privilegis abans d'executar `schematool`.

### Exercici 5 — El Metastore no troba el driver

**Solució:** revisa el JAR i la classe configurada:

```bash
ls "$HIVE_HOME/lib/"*mysql*
grep -n 'ConnectionDriverName' "$HIVE_HOME/conf/hive-site.xml"
```

### Exercici 6 — Hue mostra error de connexió a Hive

**Solució:** comprova que HiveServer2 estigui operatiu i que l'host de `hue-overrides.ini` sigui accessible des del contenidor. Inspecciona els logs:

```bash
docker logs --tail 80 hue
```

### Exercici 7 — Escriure al warehouse retorna permís denegat

**Solució:** identifica propietari, grup i permisos:

```bash
hdfs dfs -ls -d /user/hive/warehouse
hdfs dfs -stat '%u %g %a' /user/hive/warehouse
```

Ajusta només els permisos necessaris segons el compte real del servei.

### Exercici 8 — Dues bases amb el nom `hive`?

**Enunciat:** Hue té una base de dades interna i Hive un Metastore. Són el mateix?

**Solució:** no. El Metastore de Hive guarda el catàleg d'Hive. La base pròpia de Hue guarda informació de l'aplicació Hue. La guia defineix els esquemes `hive` i `hue` amb finalitats separades.

### Exercici 9 — Comprovar la connexió sense modificar dades

**Solució:** utilitza Beeline i consultes de lectura:

```sql
SHOW DATABASES;
SHOW TABLES;
```

Si el compte s'ha connectat a una base de dades que no és la prevista, utilitza `USE nom_base;`.

### Exercici 10 — Resumir l'arquitectura en una frase

**Solució:** Beeline envia SQL a HiveServer2; HiveServer2 obté la informació de les taules del Metastore, persisteix les metadades a MariaDB i coordina l'accés a dades que poden estar emmagatzemades a HDFS.

---

## 33. Glossari i resum de memòria

| Concepte | Definició breu |
|---|---|
| Apache Hive | Plataforma de taules i consultes sobre dades de l'ecosistema Hadoop |
| HiveQL / HQL | Llenguatge de consulta similar a SQL |
| HDFS | Sistema de fitxers distribuït de Hadoop |
| YARN | Gestor de recursos i d'execució d'aplicacions del clúster |
| Metastore | Servei/repositori de definicions de taules i metadades |
| MariaDB | Sistema relacional que pot persistir les metadades |
| HiveServer2 | Servidor de consultes per a clients externs |
| Beeline | Client JDBC en línia d'ordres |
| Hive CLI | Client tradicional de Hive |
| Hue | Interfície web per interactuar amb eines Hadoop |
| Sqoop | Eina per transferir dades entre bases relacionals i Hadoop |
| JDBC | Tecnologia de connexió de Java amb bases de dades/serveis de consulta |
| JAR | Arxiu de biblioteques o aplicacions Java |
| `HIVE_HOME` | Ruta principal de la instal·lació |
| `hive-site.xml` | Configuració de Hive |
| `hive-env.sh` | Variables dels processos de Hive |
| `schematool` | Utilitat d'inicialització i gestió de l'esquema del Metastore |
| Proxyuser | Identitat autoritzada a actuar en nom d'altres usuaris dins de límits definits |
| WebHDFS | API HTTP d'HDFS |
| Warehouse | Ubicació habitual dels fitxers de taules gestionades |

### Les cinc idees que cal dominar

1. **Hive és una capa de consulta**, no una substitució d'HDFS.
2. **Metastore gestiona metadades**; MariaDB les pot persistir en un esquema relacional.
3. **HiveServer2 rep consultes**, i Beeline és el client que s'hi connecta.
4. La instal·lació exigeix **coherència de versions i rutes** de Hadoop, Hive, Sqoop, JDBC i Java.
5. **Arrencar un servei és diferent d'inicialitzar-lo**: `schematool` prepara l'esquema; `metastore` i `hiveserver2` executen els serveis.

### Minifitxa per memoritzar comandes

```bash
# Instal·lació i entorn
cd ~
tar zxvf apache-hive-3.1.3-bin.tar.gz
source ~/.bashrc

# Preparar HDFS
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -ls -d /user/hive/warehouse

# Inicialització (només si la base encara no està preparada)
schematool -dbType mysql -initSchema

# Arrencada
hive --service metastore
hive --service hiveserver2

# Client
beeline -u jdbc:hive2://localhost:10000
```

---

## 34. Referències al document original

Aquests apunts s'han elaborat a partir del fitxer de classe **`M5075_Tema2_Activitat 6 Instal·lació de Hive_v02.docx`**, de 9 pàgines. Per localitzar les explicacions al document original:

- **Pàgines 1–2:** descàrrega, instal·lació, variables d'entorn, fitxers de configuració, Sqoop, directoris d'HDFS i Guava.
- **Pàgines 2–3:** `core-site.xml`, proxyusers i configuració de Hue.
- **Pàgines 3–5:** contenidor Docker Hue, `hive-site.xml`, MariaDB, driver MySQL, `schematool` i arrencada.
- **Pàgines 5–9:** diferències entre Hive CLI, Metastore i HiveServer2, arquitectura de consultes i ús de Beeline.

Les seccions d'explicació conceptual, diagnòstic, pràctiques i autoavaluació són **ampliacions pedagògiques**; les recomanacions sobre permisos, seguretat, drivers i dependències són **precaucions** i no substitueixen la configuració validada pel professor en la màquina virtual del curs.

**Fi dels apunts.**
