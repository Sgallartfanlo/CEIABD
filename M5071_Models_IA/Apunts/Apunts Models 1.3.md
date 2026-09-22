# Tema 1.3: Intel·ligència Artificial Generativa (GenAI)

**Mòdul:** M5071 - Models d'Intel·ligència Artificial  
---

## 1. Per què parlem ara d'IA Generativa (GenAI)?

En els darrers anys, la **Intel·ligència Artificial Generativa (GenAI)** ha après una velocitat d'adopció i desenvolupament sense precedents en la història de la tecnologia. 

Segons les dades i conclusions de l'**AI Index Report (2026)**:

* **Velocitat d'adopció massiva:** En només **3 anys** des del llançament de ChatGPT (considerat el primer producte de GenAI de mercat massiu), la GenAI ha aconseguit un **53% d'adopció en la població**. Aquesta velocitat supera de llarg la Taxa d'adopció d'altres tecnologies de la informació històriques com l'ordinador personal o la pròpia navegació per Internet.
* **Integració empresarial:** L'any **2025**, almenys un **70% de les organitzacions** ja utilitzaven la GenAI en alguna de les seves funcions o processos de negoci.
* **Creixement de la inversió privada:** La inversió privada en GenAI va experimentar un augment superior al **200%** respecte a l'any anterior, arribant a captar gairebé la meitat de tota la inversió privada en el sector tecnològic.
* **Impacte econòmic i excedent del consumidor:** A principis de 2026, l'excedent del consumidor associat a la GenAI als Estats Units es va estimar en uns **172.000 milions de dòlars anuals**. 
  > *Nota:* L'excedent del consumidor és una estimació econòmica del valor real que els usuaris atribueixen a l'ús d'aquestes eines més enllà del preu que paguen per elles (no representa ingressos directes ni per als usuaris ni per a les empreses).

---

## 2. Què és la IA Generativa?

La **IA Generativa (GenAI)** fa referència a la branca de la intel·ligència artificial enfocada a la **creació de contingut nou i original** (text, imatges, àudio, vídeo, codi, etc.).

### Com funciona conceptualment?
1. **Modelat probabilístic:** Els models generatius analitzen i aprenen els patrons, estructures i relacions subjacents en grans volums de dades d'entrenament.
2. **Representació i generació:** Representen aquests aprenentatges mitjançant un model probabilístic. Això els permet sintetitzar contingut completament nou però amb característiques estadísticament equivalents a les dades originals.

### Diferència principal amb la IA tradicional (Predictiva / Discriminativa)
* **IA Tradicional o Discriminativa:** El seu objectiu és analitzar una entrada per tal de classificar-la, fer una predicció o prendre una decisió (ex. identificar si un correu és spam o predir el preu d'un habitatge).
* **IA Generativa:** El seu objectiu principal és **produir una nova sortida (output)** estructuralment coherent.

### Factors clau del seu desenvolupament
L'eclosió actual de la GenAI ha estat possible gràcies a la convergència de tres elements:
1. El desenvolupament i evolució de les **xarxes neuronals profundes** (Deep Learning).
2. La disponibilitat de **grans volums de dades** (Big Data).
3. L'increment exponencial de la **capacitat de càlcul** (GPUs/TPUs).

---

## 3. Què es pot generar? Modalitats i tipologies

Els models generatius moderns poden treballar amb una gran varietat de formats o **modalitats**:

* **Text:** Documents, resums, traduccions, converses, adaptació d'estils.
* **Imatges:** Il·lustracions, fotorealisme, dissenys gràfics, diagrames.
* **Àudio:** Clonació de veu, síntesi de parla (TTS), composició musical, efectes de so.
* **Vídeo:** Generació de vídeos des de zero, animació de fotogrames.
* **Codi:** Escriptura de programes, scripts, depuració (debugging), traducció entre llenguatges de programació.
* **Dades sintètiques:** Creació de dades artificials per a entrenar altres models de ML sense comprometre la privacitat.
* **Contingut 3D:** Creació de models tridimensionals, escenes virtuals, avatars.

### Tipus de fluxos de generació

La generació es pot classificar segons la relació entre la dades d'entrada (*input*) i les de eixida (*output*):

1. **Unimodal (*Single-modality*):** L'entrada i la sortida pertanyen a la mateixa modalitat (ex. text-a-text com un resum, o imatge-a-imatge).
2. **Multimodal / Cross-modality:** La generació es produeix interactuant entre diferents tipus de dades.
   * **Text-to-Image:** Generar una imatge a partir d'un prompt de text.
   * **Text-driven Image Editing:** Editar una imatge existent mitjançant instruccions textuals.
   * **Personalized Image Synthesis:** Generar imatges noves d'un objecte/subjecte concret combinant un text i imatges de referència.
   * **Video-to-Video Synthesis / Future Video Prediction:** Predir els següents fotogrames d'una seqüència de vídeo.
   * **Class-conditional Generation:** Generar un contingut basat en una classe específica (ex. "Genera un gos Malamute").

---

## 4. Principals paradigmes de models generatius

Existeixen quatre grans arquitectures o paradigmes tecnològics sobre els quals es construeixen els models generatius actuals:

```
┌─────────────────────────────────────────────────────────────────┐
│              MODEL PARADIGMS IN GENERATIVE AI                   │
├────────────────────────────────┬────────────────────────────────┤
│          Transformers          │ Generative Adversarial Net.    │
│            (BERT, GPT)         │      (Generator / Discrim.)    │
├────────────────────────────────┼────────────────────────────────┤
│    Variational Autoencoders    │        Diffusion Models        │
│        (Encoder / Decoder)     │      (DDPM, SGM, SDE)          │
└────────────────────────────────┴────────────────────────────────┘
```

1. **Transformers:**
   * **Funcionament:** Es basen en el mecanisme d'atenció (*self-attention*) per processar i entendre les relacions entre tots els elements d'una seqüència (text, codi, etc.) de manera paral·lela.
   * **Exemples/Subtipus:** BERT (encoder-only), GPT (decoder-only).

2. **Xarxes Adversàries Generatives (GANs - *Generative Adversarial Networks*):**
   * **Funcionament:** Es componen de dues xarxes neuronals que competeixen entre sí:
     * **Generador:** Intenta crear contingut sintètic el més realista possible.
     * **Discriminador:** Intenta diferenciar si el contingut és real (de les dades d'entrenament) o fals (creat pel generador).
   * **Efecte:** Aquest entrenament competitiu millora contínuament la qualitat del resultat.

3. **Autoencoders Variacionals (VAEs - *Variational Autoencoders*):**
   * **Funcionament:** Es componen d'un **Encoder** (que redueix les dades d'entrada a un espai latent de menor dimensió) i un **Decoder** (que reconstrueix les dades a partir d'aquest espai latent). Permeten generar contingut nou variant les coordenades en l'espai latent.

4. **Models de Difusió (*Diffusion Models*):**
   * **Funcionament:** Aprenen a generar contingut destruint primer les dades afegint-hi soroll gaussià de manera progressiva i, posteriorment, aprenent el procés invers: **revertir el soroll aleatori** fins a reconstruir una imatge o contingut nítid i nou.
   * **Exemples de variants:** DDPM (*Denoising Diffusion Probabilistic Models*), SGM (*Score-based Generative Models*), SDE (*Stochastic Differential Equations*).

---

## 5. Models de Llenguatge i LLMs (Large Language Models)

* **Model de Llenguatge (LM):** És un model estadístic que calcula la distribució de probabilitats d'una seqüència de paraules. Prediu quina és la paraula més probable que ha de seguir a un text determinat basant-se en el context anterior.
* **Large Language Model (LLM):** És un model de llenguatge a gran escala, basat habitualment en l'arquitectura Transformer, que ha estat entrenat amb volums massius de text (milers de milions de paraules) i que compta amb milers de milions de paràmetres. Això li atorga la capacitat de comprendre i generar text fluid i treballar amb contextos molt amplis.

### Evolució dels LLMs més rellevants
* **2019 - 2022:** Introducció de T5, GPT-3, LaMDA, PaLM, InstructGPT.
* **2022 - 2023:** Llançament de **ChatGPT**, **GPT-4**, LLaMA / LLaMA 2, Mistral, Mixtral, Claude.
* **2024 - 2026:** Aparició de models molt més eficients, multimodals i amb capacitat de raonament avançat:
  * Famílies GPT (GPT-4o, GPT-o3, GPT-4.5, GPT-5.x)
  * Famílies Gemini (Gemini 2.0, 2.5, 3.0)
  * Models d'obertura / Open Source com LLaMA 3/4, Qwen (Qwen2, Qwen3), DeepSeek (DeepSeek-V2, V3, R1, V3.2), Mistral 3, Gemma.

---

## 6. Limitacions i reptes actuals de la GenAI

Tot i el seu gran potencial, els models generatius actuals presenten certes limitacions tècniques i operacionals que cal tenir en compte:

1. **Fiabilitat i Al·lucinacions:** Els models poden generar informació factualment incorrecta, falsa o inventada però presentada amb una aparença de total seguretat i plausibilitat.
2. **Gestió del Context:** Malgrat l'augment de les finestres de context, els models poden tenir dificultats per mantenir la coherència temporal o lògica en textos o diàlegs extremadament extensos.
3. **Raonament complex:** Solen presentar carències en tasques que requereixen un raonament lògic profund, matemàtiques d'alta precisió o coordinació de múltiples passos complexos.
4. **Falta de Control (Dificultat de determinisme):** No sempre és senzill predir, parametritzar o ajustar exactament el resultat generat per un prompt determinat.
5. **Dependència de les dades d'entrenament:** La qualitat, la neutralitat i l'abast dels resultats depenen directament de les dades amb les quals el model ha estat entrenat (risc de biaixos).
6. **Cost de recursos:** L'entrenament i la inferència dels models més grans requereixen un consum energètic i una capacitat de càlcul (infraestructura de hardware) molt elevats.

> *Nota addicional:* Cal afegir a aquestes limitacions tècniques els **riscos ètics, socials i legals** (drets d'autor, privacitat, desinformació, impacte en l'ocupació), que s'estudiaran a l'apartat 1.4.
