# NF1: Introducció a l'Aprenentatge Automàtic (Machine Learning)

## 1. Aspectes Generals i Història de la IA

* **Orígens històrics:**
* **Aristòtil (348–322 a.C.):** Estudia la possibilitat de construir un sistema hidràulic que imités el cervell humà.


* **Ramon Llull (1315):** Publica l'*Ars Magna*, on planteja les bases del raonament automàtic i la demostració lògica mitjançant màquines.


* **Alan Turing (1950):** Publica *"Computing Machinery and Intelligence"* i introdueix el **Test de Turing** per mesurar el comportament intel·ligent d'una màquina.


* **Teorema d'Incompletitud de Gödel (1931):** Estableix les limitacions dels sistemes basats en regles lògiques.




* **Conferència de Dartmouth (1956):** Naixement formal de la Intel·ligència Artificial com a disciplina.


* **Logic Theorist (A. Newell i H. Simon):** Primer programa d'ordinador que simulava el pensament humà demostrant teoremes matemàtics.




* **Evolució posterior:**
* **Anys 70:** Naixement del Processament del Llenguatge Natural (NLP).


* **Anys 80:** Primeres aplicacions comercials i aparició dels **Sistemes Experts**.


* **Anys 90 (IBM Deep Blue):** Algorismes de cerca i anàlisi massiva aplicats als escacs.


* **Actualitat:** Enfocament centrat en el tractament, la mineria de dades (*Data Mining*) i la *Business Intelligence*.





---

## 2. Definició i Tipus d'Intel·ligència Artificial

**Objectius principals de la IA:** Deducció, raonament, representació del coneixement, planificació, NLP, aprenentatge, percepció i manipulació.

| Característica | IA Feble / Específica (ANI) | IA Forta / General (AGI) |
| --- | --- | --- |
| **Estat real** | Existeix actualment

 | Només en ciència-ficció

 |
| **Focus** | Tasques concretes i limitades (ex. Siri, AlphaGo)

 | Problemes oberts, capacitats humanes generals

 |
| **Comportament** | Reactiu, computa sense raonar

 | Proactiu, imita el pensament humà

 |
| **Programació** | Programada per humans

 | S'autoprograma i apron contínuament

 |

### IA vs. Machine Learning vs. Deep Learning

* **Intel·ligència Artificial (IA):** Concepte global per aconseguir que les màquines pensin o raonin com els humans.


* **Machine Learning (ML):** Subcamp de la IA centrat en l'ús de dades i algorismes perquè els sistemes reconeguin patrons i facin prediccions sense programació explícita.


* **Deep Learning (DL):** Subcamp del ML basat en xarxes neuronals artificials profundes que aprenen automàticament amb grans volums de dades.



---

## 3. Què és i com treballa el Machine Learning?

Definit per **Arthur Samuel (1959)** com la capacitat dels ordinadors d'aprendre sense ser programats explícitament. Segons **Tom Mitchell (1997)**, un programa aprèn d'una **Experiència (E)** respecte a una **Tasca (T)** si el seu rendiment mesurat per **(P)** millora amb E.

### Procés de treball general

1. Recopilació i exploració de les dades (Data Cleaning/EDA).


2. Entrenament de l'algorisme amb dades d'entrenament (*Training Data*) per generar un **Model**.


3. Avaluació del model amb noves dades (*Test Data*).


4. Ajust i implementació si la precisió compleix els objectius.



> **Regles empíriques principals:**
> * **80/20 del temps:** 80% preparació/neteja de dades, 20% modelatge i avaluació.
> 
> 
> * **80/20 de les dades:** 80% de dades per a entrenament (*Train*), 20% per a validació/test (*Test*).
> 
> 
> 
> 

---

## 4. Tipus d'Aprenentatge Automàtic

### A. Segons la supervisió durant l'entrenament

* **Aprenentatge Supervisat:** Es disposa d'entrades ($X$) i de les seves corresponents etiquetes/respostes ($Y$).


* **Classificació:** Prediu una variable categòrica (ex. *Spam/No Spam*, *Tumor benigne/maligne*).


* **Regressió:** Prediu un valor numèric continu (ex. *Preu d'un habitatge*, *Vendes*).


* *Algorismes:* Regressió Lineal/Logística, kNN, SVM, Arbres de Decisió, Random Forest, Naive Bayes, Xarxes Neuronals.




* **Aprenentatge No Supervisat:** Dades sense etiquetar. El model descobreix patrons o estructures ocultes.


* **Agrupament (*Clustering*):** Agrupa dades similars (Ex. *K-Means, Fuzzy K-Means, GMM, DBSCAN, Clustering Jeràrquic*).


* **Reducció de Dimensionalitat:** Redueix el nombre de característiques mantinguent la informació essencial (Ex. *PCA, t-SNE, Factor Analysis*).


* **Detecció d'Anomalies:** Identifica valors atípics o *outliers* (Ex. *One-Class SVM, Isolation Forest*).


* **Regles d'Associació:** Descobreix relacions entre productes/variables (Ex. *Apriori, FP-Growth*).




* **Aprenentatge Semi-supervisat i Auto-supervisat:** Combina poques dades etiquetades amb moltes sense etiquetar.


* **Aprenentatge per Reforç (*Reinforcement Learning*):** Un **Agent** aprèn a prendre decisions en un **Entorn** mitjançant la presa d'**Accions**, rebent **Recompenses** o **Penalitzacions** per trobar la millor política (Ex. *AlphaGo, AWS DeepRacer*).



### B. Altres classificacions

* **Enfocament temporal:** Aprenentatge per lots (*Batch learning*) vs. Aprenentatge en línia (*Online learning*).


* **Estratègia:** Basat en instàncies (Ex. *k-NN*) vs. Basat en models (Ex. *Regressió lineal*).



---

## 5. Reptes del Machine Learning

* **Dades de poca qualitat:**
* *Outliers (Valors atípics):* Cal eliminar-los, corregir-los o mantenir-los segons el context.


* *Missing values (Valors nuls):* Poden imputar-se amb la mitjana/moda o eliminar les files/columnes afectades.




* **Dades no representatives:** Dades d'entrenament que no reflecteixen la realitat del problema.


* **Dades desbalancejades:** Una classe és molt més freqüent que una altra.


* *Solucions:* Down-sampling (eliminar dades de la majoritària), Over-sampling/SMOTE (generar dades sintètiques de la minoritària) o Matrius de Cost (penalitzar errors).




* **Underfitting (Subajustament):** El model és massa simple o té dades insuficients per extreure un patró.


* **Overfitting (Sobreajustament):** El model memoritza les dades d'entrenament (incloent-hi el soroll) i no té capacitat de generalitzar davant de noves dades.



### Validació i Cross-Validation

* Per avaluar si el model generalitza bé, es fan servir conjunt de Train i Test.


* **K-Fold Cross-Validation:** Es divideixen les dades en $K$ parts (folds). En cada iteració, s'utilitzen $K-1$ folds per entrenar i $1$ per validar, fent la mitjana dels resultats al final per obtenir un rendiment més robust.



---

## 6. Cicle de Vida d'un Projecte de ML i Rols

**Fases principals:**

1. Definició del problema i anàlisi de negoci.


2. Enginyeria de dades (Recol·lecció, preparació i exploració - EDA).


3. Modelat (Selecció de l'algorisme, entrenament i optimització).


4. Desplegament i Infraestructura (Formalització del pipeline i monitoratge).



**Rols a l'equip:** *Data Scientist*, *ML Engineer*, *Data Analyst*, *ML Software Engineer*, *Software Engineer*, *ML Researcher*.

---

## 7. Preparació i Transformació de Dades

### Exploració de Dades (EDA)

Fase essencial (aproximadament el 30% del temps) per conèixer distribucions, correlacions, valors nuls i *outliers* abans del modelatge.

### Transformacions Lineals (No modifiquen la distribució)

* **Min-Max Scaler:** Re-escala les dades entre 0 i 1 ($x' = \frac{x - x_{min}}{x_{max} - x_{min}}$). Molt sensible als *outliers*.


* **Standard Scaler (Z-score):** Centra les dades amb mitjana 0 i desviació estàndard 1 ($z = \frac{x - \mu}{\sigma}$).


* **Normalizer:** Esbala vectors individualment per fila perquè la seva norma sigui 1 (útil en processament de text/TF-IDF).



### Transformacions No Lineals (Sí modifiquen la distribució / Skewness)

* **Logarithmic Transform (`np.log1p`):** Utilitzat per reduir l'asimetria en dades amb cues llargues (Ex. *ingressos*).


* **Power Transformer (Yeo-Johnson / Box-Cox):** Transforma les dades perquè s'ajustin a una distribució gaussiana o normal.


* **Quantile Transformer:** Mapeja les dades a una distribució uniforme o normal basant-se en percentils; resistent a *outliers*.



> **Data Leakage (Fuita de dades):** Cal aplicar SEMPRE les transformacions i escalats sobre el conjunt de *Train* (`fit_transform`) i posteriorment aplicar-les al conjunt de *Test* (`transform`) sense tornar a aprendre. Es recomana utilitzar els **Pipelines de Scikit-learn**.
> 
> 

### Codificació de Variables Categòriques

* **One-Hot Encoding:** Crea una columna binària (0/1) per a cada categoria. Ideal quan no hi ha ordre natural.


* **Ordinal Encoding:** Assigna enters segons un ordre jeràrquic establert (Ex. *S, M, L*).


* **Target Encoding:** Reemplaça la categoria per la mitjana de la variable objectiu (*target*). Útil quan hi ha moltes categories, però requereix precaució amb el *data leakage*.
