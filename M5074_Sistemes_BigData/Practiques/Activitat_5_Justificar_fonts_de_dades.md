# Activitat 5: Justificar Fonts de Dades i Tipologies de Dades en Big Data

> **Mòdul:** M5074 Sistemes de Big Data
>
> **Unitat Formativa / Tema:** Gestió, Tipologia i Identificació de Fonts de Dades
>
> **Cicle Formatiu:** Curs d'Especialització en IA & BD (ASIX / DAW / DAM)
>
> **Centre:** Institut Sa Palomera (Generalitat de Catalunya — Departament d'Educació i FP)
>
> **Curs Acadèmic:** 2026/2027
>
> **Autor de la pràctica:** Sergi Gallart Fanlo
>
> **Professor:** Francesc Barragán

---

## Taula de Continguts

1. [Resum Executiu i Objectius](#1-resum-executiu-i-objectius)
2. [Marc Teòric: Classificació de les Dades](#2-marc-teòric-classificació-de-les-dades)
   * [2.1. Segons l'Origen: Dades Primàries vs. Secundàries](#21-segons-lorigen-dades-primàries-vs-secundàries)
   * [2.2. Segons la Naturalesa: Dades Quantitatives vs. Qualitatives](#22-segons-la-naturalesa-dades-quantitatives-vs-qualitatives)
   * [2.3. Segons l'Estructura: Dades Estructurades, Semiestructurades i No Estructurades](#23-segons-lestructura-dades-estructurades-semiestructurades-i-no-estructurades)
3. [Escenari 1: NoCancer Pharma](#3-escenari-1-nocancer-pharma)
   * [Context de l'Empresa](#context-de-lempresa)
   * [Conjunt de Preguntes 1: Dades de Fonts de Pacients](#conjunt-de-preguntes-1-dades-de-fonts-de-pacients)
   * [Conjunt de Preguntes 2: Dades Diagnòstiques](#conjunt-de-preguntes-2-dades-diagnòstiques)
4. [Escenari 2: Megacracks Associates](#4-escenari-2-megacracks-associates)
   * [Context de l'Empresa](#context-de-lempresa-1)
   * [Conjunt de Preguntes 1: Dades de l'Equip](#conjunt-de-preguntes-1-dades-de-lequip)
   * [Conjunt de Preguntes 2: Dades de Reclutament](#conjunt-de-preguntes-2-dades-de-reclutament)
5. [Matriu Comparativa i Taula d'Anàlisi Global](#5-matriu-comparativa-i-taula-danàlisi-global)
6. [Conclusions i Aplicabilitat en Entorns Big Data](#6-conclusions-i-aplicabilitat-en-entorns-big-data)

---

## 1. Resum Executiu i Objectius

En entorns d'anàlisi de Big Data i Intel·ligència Artificial, la correcta identificació i classificació de les fonts de dades és un pas fonamental abans d'iniciar qualsevol procés d'ingesta (ETL/ELT) o disseny d'arquitectures d'emmagatzematge.

### Objectius d'Aprenentatge

* **Diferenciar les fonts d'origen de dades:** Identificar quan s'han de recollir dades directament (*Primàries*) i quan s'han d'aprofitar fonts existents (*Secundàries*).
* **Avaluar la naturalesa de la informació:** Discernir entre dades mesurables numèricament (*Quantitatives*) i dades descriptives o multimèdia (*Qualitatives*).
* **Determinar el nivell d'estructuració:** Catalogar la informació segons si es pot emmagatzemar fàcilment en taules i esquemes rígids (*Estructurades*) o si requereix tractament avançat de fitxers no formats (*No estructurades*).
* **Aplicar la presa de decisions en casos d'estudi reals:** Analitzar escenaris del sector biomèdic (*NoCancer Pharma*) i de l'anàlisi esportiva d'alt rendiment (*Megacracks Associates*).

---

## 2. Marc Teòric: Classificació de les Dades

### 2.1. Segons l'Origen: Dades Primàries vs. Secundàries

* **Dades Primàries:** Són aquelles recopilades de primera mà per l'organització específicament per a l'objectiu actual de la investigació.
  * *Avantatges:* Alta precisió, adaptades als requisits de l'estudi, control total sobre la qualitat.
  * *Inconvenients:* Cost elevat i requereixen temps per a la seva obtenció.
* **Dades Secundàries:** Són dades recollides prèviament per terceres parts (organismes públics, altres empreses, registres històrics) amb finalitats diferents.
  * *Avantatges:* Disponibilitat immediata i menor cost d'obtenció.
  * *Inconvenients:* Poden no ajustar-se perfectament a la necessitat concreta o requerir processos complexos de neteja i homogeneïtzació.

### 2.2. Segons la Naturalesa: Dades Quantitatives vs. Qualitatives

* **Dades Quantitatives:** Dades de naturalesa numèrica o mesurable. Permeten l'aplicació directa d'operacions matemàtiques i anàlisi estadística.
  * *Exemples:* Edat, temperatura, salari, temps de tractament, comptatge de gols.
* **Dades Qualitatives:** Dades no numèriques que descriuen atributs, propietats, funcions, o contingut multimèdia.
  * *Exemples:* Notes escrites de metges, imatges mèdiques, arxius d'àudio, vídeos de partits de futbol, impressions o observacions visuals.

### 2.3. Segons l'Estructura: Dades Estructurades, Semiestructurades i No Estructurades

* **Dades Estructurades:** Tènen un format i esquema rígid i ben definit. Es poden organitzar directament en taules amb columnes i files (com fulls de càlcul o bases de dades relacionals SQL).
* **Dades Semiestructurades:** No s'ajusten a una taula rígida però contenen etiquetes o marcadors per separar els seus elements (ex: JSON, XML, YAML).
* **Dades No Estructurades:** Manquen d'una estructura interna predefinida. No es poden emmagatzemar directament en un full de càlcul sense processament previ.
  * *Exemples:* Imatges (DICOM, PNG), àudio (WAV, MP3), text lliure, vídeos (MP4).

---

## 3. Escenari 1: NoCancer Pharma

### Context de l'Empresa

**NoCancer Pharma** és una companyia farmacèutica que està desenvolupament un medicament genèric contra el càncer. El seu objectiu és determinar si el fàrmac redueix la propagació del càncer o disminueix la mida dels tumors sense perjudicar els pacients, obtenint l'aprovació ràpidament per davant de la competència.

---

### Conjunt de Preguntes 1: Dades de Fonts de Pacients

En aquesta fase es recullen dades demogràfiques, mèdiques i de tractament dels participants en l'estudi (edat, temps de tractament, nombre de sessions i escala numèrica d'agressivitat del càncer).

#### 1. Tipus d'Origen: Primàries o Secundàries?
* **Resposta:** **Dades Primàries.**
* **Justificació:** NoCancer Pharma ha de recopilar la informació directament dels pacients que participen en l'assaig clínic. Això garanteix que les dades siguin específiques, controlades, actualitzades i totalment adaptades als paràmetres concrets que avalua l'estudi mèdic.

#### 2. Naturalesa de la Dada: Quantitatives o Qualitatives?
* **Resposta:** **Dades Quantitatives.**
* **Justificació:** Totes les variables recollides en aquest grup tenen caràcter numèric (l'edat en anys, la durada del tractament en dies/setmanes, el número de sessions realitzades i la puntuació en l'escala d'agressivitat). Aquestes variables permeten realitzar comparacions estadístiques de l'eficàcia del medicament.

#### 3. Nivell d'Estructura: Estructurades o No Estructurades?
* **Resposta:** **Dades Estructurades.**
* **Justificació:** Aquestes variables es poden organitzar i emmagatzemar fàcilment en formats taulars (com bases de dades relacionals o fulls de càlcul), assignant columnes definides per a cadascun dels camps (ex: `ID_Pacient`, `Edat`, `Temps_Tractament`, `Num_Tractaments`, `Nivell_Agressivitat`).

---

### Conjunt de Preguntes 2: Dades Diagnòstiques

Aquestes dades inclouen les notes escrites dels metges, imatges de tomografia computada (TAC) i fitxers d'àudio de l'historial mèdic del pacient.

#### 1. Tipus d'Origen: Primàries o Secundàries?
* **Resposta:** **Dades Primàries.**
* **Justificació:** Són dades generades directament durant l'avaluació diagnòstica dels pacients participants per part dels equips mèdics de l'estudi, assegurant un seguiment directe i precís de l'evolució del tumor.

#### 2. Naturalesa de la Dada: Quantitatives o Qualitatives?
* **Resposta:** **Dades Qualitatives.**
* **Justificació:** Les dades utilitzades (notes de text lliure, imatges mèdiques complexes i gravacions d'àudio) no són inherentment numèriques, sinó descripcions qualitatives de l'estat del pacient i visualitzacions de la massa tumoral.

#### 3. Nivell d'Estructura: Estructurades o No Estructurades?
* **Resposta:** **Dades No Estructurades.**
* **Justificació:** Els arxius d'àudio, les imatges mèdiques i les notes escrites en format lliure no tenen una estructura tabular uniforme ni encaixen en columnes de fulls de càlcul. Cal utilitzar sistemes especialitzats (com magatzems d'objectes o bases de dades NoSQL) i eines de IA/Processament de Llenguatge Natural (NLP) per analitzar-les.

---

## 4. Escenari 2: Megacracks Associates

### Context de l'Empresa

**Megacracks Associates** és una agència de reclutament esportiu centrada en la identificació i fitxatge de jugadors de futbol juniors per a equips de la Lliga de Futbol Professional (LFP). L'agència necessita identificar les manques dels equips, les fortaleses dels jugadors i analitzar dades d'esdeveniments en temps real (imatges de partits, estadístiques en directe).

---

### Conjunt de Preguntes 1: Dades de l'Equip

Aquestes dades inclouen les estadístiques de rendiment en cada posició, el nombre de jugadors sota contracte per posició i els salaris dels jugadors.

#### 1. Tipus d'Origen: Primàries o Secundàries?
* **Resposta:** **Dades Secundàries.**
* **Justificació:** Megacracks Associates pot obtenir aquesta informació directament de les bases de dades oficials de la LFP, dels propis clubs de futbol o d'organismes públics de gestió esportiva. L'agència no necessita generar ni mesurar aquestes dades de primera mà.

#### 2. Naturalesa de la Dada: Quantitatives o Qualitatives?
* **Resposta:** **Dades Quantitatives.**
* **Justificació:** Totes les dades recollides (nombre de jugadors per lloc, salaris en euros, percentatges de victòries o mètriques de rendiment per posició) són valors numèrics mesurables que permeten realitzar comparacions financeres i esportives immediates.

#### 3. Nivell d me l'Estructura: Estructurades o No Estructurades?
* **Resposta:** **Dades Estructurades.**
* **Justificació:** La informació encaixa de manera natural en un model taular (ex: columnes com `Posicio`, `Num_Jugadors_Contractats`, `Salari_Mitjà`, `Rendiment_Posició`), essent molt fàcilment organitzable en fulls de càlcul o bases de dades relacionals.

---

### Conjunt de Preguntes 2: Dades de Reclutament

Aquestes dades inclouen les estadístiques de rendiment individuals dels jugadors, informes d'entrenament i resultats de les proves de condició física.

#### 1. Tipus d'Origen: Primàries o Secundàries?
* **Resposta:** **Dades Primàries.**
* **Justificació:** Els otejadors (*scouts*) i preparadors físics de Megacracks Associates han de recopilar aquesta informació de primera mà mitjançant l'observació directa, l'execució de tests físics específics i l'avaluació personalitzada dels joves talents per obtenir un avantatge competitiu.

#### 2. Naturalesa de la Dada: Quantitatives o Qualitatives?
* **Resposta:** **Dades Quantitatives.**
* **Justificació:** La valoració clau d'aquestes dades es basarà en valors mètrics i numèrics objectius (temps en carreres de velocitat, potència de salt, percentatge de passada amb èxit, quilòmetres recorreguts, etc.), facilitant la comparació objectiva entre diferents candidats.

#### 3. Nivell d'Estructura: Estructurades o No Estructurades?
* **Resposta:** **Dades Estructurades.**
* **Justificació:** Les mètriques obtingudes de les proves físiques i les estadístiques directes de rendiment es poden estandarditzar en un format estructurat amb camps predefinits (ex: `Nom_Jugador`, `Temps_100m`, `Percentatge_Passada`, `Mètrica_Física`), facilitant el seu filtratge i ordenació.

---

## 5. Matriu Comparativa i Taula d'Anàlisi Global

A continuació es mostra la síntesi de la classificació de dades per als dos escenaris analitzats:

| Escenari | Categoria de Dades | Tipus de Font (Origen) | Naturalesa | Nivell d'Estructura | Eines d'Emmagatzematge/Tractament recomanades |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NoCancer Pharma** | **Background Pacients** | Primària | Quantitativa | Estructurada | Base de dades Relacional (SQL) / CSV / Fulls de Càlcul |
| **NoCancer Pharma** | **Diagnòstiques** | Primària | Qualitativa | No Estructurada | Data Lake / Object Storage (S3) / BSON (MongoDB) / Models IA (NLP, Visió per Computador) |
| **Megacracks Assoc.** | **Dades d'Equip** | Secundària | Quantitativa | Estructurada | Base de dades Relacional / Data Warehouse (SQL) |
| **Megacracks Assoc.** | **Dades Reclutament** | Primària | Quantitativa | Estructurada | Base de dades Relacional / Sistema CRM de Reclutament |

---

## 6. Conclusions i Aplicabilitat en Entorns Big Data

1. **Heterogeneïtat de les Fonts de Dades:** Com s'ha demostrat a l'escenari de *NoCancer Pharma*, un projecte d'investigació modern sovint requereix combinar dades estructurades (paràmetres numèrics del pacient) amb dades no estructurades (imatges TAC o gravacions). Això justifica la necessitat d'arquitectures com els **Data Lakes** o tecnologies NoSQL/Persistència Poliglota.
2. **Optimitació de Recursos d'Origen:** En casos com *Megacracks Associates*, utilitzar dades secundàries per al context general (equips i salaris) redueix costos, permetent concentrar els recursos econòmics i humans en la recollida de dades primàries de valor afegit (reclutament i talent jove).
3. **Estandardització per a la Presa de Decisions:** Convertir les dades de rendiment en mètriques **quantitatives i estructurades** permet als algorismes analítics i als sistemes d'IA avaluar jugadors i tractaments mèdics de manera objectiva i automàtica.