# Apunts extensos — Apache Hadoop YARN

## 1. Què és YARN i per què serveix [GUIA]

**YARN** són les sigles de **Yet Another Resource Negotiator**. És el sistema de gestió de recursos de Hadoop, encarregat de coordinar els recursos computacionals disponibles en un clúster i repartir-los entre les aplicacions que els necessiten.

El document original assenyala tres responsabilitats principals:

- **Assignació de recursos:** determinar quina capacitat del clúster rep cada aplicació.
- **Planificació:** decidir en quin ordre i en quins recursos s'han d'executar les tasques.
- **Monitoratge:** supervisar l'execució de les tasques i l'estat dels nodes.

**Idea principal:** YARN no és el sistema que guarda els fitxers, ni és un llenguatge de programació. És qui **coordina on i amb quins recursos s'executen les aplicacions**.

### Analogia d'una empresa [AMPLIACIÓ]

Pensa en un clúster com una empresa on diversos equips comparteixen ordinadors:

- Un equip demana executar un càlcul; és el **client**.
- L'oficina que distribueix els equips disponibles és el **ResourceManager**.
- El responsable de coordinar el projecte és l'**ApplicationMaster**.
- Els encarregats de cada sala d'ordinadors són els **NodeManagers**.
- Cada reserva concreta de memòria i CPU per treballar és un **contenidor**.

L'analogia ajuda a recordar funcions, però no s'ha de confondre amb la implementació real: el ResourceManager planifica recursos; els NodeManagers supervisen els contenidors i l'ApplicationMaster gestiona l'execució pròpia de l'aplicació.

## 2. Context històric: Hadoop 1 i Hadoop 2 [GUIA]

La guia explica que YARN apareix amb **Hadoop 2.0** per separar la gestió dels recursos del processament de dades. En l'arquitectura anterior, el servei **JobTracker** concentrava responsabilitats que després es van separar.

Segons el resum, l'antic JobTracker es reparteix conceptualment entre:

1. **ResourceManager:** gestió global dels recursos del clúster.
2. **ApplicationMaster:** planificació i monitoratge de les tasques d'una aplicació.

### Per què era important aquesta separació? [AMPLIACIÓ]

Quan un únic servei concentra moltes responsabilitats, pot convertir-se en un coll d'ampolla. Separar la gestió del clúster de la lògica particular de cada aplicació permet executar diferents motors de processament sota una mateixa infraestructura de recursos.

| Aspecte | Hadoop 1 (idea general) | Hadoop 2 amb YARN |
|---|---|---|
| Gestió de recursos | Vinculada a JobTracker | ResourceManager |
| Coordinació d'una aplicació | Centralitzada en el model MapReduce | ApplicationMaster específic |
| Serveis per node | TaskTracker | NodeManager |
| Flexibilitat del processament | Fortament lligat a MapReduce | Pot donar suport a diferents frameworks |

> **Precisió:** YARN no va eliminar MapReduce. Va substituir l'arquitectura antiga de gestió i execució, i **MapReduce pot continuar executant-se sobre YARN**.

## 3. Gestió de recursos vs. processament de dades [AMPLIACIÓ]

Són responsabilitats diferents, però estan relacionades:

- **Gestió de recursos:** reservar memòria, CPU i capacitat de treball; per exemple, decidir si un node pot executar una tasca addicional.
- **Processament de dades:** llegir registres, transformar-los, sumar valors o entrenar un model. Aquest és el treball de l'aplicació i el seu motor d'execució.

Exemple: una aplicació `WordCount` compta les paraules d'un fitxer. MapReduce defineix el treball de comptatge, mentre que YARN ajuda a obtenir els recursos necessaris per executar-lo.

**Frase per a l'examen:** *HDFS emmagatzema, YARN administra recursos i MapReduce processa.* És una simplificació pràctica, no una descripció exhaustiva de tots els serveis.

## 4. Els quatre elements de l'arquitectura [GUIA]

El PDF enumera quatre elements: **ResourceManager, ApplicationMaster, NodeManager i contenidors**.

| Element | Àmbit | Responsabilitat |
|---|---|---|
| ResourceManager (RM) | Clúster | Gestionar els recursos globals i assignar-los a aplicacions |
| ApplicationMaster (AM) | Aplicació | Negociar recursos i coordinar les tasques de la seva aplicació |
| NodeManager (NM) | Node worker | Gestionar i informar sobre recursos i contenidors locals |
| Contenidor (Container) | Execució | Reservar recursos per executar un procés o una tasca |

**Regla mnemotècnica:** RM = *recursos globals*; AM = *una aplicació*; NM = *un node*; Container = *recursos assignats*.

## 5. ResourceManager en profunditat [GUIA + AMPLIACIÓ]

El **ResourceManager** administra la visió global dels recursos del clúster. Rep les peticions dels clients i intervé en l'assignació de recursos. El PDF el presenta com a component central del clúster.

### Responsabilitats

- Conèixer els nodes disponibles a partir de la informació rebuda dels NodeManagers.
- Gestionar les peticions de recursos de les aplicacions.
- Planificar l'assignació de recursos segons la disponibilitat i les polítiques configurades.
- Facilitar la posada en marxa de l'ApplicationMaster de cada aplicació.

### Components interns útils per entendre'l [AMPLIACIÓ]

**Scheduler (planificador):** decideix les assignacions de recursos d'acord amb les polítiques actives. **ApplicationsManager:** gestiona la recepció i el cicle de vida inicial de les aplicacions, incloent l'arrencada del seu ApplicationMaster.

### Què no és el ResourceManager?

No executa personalment totes les tasques de cada aplicació, no emmagatzema els blocs d'HDFS i no substitueix el NameNode. Té un rol central de coordinació de recursos.

## 6. ApplicationMaster en profunditat [GUIA + AMPLIACIÓ]

L'**ApplicationMaster** és el coordinador d'una aplicació concreta. La guia diu que envia tasques als workers i negocia recursos amb el ResourceManager.

### Responsabilitats

1. Registrar-se i comunicar-se amb el ResourceManager.
2. Sol·licitar recursos adequats per al treball pendent.
3. Coordinar les tasques als nodes on s'executaran.
4. Supervisar-ne el progrés.
5. Gestionar els estats i errors de les tasques segons el framework utilitzat.
6. Donar per acabada la seva activitat quan l'aplicació finalitza.

### Una instància per aplicació

Per exemple, si hi ha tres aplicacions independents, cadascuna pot tenir el seu propi ApplicationMaster. Això evita que un únic coordinador hagi de conèixer tots els detalls de totes les aplicacions.

### Particularitat important

L'ApplicationMaster també **s'executa dins d'un contenidor**. No és un ordinador físic exclusiu, sinó un procés d'aplicació que rep recursos per funcionar.

## 7. NodeManager en profunditat [GUIA + AMPLIACIÓ]

Un **NodeManager** s'executa habitualment a cada node de treball. Controla l'execució de contenidors locals, informa el ResourceManager de l'estat del node i vigila els recursos.

Les tasques habituals inclouen rebre ordres d'arrencada de contenidors, preparar l'entorn d'execució, supervisar processos i comunicar informació periòdica al sistema central.

### Heartbeats

Els NodeManagers envien senyals de vida (*heartbeats*) i informes d'estat. Si un node deixa de respondre durant prou temps, el sistema pot considerar-lo no disponible i prendre mesures perquè l'aplicació es recuperi, segons la seva configuració.

### NodeManager vs. DataNode

Un mateix servidor pot tenir tots dos serveis, però fan funcions diferents: **DataNode** desa blocs HDFS; **NodeManager** gestiona contenidors i recursos d'execució.

## 8. Contenidors YARN [GUIA + AMPLIACIÓ]

La guia presenta els contenidors com la quarta peça del sistema. Per estudiar-los amb precisió: **un contenidor no és un node físic**, sinó una assignació de recursos i un entorn d'execució en un node.

Un contenidor pot reservar, per exemple, 2 GiB de RAM i un nombre determinat de vcores, tot i que les quantitats reals depenen del clúster.

### Exemple

Un worker amb 8 GiB de RAM assignables a YARN podria, segons les polítiques i les reserves existents, allotjar diversos contenidors petits o menys contenidors grans. No tota la RAM del node queda necessàriament disponible per als contenidors: el sistema operatiu i altres serveis també en necessiten.

### Diferència amb Docker

Un **contenidor YARN** és una unitat de recursos i execució dins de YARN. No és automàticament un contenidor Docker: poden existir integracions, però no són conceptes equivalents.

## 9. Visió completa de l'arquitectura [AMPLIACIÓ]

```text
                         CLIENTS
                           |
                           v
                    ResourceManager
                    (visió del clúster)
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
         Worker 1      Worker 2       Worker 3
        NodeManager   NodeManager    NodeManager
             |             |             |
       +-----+----+     +--+---+      +--+---+
       |          |     |      |      |      |
       v          v     v      v      v      v
    AM d'una    Tasca Tasca  Tasca  Tasca  Tasca
    aplicació
```

El ResourceManager té una visió global; els NodeManagers actuen sobre nodes locals; l'ApplicationMaster és el coordinador lògic d'una aplicació i les tasques s'executen en contenidors assignats.

## 10. Interpretació del diagrama de la pàgina 1 [GUIA]

La **figura inferior de la pàgina 1** mostra dos clients a l'esquerra, un ResourceManager al centre i diversos nodes amb NodeManager, ApplicationMaster i contenidors a la dreta. La llegenda distingeix quatre tipus d'interacció: enviament de jobs, peticions de recursos, informació d'estat dels nodes i informació de progrés de MapReduce.

**Com llegir-lo:** la connexió inicial s'estableix entre el client i el ResourceManager; a partir d'aquí apareix la coordinació amb els workers. Les instàncies d'ApplicationMaster es dibuixen dins dels nodes de treball, mostrant que la coordinació específica de l'aplicació no ha de residir físicament al servidor ResourceManager.

**Què convé recordar:** les fletxes no impliquen que les dades HDFS hagin de passar pel ResourceManager. El dibuix descriu sobretot **control, estat i assignació de recursos**.

## 11. Execució d'un job: versió resumida del PDF [GUIA]

El PDF descriu quatre passos, que mantenim aquí amb la seva intenció original:

1. **El client envia el job al ResourceManager.** S'inicia la sol·licitud d'execució.
2. **El ResourceManager posa en marxa l'ApplicationMaster i gestiona l'assignació inicial de recursos.** L'aplicació ja disposa d'un coordinador.
3. **L'ApplicationMaster coordina l'enviament de tasques als workers.** Sol·licita i utilitza els contenidors concedits.
4. **Els NodeManagers monitoritzen els nodes durant el procés.** Informen de l'estat i gestionen els contenidors locals.

Aquest resum és especialment adequat per memoritzar la seqüència bàsica d'una pregunta teòrica.

## 12. Execució d'un job: seqüència detallada [AMPLIACIÓ]

La seqüència següent desplega tècnicament la descripció resumida:

1. El client prepara l'aplicació, els arguments i els recursos necessaris.
2. El client presenta una sol·licitud al ResourceManager.
3. El ResourceManager accepta l'aplicació si compleix les condicions i programa els recursos per inicialitzar el seu ApplicationMaster.
4. Un NodeManager arrenca el contenidor que allotja l'ApplicationMaster.
5. L'ApplicationMaster es registra davant del ResourceManager.
6. L'ApplicationMaster demana contenidors addicionals per a les tasques.
7. El ResourceManager assigna recursos segons disponibilitat i polítiques de planificació.
8. L'ApplicationMaster coordina l'arrencada de les tasques als NodeManagers corresponents.
9. Cada NodeManager arrenca i vigila els contenidors assignats.
10. Els processos de l'aplicació llegeixen i escriuen dades segons el framework, sovint fent servir HDFS.
11. L'ApplicationMaster rep els resultats/estats de les tasques i determina si l'aplicació ha finalitzat.
12. Es notifica la finalització i s'alliberen els recursos.

**Distinció clau:** el ResourceManager no ha de comunicar individualment totes les instruccions del càlcul als processos de cada tasca; aquesta coordinació pertany a l'ApplicationMaster i al framework de l'aplicació.

## 13. Interpretació del diagrama de la pàgina 2 [GUIA]

El **diagrama de la pàgina 2** amplia l'exemple a un treball MapReduce. Hi apareixen el **client JVM**, el **ResourceManager**, un node on s'executa el **MRAppMaster**, un altre **NodeManager**, una JVM amb una tasca Map o Reduce i un **sistema de fitxers compartit (per exemple, HDFS)**.

El dibuix enumera etapes com l'obtenció d'una nova aplicació, la presentació del job, la còpia de recursos, l'arrencada del contenidor de l'ApplicationMaster, l'obtenció dels splits d'entrada, la petició de recursos i el llançament de la tasca.

### Què ens ensenya aquest esquema?

- El client i el ResourceManager participen en la **presentació i acceptació** del treball.
- El MRAppMaster és el coordinador **particular de MapReduce**.
- Les tasques Map i Reduce viuen en processos d'execució en els workers.
- HDFS és utilitzat per compartir recursos i dades del job; no és el mateix sistema que YARN.

### Què és un input split? [AMPLIACIÓ]

És la porció lògica de dades d'entrada assignada a una tasca Map. Un *input split* no és necessàriament idèntic a un bloc físic d'HDFS, tot i que sovint la seva mida i ubicació hi estan relacionades.

## 14. Interpretació del diagrama de la pàgina 3 [GUIA]

La **pàgina 3**, titulada «Execució d'una aplicació a YARN», és un esquema numerat. Mostra:

- El client i la petició inicial al ResourceManager.
- El ResourceManager amb els blocs interns **Applications Master** i **Scheduler** (en termes d'arquitectura, és més precís parlar de l'**ApplicationsManager** intern i l'ApplicationMaster de l'aplicació).
- Diferents workers amb els seus NodeManagers.
- Un worker amb un contenidor que executa l'ApplicationMaster.
- Un altre worker que executa un contenidor de treball.

**Lectura de la figura:** les fletxes numerades expressen un flux de sol·licitud, arrencada del coordinador, negociació de recursos, inici dels contenidors de tasques i comunicació dels estats. La figura reforça que una sola aplicació pot coordinar treball repartit entre més d'un worker.

### Com explicar el gràfic en un examen

> El client lliura l'aplicació al ResourceManager. Aquest gestiona els recursos necessaris perquè un NodeManager executi l'ApplicationMaster. L'ApplicationMaster demana contenidors per executar les tasques als workers. Els NodeManagers inicien i supervisen aquests contenidors mentre es completa el treball.

## 15. Relacions que cal dominar [AMPLIACIÓ]

**Client → ResourceManager:** presenta l'aplicació. **ResourceManager → NodeManager:** coordina l'assignació i l'arrencada inicial d'acord amb el protocol. **ApplicationMaster ↔ ResourceManager:** negocia recursos per a l'aplicació. **ApplicationMaster ↔ NodeManager:** coordina l'arrencada i el control de contenidors. **NodeManager → ResourceManager:** envia estat i informació dels recursos locals.

| Pregunta | Resposta curta |
|---|---|
| Qui coneix els recursos globals? | ResourceManager |
| Qui coneix l'estat local del worker? | NodeManager |
| Qui coordina les tasques d'una aplicació? | ApplicationMaster |
| On s'executen les tasques? | En contenidors dels workers |
| Qui proporciona dades de fitxers distribuïts? | HDFS, quan l'aplicació l'utilitza |

## 16. Relació entre YARN, HDFS i MapReduce [AMPLIACIÓ]

```text
             Aplicació (p. ex., WordCount)
                          |
                    MapReduce
                (lògica de càlcul)
                          |
                        YARN
            (recursos, scheduling, control)
                          |
                 Nodes del clúster
                          ^
                          |
                        HDFS
              (fitxers i blocs de dades)
```

YARN i HDFS poden compartir les mateixes màquines, però tenen serveis i responsabilitats separades. Això és especialment útil quan es combinen diversos motors de processament que comparteixen una infraestructura.

### Exemple concret

Per comptar les paraules d'un text emmagatzemat a HDFS:

1. HDFS manté els blocs del text.
2. El client llança un job de WordCount.
3. YARN assigna recursos d'execució.
4. MapReduce processa les paraules en paral·lel.
5. El resultat s'escriu a HDFS.

## 17. Recursos, planificació i concurrència [AMPLIACIÓ]

### Què es planifica?

Principalment recursos de computació, com memòria i vcores. El ResourceManager fa assignacions tenint en compte polítiques de cues i disponibilitat.

### Per què calen cues?

En un centre amb molts usuaris, diferents equips poden presentar aplicacions alhora. Les cues permeten aplicar criteris organitzatius: capacitat compartida, límits, prioritats i regles de concurrència.

### Exemple numèric il·lustratiu

Si un worker té 16 GiB de memòria reservada per a contenidors YARN i una aplicació en demana 4 GiB per tasca, un límit teòric simplificat seria de quatre tasques simultànies pel criteri de memòria. En realitat, CPU, memòria reservada, overhead, límits per contenidor i polítiques poden reduir aquest nombre.

### Data locality

Quan és possible, interessa executar els càlculs a prop de les dades. Això pot reduir el trànsit de xarxa. No és una garantia absoluta: les decisions també depenen de la disponibilitat de recursos i de les prioritats de la cua.

## 18. Fallades i recuperació [AMPLIACIÓ]

| Fallada | Efecte possible | Resposta conceptual |
|---|---|---|
| Una tasca falla | No es completa la seva part del job | El framework pot reintentar-la |
| Un NodeManager deixa de respondre | El node es considera no disponible | S'ajusten les assignacions i es poden recuperar tasques |
| L'ApplicationMaster falla | Es perd el coordinador d'aquella aplicació | Es pot tornar a iniciar segons la configuració i les possibilitats de recuperació |
| El ResourceManager falla | Perill per a la coordinació global | En entorns adequats es configura alta disponibilitat |
| HDFS falla o no és accessible | Les aplicacions poden perdre accés a les dades | Cal diagnosticar els serveis HDFS per separat |

**Important:** la tolerància a fallades no significa que una tasca mai no falli. Significa que el sistema inclou mecanismes per detectar problemes i intentar continuar quan sigui possible.

## 19. Exemple conceptual: tres tasques [AMPLIACIÓ]

Suposem un fitxer dividit lògicament en tres parts i una aplicació que ha de comptar registres:

1. El client presenta l'aplicació.
2. S'inicia el seu ApplicationMaster en un worker.
3. L'ApplicationMaster sol·licita recursos per a tres tasques.
4. El ResourceManager assigna contenidors disponibles.
5. Els NodeManagers executen les tasques.
6. Les tasques processen els fragments corresponents.
7. El coordinador comprova si les tasques han acabat.
8. S'alliberen els contenidors i es notifica el resultat.

Si només hi ha recursos suficients per a dues tasques, la tercera pot esperar fins que n'hi hagi de disponibles. La disponibilitat de contenidors determina la concurrència, no necessàriament el nombre total de tasques d'una aplicació.

## 20. Ordres bàsiques de YARN [AMPLIACIÓ]

> Les ordres d'aquest apartat són complementàries: **no apareixen al resum original de tres pàgines**. Poden dependre de la configuració i de la versió del clúster.

### Comprovar la instal·lació

```bash
yarn version
```

### Arrencar i aturar YARN (entorn docent configurat)

```bash
start-yarn.sh
stop-yarn.sh
```

### Examinar processos Java

```bash
jps
```

Hi podrien aparèixer `ResourceManager` i `NodeManager`, a més d'altres dimonis de Hadoop que estiguin actius.

### Consultar els nodes

```bash
yarn node -list
```

### Consultar aplicacions

```bash
yarn application -list
```

### Consultar l'estat d'una aplicació

```bash
yarn application -status application_XXXXXXXXXXXXX_0001
```

Substitueix l'identificador per un d'obtingut al teu clúster; no és un ID real del document.

### Consultar registres

```bash
yarn logs -applicationId application_XXXXXXXXXXXXX_0001
```

### Finalitzar una aplicació (operació sensible)

```bash
yarn application -kill application_XXXXXXXXXXXXX_0001
```

Aquesta ordre interromp una aplicació activa: utilitza-la només quan sigui necessari.

## 21. Interfície web i monitoratge [AMPLIACIÓ]

En una configuració habitual de Hadoop, la interfície web del **ResourceManager** es pot consultar al port **8088**, per exemple:

```text
http://localhost:8088
```

Des d'allà es poden revisar aplicacions, estats, cues i nodes, segons la versió i la configuració. Els noms de host i ports poden ser diferents a les màquines del centre.

### Què observaries en una pràctica?

- Si el ResourceManager està accessible.
- Si els nodes apareixen com a disponibles.
- Si el job ha estat acceptat, està en execució o ha finalitzat.
- Si existeixen missatges d'error o intents fallits.
- Quins recursos s'estan utilitzant.

**Diferència:** les eines web mostren estat i diagnòstic; no substitueixen l'execució real del job ni les dades que processa.

## 22. Configuració habitual [AMPLIACIÓ]

El fitxer de configuració general de YARN és habitualment:

```text
$HADOOP_HOME/etc/hadoop/yarn-site.xml
```

Exemple docent simplificat:

```xml
<configuration>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>localhost</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
</configuration>
```

Si volem executar MapReduce sobre YARN, és habitual definir a `mapred-site.xml`:

```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
```

**Avís:** són exemples d'estudi, no una configuració completa d'un clúster de producció. No substitueixis fitxers existents sense una còpia de seguretat i sense comprovar què hi ha configurat.

## 23. Diagnòstic d'errors habituals [AMPLIACIÓ]

### `yarn: command not found`

Pot indicar que Hadoop/YARN no està instal·lat o que la ruta `bin` no és al `PATH`. Comprova les variables d'entorn i la ruta de la instal·lació.

### No es veu el ResourceManager a `jps`

Comprova si s'ha arrencat YARN, els logs del servei i la configuració del clúster.

### Els nodes no apareixen a la interfície

Revisa si els NodeManagers s'executen i es poden comunicar amb el ResourceManager, així com la resolució de noms i el tallafoc.

### Aplicació en estat `ACCEPTED` durant molt de temps

Pot estar esperant recursos, límits de concurrència o disponibilitat de contenidors; cal revisar la cua, la memòria lliure i els diagnòstics.

### Aplicació en estat `FAILED`

No és necessàriament un problema del ResourceManager. El codi, les dependències, les rutes HDFS, els permisos o la memòria de les tasques poden ser la causa. Inspecciona els logs de l'aplicació.

### Aplicació en estat `KILLED`

Algú o algun mecanisme l'ha finalitzada. S'ha de consultar el missatge de diagnòstic abans d'atribuir-ne la causa.

## 24. Confusions freqüents [AMPLIACIÓ]

1. **YARN no és HDFS.** YARN coordina computació; HDFS organitza emmagatzematge.
2. **YARN no és MapReduce.** MapReduce és un model i motor de càlcul que pot funcionar sobre YARN.
3. **ResourceManager no és ApplicationMaster.** El primer és global; el segon és propi d'una aplicació.
4. **NodeManager no és DataNode.** Un s'ocupa dels contenidors; l'altre dels blocs de dades.
5. **Contenidor no és node físic.** Una màquina pot executar diversos contenidors.
6. **No hi ha un únic ApplicationMaster per clúster.** Cada aplicació admesa té el seu coordinador, mentre funciona.
7. **Més contenidors no garanteixen linealment més rendiment.** També intervenen I/O, xarxa, dependències, repartiment de dades i overhead.
8. **El ResourceManager no rep tots els bytes de les dades a processar.** Les dades circulen segons l'arquitectura de l'aplicació i l'emmagatzematge.
9. **L'ApplicationMaster també necessita recursos.** Cal iniciar-lo abans que pugui gestionar la resta de tasques.
10. **Heartbeat no és resultat del càlcul.** És informació periòdica d'activitat/estat del node.

## 25. Comparatives per memoritzar [AMPLIACIÓ]

### ResourceManager vs. ApplicationMaster

| Pregunta | ResourceManager | ApplicationMaster |
|---|---|---|
| Abast | Clúster | Aplicació |
| Objectiu | Administrar recursos | Coordinar un treball específic |
| Sol·licita recursos per a tasques? | Els concedeix segons planificació | Els negocia per a la seva aplicació |
| Durada | Servei de llarga durada | Fins que finalitza l'aplicació |
| Ubicació típica | Node de gestió | Contenidor assignat en un worker |

### NodeManager vs. contenidor

| NodeManager | Contenidor |
|---|---|
| Servei executat en un node | Unitat concreta de recursos i execució |
| Gestiona diversos contenidors | Allotja un procés o tasca |
| Envia estat al ResourceManager | És supervisat pel NodeManager |
| Es manté en funcionament entre jobs | Té un cicle de vida vinculat al treball |

### Hadoop 1 vs. Hadoop 2

| Hadoop 1 | Hadoop 2 amb YARN |
|---|---|
| Arquitectura MapReduce més centralitzada | Gestió de recursos separada del motor de càlcul |
| JobTracker/TaskTracker | ResourceManager/NodeManager i ApplicationMaster |
| Forta dependència del model MapReduce | Més varietat de motors compatibles |

## 26. Exercicis pràctics proposats i resolts [AMPLIACIÓ]

### Exercici 1. Assignar els rols

**Enunciat:** tens un clúster amb un ResourceManager, tres workers i dues aplicacions independents. Quins components esperes trobar?

**Solució:** un servei ResourceManager per a la coordinació global, NodeManagers als workers, un ApplicationMaster per cada aplicació que s'estigui executant i els contenidors necessaris per a les tasques.

### Exercici 2. Identificar el coll d'ampolla

**Enunciat:** una aplicació té 15 tasques preparades, però només disposa de recursos per executar 5 tasques simultànies. Quantes poden treballar alhora?

**Solució:** com a màxim 5, segons els recursos disponibles i la configuració. Les altres hauran d'esperar o planificar-se en onades.

### Exercici 3. Què falla?

**Enunciat:** una aplicació apareix com a `ACCEPTED` però no comença a executar tasques.

**Solució:** revisar la disponibilitat dels contenidors, els límits de la cua i si l'ApplicationMaster s'ha pogut posar en marxa.

### Exercici 4. Distingir serveis

**Enunciat:** un servidor conté blocs HDFS i també executa processos per als jobs. Quins dos serveis podria tenir?

**Solució:** DataNode per als blocs i NodeManager per a l'execució de contenidors.

### Exercici 5. Ordres de diagnòstic

**Enunciat:** vols veure els processos Java i les aplicacions YARN.

**Solució:** `jps` i `yarn application -list`, respectivament.

### Exercici 6. Lectura de la pàgina 1

**Enunciat:** què signifiquen les fletxes entre ResourceManager i nodes treballadors?

**Solució:** representen comunicacions de gestió, peticions i estats, no un flux obligatori de dades HDFS a través del ResourceManager.

### Exercici 7. Execució d'una aplicació

**Enunciat:** ordena: executar tasques, registrar AM, enviar job, arrencar AM, demanar contenidors.

**Solució:** enviar job → arrencar AM → registrar AM → demanar contenidors → executar tasques.

### Exercici 8. Contenidors

**Enunciat:** un contenidor és un ordinador, un directori d'HDFS o una reserva de recursos?

**Solució:** una reserva de recursos i un entorn d'execució, no un ordinador físic.

## 27. Preguntes tipus examen amb resposta

### Bloc A. Fonaments

1. **Què significa YARN?** Yet Another Resource Negotiator.
2. **Quina és la funció general de YARN?** Gestionar recursos del clúster i facilitar la planificació i execució d'aplicacions.
3. **Amb quina generació de Hadoop apareix?** Amb Hadoop 2.
4. **Quina arquitectura anterior ajuda a substituir?** La gestió de jobs de Hadoop 1 basada en JobTracker i TaskTracker.
5. **YARN és un sistema de fitxers?** No; aquest paper habitualment correspon a HDFS.
6. **YARN executa només MapReduce?** No, està dissenyat per donar suport a diversos frameworks.
7. **Quina és la gran idea de la seva introducció?** Separar gestió de recursos i processament.
8. **Quina diferència hi ha entre recursos i tasques?** Els recursos són capacitats com memòria i CPU; les tasques són processos que les utilitzen.
9. **Quins són els quatre elements del PDF?** ResourceManager, ApplicationMaster, NodeManager i contenidors.
10. **Què és un worker?** Un node del clúster que participa en l'execució i/o emmagatzematge de dades.

### Bloc B. Components

11. **Qui coneix la disponibilitat global de recursos?** ResourceManager.
12. **Qui coordina una aplicació particular?** ApplicationMaster.
13. **Qui supervisa els recursos d'un worker?** NodeManager.
14. **Què és un contenidor?** Una assignació de recursos i un entorn d'execució en un node.
15. **Quants ResourceManagers descriu la guia?** Un de principal per clúster.
16. **Quants ApplicationMasters hi ha per aplicació activa?** Habitualment un coordinador actiu per aplicació.
17. **On s'executa l'ApplicationMaster?** En un contenidor assignat a un node del clúster.
18. **Què informa el NodeManager?** L'estat i els recursos del node, així com informació sobre contenidors.
19. **Per què el NodeManager no és el DataNode?** Gestionen execució i emmagatzematge, respectivament.
20. **Per què l'AM negocia recursos amb el RM?** Per aconseguir contenidors per a les tasques de la seva aplicació.
21. **Què fa el Scheduler?** Distribuir recursos segons polítiques i disponibilitat.
22. **Pot un worker allotjar més d'un contenidor?** Sí, si disposa dels recursos necessaris.
23. **Un contenidor YARN equival sempre a Docker?** No.
24. **L'ApplicationMaster viu permanentment?** No, el seu cicle està vinculat a l'aplicació.
25. **Què vol dir RM?** ResourceManager.

### Bloc C. Fluxos d'execució

26. **Quin és el primer pas del PDF quan es llança un job?** El client l'envia al ResourceManager.
27. **Què passa després?** Es gestiona l'inici de l'ApplicationMaster i la reserva inicial de recursos.
28. **Qui negocia els contenidors de les tasques?** ApplicationMaster amb ResourceManager.
29. **Qui arrenca els contenidors als workers?** Els NodeManagers segons les peticions d'execució.
30. **Qui supervisa el progrés d'una aplicació?** Principalment el seu ApplicationMaster, amb informació dels processos.
31. **Què vol dir `job submission`?** Presentació de l'aplicació al sistema.
32. **Què és el MRAppMaster de la pàgina 2?** L'ApplicationMaster específic d'un job MapReduce.
33. **Per què apareix HDFS al diagrama de la pàgina 2?** Perquè els recursos i les dades del job poden residir en un sistema de fitxers compartit.
34. **El ResourceManager processa totes les dades del job?** No.
35. **Què és un input split?** La divisió lògica de les dades que rep una tasca Map.
36. **Qui informa periòdicament de l'estat dels nodes?** NodeManager.
37. **Què passa amb els contenidors després del job?** Se n'alliberen els recursos.
38. **Què pot passar si no hi ha recursos suficients?** L'aplicació o algunes tasques esperen.
39. **Què representa la fletxa inicial de la pàgina 3?** La petició de l'aplicació des del client al ResourceManager.
40. **Per què es veuen diversos workers al diagrama?** Per mostrar l'execució distribuïda de tasques.

### Bloc D. Diagnòstic i comparatives

41. **Per a què serveix `yarn application -list`?** Per consultar aplicacions, segons els filtres i l'estat.
42. **Per a què serveix `yarn node -list`?** Per veure nodes registrats segons els paràmetres de consulta.
43. **Quina ordre mostra processos Java?** `jps`.
44. **Quina ordre inicia YARN en un entorn Hadoop configurat?** `start-yarn.sh`.
45. **Quin port web és habitual per al ResourceManager?** 8088.
46. **Què indica l'estat `RUNNING`?** Que una aplicació està en execució.
47. **Què indica `FINISHED`?** Que l'aplicació ha acabat; convé consultar l'estat final per saber si va tenir èxit.
48. **Què indica `FAILED`?** Que el job o l'aplicació ha fallat.
49. **Quina diferència hi ha entre `FAILED` i `KILLED`?** Error d'execució versus finalització forçada.
50. **On busques detalls d'un error?** A l'estat i als logs de l'aplicació, entre altres fonts.
51. **Per què no has de matar qualsevol aplicació?** Perquè interrompries el treball dels usuaris.
52. **Per què cal comprovar les cues?** Perquè poden limitar els recursos i la concurrència.
53. **Què són els heartbeats?** Comunicacions periòdiques d'estat o vida dels serveis.
54. **Quin component gestiona els blocs HDFS?** DataNode sota la coordinació del NameNode.
55. **Quin component coordina els contenidors del worker?** NodeManager.
56. **És correcte dir que YARN substitueix HDFS?** No.
57. **És correcte dir que YARN elimina MapReduce?** No.
58. **Per què és important la proximitat entre tasques i dades?** Pot reduir el trànsit de xarxa.
59. **Què són els vcores?** Unitats de capacitat de CPU administrades per YARN.
60. **Què has d'explicar si et demanen el diagrama de les pàgines 1–3?** Els rols dels quatre components i el flux client → RM → AM → contenidors als workers, amb monitoratge dels NM.

## 28. Glossari

| Terme | Definició |
|---|---|
| YARN | Gestor de recursos i d'execució d'aplicacions de Hadoop |
| Hadoop | Ecosistema per a emmagatzematge i processament distribuït |
| Clúster | Grup de màquines que treballen conjuntament |
| Client | Usuari o procés que presenta una aplicació |
| ResourceManager | Coordinador global dels recursos YARN |
| Scheduler | Planificador d'assignació de recursos |
| ApplicationsManager | Component intern de RM que gestiona la recepció i l'arrencada d'aplicacions |
| ApplicationMaster | Coordinador d'una aplicació |
| MRAppMaster | ApplicationMaster propi de MapReduce |
| NodeManager | Servei de gestió de contenidors a cada worker |
| Worker | Node que aporta capacitat de treball |
| Container | Unitat de recursos assignats i d'execució |
| vcore | Unitat de capacitat de CPU gestionada per YARN |
| Job | Treball enviat al sistema |
| Task | Operació concreta que forma part d'un job |
| Heartbeat | Comunicació periòdica d'estat |
| HDFS | Sistema de fitxers distribuït de Hadoop |
| DataNode | Servei que emmagatzema blocs HDFS |
| NameNode | Servei que gestiona l'espai de noms i metadades HDFS |
| MapReduce | Model de processament paral·lel basat en Map i Reduce |
| Input split | Part lògica de les dades d'entrada d'una tasca Map |
| Queue | Cua que aplica polítiques d'assignació de recursos |
| Data locality | Preferència per processar dades a prop d'on resideixen |
| Job logs | Registres i diagnòstics de l'execució |

## 29. Resum final i checklist

### Resum de cinc frases

1. **YARN és el gestor de recursos de Hadoop** i separa les decisions de recursos de la lògica de processament.
2. El **ResourceManager** té la visió global del clúster.
3. Cada aplicació compta amb un **ApplicationMaster** que negocia recursos i coordina les seves tasques.
4. Els **NodeManagers** gestionen i monitoritzen els contenidors als workers.
5. Els **contenidors** són les unitats de recursos on s'executen processos; no són nodes físics.

### Checklist d'autoavaluació

- [ ] Sé què significa YARN i per què es va introduir a Hadoop 2.
- [ ] Puc explicar la diferència entre Hadoop 1 i Hadoop 2.
- [ ] Distingeixo ResourceManager, ApplicationMaster, NodeManager i contenidor.
- [ ] Puc explicar els quatre passos del resum original.
- [ ] Sé llegir les fletxes i els components del diagrama de la pàgina 1.
- [ ] Sé identificar MRAppMaster, HDFS i task JVM al diagrama de la pàgina 2.
- [ ] Puc explicar la seqüència numerada del diagrama de la pàgina 3.
- [ ] No confonc HDFS, YARN i MapReduce.
- [ ] Conec les ordres bàsiques de consulta i diagnòstic de YARN.
- [ ] Entenc que els contenidors limiten els recursos disponibles per a les tasques.
- [ ] Puc resoldre les 60 preguntes sense mirar les solucions.

---

## Nota final sobre la fidelitat al document

El PDF de partida és un **resum de tres pàgines**. La seva informació central és: definició de YARN, context de Hadoop 2, separació de JobTracker en responsabilitats, quatre elements de l'arquitectura i quatre passos bàsics d'execució. Els diagrames ocupen bona part de les pàgines 1, 2 i 3. Les explicacions addicionals d'aquests apunts, incloses les comandes Linux/YARN, les configuracions XML, els exercicis i els exemples, són **material d'ampliació** i no una transcripció literal de la guia.

**Material de referència principal:** `M5075_NF1_2_DOC01B_YARN_Resum.pdf` · M5075 — Big Data Aplicat.
