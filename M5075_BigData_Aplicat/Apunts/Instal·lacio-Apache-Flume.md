# Apache Flume — Apunts extensos d'instal·lació

## Com utilitzar aquests apunts

La guia original és molt breu i consta de dues pàgines. Aquests apunts **reprodueixen tots els passos i les comandes de la guia**, n'expliquen el significat i hi afegeixen comprovacions, bones pràctiques, diagnòstic d'errors i exercicis d'autoavaluació. Per distingir l'origen del contingut:

- **[GUIA]**: procediment o informació que apareix al PDF.
- **[AMPLIACIÓ]**: explicació, comprovació o recomanació afegida per facilitar l'aprenentatge; no és un pas exigit explícitament pel PDF.

**Important:** la ruta `/home/hadoop/flume` és la que especifica el document. Si instal·les Flume amb un usuari o directori diferent, has d'adaptar-la. Els exemples de configuració i verificació poden dependre de la instal·lació de Java, Hadoop i dels permisos de la màquina.

---

## 1. Objectiu de l'activitat

**[GUIA]** L'activitat 5a consisteix a instal·lar Apache Flume a partir d'un paquet comprimit, ubicar els fitxers en una carpeta anomenada `flume`, configurar les variables d'entorn del shell i apartar una llibreria Guava que pot causar conflictes.

**[AMPLIACIÓ]** En acabar, hauríem de ser capaços de:

1. Reconèixer els components principals del flux de dades de Flume.
2. Descarregar i descomprimir la distribució indicada.
3. Localitzar la carpeta d'instal·lació i la carpeta de configuració.
4. Entendre el contingut del fitxer `~/.bashrc`.
5. Recarregar les variables sense haver de reiniciar l'equip.
6. Verificar que la comanda `flume-ng` està disponible.
7. Identificar errors de ruta, permisos, Java i dependències.

### Abast exacte de la guia

El PDF **no** inclou la creació d'agents, el fitxer de configuració d'un agent, la posada en marxa d'HDFS ni cap prova d'ingesta. Per això, aquests apunts se centren en **instal·lar i comprovar Flume** i només ofereixen un exemple pràctic opcional al final, separat del procediment oficial.

---

## 2. Què és Apache Flume?

**[AMPLIACIÓ]** Apache Flume és una eina d'ingesta de dades, especialment útil per recollir registres, missatges i esdeveniments, transportar-los mitjançant un flux configurable i enviar-los cap a una destinació d'emmagatzematge, com HDFS.

La idea més important és que Flume organitza el moviment de dades mitjançant **agents**. Aquests agents incorporen tres elements:

| Component | Nom en anglès | Funció |
|---|---|---|
| Font | `Source` | Rep els esdeveniments des de l'origen. |
| Canal | `Channel` | Actua com a buffer o cua temporal. |
| Destinació | `Sink` | Consumeix esdeveniments del canal i els envia a la sortida. |

### 2.1. Arquitectura representada a la portada

**[GUIA, pàgina 1]** El diagrama mostra un **servidor web** que envia dades a un **agent Flume**, format per `Source`, `Channel` i `Sink`, i finalment cap a **HDFS**.

```text
+---------------+      +------------------------------------+      +-------+
| Servidor web  | ---> | Agent Apache Flume                 | ---> | HDFS  |
| (origen)      |      | Source ---> Channel ---> Sink       |      |       |
+---------------+      +------------------------------------+      +-------+
```

**[AMPLIACIÓ]** El `Channel` desacobla el ritme d'arribada de dades del ritme amb què es poden escriure al destí. Per exemple, una font pot continuar rebent esdeveniments mentre el sink els va consumint, sempre que hi hagi capacitat al canal. Un canal de memòria és ràpid, però els esdeveniments no confirmats poden perdre's si el procés cau; un canal de fitxer prioritza la recuperació davant de fallades.

### 2.2. Conceptes essencials

- **Agent:** procés de Flume que conté fonts, canals i destinacions.
- **Esdeveniment:** unitat de dades transportada per Flume; acostuma a contenir un cos i capçaleres.
- **Ingesta:** recepció i introducció de dades al pipeline.
- **Buffer:** espai temporal on les dades esperen ser consumides.
- **HDFS:** sistema de fitxers distribuït de l'ecosistema Hadoop.
- **Variable d'entorn:** valor disponible per als processos del shell; permet evitar rutes escrites repetidament.
- **Classpath:** conjunt de rutes de recursos o classes que Java pot consultar.

---

## 3. Preparació abans d'instal·lar

**[AMPLIACIÓ]** La guia parteix d'un entorn Linux amb shell Bash. Abans de fer els passos es pot revisar:

```bash
whoami
pwd
printf 'HOME=%s\n' "$HOME"
java -version
command -v wget
command -v tar
```

- `whoami`: mostra l'usuari actual.
- `pwd`: mostra el directori actual.
- `$HOME`: directori personal de l'usuari.
- `java -version`: comprova que Java és accessible; Flume necessita Java per executar-se.
- `command -v`: comprova si el shell troba una eina executable.

**Precaució amb els permisos:** `/home/hadoop/flume` serà útil si aquesta carpeta existeix i és accessible per l'usuari que instal·la Flume. La guia no explica explícitament en quin directori inicial s'executa `wget`; aquest detall condiciona on quedarà la carpeta després de `mv`.

### 3.1. Situació ideal abans de començar

```text
/home/hadoop/
└── (encara no hi ha el directori flume)
```

Si el sistema utilitza un usuari diferent, per exemple `/home/iabd`, es pot instal·lar allí, però llavors **cal canviar `FLUME_HOME` en conseqüència**. No s'ha de copiar literalment una ruta que no coincideix amb la ubicació real.

---

## 4. Pas 1: descarregar el paquet

**[GUIA, pàgina 1]**

```bash
wget https://dlcdn.apache.org/flume/1.11.0/apache-flume-1.11.0-bin.tar.gz
```

### Explicació

- `wget` és una eina de terminal per descarregar arxius.
- `https://` especifica el protocol de transferència segur.
- `dlcdn.apache.org` és el domini del servidor de descàrregues indicat.
- `flume/1.11.0/` identifica la versió utilitzada a la guia.
- `apache-flume-1.11.0-bin.tar.gz` és el nom del paquet binari comprimit.

**[AMPLIACIÓ]** La disponibilitat d'aquesta URL pot variar amb el temps. Si dona un error HTTP, no vol dir necessàriament que la comanda tingui una sintaxi incorrecta; pot ser necessari obtenir la mateixa versió de l'arxiu històric oficial d'Apache i comprovar que es tracta de la distribució adequada.

### Verificar la descàrrega

```bash
ls -lh apache-flume-1.11.0-bin.tar.gz
file apache-flume-1.11.0-bin.tar.gz
```

`ls -lh` indica existència i mida llegible. `file` intenta identificar el tipus de fitxer.

**Possible error:** `wget: command not found` → l'eina no està instal·lada o no es troba al `PATH`.

---

## 5. Pas 2: descomprimir el paquet

**[GUIA, pàgina 1]**

```bash
tar -xvf apache-flume-1.11.0-bin.tar.gz
```

### Què significa `tar -xvf`?

| Opció | Significat | Efecte |
|---|---|---|
| `-x` | extract | Extreu el contingut de l'arxiu. |
| `-v` | verbose | Mostra els fitxers que s'extreuen. |
| `-f` | file | Indica que el següent argument és l'arxiu a tractar. |

**[AMPLIACIÓ]** En molts sistemes `tar` reconeix la compressió gzip de manera automàtica. També es pot trobar la sintaxi explícita `tar -xzvf ...`, on `-z` indica gzip.

### Verificar la carpeta creada

```bash
ls -ld apache-flume-1.11.0-bin
ls apache-flume-1.11.0-bin
```

La carpeta contindrà la distribució de Flume, amb subdirectoris dedicats als executables, la configuració i les dependències.

### Diferència entre `.tar` i `.gz`

- `.tar`: agrupa fitxers en un arxiu.
- `.gz`: indica compressió amb gzip.
- `.tar.gz`: arxiu `tar` comprimit amb gzip.

No és una imatge ISO ni una instal·lació automàtica amb un gestor de paquets: simplement s'estan desplegant els fitxers.

---

## 6. Pas 3: esborrar el fitxer descarregat

**[GUIA, pàgina 1]**

```bash
rm apache-flume-1.11.0-bin.tar.gz
```

### Explicació

- `rm` elimina un fitxer.
- En aquest cas elimina **l'arxiu comprimit**, no la carpeta ja descomprimida.
- Serveix per recuperar espai de disc després d'extreure el paquet.

**[AMPLIACIÓ]** Abans d'esborrar-lo, és prudent verificar que la descompressió ha finalitzat correctament:

```bash
ls -ld apache-flume-1.11.0-bin
```

Si la carpeta no existeix, cal revisar la descàrrega o la comanda `tar` abans d'eliminar l'original.

> **Atenció:** `rm` és una comanda destructiva. No afegeixis comodins (`*`) si no tens clar què se suprimirà.

---

## 7. Pas 4: canviar el nom del directori

**[GUIA, pàgina 1]**

```bash
mv apache-flume-1.11.0-bin flume
```

### Explicació

- `mv` permet **moure** o **reanomenar** fitxers i carpetes.
- Com que el destí és `flume`, la carpeta canvia de nom de `apache-flume-1.11.0-bin` a `flume`, si no hi havia ja una carpeta de destí amb aquest nom.
- Simplifica les rutes que s'utilitzen en les variables d'entorn.

**[AMPLIACIÓ]** `mv` actua respecte del directori actual; no col·loca automàticament Flume a `/home/hadoop`. Perquè la variable de la guia funcioni, s'hauria d'haver executat el procediment en `/home/hadoop` o haver traslladat després la carpeta al lloc adequat.

### Comprovació

```bash
pwd
ls -ld flume
ls flume/bin
```

Si `pwd` mostra `/home/hadoop`, la carpeta resultant seria `/home/hadoop/flume`.

### Exemple de situació alternativa

Si has treballat dins de `/home/iabd`, el destí real serà `/home/iabd/flume` i `FLUME_HOME` hauria d'apuntar a aquest directori. **No barregis la ruta de la guia amb la ruta de la teva instal·lació.**

---

## 8. Pas 5: editar les variables d'entorn

**[GUIA, pàgina 1]**

```bash
sudo nano ~/.bashrc
```

### Què és `~/.bashrc`?

**[AMPLIACIÓ]** És un fitxer de configuració habitual del shell Bash que es llegeix quan s'inicia una sessió interactiva de Bash (segons el tipus de sessió i la configuració). S'hi acostumen a posar àlies, personalitzacions i variables d'entorn.

| Element | Què significa? |
|---|---|
| `sudo` | Executar com un usuari amb privilegis elevats; normalment administrador. |
| `nano` | Editor de text en terminal. |
| `~` | Abreviatura del directori personal de l'usuari. |
| `.bashrc` | Fitxer de configuració de Bash, ocult perquè comença amb punt. |

**Recomanació [AMPLIACIÓ]:** si estàs editant **el teu propi** `~/.bashrc`, habitualment n'hi ha prou amb `nano ~/.bashrc`, sense `sudo`, per evitar canvis de propietari o problemes de permisos. El PDF proposa explícitament `sudo nano ~/.bashrc` i es recull aquí tal com apareix.

### Tecles útils de Nano

- `Ctrl + O`: desar els canvis.
- `Enter`: confirmar el nom del fitxer.
- `Ctrl + X`: sortir de Nano.
- `Ctrl + W`: cercar text.

### Còpia de seguretat opcional

```bash
cp ~/.bashrc ~/.bashrc.bak
```

Desa una còpia abans de fer canvis. No és un pas del PDF, però és útil quan s'aprèn administració de sistemes.

---

## 9. Pas 6: definir `FLUME_HOME`, `FLUME_CONF_DIR`, `FLUME_CLASSPATH` i `PATH`

**[GUIA, pàgines 1 i 2]** Les quatre línies que s'han d'afegir al `~/.bashrc` són:

```bash
export FLUME_HOME=/home/hadoop/flume
export FLUME_CONF_DIR=$FLUME_HOME/conf
export FLUME_CLASSPATH=$FLUME_CONF_DIR
export PATH=$PATH:$FLUME_HOME/bin
```

### 9.1. `FLUME_HOME`

```bash
export FLUME_HOME=/home/hadoop/flume
```

Defineix la carpeta principal de Flume. La resta de rutes es poden construir a partir d'aquesta.

- `export`: fa que la variable estigui disponible per als processos fills iniciats des del shell.
- `FLUME_HOME`: nom de la variable.
- `/home/hadoop/flume`: valor de la variable; ruta absoluta.

**Exemple:** després de definir-la, `$FLUME_HOME/bin` representa `/home/hadoop/flume/bin`.

### 9.2. `FLUME_CONF_DIR`

```bash
export FLUME_CONF_DIR=$FLUME_HOME/conf
```

Apunta a la carpeta `conf` situada dins de la carpeta d'instal·lació. És on es poden ubicar fitxers de configuració, com les propietats d'agents.

**Avantatge:** si Flume es trasllada de carpeta, normalment només cal canviar `FLUME_HOME` i la resta de variables dependents es recalcularan.

### 9.3. `FLUME_CLASSPATH`

```bash
export FLUME_CLASSPATH=$FLUME_CONF_DIR
```

Relaciona la cerca de recursos i classes Java amb la carpeta de configuració, tal com especifica la guia. El classpath és un mecanisme de Java per localitzar dependències i recursos.

**[AMPLIACIÓ]** El comportament exacte del classpath final també depèn dels scripts d'arrencada de Flume i de les biblioteques que incorporen; aquesta línia no implica que la carpeta `conf` contingui totes les dependències de Java.

### 9.4. `PATH`

```bash
export PATH=$PATH:$FLUME_HOME/bin
```

Afegeix la carpeta dels executables de Flume a la variable `PATH` ja existent.

- La primera aparició de `$PATH` conserva les rutes anteriors.
- Els dos punts `:` separen diferents carpetes en Unix/Linux.
- `$FLUME_HOME/bin` afegeix la carpeta que conté l'executable `flume-ng`.

**Sense aquesta línia**, potser hauries d'executar Flume especificant la ruta completa:

```bash
/home/hadoop/flume/bin/flume-ng version
```

**Amb aquesta línia**, el shell hauria de poder trobar-lo per nom:

```bash
flume-ng version
```

### 9.5. Què passaria si escrivíssim malament la ruta?

Per exemple, si `FLUME_HOME` apunta a una carpeta inexistent:

```bash
export FLUME_HOME=/home/hadoop/flume_inexistent
```

Les variables es defineixen igualment; Bash **no valida l'existència de la ruta** en assignar-la. El problema apareixerà en intentar executar fitxers que no hi són.

---

## 10. Pas 7: recarregar `~/.bashrc`

**[GUIA, pàgina 2]**

```bash
source ~/.bashrc
```

### Què fa `source`?

**[AMPLIACIÓ]** Executa les instruccions del fitxer dins del shell actual. Això és important perquè, si només desés el fitxer, els valors no necessàriament s'aplicarien a la terminal que ja tenies oberta.

`source ~/.bashrc` i `. ~/.bashrc` tenen una funció equivalent en Bash.

### Comprovar les quatre variables

```bash
echo "$FLUME_HOME"
echo "$FLUME_CONF_DIR"
echo "$FLUME_CLASSPATH"
printf '%s\n' "$PATH"
```

**Resultats esperats per a les tres primeres**, si has seguit literalment la ruta de la guia:

```text
/home/hadoop/flume
/home/hadoop/flume/conf
/home/hadoop/flume/conf
```

La quarta, `PATH`, ha de conservar les rutes prèvies i incloure `/home/hadoop/flume/bin`.

### Diferència entre definir i exportar

```bash
FLUME_HOME=/home/hadoop/flume
```

Això assigna una variable del shell. En canvi:

```bash
export FLUME_HOME=/home/hadoop/flume
```

La defineix i l'exporta perquè els programes executats des d'aquella sessió la puguin consultar com a variable d'entorn.

---

## 11. Pas 8: apartar la biblioteca Guava antiga

**[GUIA, pàgina 2]**

```bash
mv $FLUME_HOME/lib/guava-11.0.2.jar $FLUME_HOME/lib/guava-11.0.2.jar-old
```

### Per què apareix aquest pas?

La guia indica que es fa **per evitar alguns errors**, però **no especifica quin error concret**, ni en quina combinació de versions es manifesta.

**[AMPLIACIÓ]** Guava és una llibreria de Java que pot ser utilitzada per altres components del seu ecosistema. Quan diverses versions d'una mateixa biblioteca apareixen en el classpath, poden sorgir incompatibilitats. Apartar una versió potencialment conflictiva és una possible solució en entorns concrets.

### Què fa exactament la comanda?

1. Identifica el fitxer `guava-11.0.2.jar` dins de `$FLUME_HOME/lib`.
2. El reanomena a `guava-11.0.2.jar-old`.
3. **No elimina físicament el fitxer**; continua a la mateixa carpeta amb un altre nom.
4. Evita que es tracti com un `.jar` estàndard si els scripts només carreguen els arxius amb aquesta extensió.

### Comprovació abans i després

```bash
ls -l "$FLUME_HOME/lib/guava-11.0.2.jar"
```

Després d'executar la comanda de la guia:

```bash
ls -l "$FLUME_HOME/lib/guava-11.0.2.jar-old"
```

**Precaució:** no és una reparació universal. Si el fitxer no existeix, la comanda fallarà. Si el problema de dependències té un altre origen, aquest canvi podria no resoldre'l.

### Com revertir el canvi, si cal

**[AMPLIACIÓ]**

```bash
mv "$FLUME_HOME/lib/guava-11.0.2.jar-old" "$FLUME_HOME/lib/guava-11.0.2.jar"
```

Només s'hauria de fer després d'entendre l'error i revisar si ja existeix algun fitxer amb el nom de destí, per evitar sobreescriptures accidentals.

---

## 12. Resum: totes les comandes de la guia en ordre

> **[GUIA]** Aquest bloc agrupa les instruccions originals. **Abans d'executar-lo**, situa't al directori que correspongui amb la ruta definitiva `/home/hadoop/flume` i assegura't que no sobrescriuràs cap instal·lació existent.

```bash
# 1. Descarregar
wget https://dlcdn.apache.org/flume/1.11.0/apache-flume-1.11.0-bin.tar.gz

# 2. Descomprimir
tar -xvf apache-flume-1.11.0-bin.tar.gz

# 3. Eliminar l'arxiu comprimit
rm apache-flume-1.11.0-bin.tar.gz

# 4. Reanomenar la carpeta
mv apache-flume-1.11.0-bin flume

# 5. Obrir el fitxer d'entorn (tal com diu la guia)
sudo nano ~/.bashrc
```

Afegir dins de `~/.bashrc`:

```bash
export FLUME_HOME=/home/hadoop/flume
export FLUME_CONF_DIR=$FLUME_HOME/conf
export FLUME_CLASSPATH=$FLUME_CONF_DIR
export PATH=$PATH:$FLUME_HOME/bin
```

Després de desar i sortir de Nano:

```bash
# 6. Recarregar les variables
source ~/.bashrc

# 7. Apartar Guava antiga
mv $FLUME_HOME/lib/guava-11.0.2.jar $FLUME_HOME/lib/guava-11.0.2.jar-old
```

---

## 13. Comprovacions finals recomanades

**[AMPLIACIÓ — no apareixen al PDF]** La guia acaba amb el canvi de nom de Guava. Per assegurar que l'entorn està ben configurat, es poden executar unes verificacions no destructives.

### 13.1. Comprovar que existeix el directori d'instal·lació

```bash
test -d "$FLUME_HOME" && echo 'Directori Flume: OK' || echo 'Directori Flume: NO TROBAT'
```

### 13.2. Comprovar els executables

```bash
ls -l "$FLUME_HOME/bin/flume-ng"
command -v flume-ng
```

`command -v flume-ng` hauria de mostrar la ruta de l'executable si el `PATH` està ben configurat.

### 13.3. Comprovar Java

```bash
java -version
```

Si Java no està disponible, Flume no podrà executar-se. La versió de Java compatible depèn de la distribució concreta i de les dependències.

### 13.4. Mostrar la versió de Flume

```bash
flume-ng version
```

Si tot funciona, hauria de mostrar informació de la distribució de Flume. Si la comanda no es reconeix, comprova `PATH` i la ruta de `flume-ng`.

### 13.5. Comprovació compacta

```bash
printf 'FLUME_HOME=%s\n' "$FLUME_HOME"
printf 'FLUME_CONF_DIR=%s\n' "$FLUME_CONF_DIR"
printf 'FLUME_CLASSPATH=%s\n' "$FLUME_CLASSPATH"
command -v flume-ng
flume-ng version
```

La verificació `flume-ng version` és un test inicial; **no garanteix** que un pipeline amb un agent, HDFS o altres integracions estigui correctament configurat.

---

## 14. Errors habituals i diagnòstic

**[AMPLIACIÓ]**

| Símptoma | Causa possible | Què revisar |
|---|---|---|
| `wget: command not found` | No es troba `wget`. | Instal·lació de l'eina i `PATH`. |
| Error 404 en descarregar | URL canviada o paquet no disponible en aquell servidor. | Disponibilitat de la versió indicada. |
| `tar: Cannot open` | Fitxer inexistent o nom incorrecte. | `pwd` i `ls -l`. |
| `mv: cannot stat` | La carpeta o el `.jar` no existeixen. | Nom i ruta d'origen. |
| `Permission denied` | No hi ha permisos suficients. | Propietari, permisos i directori. |
| `flume-ng: command not found` | `PATH` incorrecte o no recarregat. | `source ~/.bashrc` i `command -v flume-ng`. |
| `No such file or directory` | `FLUME_HOME` no coincideix amb la instal·lació. | `echo "$FLUME_HOME"` i `ls "$FLUME_HOME"`. |
| Java no s'executa | Java absent o variable d'entorn mal configurada. | `java -version` i configuració de Java. |
| Error de classes Java | Conflicte de dependències o classpath. | Logs, versions dels `.jar` i compatibilitat. |
| La comanda Guava falla | El fitxer ja ha estat reanomenat o no forma part del paquet. | `ls "$FLUME_HOME/lib"`. |

### 14.1. Mètode de diagnòstic en cinc passos

1. Llegir el **primer error rellevant**, no únicament l'última línia de sortida.
2. Comprovar la carpeta actual (`pwd`).
3. Verificar que els fitxers existeixen (`ls`).
4. Revisar les variables (`echo "$FLUME_HOME"`).
5. Executar una comprovació específica (`command -v flume-ng`, `java -version`, etc.).

### 14.2. No aplicar correccions a cegues

No és recomanable:

- Fer `sudo` sobre totes les comandes sense necessitat.
- Canviar permisos de forma indiscriminada amb `chmod -R 777`.
- Eliminar biblioteques aleatòriament de `lib`.
- Substituir versions dels `.jar` sense comprovar compatibilitats.
- Esborrar la carpeta completa de Flume perquè una variable no funciona.

---

## 15. Exercici opcional: primer agent local de Flume

**[AMPLIACIÓ — no forma part de la guia d'instal·lació]** Aquest exemple permet connectar els conceptes Source → Channel → Sink després de verificar la instal·lació. No requereix HDFS, però sí que `flume-ng` funcioni i que la distribució admeti els components indicats.

### 15.1. Crear una carpeta de proves

```bash
mkdir -p "$HOME/flume-proves"
nano "$HOME/flume-proves/prova.conf"
```

### 15.2. Exemple d'agent amb Netcat i Logger Sink

Afegir al fitxer `prova.conf`:

```properties
# Declaració dels components
agent1.sources = source1
agent1.channels = channel1
agent1.sinks = sink1

# Source: escolta text en un port local
agent1.sources.source1.type = netcat
agent1.sources.source1.bind = 127.0.0.1
agent1.sources.source1.port = 44444

# Channel: cua en memòria RAM
agent1.channels.channel1.type = memory
agent1.channels.channel1.capacity = 1000
agent1.channels.channel1.transactionCapacity = 100

# Sink: escriu els esdeveniments al log
agent1.sinks.sink1.type = logger

# Connexions entre components
agent1.sources.source1.channels = channel1
agent1.sinks.sink1.channel = channel1
```

### 15.3. Iniciar l'agent

```bash
flume-ng agent \
  --name agent1 \
  --conf "$FLUME_CONF_DIR" \
  --conf-file "$HOME/flume-proves/prova.conf" \
  -Dflume.root.logger=INFO,console
```

El procés quedarà a l'escolta fins que es tanqui.

### 15.4. Enviar un missatge des d'un segon terminal

```bash
nc 127.0.0.1 44444
```

Escriu una línia de text i prem `Enter`. Si el sistema no té `nc`, caldrà instal·lar una eina compatible o emprar un altre client TCP. L'agent hauria de mostrar un esdeveniment al log.

### 15.5. Aturar l'agent

Prem `Ctrl + C` a la terminal on s'està executant Flume.

**Què demostra aquesta prova?** Que pots definir un agent, rebre dades des d'una font de xarxa, emmagatzemar-les temporalment en un canal i consumir-les des d'un sink.

**Què no demostra?** No verifica que Flume escrigui a HDFS ni que existeixi cap configuració de Hadoop funcional.

---

## 16. Comparativa de conceptes que poden confondre

| Concepte A | Concepte B | Diferència clau |
|---|---|---|
| Instal·lació | Configuració | Instal·lar posa fitxers; configurar n'estableix el comportament. |
| `wget` | `tar` | Descarrega un arxiu / n'extreu contingut. |
| `rm` | `mv` | Elimina / mou o reanomena. |
| `FLUME_HOME` | `FLUME_CONF_DIR` | Ruta principal / ruta dels fitxers de configuració. |
| `PATH` | `CLASSPATH` | Cerca d'executables / cerca de recursos i classes Java. |
| `~/.bashrc` | `source ~/.bashrc` | Fitxer de configuració / ordre que n'aplica el contingut al shell actual. |
| `Source` | `Sink` | Rep esdeveniments / els envia al destí. |
| `Channel` | HDFS | Buffer intermedi / emmagatzematge distribuït de destí. |
| `.tar.gz` | `.jar` | Paquet comprimit / arxiu Java amb classes i recursos. |

---

## 17. Checklist per repetir la pràctica

Marca les caselles en acabar cada tasca:

- [ ] He identificat l'usuari i el directori d'instal·lació.
- [ ] He comprovat que la ruta final serà coherent amb `FLUME_HOME`.
- [ ] He descarregat `apache-flume-1.11.0-bin.tar.gz`.
- [ ] He descomprimit el paquet sense errors.
- [ ] He comprovat que la carpeta extreta existeix.
- [ ] He eliminat el fitxer `.tar.gz` si ja no el necessito.
- [ ] He reanomenat la carpeta a `flume`.
- [ ] He fet una còpia opcional de `~/.bashrc`.
- [ ] He afegit les quatre variables d'entorn indicades.
- [ ] He desat el fitxer i executat `source ~/.bashrc`.
- [ ] He comprovat el valor de `FLUME_HOME`.
- [ ] He revisat l'existència de `guava-11.0.2.jar`.
- [ ] He aplicat el canvi de nom de Guava indicat a la guia, si correspon.
- [ ] He verificat `command -v flume-ng`.
- [ ] He verificat `flume-ng version`.
- [ ] Sé explicar per què es fa cada pas.

---

## 18. Preguntes d'autoavaluació amb resposta

### Preguntes sobre la guia original

**1. Quin és l'objectiu principal de l'activitat 5a?**  
Instal·lar Flume, configurar-ne les variables d'entorn i fer un ajust de compatibilitat sobre una biblioteca Guava.

**2. Quina versió de Flume apareix a la guia?**  
La versió `1.11.0`.

**3. Amb quina comanda es descarrega el paquet?**  
Amb `wget` i la URL de la distribució indicada.

**4. Quina extensió té el paquet descarregat?**  
`.tar.gz`.

**5. Quina comanda s'utilitza per extreure'l?**  
`tar -xvf apache-flume-1.11.0-bin.tar.gz`.

**6. Què vol dir l'opció `-x` de `tar`?**  
Extreure els fitxers de l'arxiu.

**7. Quina opció de `tar` mostra els fitxers processats?**  
`-v`.

**8. Per què s'utilitza `rm` després de descomprimir?**  
Per eliminar el paquet comprimit un cop extret.

**9. Quina carpeta es reanomena?**  
`apache-flume-1.11.0-bin`.

**10. Quin és el nom final de la carpeta?**  
`flume`.

**11. Quina comanda la reanomena?**  
`mv apache-flume-1.11.0-bin flume`.

**12. Quin fitxer s'edita per afegir les variables?**  
`~/.bashrc`.

**13. Quin editor proposa el PDF?**  
`nano`, mitjançant `sudo nano ~/.bashrc`.

**14. Quin valor té `FLUME_HOME` segons la guia?**  
`/home/hadoop/flume`.

**15. A què apunta `FLUME_CONF_DIR`?**  
A `$FLUME_HOME/conf`.

**16. A què apunta `FLUME_CLASSPATH`?**  
A `$FLUME_CONF_DIR`, segons el PDF.

**17. Per a què serveix afegir `$FLUME_HOME/bin` a `PATH`?**  
Per poder localitzar executables de Flume des del shell sense escriure'n la ruta completa.

**18. Quina comanda recarrega el fitxer de configuració?**  
`source ~/.bashrc`.

**19. Quin arxiu de Guava es reanomena?**  
`guava-11.0.2.jar`.

**20. Quin nou nom rep?**  
`guava-11.0.2.jar-old`.

**21. El PDF especifica el missatge d'error exacte que evita la modificació de Guava?**  
No. Només indica que s'efectua per evitar alguns errors.

**22. El PDF inclou un agent Flume que escrigui a HDFS?**  
No. Mostra l'arquitectura en un esquema, però no proporciona la configuració d'un agent.

### Preguntes de comprensió i ampliació

**23. Què representa el bloc `Source`?**  
El component que rep esdeveniments d'un origen.

**24. Què fa el `Channel`?**  
Emmagatzema temporalment els esdeveniments mentre esperen ser consumits.

**25. Què fa el `Sink`?**  
Llegeix els esdeveniments del canal i els envia a una destinació.

**26. Per què és útil un canal entre origen i destí?**  
Per desacoblar les velocitats de producció i consum de dades.

**27. Què passa si `FLUME_HOME` apunta a una carpeta incorrecta?**  
Les variables poden definir-se igualment, però fallaran les operacions que necessiten els fitxers reals.

**28. Quina comanda mostra el directori actual?**  
`pwd`.

**29. Quina comanda mostra el valor de `FLUME_HOME`?**  
`echo "$FLUME_HOME"`.

**30. Quina comanda indica la ruta d'un executable disponible al `PATH`?**  
`command -v flume-ng`.

**31. Quina ordre permet una verificació bàsica de Flume?**  
`flume-ng version`.

**32. Una comprovació correcta de `flume-ng version` garanteix que funciona HDFS?**  
No; només verifica un aspecte bàsic de l'execució de Flume.

**33. És imprescindible utilitzar `sudo` per editar el `~/.bashrc` personal?**  
Normalment no, si el fitxer pertany a l'usuari i té permisos d'escriptura.

**34. Quina diferència hi ha entre `PATH` i `CLASSPATH`?**  
`PATH` s'utilitza per trobar executables; el classpath Java es fa servir per trobar classes i recursos.

**35. Què passa si s'executa `source ~/.bashrc`?**  
Es processen les instruccions del fitxer en el shell actual.

**36. Per què cal revisar `pwd` abans de fer `mv ... flume`?**  
Perquè el nom de destí és relatiu al directori des del qual s'executa la comanda.

**37. Reanomenar un `.jar` equival a desinstal·lar-lo?**  
No; el fitxer es conserva al disc, però deixa de tenir el nom anterior.

**38. Per què no convé canviar dependències Java a cegues?**  
Perquè poden ser necessàries per a altres components i provocar errors nous.

**39. Quina extensió acostuma a tenir un arxiu de biblioteca Java?**  
`.jar`.

**40. Què vol dir HDFS?**  
Hadoop Distributed File System.

**41. El canal de memòria conserva necessàriament els missatges si es perd el procés?**  
No; pot perdre els missatges que encara hi tenia.

**42. Quina és la diferència principal entre la instal·lació i la configuració d'un agent?**  
La instal·lació desplega el programari; l'agent defineix com es transportaran les dades.

**43. Què és una ruta absoluta?**  
Una ruta que comença des de l'arrel del sistema, com `/home/hadoop/flume`.

**44. Què vol dir el símbol `~` al shell?**  
Habitualment representa el directori personal de l'usuari.

**45. Què és una variable d'entorn?**  
Un valor exportat que els processos fills poden consultar.

**46. Per què és útil conservar `$PATH` en escriure `PATH=$PATH:...`?**  
Per mantenir les rutes d'executables que ja existien.

**47. Què indica el caràcter `:` dins de `PATH`?**  
Separa diferents carpetes.

**48. Com verificar que la carpeta de configuració existeix?**  
Amb `ls -ld "$FLUME_CONF_DIR"`.

**49. Quina comanda pot comprovar si Java és accessible?**  
`java -version`.

**50. Quin error és habitual si el fitxer que es vol reanomenar no existeix?**  
Un error de `mv` que indica que no es pot trobar l'origen (`cannot stat`).

---

## 19. Mini examen pràctic resolt

### Exercici A: completar una configuració

**Enunciat:** Omple els valors de les variables que apareixen a la guia, suposant que Flume està instal·lat a `/home/hadoop/flume`.

**Solució:**

```bash
export FLUME_HOME=/home/hadoop/flume
export FLUME_CONF_DIR=$FLUME_HOME/conf
export FLUME_CLASSPATH=$FLUME_CONF_DIR
export PATH=$PATH:$FLUME_HOME/bin
```

### Exercici B: instal·lació en una altra ruta

**Enunciat:** Si Flume estigués instal·lat a `/opt/flume`, com adaptaries la configuració?

**Solució [AMPLIACIÓ]:**

```bash
export FLUME_HOME=/opt/flume
export FLUME_CONF_DIR=$FLUME_HOME/conf
export FLUME_CLASSPATH=$FLUME_CONF_DIR
export PATH=$PATH:$FLUME_HOME/bin
```

Només canvia `FLUME_HOME`, perquè les altres variables depenen d'aquesta.

### Exercici C: diagnosticar un `command not found`

**Enunciat:** Has editat `.bashrc`, però `flume-ng` no funciona com a comanda.

**Solució proposada [AMPLIACIÓ]:**

```bash
source ~/.bashrc
echo "$FLUME_HOME"
ls -l "$FLUME_HOME/bin/flume-ng"
command -v flume-ng
```

Si el fitxer no existeix, revisa la instal·lació. Si existeix però no es localitza, revisa `PATH`. Si es localitza però no arrenca, investiga Java, permisos i logs.

### Exercici D: entendre la comanda Guava

**Enunciat:** Explica la diferència entre aquestes dues ordres:

```bash
rm "$FLUME_HOME/lib/guava-11.0.2.jar"
mv "$FLUME_HOME/lib/guava-11.0.2.jar" "$FLUME_HOME/lib/guava-11.0.2.jar-old"
```

**Solució:** la primera elimina el fitxer; la segona el conserva amb un altre nom. La guia utilitza la segona.

---

## 20. Resum per memoritzar abans de l'examen

**La instal·lació de Flume a la guia segueix set accions fonamentals:**

1. **Descarregar** el paquet `apache-flume-1.11.0-bin.tar.gz` amb `wget`.
2. **Descomprimir-lo** amb `tar -xvf`.
3. **Eliminar** el comprimit amb `rm` quan ja estigui extret.
4. **Reanomenar** la carpeta a `flume` amb `mv`.
5. **Editar** `~/.bashrc` per definir `FLUME_HOME`, `FLUME_CONF_DIR`, `FLUME_CLASSPATH` i ampliar `PATH`.
6. **Recarregar** el fitxer amb `source ~/.bashrc`.
7. **Reanomenar** el JAR antic `guava-11.0.2.jar` a `guava-11.0.2.jar-old`, com indica el document.

### Les quatre variables que has de saber explicar

| Variable | Valor a la guia | Funció |
|---|---|---|
| `FLUME_HOME` | `/home/hadoop/flume` | Directori principal de Flume. |
| `FLUME_CONF_DIR` | `$FLUME_HOME/conf` | Directori de configuració. |
| `FLUME_CLASSPATH` | `$FLUME_CONF_DIR` | Ruta que la guia afegeix al classpath de Flume. |
| `PATH` | `$PATH:$FLUME_HOME/bin` | Permet trobar els executables de Flume. |

### Les tres peces del diagrama

```text
SOURCE -> CHANNEL -> SINK -> HDFS
```

- `Source`: rep.
- `Channel`: emmagatzema temporalment.
- `Sink`: envia.

### Una advertència clau

**La carpeta d'instal·lació real i `FLUME_HOME` han de coincidir.** Aquesta és una de les comprovacions més útils per prevenir errors en seguir una guia amb rutes fixes.

---

## 21. Glossari

| Terme | Definició |
|---|---|
| Apache Flume | Eina d'ingesta i transport d'esdeveniments. |
| Agent | Unitat d'execució amb fonts, canals i sinks. |
| Source | Component d'entrada de dades. |
| Channel | Buffer o cua d'esdeveniments. |
| Sink | Component de sortida de dades. |
| HDFS | Sistema de fitxers distribuït de Hadoop. |
| `wget` | Utilitat de descàrrega per terminal. |
| `tar` | Utilitat per empaquetar i extreure arxius. |
| `rm` | Elimina fitxers o directoris segons les opcions. |
| `mv` | Mou o reanomena fitxers i carpetes. |
| `nano` | Editor de text de terminal. |
| `.bashrc` | Fitxer habitual de configuració de Bash. |
| `source` | Executa un fitxer dins del shell actual. |
| `export` | Exporta una variable a l'entorn dels processos fills. |
| `FLUME_HOME` | Ruta arrel de la instal·lació de Flume. |
| `FLUME_CONF_DIR` | Directori de fitxers de configuració de Flume. |
| `FLUME_CLASSPATH` | Variable de classe/recursos emprada en l'entorn de Flume. |
| `PATH` | Conjunt de carpetes on es busquen executables. |
| Guava | Biblioteca de Java que pot intervenir en conflictes de dependències. |
| JAR | Format d'arxiu que pot contenir classes i recursos Java. |
| HDFS | Hadoop Distributed File System. |
| Permisos | Regles que determinen qui pot llegir, escriure o executar fitxers. |

---

## 22. Fonts i límits d'aquests apunts

**Font principal:** *M5075_NF1_4_Instal·lació de Flume.docx.pdf*, Activitat 5a, pàgines 1–2.

La primera pàgina conté el diagrama d'arquitectura i els passos de descàrrega, extracció, eliminació del comprimit, canvi de nom de la carpeta i inici de les variables d'entorn. La segona pàgina conté les variables restants, la recàrrega de `.bashrc` i la instrucció de Guava.

La guia també esmenta la documentació oficial d'Apache Flume i un material introductori d'AprenderBigData.com. Aquests apunts **no pressuposen haver consultat aquells enllaços**: les explicacions [AMPLIACIÓ] són material didàctic afegit per estudiar la guia.

**Final dels apunts.**
