# Tema 2.2: Problemes de Cerca en Intel·ligència Artificial


## 1. Idea General i Conceptes Fonamentals

En l'àmbit de la Intel·ligència Artificial (IA), un **problema de cerca** consisteix a trobar quina seqüència d'accions ha de seguir un **agent** per passar d'un **estat inicial** a un **estat objectiu (meta)** dins d'un entorn definit.

### Conceptes Clau:
* **Món:** Representa tota la informació disponible de l'entorn i de l'agent.
* **Estat:** Configuració concreta de l'agent i del problema a l'entorn en un moment donat (ex. posició de l'agent, ubicació dels objectes o altres agents).
  * *Nota:* Un estat de cerca **no conté tota la informació del món**, només la rellevant per resoldre el problema.
* **Estat Inicial:** La configuració de partida des de la qual comença la cerca.
* **Espai d'Estats:** Conjunt de tots els estats possibles als quals es pot arribar en el problema.
* **Accions:** Conjunt de moviments o operacions possibles que l'agent pot executar des d'un estat determinat per modificar-lo.
* **Transició (Funció de transició):** Funció $T(s, a) \to s'$ que, donat un estat actual $s$ i una acció $a$, retorna el nou estat resultants $s'$.
* **Cost d'Acció:** Valor numèric associat a executar una acció concreta des d'un estat cap a un altre, normalment denotat com $c(s, a, s')$.
* **Meta (Funció de test d'objectiu):** Funció booleana que determina si un estat actual compleix les condicions per ser considerat un estat objectiu.

### Exemples de Problemes de Cerca (no tots són camins físics):
1. **Problema del Viatjant de Comerç (TSP - Traveling Salesperson Problem).**
2. **Cerca de rutes en xarxes informàtiques o rutes aèries.**
3. **Disseny i traçat de circuits en microxips.**
4. **Assemblatge automatitzat de components industrials.**
5. **Navegació i desplaçament de robots autònoms.**
6. **Problemes d'assignació eficient de recursos.**
7. **Puzles lògics (ex. el Puzle de 8 peces o 8-puzzle).**

---

## 2. Formulació i Definició d'un Problema de Cerca

Per definir correctament un problema de cerca cal seguir una metodologia clara en 6 passos:

1. **Recollir la informació i concretar l'objectiu:** Entendre com són l'agent i l'entorn, i quin és el propòsit final (anar d'un punt $A$ a un $B$, o bé visitar una sèrie de punts entremitjos).
2. **Definir la informació requerida als estats:** Decidir quines variables cal emmagatzemar. Si l'objectiu només és anar d'A a B, n'hi ha prou amb la posició actual. Si cal visitar diversos nodes, l'estat ha d'incloure el conjunt de punts ja visitats.
3. **Especificar l'estat inicial:** Definir com comença el sistema (ha de ser una configuració vàlida i resoluble).
4. **Especificar la funció de meta:** Determinar si hi ha un estat final explícit o una condició booleana que verifica si s'ha assolit l'objectiu.
5. **Definir l'Espai d'Estats i les Transicions:**
   * Es pot visualitzar conceptualment com un **Graf de l'Espai d'Estats**, on els **nodes** són els estats i les **arestes** (orientades o ponderades) representen les accions.
   * **Atenció:** En la pràctica, *no es construeix el graf sencer a la memòria*, ja que pot ser immens o infinit. Es generen els nodes **a petició (on demand)** mitjançant les funcions d'accions i transició.
6. **Especificar el tipus de solució buscada:**
   * Seqüència d'accions (camí) vs. només l'estat final.
   * Una solució qualsevol vs. la solució de cost mínim (solució òptima).

---

## 3. Graf d'Espai d'Estats vs. Arbre de Cerca

* **Graf de l'Espai d'Estats:** Representació lògica del problema. Cada estat únic hi apareix només una vegada.
* **Arbre de Cerca:** Representació de les diferents *seqüències d'accions* o camins possibles explorats des de l'estat inicial.
  * La **arrel** és l'estat inicial.
  * Cada **node de l'arbre de cerca** correspon a un **camí complet** en el graf d'espai d'estats.
  * Poden aparèixer estats duplicats en branques diferents de l'arbre.

---

## 4. Algorisme General de Cerca i Pseudocodi

Els algorismes de cerca mantenen una estructura de dades anomenada **Frontera** (o conjunt de nodes pendents d'explorar).

* **Frontera:** Emmagatzema tots els camins parcials descoberts fins al moment.
* **Nodes Visitats / Explorats:** Nodes que ja s'han extret de la frontera i s'han expandit.

### Tipus d'Estratègia de Cerca:
* **Tree Search:** Algorisme de cerca pur sobre l'arbre. No recorda els estats ja visitats; pot entrar en bucles infinits si el graf té cicles.
* **Graph Search:** Cerca que manté un conjunt addicional d'estats **ja visitats** per no tornar a afegir a la frontera estats repetits.

### Pseudocodi General (Tree Search)

```python
function TREE-SEARCH(problem, frontier) return a solution or failure
    frontier.INSERT(MAKE-NODE(INITIAL-STATE[problem]))
    
    while not IS-EMPTY(frontier) do
        node = POP(frontier) // Selecció del node segons l'estratègia
        
        if problem.IS-GOAL(node.STATE) then 
            return node // Solució trobada
            
        for each child-node in EXPAND(problem, node) do
            add child-node to frontier
            
    return failure

function EXPAND(problem, node) yields nodes
    s = node.STATE
    for each action in problem.ACTIONS(s) do
        s' = problem.RESULT(s, action)
        yield NODE(STATE=s', PARENT=node, ACTION=action, COST=node.COST + COST(s, action, s'))
```

---

## 5. Propietats per a l'Avaluació d'Algorismes de Cerca

Per comparar el rendiment dels diferents algorismes s'utilitzen 4 mètriques:

1. **Completitud:** Garanteix l'algorisme trobar una solució si aquesta existeix?
2. **Optimalitat:** Aconsegueix l'algorisme la solució amb el cost mínim ($C^*$)?
3. **Complexitat Temporal:** Quant temps (o quants nodes expandits) necessita per trobar la solució?
4. **Complexitat Espacial:** Quanta memòria es requereix per mantenir la frontera i els nodes explorats?

### Paràmetres formalitzats:
* $b$: Factor de ramificació (*branching factor*), nombre mitjà de successors per node.
* $d$ o $s$: Profunditat de la solució més propera / òptima.
* $m$: Profunditat màxima de l'espai d'estats (pot ser $\infty$).
* $C^*$: Cost de la solució òptima.
* $\epsilon$: Cost mínim d'una acció ($\epsilon > 0$).

---

## 6. Cerca Cega o No Informada (Uninformed Search)

Els algorismes de cerca cega només utilitzen la informació definida en el problema (estat inicial, accions, transicions i test de meta). No disposen d'orientació sobre quina direcció és millor.

### 6.1. Depth-First Search (DFS) / Primer en Profunditat
* **Estratègia:** Selecciona sempre el node més profund de la frontera.
* **Estructura de la Frontera:** Pila (LIFO - *Last In, First Out*).
* **Completitud:** **NO** (en espais d'estats d'infinita profunditat o amb cicles en *Tree Search*). **SÍ** si és un graf finit i es controlen els estats visitats.
* **Optimalitat:** **NO**. Pot trobar una solució molt costosa en una branca abans de trobar una solució millor a menor profunditat.
* **Complexitat Temporal:** $\mathcal{O}(b^m)$ — En el pitjor dels casos explora tot l'arbre.
* **Complexitat Espacial:** $\mathcal{O}(b \cdot m)$ — Modesta i lineal respecte a la profunditat. Aquest és el seu gran avantatge.

### 6.2. Breadth-First Search (BFS) / Primer en Amplada
* **Estratègia:** Selecciona el node menys profund de la frontera (explora per nivells).
* **Estructura de la Frontera:** Cua (FIFO - *First In, First Out*).
* **Completitud:** **SÍ** (si el factor de ramificació $b$ és finit).
* **Optimalitat:** **NO** en el cas general. **SÍ** només si totes les accions tenen el mateix cost constant.
* **Complexitat Temporal:** $\mathcal{O}(b^s)$ on $s$ és la profunditat de la solució.
* **Complexitat Espacial:** $\mathcal{O}(b^{s+1})$ — Alt consum de memòria, ja que cal guardar tots els nodes del següent nivell a la frontera.

### 6.3. Uniform Cost Search (UCS) / Cerca de Cost Uniforme
* **Estratègia:** Selecciona el node amb el **menor cost acumulat des de l'inici**, $g(n)$, on $g(n) = \sum \text{costos de les accions}$.
* **Estructura de la Frontera:** Cua de Prioritat (ordenada ascendentment per $g(n)$).
* **Completitud:** **SÍ** (si cada pas té un cost mínim $\epsilon > 0$).
* **Optimalitat:** **SÍ**. Troba sempre la solució de cost mínim.
* **Complexitat Temporal:** $\mathcal{O}\left(b^{1 + \lfloor C^* / \epsilon \rfloor}\right)$
* **Complexitat Espacial:** $\mathcal{O}\left(b^{1 + \lfloor C^* / \epsilon \rfloor}\right)$

---

## 7. Cerca Informada o Heurística (Informed Search)

La cerca informada utilitza coneixement específic del domini del problema per guiar l'exploració cap a l'objectiu mitjançant una **funció heurística $h(n)$**.

* **Heurística $h(n)$:** Estimació del cost restant des del node $n$ fins a l'estat meta més proper.
* **Propietat clau:** $h(n) \ge 0$, i $h(\text{meta}) = 0$.
* **Com s'obtenen?** Sovint relaxant les restriccions del problema original (ex. en un mapa, la distància en línia recta o la distància de Manhattan ignorant parets).

### 7.1. Greedy Best-First Search (Cerca Voraç)
* **Estratègia:** Avalua els nodes únicament segons la seva heurística: $f(n) = h(n)$. Selecciona el node que sembla estar més a prop de la meta.
* **Estructura de la Frontera:** Cua de Prioritat (ordenada per $h(n)$).
* **Completitud:** **NO** (es pot quedar atrapat en bucles en *Tree Search*).
* **Optimalitat:** **NO**.
* **Complexitat Temporal:** $\mathcal{O}(b^m)$ en el pitjor dels casos (amb una mala heurística). Si l'heurística és molt bona, el temps pot ser molt reduït.
* **Complexitat Espacial:** $\mathcal{O}(b^m)$.

### 7.2. Algorisme $A^*$ ($A^*$ Search)
* **Estratègia:** Combina el cost real acumulat $g(n)$ i el cost estimat restant $h(n)$:
  $$f(n) = g(n) + h(n)$$
  on $f(n)$ representa l'estimació del cost total del millor camí passant per $n$.
* **Estructura de la Frontera:** Cua de Prioritat (ordenada per $f(n)$).
* **Completitud:** **SÍ**.
* **Optimalitat:** **SÍ** (si l'heurística compleix la condició d'**Admissibilitat**).
* **Complexitat Temporal:** $\mathcal{O}(b^s)$ en el pitjor dels casos.
* **Complexitat Espacial:** $\mathcal{O}(b^s)$ — Mantenir la frontera requereix molta memòria.

#### Condició d'Admissibilitat d'una Heurística:
Una heurística $h(n)$ és **admissible** si **mai sobreestima** el cost real per arribar a la meta.
$$0 \le h(n) \le h^*(n)$$
on $h^*(n)$ és el cost real mínim des de $n$ fins a l'objectiu.

#### Requisit addicional per a Graph Search ($A^*$ en grafs):
Per garantir l'optimalitat d' $A^*$ fent servir *Graph Search* (evitant duplicats), l'heurística ha de ser **consistent (o monòtona)**:
$$h(n) \le c(n, a, n') + h(n')$$

### 7.3. Iterative Deepening $A^*$ ($IDA^*$)
* **Motivació:** Resoldre el gran consum de memòria d' $A^*$.
* **Mecanisme:** Executa una cerca en profunditat (DFS) modificada. S'estableix un límit o fita sobre el valor de $f(n)$. Qualsevol node amb $f(n) > \text{fita}$ és descartat en la iteració actual. Si no es troba la meta, es fa una nova iteració augmentant la fita al valor $f(n)$ mínim dels nodes descartats.
* **Avantatges:**
  * Complexitat espacial **lineal** $\mathcal{O}(b \cdot d)$ gràcies a l'ús de DFS.
  * Manté l'optimalitat i completitud d' $A^*$.
* **Inconvenient:** Re-visita i re-expandeix nodes repetidament en cada iteració.

---

## 8. Taula Comparativa dels Algorismes de Cerca

| Algorisme | Criteri de Selecció / $f(n)$ | Complet? | Òptim? | Complexitat Temporal | Complexitat Espacial |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **DFS** | Més profund (Pila) | No | No | $\mathcal{O}(b^m)$ | $\mathcal{O}(b \cdot m)$ |
| **BFS** | Menys profund (Cua) | Sí | Només si costos iguals | $\mathcal{O}(b^s)$ | $\mathcal{O}(b^{s+1})$ |
| **UCS** | Cost acumulat $g(n)$ | Sí | Sí | $\mathcal{O}(b^{C^*/\epsilon})$ | $\mathcal{O}(b^{C^*/\epsilon})$ |
| **Greedy** | Heurística $h(n)$ | No | No | $\mathcal{O}(b^m)$ | $\mathcal{O}(b^m)$ |
| **$A^*$** | $f(n) = g(n) + h(n)$ | Sí | Sí (si $h$ és admissible) | $\mathcal{O}(b^s)$ | $\mathcal{O}(b^s)$ |
| **$IDA^*$** | $f(n)$ amb fita iterativa | Sí | Sí (si $h$ és admissible) | Variable | $\mathcal{O}(b \cdot s)$ |

---

## 9. Altres Tipus de Problemes de Cerca en IA

A més de la cerca tradicional en espais d'estats, existeixen altres categories:

1. **Cerca Local (Local Search):** Se centra exclusivament a trobar un **estat final vàlid o òptim**, sense importar el camí seguit per arribar-hi (ex. *Hill Climbing*, *Simulated Annealing*, Algorismes Genètics).
2. **Problemes de Satisfacció de Restriccions (CSP - Constraint Satisfaction Problems):** L'objectiu és trobar una assignació de valors a variables que compleixi un conjunt de restriccions (ex. Sudoku, acoloriment de mapes).
3. **Cerca Adversària / Jocs (Adversarial Search):** Entorns on hi ha un o més agents oponents intentant maximitzar el seu propi benefici (ex. Escacs, Tres en ratlla; algorismes Minimax i poda Alfa-Beta).

---

## 10. Implementació i Llibreries en Python

Per a la implementació de cerca de camins i algorismes de cerca en entorns Python, destaca la llibreria:

* **`pathfinding`**: Proporciona eines i estructures d'algorismes ja optimitzades per a BFS, Dijkstra (UCS), $A^*$, entre d'altres, sobre graelles i grafs.

```bash
pip install pathfinding
```