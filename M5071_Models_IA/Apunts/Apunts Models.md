# Apunts de Mòdul: Models d'Intel·ligència Artificial (M5071)
**Tema 1.1: Introducció a la Intel·ligència Artificial**

---

## 1. Concepte d'Intel·ligència Artificial

### Definició i Ambigüitat
No existeix una única definició consensuada ni per al concepte d'**Intel·ligència** ni per al d'**Intel·ligència Artificial (IA)**. Les definicions varien segons la font:

* **Intel·ligència**:
  * *Enciclopèdia Britannica*: Habilitat d'aprendre de l'experiència, adaptar-se a noves situacions, entendre conceptes abstractes i utilitzar el coneixement per manipular l'entorn.
  * *Enciclopèdia.cat*: Facultat per comprendre el món i prendre'n consciència per resoldre situacions noves.
* **Intel·ligència Artificial**:
  * *Enciclopèdia Britannica*: Realització de tasques comunament associades a éssers intel·ligents.
  * *Enciclopèdia.cat*: Representació simbòlica del coneixement i dels mètodes d'inferència simbòlica per ordinador.
  * *Definicions generals*:
    * Branca de la computació i les matemàtiques que busca dotar les màquines de capacitats humanes com comunicar-se o aprendre.
    * Disciplina científica que s'ocupa de crear programes informàtics que executen operacions comparables a les de la ment humana (aprenentatge, raonament lògic).

---

### Enfocaments de la IA

| Enfocament | Descripció | Objectiu i Problema |
| :--- | :--- | :--- |
| **IA com a Ciència Cognitiva** | Estudia el procés mental i com s'obté el resultat, no només la resposta. | **Objectiu:** Generar models predictius com fórmules científiques.<br>**Problema:** Falta de dades i matemàtiques adequades. |
| **IA com a Enginyeria del Coneixement** | Aplicació de tècniques pràctiques per resoldre problemes on la prioritat és el resultat. | **Objectiu:** Més pragmàtic i realista.<br>**Problema:** Absència d'una base sòlida de Teoria del Coneixement. |

---

## 2. Principals Tipus, Tècniques i Subcamps d'IA

La classificació de la IA no és única i evoluciona constantment. S'estructura en diferents nivells d'abstracció i jerarquia:

![Mapa de Models i Tècniques d'IA](./img/M01%20-%20Models%20de%20Intel%C2%B7lig%C3%A8ncia%20Artificial.png)

### Tècniques Principals d'IA
* **Sistemes de Machine Learning (ML)**: Algorismes supervisats, no supervisats i d'aprenentatge per reforç.
* **Xarxes Neuronals Artificials (ANN)**: Modelat inspirat en el funcionament del cervell.
* **Sistemes basats en regles i Raonament basat en casos**: Inferència de coneixement a partir de regles predefinides o experiències prèvies.
* **Algorismes Genètics**: Optimització basada en principis de selecció natural i evolució.
* **Automàts Cel·lulars**: Models sistemàtics de regles sobre graelles discretes.
* **Sistemes Difusos (*Fuzzy Logic*)**: Gestió del raonament amb graus d'incertesa.
* **Sistemes Multiagent**: Coordinació de múltiples entitats intel·ligents.

---

## 3. Història i Evolució de la IA

### Inicis (Anys 40 - Mitjans dels 60)
* **Anys 40**: McCulloch i Pitts creen el primer model teòric de neurona artificial.
* **1950**: Alan Turing publica "Poden pensar les màquines?" i proposa la **Prova de Turing** ("joc d'imitació") per determinar la intel·ligència d'una màquina.
* **1955/1956**: John McCarthy encunya oficialment el terme *"Intel·ligència Artificial"*.
* **Desenvolupaments clau**:
  * Neix el concepte de *Machine Learning*.
  * Creació del llenguatge LISP per a informació simbòlica.
  * Primers models supervisats, no supervisats i primeres idees de Processament de Llenguatge Natural (PLN).
  * Primeres IA conversacionals (**ELIZA** al MIT per Joseph Weizenbaum) i sistemes experts (**DENDRAL**).
  * Creació del robot industrial **UNIMATE** (1961) a General Motors i el robot d'ús general **SHAKEY** (1966) a Stanford.

---

### Hiverns de la IA (Anys 70 - Anys 80)
* **Anys 70**: Etapes de retallades en inversió i interès per no assolir les expectatives i l'optimisme inicials. Els sistemes s'avaluaven com a costosos i amb fallades.
* **Desenvolupaments clau**:
  * Continua el desenvolupament de sistemes experts com **MYCIN**.
  * Aconseguiments en sistemes d'experts i projectes de cinquena generació de computadors al Japó.
  * Innovacions en robòtica humanoide i visió per computador.
  * Introducció de models per processar la informació incerta, com les **Xarxes Bayesianes**.
  * Innovacions tecnològiques en xarxes neuronals.

---

### Explosió de l'Aprenentatge Profund (Anys 90 - 2010s)
* **Desenvolupament de Deep Learning**: S'utilitza per entrenar xarxes neuronals complexes, desencadenant un gran creixement en les dècades posteriors.
* **Anys 90**:
  * **1997**: La computadora **Deep Blue** d'IBM guanya el campió mundial d'escacs Garri Kaspàrov.
  * Creació de chatbots avançats (**ALICE**) i desenvolupaments en robòtica social com **KISMET** (MIT) o la mascota robòtica **AIBO** de Sony (1999).
* **Anys 2000 - 2010**:
  * Robòtica domèstica de massa (**Roomba** el 2002).
  * Substitució de CPUs per **GPUs** per accelerar el processament de la IA.
  * Debats teòrics sobre la IA ètica i l'aparició d'IAs "sobrehumanes".
  * **2011**: **IBM Watson** guanya el concurs *Jeopardy!* i Apple integra **Siri** com a assistent virtual.
  * **2014**: Lanzament d'**Amazon Alexa** i aparició del chatbot **Eugene Goostman**, que supera la prova de Turing segons un terç dels jutges.

---

### Era Actual (2010s - Actualitat)
* **2016**: El bot de Microsoft, **Tay**, falla a xarxes socials per comentaris no desitjats, remarcant la importància de l'ètica i el control.
* **2017**: **AlphaGo** de Google (DeepMind) guanya a Ke Jie en el joc de Go (joc amb més de $2^{70}$ posicions possibles).
* **Models Llenguatge Massius (LLMs) i Generatius**:
  * OpenAI presenta **GPT-3**, demostrant una capacitat sense precedents per comprendre i generar llenguatge natural.
  * Proliferació de models multimodals capaços de processar i generar text, imatge, àudio i codi.
