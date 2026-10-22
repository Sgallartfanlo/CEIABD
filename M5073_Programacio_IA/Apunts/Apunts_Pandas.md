# Introducció i Guia Teòrica de Pandas

---

## 1. Contingut Teòric

### 1.1. Què és Pandas?

**Pandas** és una biblioteca fonamental de Python dissenyada per a l'anàlisi, manipulació i neteja de dades. El seu nom deriva del terme *"Panel Data"* (dades de panell) i constitueix una eina essencial en àmbits com la ciència de dades, el *machine learning* i el *big data*.

#### Característiques principals:
- **Estructures de dades eficients i flexibles:** dissenyades per treballar amb dades estructurades i de diferents tipus.
- **Rendiment optimitzat:** operacions d'alt rendiment adaptades per a grans volums de dades.
- **Integració de l'ecosistema Python:** s'integra de forma nativa amb biblioteques com NumPy, Matplotlib, Seaborn i Scikit-learn.
- **Transformació de dades:** àmplitat de funcions integrades per a la neteja, filtres, agregacions i transformacions de datasets.

```python
# Importació estàndard de biblioteques
import pandas as pd
import numpy as np
```

---

### 1.2. Estructures de Dades Fonamentals

Pandas es basa principalment en dues estructures de dades: la **Series** i el **DataFrame**.

#### **A. Series**
Una **Series** és un array unidimensional etiquetat capaç de contenir qualsevol tipus de dades (enters, cadenes de text, flotants, objectes de Python, etc.).

* **Components clau:**
  - **Valors (`values`)**: array NumPy subjacents que emmagatzema les dades.
  - **Índex (`index`)**: conjunt d'etiquetes associades als valors (poden ser numèriques o de text).
  - **Nom (`name`)**: identificador opcional de la Series.

```python
# Creació d'una Series
s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'], name='Exemple')

print(s)
print(f"Valors: {s.values}")
print(f"Índex: {s.index}")
```

#### **B. DataFrame**
Un **DataFrame** és una estructura de dades bidimensional (taula) amb columnes que poden contenir diferents tipus de dades. Es pot comparar amb una taula d'una base de dades SQL o un full de càlcul d'Excel.

* **Components clau:**
  - **Columnes:** cada columna és internament una *Series*.
  - **Índex de files:** etiquetes que identifiquen de manera única cada fila.
  - **Valors:** matriu bidimensional de dades.

```python
# Creació d'un DataFrame
df = pd.DataFrame({
    'nom': ['Anna', 'Bernat', 'Carla'],
    'edat': [25, 30, 28],
    'ciutat': ['Barcelona', 'Girona', 'Tarragona']
})

print(df)
```

---

### 1.3. Conceptes Claus

#### Indexació i Selecció
Per accedir a les dades d'un DataFrame s'utilitzen principalment tres enfocaments:
- **`loc[]`**: Accés basat en **etiquetes** (noms de files/columnes).
- **`iloc[]`**: Accés basat en **posició numèrica** (indexació $0, 1, 2, \dots$).
- **`[]`**: Accés directe per seleccionar columnes o aplicar filtres mitjançant màscares booleanes.

```python
estudiants = pd.DataFrame({
    'nom': ['Anna', 'Bernat', 'Carla', 'David'],
    'edat': [19, 20, 19, 21],
    'nota': [8.5, 7.0, 9.2, 6.8]
})

# Exemple d'ús de .loc[]
print(estudiants.loc[0])        # Retorna la primera fila (per etiqueta)
print(estudiants.loc[0, 'nom']) # Retorna 'Anna'

# Exemple d'ús de .iloc[]
print(estudiants.iloc[1])       # Retorna la segona fila (posició 1)

# Accés directe a columnes
print(estudiants["nom"])        # Retorna la Series corresponent a 'nom'
```

#### Operacions Comunes
- **Filtratge de dades:** Extracció de subconjunts mitjançant condicions booleanes (`df[df['nota'] >= 5]`).
- **Ordenació:** Reorganització de les files segons els valors d'una o diverses columnes.
- **Agrupació i agregació:** Càlcul d'estadístiques per grups específics de dades (`groupby`).
- **Combinació de dades:** Fusió de diferents font de dades mitjançant unions (`merge` o `concat`).

#### Gestió de Valors Nuls (`NaN`)
- **Detecció:** Identificació d'absència de dades amb `isna()` / `isnull()`.
- **Eliminació:** Neteja de files o columnes amb nuls mitjançant `dropna()`.
- **Imputació/Ompliment:** Substitució de valors nuls per un valor fix o un valor calculat (p. ex., la mitjana) amb `fillna()`.

---

## 2. Glossari de Funcions Elementals

### 2.1. Creació i Lectura de Dades

| Funció | Descripció | Exemple |
| :--- | :--- | :--- |
| `pd.Series()` | Crea una Series unidimensional. | `pd.Series([1, 2, 3])` |
| `pd.DataFrame()` | Crea un DataFrame bidimensional. | `pd.DataFrame({'col': [1, 2]})` |
| `pd.read_csv()` | Carrega dades des d'un fitxer CSV. | `pd.read_csv('dades.csv')` |
| `pd.read_excel()` | Carrega dades des d'un fitxer Excel. | `pd.read_excel('dades.xlsx')` |
| `pd.read_json()` | Carrega dades des d'un fitxer JSON. | `pd.read_json('dades.json')` |

```python
# Creació de Series personalitzada
temperatures = pd.Series(
    [15, 18, 20, 19, 17],
    index=['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres'],
    name='Temperatures'
)

# Creació de DataFrame
estudiants = pd.DataFrame({
    'nom': ['Anna', 'Bernat', 'Carla', 'David'],
    'edat': [19, 20, 19, 21],
    'nota': [8.5, 7.0, 9.2, 6.8]
})
```

---

### 2.2. Visualització i Exploració de Dades

| Funció / Atribut | Descripció |
| :--- | :--- |
| `.head(n)` | Retorna les primeres $n$ files (per defecte $n=5$). |
| `.tail(n)` | Retorna les últimes $n$ files (per defecte $n=5$). |
| `.info()` | Mostra un resum del DataFrame (tipus de dada, memòria, valors no nuls). |
| `.describe()` | Genera estadístiques descriptives de les columnes numèriques. |
| `.shape` | Atribut que indica les dimensions del DataFrame `(files, columnes)`. |
| `.columns` | Retorna les etiquetes de les columnes. |
| `.index` | Retorna l'índex del DataFrame. |
| `.dtypes` | Retorna els tipus de dades de cada columna. |

```python
# Exemples d'exploració
print(estudiants.head(2))
print(estudiants.info())
print(estudiants.describe())
print(f"Dimensions: {estudiants.shape}")
```

---

### 2.3. Selecció i Indexació

| Funció / Mètode | Descripció |
| :--- | :--- |
| `df['col']` | Selecciona una columna com a Series. |
| `df[['col1', 'col2']]` | Selecciona múltiples columnes com a DataFrame. |
| `.loc[]` | Selecció per etiqueta de fila/columna. |
| `.iloc[]` | Selecció per indexació entera de posició. |
| `.at[]` | Accés ràpid a un únic valor escalar per etiqueta. |
| `.iat[]` | Accés ràpid a un únic valor escalar per posició. |

```python
# Selecció de múltiples columnes
df_sub = estudiants[['nom', 'nota']]

# Accés puntual per posició o etiqueta
valor_loc = estudiants.loc[0, 'nom']   # 'Anna'
valor_iloc = estudiants.iloc[1, 2]    # Nota del segon estudiant (7.0)
```

---

### 2.4. Filtratge

| Funció / Mètode | Descripció |
| :--- | :--- |
| `df[condició]` | Filtra les files que compleixen una condició booleana. |
| `.query()` | Filtra files utilitzant una expressió en sintaxi d'estil SQL. |
| `.isin()` | Filtra si els valors estan continguts en una llista donada. |
| `.between()` | Comprova si els valors es troben en un rang determinat. |

```python
# Filtre amb condició booleana
excel_lents = estudiants[estudiants['nota'] >= 8.0]

# Filtre amb condicionals múltiples (& per AND, | per OR)
joves_excel_lents = estudiants[(estudiants['edat'] < 20) & (estudiants['nota'] >= 8.0)]

# Filtratge amb .query()
resultat = estudiants.query('edat == 19 and nota > 8')

# Filtratge amb .isin()
noms_seleccionats = estudiants[estudiants['nom'].isin(['Anna', 'Carla'])]
```

---

### 2.5. Ordenació

| Funció | Descripció |
| :--- | :--- |
| `.sort_values()` | Ordena el DataFrame segons els valors d'una o més columnes. |
| `.sort_index()` | Ordena el DataFrame segons l'índex de les files. |
| `.nlargest(n, 'col')` | Retorna els $n$ registres amb els valors més grans en una columna. |
| `.nsmallest(n, 'col')` | Retorna els $n$ registres amb els valors més petits en una columna. |

```python
# Ordenar per nota de forma descendent
estudiants_ordenats = estudiants.sort_values('nota', ascending=False)

# Obtenir els 2 millors estudiants
top_2 = estudiants.nlargest(2, 'nota')
```

---

### 2.6. Modificació de Dades i Estructura

| Funció | Descripció |
| :--- | :--- |
| `.rename()` | Redefineix els noms de columnes o files. |
| `.drop()` | Elimina files o columnes especifiques del DataFrame. |
| `.drop_duplicates()` | Elimina files amb valors duplicats. |
| `.replace()` | Substitueix valors específics per altres de nous. |
| `.astype()` | Modifica el tipus de dades d'una columna. |

```python
# Renombrar columnes
df_renombrat = estudiants.rename(columns={'nom': 'nombre', 'edat': 'edad'})

# Afegir una columna nova basada en un càlcul booleà
estudiants['aprovat'] = estudiants['nota'] >= 5.0

# Eliminar una columna
df_sense_edat = estudiants.drop('edat', axis=1)

# Substituir valors específics
estudiants['nom'] = estudiants['nom'].replace({'Anna': 'Ana'})
```

---

### 2.7. Valors Nuls

| Funció | Descripció |
| :--- | :--- |
| `.isna()` / `.isnull()` | Detecta valors nuls retornant una màscara booleana. |
| `.notna()` / `.notnull()` | Detecta valors no nuls. |
| `.dropna()` | Elimina files o columnes que contenen valors nuls. |
| `.fillna()` | Substitueix els valors nuls per un valor determinat. |

```python
dades = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8]
})

# Comptar valors nuls per columna
nuls_per_col = dades.isna().sum()

# Omplir nuls amb la mitjana de la columna
dades_imputades = dades.fillna(dades.mean())
```

---

### 2.8. Agregació i Estadístiques

| Funció | Descripció |
| :--- | :--- |
| `.sum()` | Càlcul de la suma de valors. |
| `.mean()` | Càlcul de la mitjana aritmètica. |
| `.median()` | Càlcul de la mediana. |
| `.min()` / `.max()` | Càlcul del valor mínim i màxim. |
| `.std()` | Càlcul de la desviació estàndard. |
| `.count()` | Recompte d'elements no nuls. |
| `.value_counts()` | Compta les freqüències de cada valor únic. |
| `.unique()` | Obté un array amb els valors únics d'una Series. |
| `.nunique()` | Recompte del nombre de valors únics en una Series. |

```python
mitjana_nota = estudiants['nota'].mean()
freq_edats = estudiants['edat'].value_counts()
num_edats_uniques = estudiants['edat'].nunique()
```

---

### 2.9. Agrupació i Taules Dinàmiques

| Funció | Descripció |
| :--- | :--- |
| `.groupby()` | Agrupa dades segons una o més categories. |
| `.agg()` | Aplica una o múltiples funcions d'agregació a dades agrupades. |
| `.pivot_table()` | Crea una taula dinàmica multidimensional. |

```python
vendes = pd.DataFrame({
    'producte': ['A', 'B', 'A', 'C'],
    'categoria': ['Electronics', 'Electronics', 'Electronics', 'Home'],
    'preu': [100, 150, 100, 50],
    'quantitat': [2, 1, 3, 5]
})

# Agrupar i calcular la mitjana
mitjana_categoria = vendes.groupby('categoria')['preu'].mean()

# Aplicar múltiples agregacions simultànies
resum_vendes = vendes.groupby('categoria')['quantitat'].agg(['sum', 'mean', 'max'])

# Taula dinàmica
pivot = pd.pivot_table(vendes, values='quantitat', index='producte', columns='categoria', aggfunc='sum', fill_value=0)
```

---

### 2.10. Combinació de DataFrames

| Funció / Mètode | Descripció |
| :--- | :--- |
| `pd.concat()` | Concatena DataFrames al llarg d'un eix (vertical o horitzontal). |
| `.merge()` | Combina DataFrames estil SQL JOIN (inner, left, right, outer). |
| `.join()` | Uneix DataFrames utilitzant principalment els seus índexs. |

```python
df1 = pd.DataFrame({'id': [1, 2], 'nom': ['Anna', 'Bernat']})
df2 = pd.DataFrame({'id': [1, 2], 'nota': [8.5, 7.0]})

# Fusió estil INNER JOIN
df_merged = df1.merge(df2, on='id', how='inner')

# Concatenació vertical de DataFrames
df3 = pd.DataFrame({'id': [3], 'nom': ['Carla']})
df_concat = pd.concat([df1, df3], ignore_index=True)
```

---

### 2.11. Aplicació de Funcions

| Funció | Descripció |
| :--- | :--- |
| `.apply()` | Aplica una funció a cada fila o columna d'un DataFrame (o elements de Series). |
| `.applymap()` / `.map()` | Aplica una funció element per element (`.map` per Series, `.applymap` per DataFrames). |

```python
# Transformació de valors amb lambda
estudiants['nota_doble'] = estudiants['nota'].apply(lambda x: x * 2)

# Classificació mitjançant funció personalitzada
def classificar(nota):
    return 'Aprovat' if nota >= 5 else 'Suspès'

estudiants['estat'] = estudiants['nota'].apply(classificar)
```

---

### 2.12. Exportació de Dades

| Funció | Descripció |
| :--- | :--- |
| `.to_csv()` | Guarda el DataFrame en un fitxer CSV. |
| `.to_excel()` | Exporta el DataFrame a un full de càlcul Excel. |
| `.to_json()` | Converteix i guarda el DataFrame en format JSON. |

```python
# Exemples d'exportació de dades (sense incloure l'índex)
# estudiants.to_csv('estudiants.csv', index=False)
# estudiants.to_excel('estudiants.xlsx', sheet_name='Resultats', index=False)
# estudiants.to_json('estudiants.json', orient='records', indent=2)
```

---

## 3. Recursos Addicionals i Bones Pràctiques

### Documentació i Enllaços d'Interès
- **Documentació Oficial de Pandas:** [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
- **Guia d'inici ràpid (10 Minutes to Pandas):** [https://pandas.pydata.org/docs/user_guide/10min.html](https://pandas.pydata.org/docs/user_guide/10min.html)

### Recomanacions de Desenvolupament
- **Còpies vs. Vistes:** Moltes operacions de Pandas retornen una còpia. Per aplicar modificacions sobre el DataFrame original, assegura't de reassignar la variable (`df = df.operacio()`) o fer servir l'argument `inplace=True` quan estigui disponible.
- **Visualització integrada:** Es recomana complementar l'ús de Pandas amb eines de representació gràfica com **Matplotlib** o **Seaborn** per a l'Anàlisi Exploratòria de Dades (EDA).
- **Format de Treball:** Per al desenvolupament iteratiu i anàlisi interactiva, l'entorn de treball recomanat és **Jupyter Notebook** o **Google Colab**.