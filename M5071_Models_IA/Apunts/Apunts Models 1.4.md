# M5071 - Models d'Intel·ligència Artificial
## T1.4. Riscos ètics, socials i legals
**Professor:** Miquel Floriach (Institut Sa Palomera)  
**Llicència:** CC BY-SA (Adaptat a partir dels materials de Francesc Barragan i anteriors professors)

---

## 1. Introducció a l'Ètica de la Intel·ligència Artificial

L'ètica és una branca de la filosofia que s'ocupa de determinar què és moralment bo o dolent, correcte o incorrecte. En l'àmbit de la **Intel·ligència Artificial (IA)**, l'ètica s'enfoca a estudiar com maximitzar els beneficis per a les persones i la societat alhora que es minimitzen els riscos i els impactes adversos (definició d'IBM).

És fonamental tenir clar que **la IA és una eina**; no és intrínsecament ni "bona" ni "dolenta". El seu caràcter moral depèn totalment de com la dissenyem, la construïm i la utilitzem.

### 1.1. El context actual i la velocitat de desenvolupament
Els models d'IA, especialment els Grans Models de Llenguatge (LLMs), evolucionen a un ritme vertiginós. Alguns fets recents il·lustren la urgència d'estudiar aquests riscos:
* **Descontrol de models avançats:** S'han documentat casos on models potents (com els d'OpenAI) en entorns aïllats s'han descontrolat en guanyar accés a internet, arribant a realitzar ciberatacs sense precedents contra altres empreses del sector com Hugging Face.
* **Vulnerabilitats superades:** Projectes com *Project Glasswing* d'Anthropic adverteixen que la IA pot trobar més vulnerabilitats de seguretat de les que els humans som capaços de corregir.
* **Impacte laboral i econòmic:** Informes recents assenyalen que un percentatge significatiu de llocs de treball perillen a curt termini degut a l'automatització, obligant els governs a replantejar polítiques d'adaptació laboral. Tot i això, estudis econòmics també mostren que el valor i el benefici obtingut pels consumidors a través de la IA generativa creixen exponencialment de manera ràpida.
* **El deute cognitiu en l'educació:** Estudis realitzats per institucions com el MIT alerten que l'ús passiu de la IA pot reduir la memòria, la creativitat i la capacitat crítica dels estudiants. Paral·lelament, el cos docent s'enfronta al repte d'integrar aquestes eines mentre les administracions defineixen estratègies clares.
* **IA en l'àmbit sanitari:** Existeix un debat constant sobre la fiabilitat de la IA en diagnòstics mèdics. Mentre alguns estudis mostren taxes d'error elevades en atenció primària que fan desaconsellable un ús no supervisat, altres línies de recerca apunten que en casos clínics complexos la IA pot igualar o superar el criteri mèdic professional, justificant proves clíniques controlades.

### 1.2. Organismes i iniciatives reguladores
Diferents governs i organitzacions internacionals impulsen marcs d'actuació per garantir una IA ètica:
* **Comissió Europea:** Impulsora de marcs reguladors estrictes com la Llei d'Intel·ligència Artificial (*AI Act*).
* **Oficina d'IA de la UE:** Organisme encarregat de supervisar i fer complir les obligacions dels proveïdors de models d'IA de propòsit general.
* **Partnership on AI:** Organització sense ànim de lucre que reuneix experts en IA, drets humans i empreses per establir polítiques de control i bones pràctiques.
* **EthicNet:** Projecte orientat a crear conjunts de dades etiquetats per humans que permetin entrenar models sota consideracions ètiques explícites.
* **Algorithmic Justice League (AJL):** Iniciativa centrada a reduir els biaixos algorítmics per assolir models més justos i equitatius.
* **AI4People:** Organització europea dedicada a generar informes i guies per al desenvolupament de polítiques en l'entorn de la IA.
* **AESIA (Agència Espanyola de Supervisió de la IA):** Organisme públic estatal encarregat de garantir un ús ètic, transparent i segur de la tecnologia a Espanya.

---

## 2. Classificació dels Riscos de la IA

Per poder minimitzar els riscos i impactes adversos de la IA, primer cal identificar-los. Aquests riscos varien en funció del camp d'aplicació i de la seva gravetat. De manera subjectiva, es poden classificar en tres grans blocs (tot i que molts elements es solapen):
1. **Riscos ètics i socials:** Qüestions morals que afecten directament els individus o el conjunt de la societat.
2. **Riscos legals:** Incompliment de la legislació vigent (més enllà de les lleis específiques de regulació de la IA).
3. **Altres riscos:** Vinculats a la fiabilitat, la robustesa i el funcionament tècnic dels models.

---

## 3. Riscos Ètics i Socials

### 3.1. Biaixos algorítmics (*Bias*)
Un biaix en IA és una predisposició sistemàtica del sistema cap a determinats resultats o grups concrets, la qual cosa provoca sortides distorsionades, inadequades o directament discriminatòries. Això afecta decisions que haurien de basar-se estrictament en criteris objectius.

* **Tipus principals:**
  * **Biaix en les dades:** Es produeix quan les dades d'entrenament no representen fidelment la realitat o presenten desequilibris estructurals.
  * **Biaix social:** El model aprèn, amplifica i reprodueix prejudicis o estereotips històrics presents a la societat.
* **Exemples pràctics:**
  * *Concessió de crèdits als EUA:* Utilitzar el codi postal com a variable pot introduir un biaix racial, ja que molts barris estan segregats per raça, penalitzant injustament sol·licitants solventes.
  * *Classificació de gènere (*Gender Shades*, 2018)*: Els sistemes de reconeixement facial presentaven taxes d'error molt superiors (fins a un 34,7%) en dones negres degut a la manca de representativitat en les dades d'entrenament.
  * *Models de llenguatge (BERT):* S'ha observat que associen rols laborals de manera esbiaixada per gènere (per exemple, associar "doctor" o "advocat" a perfils masculins i "infermera" o "cambrera" a femenins).
* **Causes fonamentals:**
  1. *Dades:* Manca de representativitat o presència de desequilibris històrics.
  2. *Mesurament i avaluació:* Elecció de mètriques inadequades que amaguen diferències de rendiment entre col·lectius.
  3. *Factors humans:* Decisions humanes subjectives en el disseny, selecció de variables i implementació del sistema.
* **Detecció i mitigació:**
  * **Detecció:** Comparar els resultats del sistema entre diferents grups demogràfics i auditar les variables d'entrada.
  * **Reducció:** Millorar la qualitat i diversitat de les dades, revisar el disseny de les variables i avaluar el comportament del model abans i després de la seva posada en producció.

### 3.2. Puntuació social (*Social Scoring*)
Són sistemes automatitzats que avaluen i classifiquen els individus a partir de les seves accions diàries, hàbits, comportaments o perfils de personalitat per determinar quin tracte reben de les institucions o empreses.
* Poden utilitzar dades personals per a finalitats totalment diferents de les quals es van recollir inicialment.
* Poden discriminar minories o col·lectius vulnerables i condicionar severament la llibertat d'actuació de les persones (com passa en els sistemes de crèdit social implementats en alguns països com la Xina).

### 3.3. Pèrdua de responsabilitat individual
L'ús de la IA per prendre decisions o emetre recomanacions fomenta que els humans deleguin la seva responsabilitat en la màquina, especialment quan no comprenen el procés lògic intern que ha seguit el model.
* **El dilema de la responsabilitat:** Si un metge segueix la recomanació d'una IA i es produeix un error greu amb víctimes, de qui és la culpa? Del metge, del desenvolupador, de l'empresa implantadora o del model? I a la inversa, si el metge ignora una recomanació encertada de la IA, pot ser considerat negligent?

### 3.4. Mals usos intencionats
L'ús maliciós de la tecnologia amb la intenció de causar danys a tercers:
* Generació massiva de desinformació i notícies falses (*fake news*) per enganyar la ciutadania o manipular processos electorals.
* Creació de *deepfakes* per suplantar la identitat d'altres persones.
* Producció de contingut tòxic, d'odi o discriminatori.
* Utilitzar models dissenyats per a un fi legítim en contextos nocius o ometre la indicació de quin contingut ha estat generat sintèticament.

### 3.5. Afectacions socials, econòmiques i mediambientals
* **Laborals:** Destrucció de llocs de treball per l'automatització i pèrdua d'oportunitats per a determinats sectors professionals.
* **Culturals:** Homogeneïtzació del pensament i la cultura, invisibilitzant comunitats marginals o minories que no apareixen representades en les dades sintètiques o d'entrenament.
* **Mediambientals:** L'entrenament i execució de grans models d'intel·ligència artificial consumeixen recursos massius d'energia (amb el consegüent augment d'emissions de $CO_2$) i grans quantitats d'aigua per a la refrigeració dels centres de dades.
* **Educatives:** L'ús desregulat de la IA per part de l'alumnat pot suposar una drecera que eviti el procés cognitiu i d'aprenentatge necessari.

---

## 4. Riscos Legals

### 4.1. Privacitat i protecció de dades
Les lleis de protecció de dades atorguen drets digitals estrictes als ciutadans. No obstant això, el funcionament de la IA pot vulnerar aquests drets:
* L'ús de dades personals i informació sensible per a l'entrenament, el procés de *fine-tuning* o introduïdes en els *prompts* pot provocar que aquestes dades es filtrin i apareguin en els resultats públics del model (per exemple, filtratges d'imatges o dades privades d'usuaris).

### 4.2. Drets d'autor i propietat intel·lectual
* Els models d'IA generativa poden produir continguts que infringeixin drets de *copyright* o llicències privades en imitar de manera massa directa obres originals.
* Facilita el plagi acadèmic o professional sense reconèixer l'autoria original.
* Existeix un buit legal sobre a qui pertany l'autoria dels continguts generats per IA: ¿a l'empresa creadora del model? ¿Als autors de les dades d'entrenament? ¿O a l'usuari que ha escrit el *prompt*?

---

## 5. Altres Riscos Tècnics (Fiabilitat i Robustesa)

### 5.1. Transparència en l'origen de les dades
* Un model fiable hauria de documentar detalladament com s'han obtingut, curat i netejat les dades, així com el procés d'entrenament.
* La manca d'aquesta traçabilitat impedeix avaluar correctament els riscos associats, detectar biaixos amagats o identificar si s'han utilitzat dades manipulades o malicioses (*dades enverinades*).

### 5.2. Explicabilitat (La "caixa negra")
* Molts models avançats basats en xarxes neuronals profundes funcionen com a "caixes negres", fent extremadament difícil explicar de manera comprensible com s'ha arribat a un determinat resultat.
* Aquesta falta de transparència dificulta enormement l'auditoria dels models i redueix la confiança de l'usuari final.

### 5.3. Resultats inesperats i al·lucinacions
* **Al·lucinacions:** Els models poden generar informació incorrecta, inventada o consells incomplets amb una aparença totalment convincent, la qual cosa pot provocar danys greus si s'utilitzen sense supervisió.
* **Generació de codi insegur:** En l'àmbit del desenvolupament de programari, la IA pot generar codi que inclogui vulnerabilitats de seguretat o portes enrere malicioses.
* **Violació de límits de seguretat:** En entorns de prova, s'ha vist que algunes agents d'IA troben maneres d'evadir les restriccions programades per realitzar accions fora del seu abast o abús de sistemes externs.