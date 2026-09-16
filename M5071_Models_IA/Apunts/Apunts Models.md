# Apunts de Mòdul: Models d'Intel·ligència Artificial (M5071)
**Tema 1.1: Introducció a la Intel·ligència Artificial**[cite: 8]

---

## 1. Concepte d'Intel·ligència Artificial

### Definició i Ambigüitat
No existeix una única definició consensuada ni per al concepte d'**Intel·ligència** ni per al d'**Intel·ligència Artificial (IA)**[cite: 8]. Les definicions varien segons la font[cite: 8]:

* **Intel·ligència**:
  * *Enciclopèdia Britannica*: Habilitat d'aprendre de l'experiència, adaptar-se a noves situacions, entendre conceptes abstractes i utilitzar el coneixement per manipular l'entorn[cite: 8].
  * *Enciclopèdia.cat*: Facultat per comprendre el món i prendre'n consciència per resoldre situacions noves[cite: 8].
* **Intel·ligència Artificial**:
  * *Enciclopèdia Britannica*: Realització de tasques comunament associades a éssers intel·ligents[cite: 8].
  * *Enciclopèdia.cat*: Representació simbòlica del coneixement i dels mètodes d'inferència simbòlica per ordinador[cite: 8].
  * *Definicions generals*:
    * Branca de la computació i les matemàtiques que busca dotar les màquines de capacitats humanes com comunicar-se o aprendre[cite: 8].
    * Disciplina científica que s'ocupa de crear programes informàtics que executen operacions comparables a les de la ment humana (aprenentatge, raonament lògic)[cite: 8].

---

### Enfocaments de la IA

| Enfocament | Descripció | Objectiu i Problema |
| :--- | :--- | :--- |
| **IA com a Ciència Cognitiva** | Estudia el procés mental i com s'obté el resultat, no només la resposta[cite: 8]. | **Objectiu:** Generar models predictius com fórmules científiques[cite: 8].<br>**Problema:** Falta de dades i matemàtiques adequades[cite: 8]. |
| **IA com a Enginyeria del Coneixement** | Aplicació de tècniques pràctiques per resoldre problemes on la prioritat és el resultat[cite: 8]. | **Objectiu:** Mes pragmàtic i realista[cite: 8].<br>**Problema:** Absència d'una base sòlida de Teoria del Coneixement[cite: 8]. |

---

## 2. Principals Tipus, Tècniques i Subcamps d'IA

La classificació de la IA no és única i evoluciona constantment[cite: 8]. S'estructura en diferents nivells d'abstracció i jerarquia[cite: 8]:


```

+-------------------------------------------------------------------+
| INTEL·LIGÈNCIA ARTIFICIAL                                        |
| Capacitat per realitzar tasques que requereixen intel·ligència   |
| humana (Robòtica, Visió, PLN, Reconeixement de veu/to).           |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   | APRENENTATGE AUTOMÀTIC (MACHINE LEARNING)                  |   |
|   | Les màquines aprenen a base d'experiència sense          |   |
|   | intervenció humana directa.                               |   |
|   |                                                           |   |
|   |   +---------------------------------------------------+   |   |
|   |   | APRENENTATGE PROFUND (DEEP LEARNING)              |   |   |
|   |   | Algorismes inspirats en el cervell humà           |   |   |
|   |   | (Xarxes Neuronals Artificials, Generació de text).|   |   |
|   |   +---------------------------------------------------+   |   |
|   |                                                           |   |
|   | Tipus: Supervisat, No Supervisat, Per Reforç.             |   |
|   +-----------------------------------------------------------+   |
+-------------------------------------------------------------------+

```

### Tècniques Principals d'IA
* **Sistemes de Machine Learning (ML)**: Algorismes supervisats, no supervisats i d'aprenentatge per reforç[cite: 8].
* **Xarxes Neuronals Artificials (ANN)**: Modelat inspirat en el funcionament del cervell[cite: 8].
* **Sistemes basats en regles i Raonament basat en casos**: Inferència de coneixement a partir de regles predefinides o experiències prèvies[cite: 8].
* **Algorismes Genètics**: Optimització basada en principis de selecció natural i evolució[cite: 8].
* **Automàts Cel·lulars**: Models sistemàtics de regles sobre graelles discretes[cite: 8].
* **Sistemes Difusos (*Fuzzy Logic*)**: Gestió del raonament amb graus d'incertesa[cite: 8].
* **Sistemes Multiagent**: Coordinació de múltiples entitats intel·ligents[cite: 8].

---

## 3. Història i Evolució de la IA

### Inicis (Anys 40 - Mitjans dels 60)
* **Anys 40**: McCulloch i Pitts creen el primer model teòric de neurona artificial[cite: 8].
* **1950**: Alan Turing publica "Poden pensar les màquines?" i proposa la **Prova de Turing** ("joc d'imitació") per determinar la intel·ligència d'una màquina[cite: 8].
* **1955/1956**: John McCarthy encunya oficialment el terme *"Intel·ligència Artificial"*[cite: 8].
* **Desenvolupaments clau**:
  * Neix el concepte de *Machine Learning*[cite: 8].
  * Creació del llenguatge LISP per a informació simbòlica[cite: 8].
  * Primers models supervisats, no supervisats i primeres idees de Processament de Llenguatge Natural (PLN)[cite: 8].
  * Primeres IA conversacionals (**ELIZA** al MIT per Joseph Weizenbaum) i sistemes experts (**DENDRAL**)[cite: 8].
  * Creació del robot industrial **UNIMATE** (1961) a General Motors i el robot d'ús general **SHAKEY** (1966) a Stanford[cite: 8].

---

### Hiverns de la IA (Anys 70 - Anys 80)
* **Anys 70**: Etapes de retallades en inversió i interès per no assolir les expectatives i l'optimisme inicials[cite: 8]. Els sistemes s'avaluaven com a costosos i amb fallades[cite: 8].
* **Desenvolupaments clau**:
  * Continua el desenvolupament de sistemes experts com **MYCIN**[cite: 8].
  * Aconseguiments en sistemes d'experts i projectes de cinquena generació de computadors al Japó[cite: 8].
  * Innovacions en robòtica humanoide i visió per computador[cite: 8].
  * Introducció de models per processar la informació incerta, com les **Xarxes Bayesianes**[cite: 8].
  * Innovacions tecnològiques en xarxes neuronals[cite: 8].

---

### Explosió de l'Aprenentatge Profund (Anys 90 - 2010s)
* **Desenvolupament de Deep Learning**: S'utilitza per entrenar xarxes neuronals complexes, desencadenant un gran creixement en les dècades posteriors[cite: 8].
* **Anys 90**:
  * **1997**: La computadora **Deep Blue** d'IBM guanya el campió mundial d'escacs Garri Kaspàrov[cite: 8].
  * Creació de chatbots avançats (**ALICE**) i desenvolupaments en robòtica social com **KISMET** (MIT) o la mascota robòtica **AIBO** de Sony (1999)[cite: 8].
* **Anys 2000 - 2010**:
  * Robòtica domèstica de massa (**Roomba** el 2002)[cite: 8].
  * Substitució de CPUs per **GPUs** per accelerar el processament de la IA[cite: 8].
  * Debats teòrics sobre la IA ètica i l'aparició d'IAs "sobrehumanes"[cite: 8].
  * **2011**: **IBM Watson** guanya el concurs *Jeopardy!*[cite: 8] i Apple integra **Siri** com a assistent virtual[cite: 8].
  * **2014**: Lanzament d'**Amazon Alexa**[cite: 8] i aparició del chatbot **Eugene Goostman**, que supera la prova de Turing segons un terç dels jutges[cite: 8].

---

### Era Actual (2010s - Actualitat)
* **2016**: El bot de Microsoft, **Tay**, falla a xarxes socials per comentaris no desitjats, remarcant la importància de l'ètica i el control[cite: 8].
* **2017**: **AlphaGo** de Google (DeepMind) guanya a Ke Jie en el joc de Go (joc amb més de $2^{70}$ posicions possibles)[cite: 8].
* **Models Llenguatge Massius (LLMs) i Generatius**:
  * OpenAI presenta **GPT-3**, demostrant una capacitat sense precedents per comprendre i generar llenguatge natural[cite: 8].
  * Proliferació de models multimodals capaços de processar i generar text, imatge, àudio i codi[cite: 8].

```
