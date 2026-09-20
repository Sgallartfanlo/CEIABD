# M5074: Ciència de Dades, Metodologies i Dades a l'Empresa

Aquest dipòsit conté els apunts estructurats i resums del mòdul **M5074**, cobrint des dels conceptes fonamentals de les dades fins a les metodologies de ciència de dades i la seva aplicació en l'entorn empresarial.

---

## 1. Introducció als Conceptes de Dades

### 1.1. Definicions i Importància
* **Dades**: Qualsevol col·lecció d'informació que es pot recopilar, analitzar i interpretar per a la presa de decisions.
* **Valor per als negocis**: Actiu valuós que permet optimitzar operacions, conèixer els clients, reduir costos, augmentar beneficits i innovar.
* **Impacte social**: ONG, governs i institucions les utilitzen per afrontar reptes globals (canvi climàtic, pobresa, malalties, etc.).
* **Volum actual**: Generació exponencial de dades (aproximadament 2,5 trilions de bytes diaris i una previsió superior als 180 zettabytes per al 2026).

---

### 1.2. Data Analysis vs. Data Analytics

* **Data Analysis**
  * **Enfocament:** Reactiu / Explicatiu
  * **Temporalitats / Objectiu:** **Passat:** Examina, neteja i transforma dades per respondre preguntes específiques.
  * **Exemple:** Analitzar les vendes passades d'entrades de cinema per trobar patrons de consum.

* **Data Analytics**
  * **Enfocament:** Proactiu / Predictiu
  * **Temporalitats / Objectiu:** **Futur:** Aplica tècniques i processos per identificar tendències i fer prediccions contínues.
  * **Exemple:** Utilitzar modelatge de dades per predir l'èxit de pel·lícules futures.

---

### 1.3. Classificació de les Dades

#### A. Segons l'Origen (Primàries vs. Secundàries)
* **Dades Primàries**: Recopilades directament per la mateixa organització/investigador per a un propòsit específic (enquestes, experiments, entrevistes).
  * *Avantatges*: Alta precisió, adaptabilitat i control de qualitat.
  * *Limitacions*: Major cost i temps.
* **Dades Secundàries**: Recollides per tercers (informes governamentals, bases de dades externes, etc.).
  * *Avantatges*: Més ràpides i econòmiques d'obtenir, gran volum.
  * *Limitacions*: Poden no ajustar-se perfectament a l'objectiu o ser menys precises.

#### B. Segons la Naturalesa (Quantitatives vs. Qualitatives)


```

```
                          DADES
                            │
    ┌───────────────────────┴───────────────────────┐

```

Quantitatives (Numèriques)               Qualitatives (Categòriques)
│                                               │
┌────┴───────────┐                              ┌────┴───────────┐
Discretes      Contínues                        Nominals        Ordinals
│
┌───────┴───────┐
Interval          Ràtio

```

1. **Dades Quantitatives** (Numèriques i mesurables):
   * **Discretes**: Valors enters i comptables (ex. número d'estudiants en una aula).
   * **Contínues**: Valors dins d'un rang continu, poden incloure decimals (ex. alçada, angles).
     * *D'Interval*: Tenen una escala amb punts equidistants però **sense zero absolut** (ex. temperatura en °C o °F; 0°C no vol dir "absència de temperatura").
     * *De Ràtio*: Inclouen un **zero absolut** que representa l'absència real de la propietat mesurada (ex. mesura d'alçada o temps des de zero).
2. **Dades Qualitatives** (Descriptives i no numèriques):
   * **Nominals**: Categories sense ordre natural (ex. color dels ulls, gènere).
   * **Ordinals**: Categories amb un ordre o escala lògica (ex. nivells de satisfacció: "molt d'acord", "d'acord", "en desacord").

#### C. Segons la Structura (Estructurades vs. No Estructurades)
* **Dades Estructurades**: Formats definits (taules, bases de dades relacionals, fulls de càlcul).
  * *Exemples*: Historial de transaccions, dates, números de compte.
  * *Pro/Contres*: Molt fàcils de consultar i analitzar, però poc flexibles davant canvis de requisits.
* **Dades No Estructurades**: Sense model predefinit.
  * *Exemples*: Fitxers d'àudio, vídeos de seguretat, imatges, publicacions en xarxes socials.
  * *Pro/Contres*: Aporten informació rica i complexa, però requereixen eines avançades d'IA i emmagatzematge especialitzat per processar-les.

---

## 2. Dades a l'Empresa (Business Data)

### 2.1. Dades Internes vs. Externes

* **Dades Internes (Primàries)**: Generades dins la pròpia organització.
  * *Tipus*: Financeres, de vendes, clients, operacions, empleats, màrqueting i comunicació.
  * *Avantatges*: Altament rellevants, confidencials, segures, d'accés ràpid i sota control propi de qualitat.
* **Dades Externes (Secundàries)**: Procedents de fora de l'organització.
  * *Tipus*: Públiques (dades obertes de governs), de tercers (data brokers), sindicades o d'associació/col·laboració.
  * *Avantatges*: Visibilitat del mercat, benchmark amb la competència, innovació i reducció de costos d'estudi.

---

### 2.2. Mètodes de Recollida de Dades

#### A. Recollida Manual
* **Enquestes**: Formularis estructurats per analitzar patrons en mostres representatives.
* **Entrevistes**: Converses a fons per obtenir insights qualificats.
* **Observació**: Registre directe del comportament en un entorn real.

#### B. Recollida Automatitzada (Instrumentació)
1. **Monitoratge continu**: Captura ininterrompuda de dades (ex. sensors de temperatura/pressió en fàbriques).
2. **Monitoratge d'intervals**: Captura en franges horàries programades per reduir costos (ex. videovigilància de 1:00 a 5:00).
3. **Basat en esdeveniments**: S'activa únicament quan succeeix una desviació o disparador (ex. detecció de frau bancari per pagament inusual).
4. **Seguiment en línia**: Monitoratge passiu de clics, desplaçaments i comportaments d'usuaris en webs/apps mòbils.

---

### 2.3. Segons la Comercialització i Ús

* **Dades Sindicades**: Recollides per una sola font que en ven llicències a múltiples empreses (ex. dades d'audiència de Nielsen). Baix cost, però nul avantatge competitiu exclusiu.
* **Dades de Tercers**: Comercialitzades per "brokers de dades" agregant diferents fonts. Útils per a nous mercats, però amb poc control de qualitat.
* **Dades Personalitzades**: Recollides i adaptades exclusivament per a una entitat (ex. recomanacions de Netflix). Alt cost, però màxim avantatge competitiu i rellevància.

---

## 3. Ciència de Dades i Metodologies

### 3.1. Definició i Mètode
La **Ciència de Dades** combina el mètode científic, les matemàtiques/estadística, la programació avançada, la Intel·ligència Artificial i la narració de dades (*data storytelling*) per extreure informació i valor oculta.
* **Tècnica clau (Els 5 Per què)**: Formulació iterativa d'aquesta pregunta per trobar la causa arrel d'un problema de negoci o tècnic.

---

### 3.2. Metodologies Clàssiques de Data Mining


```

+-------------------------------------------------------------------------+
|                              METODOLOGIES                               |
+-------------------+-------------------------------+---------------------+
|     CRISP-DM      |              KDD              |        SEMMA        |
|  (Business First) |   (Data Refining Process)     |  (Model Focused)    |
+-------------------+-------------------------------+---------------------+
| 1. Business Und.  | 1. Selecció                   | 1. Sample (Mostra)  |
| 2. Data Und.      | 2. Preprocessament            | 2. Explore          |
| 3. Data Prep.     | 3. Transformació              | 3. Modify           |
| 4. Modeling       | 4. Mineria de dades           | 4. Model            |
| 5. Evaluation     | 5. Interpretació i avaluació  | 5. Assess (Avaluar) |
| 6. Deployment     |                               |                     |
+-------------------+-------------------------------+---------------------+

```

* **CRISP-DM**: Enfocament cíclic i el més utilitzat; destaca per començar amb la **comprensió del negoci**.
* **KDD**: Enfocat en el refinament metòdic i l'extracció de coneixement des de bases de dades.
* **SEMMA**: Creat per SAS Institute, molt centrat en la part pràctica de modelat tècnic.

---

### 3.3. Els 6 Passos de la Metodologia del Curs

1. **Comprensió del Negoci**: Definició de la problemàtica, tallers de *Design Thinking*, definició del focus analític.
2. **Homologació i Preparació de Dades**: Fase que consumeix més temps (recollida, neteja de valors atípics/imputació de buits i integració de fonts).
3. **Representació i Transformació de Dades**: Utilització d'estadística descriptiva i transformació de dades no estructurades a valors numèrics (0 i 1, tokenització, normalització).
4. **Visualització i Presentació de Dades**: Creació de gràfics impactants i narratius per validar hipòtesis i comunicar resultats.
5. **Models de Dades (Entrenament de ML)**:
   * **Aprenentatge Supervisat**: Algorismes entrenats amb dades etiquetades (ex. classificació, detecció de frau, regressió).
   * **Aprenentatge No Supervisat**: Troba patrons en dades sense etiquetar (ex. agrupament/clustering, sistemes de recomanació, segmentació de clients).
6. **Implementació de Models**: Integració del model generat dins dels entorns de producció de l'empresa i el seu manteniment.

---

### 3.4. Equip de Treball en Projectes de Dades

* **Analista de Dades (Data Analyst)**: Recopila, organitza i analitza dades estructurades. Comunica resultats visualment.
* **Científic de Dades (Data Scientist)**: Desenvolupa hipòtesis, treballa amb dades estructurades/no estructurades i entrena models d'Aprenentatge Automàtic.
* **Enginyer de Dades (Data Engineer)**: Construeix i manté les canalitzacions (*pipelines*), la infraestructura de dades i implementa els models en producció.

```
