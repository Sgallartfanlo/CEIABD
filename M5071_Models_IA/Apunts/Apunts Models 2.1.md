# Tema 2.1: Estructures Abstractes de Dades (TAD)

## 1. Introducció a la Resolució de Problemes i la IA

### 1.1 Conceptes Fonamentals
- **Intel·ligència Artificial (IA):** Desenvolupament de sistemes capaços de realitzar tasques que comunament s'associen a éssers intel·ligents.
- **Intel·ligència:** Capacitat de resoldre problemes.
- **Resolució de problemes:** Procés en què, a partir d'unes **dades inicials** i mitjançant un conjunt de **procediments**, es determina la seqüència de passos o elements que condueixen a la **solució**.

### 1.2 El Repte de la Representació
Per tal que un programa informàtic o model de IA pugui resoldre un problema, cal donar resposta a la següent qüestió:  
*Com representem les dades, els passos i les solucions de manera formal perquè hi puguem aplicar algorismes de resolució?*

#### Tipus de Solucions Cercades
Depenent del context i la necessitat de l'aplicació, es pot cercar:
- **Una solució qualsevol:** Trobar un camí o estat vàlid sense importar l'eficiència.
- **Totes les solucions:** Explorar completament l'espai d'estats.
- **La solució més curta / menys costosa:** Optimització (ex. camí mínim, reducció del cost de computació).

#### Procés General d'Abstracció
1. **Descripció informal:** Formulació del problema en llenguatge natural.
2. **Abstracció i Formalització:** Traducció del problema a un **llenguatge formal i estructurat** utilitzant **Tipus Abstractes de Dades (TAD)**.
3. **Disseny d'Algorismes:** Definició d'estratègies (cerca, optimització, planificació) sobre les estructures formals definides.

---

## 2. Agents Racionals i Planificació

Un dels objectius principals de la IA és la creació d'**agents racionals** (o intel·ligents).

### Característiques d'un Agent Racional:
1. **Objectius o preferències:** Defineixen el criteris d'èxit o la funció d'utilitat.
2. **Accions:** Conjunt d'operacions executables per modificar l'entorn.
3. **Entorn:** Medi específic on l'agent existeix, percep i actua.

### Planificació i Simulació d'Intel·ligència
- Els agents poden ser de resposta directa (reactius) o considerants de conseqüències.
- Quan l'agent **té en compte les conseqüències futures** de les seves accions abans d'executar-les, diem que **planifica**. La planificació requereix simular mentalment diferents trajectòries usant estructures de dades per representar els possibles estats futurs.

---

## 3. Tipus Abstractes de Dades (TAD)

Un **Tipus Abstracte de Dades (TAD)** és un model matemàtic per a tipus de dades on el tipus és definit pel seu **comportament (semàntica)** des del punt de vista de l'usuari de la dada, observant valors i operacions possibles.

### Principis Clau:
- **TAD = Dades + Operacions definides.** Un TAD no existeix sense la definició clara de les seves operacions.
- **Abstracció i Encapsulació:** Són independents de la implementació física o del llenguatge de programació. L'usuari de l'estructura utilitza la seva interfície pública sense necessitat de conèixer com s'emmagatzema internament a la memòria.

---

## 4. Estructures de Dades Lineals

### 4.1 Pila (Stack)
Estructura de dades de tipus **LIFO** (*Last In, First Out*): el darrer element a entrar és el primer a sortir.

* **Operacions Principals:**
  * `push(element)` / `afegir`: Afegeix un nou element al cim (*top*).
  * `peek()` / `consultar`: Retorna l'element del cim sense extreure'l.
  * `pop()` / `treure`: Elimina i retorna l'element situat al cim.
* **Casos d'ús típics:**
  * Historial d'accions en entorns d'edició (desfer/rehfer - `Ctrl+Z`).
  * Gestió de la pila de crides de funcions (*Call Stack*) en la memòria d'execució de programes.
  * Algorismes de cerca en profunditat (DFS - *Depth-First Search*).

### 4.2 Cua (Queue)
Estructura de dades de tipus **FIFO** (*First In, First Out*): el primer element a entrar és el primer a sortir.

* **Operacions Principals:**
  * `enqueue(element)` / `afegir`: Afegeix un nou element al final de la cua (*back*).
  * `front()` / `consultar`: Retorna el primer element de la cua (*front*) sense extreure'l.
  * `dequeue()` / `treure`: Elimina i retorna el primer element de la cua.
* **Casos d'ús típics:**
  * Gestió de peticions a servidors web o sistemes distribuits.
  * Cues d'impressió o processament de tasques asíncrones.
  * Algorismes de cerca en amplada (BFS - *Breadth-First Search*).

### 4.3 Cua amb Prioritat (Priority Queue)
Variació de la cua on cada element té associada una **prioritat**. Els elements amb major prioritat són processats abans que aquells amb menor prioritat, independentment de l'ordre d'arribada.

* **Operacions Principals:**
  * `enqueue(element, prioritat)`: Insereix l'element posicionant-lo segons la seva prioritat.
  * `front()` / `peek()`: Retorna l'element amb major prioritat.
  * `dequeue()`: Elimina i retorna l'element amb major prioritat.
* **Implementació usual:** Es solen implementar de manera eficient mitjançant **Heaps** (*Min Heap* o *Max Heap*), estructures en forma d'arbre.
* **Casos d'ús:** Algorisme de cerca $A^*$ o de Dijkstra.

### 4.4 Llistes (List)
Conjunt ordenat d'elements on es pot accedir, afegir o eliminar en **qualsevol posició** (per índex o referència).

* **Operacions Principals:**
  * Insereix/Afegeix en la posició $i$.
  * Consulta de l'element en la posició $i$.
  * Elimina l'element de la posició $i$.

---

## 5. Exemple Comparatiu en Python: Pila vs Cua

Tot i que tant una Pila com una Cua es poden estructurar en Python utilitzant el tipus nativa `list`, la **diferència rau en quines operacions s'exposen i com s'executen**.

```python
# --- IMPLEMENTACIÓ D'UNA PILA (LIFO) ---
def crear_pila():
    return []

def afegir_element_pila(p, element):
    p.append(element)  # Push al final

def consultar_element_pila(p):
    if len(p) == 0:
        return None
    return p[-1]        # Cim de la pila

def treure_element_pila(p):
    if len(p) == 0:
        return None
    return p.pop()      # Treu el darrer element afegit


# --- IMPLEMENTACIÓ D'UNA CUA (FIFO) ---
def crear_cua():
    return []

def afegir_element_cua(c, element):
    c.append(element)  # Enqueue al final

def consultar_element_cua(c):
    if len(c) == 0:
        return None
    return c[0]         # Davant de la cua

def treure_element_cua(c):
    if len(c) == 0:
        return None
    return c.pop(0)     # Treu el primer element afegit
```

---

## 6. Estructures de Dades No Lineals

### 6.1 Grafs (Graph)
Estructura formada per un conjunt d'elements anomenats **nodes** (o vèrtexs) i un conjunt de connexions entre parells de nodes anomenades **arestes** (o enllaços). La matemàtica discreta és l'àrea encarregada de l'estudi formal dels grafs.

#### Operacions Comunes sobre Grafs:
- `adjacent(G, x, y)`: Comprova si existeix una aresta del node $x$ al node $y$.
- `neighbors(G, x)`: Llista tots els nodes $y$ adjacents al node $x$.
- `add_vertex(G, x)`: Afegeix el node $x$ al graf $G$.
- `remove_vertex(G, x)`: Elimina el node $x$ del graf $G$.
- `add_edge(G, x, y, z)`: Afegeix una aresta $z$ entre $x$ i $y$.
- `remove_edge(G, x, y)`: Elimina l'aresta entre $x$ i $y$.
- `get_vertex_value(G, x)` / `set_vertex_value(G, x, v)`: Consulta o assigna valor a un node.
- `get_edge_value(G, x, y)` / `set_edge_value(G, x, y, v)`: Consulta o assigna pes/valor a una aresta.

---

### 6.2 Arbres (Tree)
Un **arbre** és un cas particular de graf que compleix dues propietats fonamentals:
1. Tots els nodes estan connectats.
2. **No conté cap cicle** (és un graf acíclic connectat).

#### Anatomia d'un Arbre:
- **Arrel (Root):** Node principal (o pare/ascendent superior) sense cap pare.
- **Fills / Descendents:** Nodes connectats immediatament a un node pare de nivell superior.
- **Fulles (Leaves):** Nodes que no tenen cap descendent.
- **Altura:** Distància o nivell màxim des de l'arrel fins a la fulla més profunda.
- **Subarbre:** Si seleccionem un node intern qualsevol i tots els seus descendents, obtenim de nou una estructura d'arbre (propietat recursiva).

#### Operacions Típiques sobre Arbres:
- Enumerar tots els elements o una secció de l'arbre.
- Cercar un element.
- Afegir / Eliminar un element en una posició.
- **Pruning (Poda):** Eliminar una secció o subarbre enter.
- **Grafting (Empelt):** Afegir una secció o subarbre enter.
- Cercar l'arrel d'un node determinat.
- Trobar el **més baix ancestral comú** (*Lowest Common Ancestor*) entre dos nodes.

---

## 7. Criteris d'Implementació i Llibreries

### 7.1 Complexitat i Eficiència
Un mateix TAD es pot implementar de diferents maneres internament. La selecció de la implementació depèn de quines operacions cal optimitzar:
- **Inserció eficient** vs. **Consulta/Cerca eficient** vs. **Esborrat eficient**.
- **Seguretat en entorns multithread:** Garantir la coherència de les dades quan hi ha accés simultani per diversos fils d'execució.

### 7.2 Llibreries en Python
Per treballar amb grafs i algorismes complexos en entorns reals de IA, s'utilitzen llibreries especialitzades com **`networkx`**, la qual permet crear, manipular i estudiar l'estructura, dinàmica i funcions de xarxes/grafs complexos.

---

## 8. Aplicació dels TADs en la Intel·ligència Artificial

Els Tipus Abstractes de Dades jugen un paper doble i fonamental en el desenvolupament de solucions de IA:

1. **Representació:** Permeten modelar problemes complexos del món real en formats matemàtics i computacionals (grafs d'estats, arbres de decisió, etc.).
2. **Solució:** Permeten aplicar algorismes estàndard sobre aquestes representacions:
   - **Algorismes de Cerca:** Exploració d'espais d'estats (DFS, BFS, A*).
   - **Satisfacció de Restriccions (CSP):** Resolució de problemes amb variables i dominis.
   - **Jocs i Entorns Adversaris:** Arbres Minimax, cerca MCTS (*Monte Carlo Tree Search*).
   - **Extracció de Regles i Presa de Decisions:** Arbres de decisió en aprenentatge automàtic.
