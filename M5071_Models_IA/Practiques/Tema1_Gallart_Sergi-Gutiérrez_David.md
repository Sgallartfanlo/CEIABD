# Pràctica Tema 1: Sistemes d'Intel·ligència Artificial (M5071)

Aquest dipòsit conté l'anàlisi de dos supòsits pràctics d'implantació de sistemes d'Intel·ligència Artificial (IA) en l'àmbit educatiu, avaluant la seva caracterització tècnica, l'impacte en els processos de negoci, el marc legal segons l'**EU AI Act** i les mesures per garantir una **IA Fiable**.

---

## 👨‍💻 Informació del Projecte

* **Assignatura:** M5071 - Models d'Intel·ligència Artificial
* **Activitat:** Pràctica Tema 1 – Sistemes d'Intel·ligència Artificial
* **Autors:** Sergi Gallart Fanlo & David Gutiérrez Navío
* **Professor:** Miquel Floriach
* **Curs acadèmic:** 2026/2027

---

## 📑 Índex de Continguts

1. [Context 1: Assistent per a coordinadors TIC](#context-1-assistent-per-a-coordinadors-tic)
   * [Caracterització del Sistema i Indústria 4.0](#11-caracterització-del-sistema-i-indústria-40)
   * [Nivell de Risc, Marc Legal i Mitigació](#12-nivell-de-risc-marc-legal-i-mitigació)
2. [Context 2: Seleccionador d'alumnes per a beques Erasmus+](#context-2-seleccionador-dalumnes-per-a-beques-erasmus)
   * [Caracterització i Automatització](#21-caracterització-i-automatització)
   * [Nivell de Risc (EU AI Act), Marc Legal i Reformulació](#22-nivell-de-risc-eu-ai-act-marc-legal-i-reformulació)
3. [Avaluació Global de IA Fiable](#-avaluació-global-de-ia-fiable)

---

## 🖥️ Context 1: Assistent per a coordinadors TIC

**Descripció:** Sistema d'IA conversacional (basat en models LLM / Transformers) per permetre als coordinadors TIC consultar l'inventari de magatzems i aules en llenguatge natural.

### 1.1 Caracterització del Sistema i Indústria 4.0
* **Tasques:** Comprensió de consultes en llenguatge natural sobre equipament, aules i préstecs (cerca per nom, ID, NSI, DNI, etc.).
* **Tècniques d'IA:** Processament del Llenguatge Natural (NLP), extracció d'informació, raonament i LLMs.
* **Tecnologies complementàries:**
  * **IoT:** Seguiment i localització de dispositius físics en temps real.
  * **Bessons Digitals (Digital Twins):** Representació virtual de l'inventari i l'estat de les aules.
  * **Edge Computing / Cloud & 5G:** Processament local per reduir la latència i connectivitat massiva.

### 1.2 Nivell de Risc, Marc Legal i Mitigació
* **Classificació de Risc (EU AI Act):** **Risc Mínim** (o risc de transparència).
* **Obligacions Legals:** Informar els usuaris que interactuen amb una IA i complir el RGPD.
* **Estratègia de Rebaix de Risc:** Anonimització o ús d'identificadors opacs interns en comptes de dades personals directes.

---

## 🎓 Context 2: Seleccionador d'alumnes per a beques Erasmus+

**Descripció:** Sistema d'IA autònom dissenyat per recollir dades acadèmiques, d'assistència, valoracions docents i proves per baremar, decidir i publicar directament la resolució de les beques Erasmus+.

### 2.1 Caracterització i Automatització
* **Tasques:** Creuament de dades, avaluació ponderada, presa de decisió final i publicació autònoma en lloc web.
* **Tècniques d'IA:** Sistemes basats en regles, algoritmes de Machine Learning (Scoring/Classificació) i NLP per a les valoracions dels docents.
* **Tipus d'automatització:** Automatització completa sense cap filtre ni revisió humana prèvia (*High Risk Scenario*).

### 2.2 Nivell de Risc (EU AI Act), Marc Legal i Reformulació
* **Classificació de Risc:** **RISC ALT** (Segons l'Annex III de la Llei d'IA de la UE, per determinar l'accés a l'educació/beques).
* **Obligacions d'Alt Risc:** Sistema de gestió de riscos, governança de dades d'alta qualitat, registre d'activitat, supervisió humana i registre a la base de dades de la UE.
* **Reformulació del Sistema (Per a la conformitat legal i ètica):**
  1. **Eliminar la presa de decisions autònoma** i la publicació directa.
  2. Implementar un rol d'**assistent d'ordenació** on una **Comissió Humana** revisi i aprovi la resolució final.
  3. Garantir el dret a reclamació i a l'explicació de les puntuacions.

---

## 🛡️ Avaluació Global de IA Fiable

A continuació es detallen les mesures de mitigació aplicades a cadascun dels 7 requisits per a una IA fiable segons la Unió Europea:

| Requisit de IA Fiable | Context 1 (Assistent TIC) | Context 2 (Beques Erasmus+) |
| :--- | :--- | :--- |
| **1. Acció i supervisió humana** | El coordinador supervisa i valida les fonts de dades. | La IA passa a generar un esborrany que requereix signatura digital d'una comissió. |
| **2. Solidesa tècnica i seguretat** | Pla de replegament a consultes directes SQL en cas d'error. | Validació automatitzada de la integritat de les dades d'origen. |
| **3. Privacitat i gestió de dades** | Anonimització i control d'accés segons perfil. | Minimització de dades i publicació de resultats mitjançant codis anònims. |
| **4. Transparència** | Avís d'interacció amb IA i enllaços directes de verificació. | Desglossament detallat del barem i explicabilitat de les puntuacions. |
| **5. Diversitat i no discriminació** | Disseny universal i auditories d'accessibilitat. | Estandardització de rúbriques docents i proves d'equitat algorítmica. |
| **6. Benestar social i mediambiental** | Ús de models lleugers (Edge Computing / Servidors locals). | Publicació transparent de criteris per evitar desconfiança social. |
| **7. Rendiment de comptes** | Registre d'auditoria (logs) de consultes i respostes. | Responsabilitat legal última a càrrec de la Direcció del centre. |

> **Conclusió final:** El projecte de beques Erasmus+ en la seva versió original **no és fiable ni legal**. Un cop redefinit com a sistema d'ajuda a la decisió amb supervisió humana obligatòria, compleix plenament els requisits ètics i legals de la Unió Europea.