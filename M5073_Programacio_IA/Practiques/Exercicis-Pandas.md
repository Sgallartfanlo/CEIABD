# Bateria d'Exercicis de Pandas

Aquest document conté la col·lecció completa d'exercicis pràctics i les seves resolucions en Python utilitzant la biblioteca Pandas.

---

## Bloc 1: Creació i Exploració Bàsica

### Exercici 1.1
Crea una `Series` amb les temperatures mitjanes dels últims 7 dies a Barcelona (inventa les dades). L'índex ha de ser els dies de la setmana en català.

```python
import pandas as pd
import numpy as np

temperatures = pd.Series(
    [22.1, 21.8, 23.4, 24.1, 22.9, 21.5, 20.7],
    index=["dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte", "diumenge"],
    name="temperatura_media_barcelona"
)

print(temperatures)
```

---

### Exercici 1.2
Crea un `DataFrame` amb informació de 5 estudiants del cicle: `nom`, `cognoms`, `edat`, `nota_prog`, `nota_bd`, `nota_sisop`. Mostra les primeres 3 files i la informació general del DataFrame.

```python
estudiants = pd.DataFrame({
    'nom': ['Anna', 'Bernat', 'Carla', 'David', 'Eva'],
    'cognoms': ['García', 'López', 'Martínez', 'Sánchez', 'Pérez'],
    'edat': [19, 20, 21, 18, 22],
    'nota_prog': [8.5, 7.8, 9.1, 6.9, 8.7],
    'nota_bd': [7.9, 8.4, 8.8, 8.2, 9.3],
    'nota_sisop': [8.1, 7.6, 9.0, 7.4, 8.9]
})

print("Primeres 3 files:")
print(estudiants.head(3))
print("\nInformació general:")
print(estudiants.info())
```

---

### Exercici 1.3
A partir del DataFrame anterior, mostra les dimensions, els noms de les columnes, els tipus de dades i les estadístiques descriptives.

```python
print('Dimensions:', estudiants.shape)
print('Noms de columnes:', estudiants.columns.tolist())
print('Tipus de dades:\n', estudiants.dtypes)
print('\nEstadístiques descriptives:\n', estudiants.describe())
```

---

## Bloc 2: Indexació i Selecció

### Exercici 2.1
Del DataFrame d'estudiants, selecciona només les columnes `nom` i `nota_prog`. Després selecciona l'estudiant de la posició 2 utilitzant `iloc`.

```python
# Seleccionar columnes 'nom' i 'nota_prog'
col_seleccionades = estudiants[['nom', 'nota_prog']]
print("Columnes seleccionades:")
print(col_seleccionades)

# Seleccionar l'estudiant de la posició 2 amb iloc
estudiant_pos2 = estudiants.iloc[2]
print("\nEstudiant a la posició 2:")
print(estudiant_pos2)
```

---

### Exercici 2.2
Accedeix a la nota de programació del primer estudiant utilitzant dos mètodes diferents (`loc` i `at`).

```python
# Accés amb loc
nota_loc = estudiants.loc[0, 'nota_prog']

# Accés amb at
nota_at = estudiants.at[0, 'nota_prog']

print(f"Nota amb loc: {nota_loc}")
print(f"Nota amb at: {nota_at}")
```

---

### Exercici 2.3
Crea una nova columna `nota_mitjana` que calculi la mitjana de les tres assignatures per cada estudiant.

```python
estudiants['nota_mitjana'] = (estudiants['nota_prog'] + estudiants['nota_bd'] + estudiants['nota_sisop']) / 3
print(estudiants[['nom', 'nota_mitjana']])
```

---

## Bloc 3: Filtratge i Ordenació

### Exercici 3.1
Filtra els estudiants que tinguin una nota mitjana superior a 7.

```python
mitjana_alta = estudiants[estudiants['nota_mitjana'] > 7]
print(mitjana_alta)
```

---

### Exercici 3.2
Mostra els estudiants menors de 20 anys ordenats per nota mitjana de manera descendent.

```python
joves_ordenats = estudiants[estudiants['edat'] < 20].sort_values('nota_mitjana', ascending=False)
print(joves_ordenats)
```

---

### Exercici 3.3
Utilitza el mètode `query()` per seleccionar els estudiants amb `nota_prog > 6` i `nota_bd > 6`.

```python
filtrats_query = estudiants.query('nota_prog > 6 and nota_bd > 6')
print(filtrats_query)
```

---

## Bloc 4: Operacions amb Valors Nuls

### Exercici 4.1
Crea un DataFrame amb dades d'un gimnàs que contingui: `nom_usuari`, `edat`, `pes`, `altura`, `data_ultima_visita`. Introdueix alguns valors `NaN` deliberadament.

```python
gimnas = pd.DataFrame({
    'nom_usuari': ['Marc', 'Laura', 'Arnau', 'Marta', 'Joan', None],
    'edat': [22, 30, np.nan, 25, 40, 28],
    'pes': [75.5, np.nan, 68.0, 60.2, np.nan, 82.1],
    'altura': [1.78, 1.65, 1.72, np.nan, 1.80, 1.75],
    'data_ultima_visita': ['2026-10-01', '2026-09-15', None, '2026-10-10', '2026-10-18', '2026-09-20']
})

print(gimnas)
```

---

### Exercici 4.2
Detecta quines files i columnes tenen valors nuls. Calcula el percentatge de valors nuls per columna.

```python
print("Valors nuls per fila:\n", gimnas.isna().sum(axis=1))
print("\nPercentatge de valors nuls per columna:\n", (gimnas.isna().mean() * 100))
```

---

### Exercici 4.3
Omple els valors nuls de `pes` amb la mitjana, els de `altura` amb la mediana, i elimina les files on `nom_usuari` sigui nul.

```python
# Eliminar les files on 'nom_usuari' sigui nul
gimnas_net = gimnas.dropna(subset=['nom_usuari']).copy()

# Omplir valors nuls de 'pes' amb la mitjana i d''altura' amb la mediana
gimnas_net['pes'] = gimnas_net['pes'].fillna(gimnas_net['pes'].mean())
gimnas_net['altura'] = gimnas_net['altura'].fillna(gimnas_net['altura'].median())

print(gimnas_net)
```

---

## Bloc 5: Agregació i Estadístiques

### Exercici 5.1
Crea un DataFrame amb vendes d'una botiga online: `producte`, `categoria`, `preu`, `quantitat`, `mes`. Calcula el total de vendes per categoria.

```python
vendes_botiga = pd.DataFrame({
    'producte': ['Ratolí', 'Teclat', 'Monitor', 'Ratolí', 'Auriculars', 'Teclat'],
    'categoria': ['Perifèrics', 'Perifèrics', 'Pantalles', 'Perifèrics', 'Àudio', 'Perifèrics'],
    'preu': [25.0, 45.0, 180.0, 25.0, 60.0, 45.0],
    'quantitat': [10, 5, 2, 8, 4, 7],
    'mes': ['Octubre', 'Octubre', 'Setembre', 'Setembre', 'Octubre', 'Setembre']
})

vendes_botiga['total_venda'] = vendes_botiga['preu'] * vendes_botiga['quantitat']
print(vendes_botiga.groupby('categoria')['total_venda'].sum())
```

---

### Exercici 5.2
Del DataFrame anterior, troba quin producte s'ha venut més vegades i quin ha generat més ingressos.

```python
producte_mes_venut = vendes_botiga.groupby('producte')['quantitat'].sum().idxmax()
producte_mes_ingressos = vendes_botiga.groupby('producte')['total_venda'].sum().idxmax()

print(f"Producte més venut (quantitat): {producte_mes_venut}")
print(f"Producte amb més ingressos: {producte_mes_ingressos}")
```

---

### Exercici 5.3
Calcula la mitjana de preus per categoria i el nombre de productes diferents per categoria.

```python
print("Mitjana de preus per categoria:\n", vendes_botiga.groupby('categoria')['preu'].mean())
print("\nNombre de productes diferents per categoria:\n", vendes_botiga.groupby('categoria')['producte'].nunique())
```

---

## Bloc 6: Agrupació i Pivot

### Exercici 6.1
Amb el DataFrame de vendes, agrupa per `mes` i `categoria` i calcula les vendes totals.

```python
print(vendes_botiga.groupby(['mes', 'categoria'])['total_venda'].sum())
```

---

### Exercici 6.2
Crea una pivot table que mostri les vendes totals amb `mes` com a files i `categoria` com a columnes.

```python
pivot_vendes = pd.pivot_table(vendes_botiga, values='total_venda', index='mes', columns='categoria', aggfunc='sum', fill_value=0)
print(pivot_vendes)
```

---

### Exercici 6.3
Utilitzant `groupby` i `agg()`, calcula simultàniament la suma, mitjana i màxim de les vendes per categoria.

```python
print(vendes_botiga.groupby('categoria')['total_venda'].agg(['sum', 'mean', 'max']))
```

---

## Bloc 7: Aplicació de Funcions

### Exercici 7.1
Crea un DataFrame amb noms de persones i les seves edats. Crea una nova columna `generacio` que classifiqui les persones en: `'Gen Z'` (menors de 25), `'Millennials'` (25-40), `'Gen X'` (41-56), `'Boomers'` (més de 56). Utilitza `apply()` amb una funció lambda o definida.

```python
persones = pd.DataFrame({
    'nom': ['Pau', 'Júlia', 'Sergi', 'Elena', 'Marc'],
    'edat': [22, 35, 48, 60, 19]
})

def classificar_generacio(edat):
    if edat < 25:
        return 'Gen Z'
    elif edat <= 40:
        return 'Millennials'
    elif edat <= 56:
        return 'Gen X'
    else:
        return 'Boomers'

persones['generacio'] = persones['edat'].apply(classificar_generacio)
print(persones)
```

---

### Exercici 7.2
Tens un DataFrame amb preus en euros. Crea columnes noves amb els preus en dòlars (multiplicar per $1.1$) i en lliures (multiplicar per $0.85$) utilitzant `apply()`.

```python
preus = pd.DataFrame({'preu_eur': [10.0, 50.0, 100.0, 250.0]})

preus['preu_usd'] = preus['preu_eur'].apply(lambda x: x * 1.1)
preus['preu_gbp'] = preus['preu_eur'].apply(lambda x: x * 0.85)

print(preus)
```

---

### Exercici 7.3
Crea una funció que detecti si un email és vàlid (conté `@` i un punt després de `@`) i aplica-la a una columna d'emails.

```python
emails = pd.DataFrame({'email': ['test@gmail.com', 'correu_invalid', 'alumne@ies.cat', 'error.@com']})

def validar_email(email):
    if '@' in email:
        part_post_arroba = email.split('@')[1]
        return '.' in part_post_arroba
    return False

emails['valid'] = emails['email'].apply(validar_email)
print(emails)
```

---

## Bloc 8: Combinació de DataFrames

### Exercici 8.1
Crea dos DataFrames: un amb informació d'empleats (`id_empleat`, `nom`, `departament`) i un altre amb salaris (`id_empleat`, `salari_brut`, `antiguitat`). Fusiona'ls utilitzant `merge()`.

```python
empleats = pd.DataFrame({'id_empleat': [1, 2, 3], 'nom': ['Anna', 'Pere', 'Clàudia'], 'departament': ['IT', 'HR', 'Vendes']})
salaris = pd.DataFrame({'id_empleat': [1, 2, 4], 'salari_brut': [30000, 28000, 35000], 'antiguitat': [3, 5, 1]})

df_fusionat = empleats.merge(salaris, on='id_empleat', how='inner')
print(df_fusionat)
```

---

### Exercici 8.2
Tens dos DataFrames amb vendes de diferents trimestres. Concatena'ls verticalment per tenir totes les vendes de l'any.

```python
vendes_q1 = pd.DataFrame({'mes': ['Gener', 'Febrer', 'Març'], 'vendes': [1000, 1200, 1100]})
vendes_q2 = pd.DataFrame({'mes': ['Abril', 'Maig', 'Juny'], 'vendes': [1500, 1300, 1400]})

vendes_any = pd.concat([vendes_q1, vendes_q2], ignore_index=True)
print(vendes_any)
```

---

### Exercici 8.3
Crea un DataFrame amb productes i preus, i un altre amb productes i proveïdors. Realitza diferents tipus de merge: `inner`, `left`, `right` i `outer`. Observa les diferències.

```python
df_prod = pd.DataFrame({'id_prod': [101, 102, 103], 'producte': ['A', 'B', 'C'], 'preu': [10, 20, 30]})
df_prov = pd.DataFrame({'id_prod': [101, 102, 104], 'proveidor': ['Prov1', 'Prov2', 'Prov3']})

print("INNER:\n", df_prod.merge(df_prov, on='id_prod', how='inner'))
print("\nLEFT:\n", df_prod.merge(df_prov, on='id_prod', how='left'))
print("\nRIGHT:\n", df_prod.merge(df_prov, on='id_prod', how='right'))
print("\nOUTER:\n", df_prod.merge(df_prov, on='id_prod', how='outer'))
```

---

## Bloc 9: Lectura i Escriptura de Fitxers

### Exercici 9.1
Crea un DataFrame amb dades inventades d'un hotel (`data_reserva`, `nom_client`, `tipus_habitacio`, `preu_nit`, `nits`). Exporta'l a CSV i torna a llegir-lo.

```python
hotel = pd.DataFrame({
    'data_reserva': ['2026-10-01', '2026-10-02', '2026-10-03'],
    'nom_client': ['Anna', 'Bernat', 'Carla'],
    'tipus_habitacio': ['Doble', 'Individual', 'Suite'],
    'preu_nit': [80, 50, 150],
    'nits': [3, 2, 5]
})

hotel.to_csv('hotel.csv', index=False)
hotel_llegit = pd.read_csv('hotel.csv')
print(hotel_llegit)
```

---

### Exercici 9.2
Exporta el DataFrame anterior a Excel amb un nom de full personalitzat. Llegeix només les primeres 10 files del fitxer Excel.

```python
hotel.to_excel('hotel.xlsx', sheet_name='Dades_Hotel', index=False)
hotel_excel_primeres = pd.read_excel('hotel.xlsx', nrows=10)
print(hotel_excel_primeres)
```

---

### Exercici 9.3
Crea un fitxer JSON amb estructura jeràrquica (per exemple, clients amb múltiples comandes) i llegeix-lo amb Pandas.

```python
import json

dades_json = [
    {"client": "Anna", "comandes": [{"id": 1, "total": 40}, {"id": 2, "total": 60}]},
    {"client": "Joan", "comandes": [{"id": 3, "total": 100}]}
]

with open('clients_comandes.json', 'w') as f:
    json.dump(dades_json, f)

df_json = pd.read_json('clients_comandes.json')
print(df_json)
```

---

## Bloc 10: Cas Pràctic Integrador

### Exercici 10.1
Tens un dataset d'una escola amb les següents dades: `id_estudiant`, `nom`, `edat`, `curs`, `nota_mates`, `nota_fisica`, `nota_quimica`, `nota_llengua`, `faltes_assistencia`.

Realitza les següents tasques:
- **a)** Carrega les dades (crea el DataFrame manualment amb almenys 15 estudiants).
- **b)** Neteja les dades: detecta i tracta valors nuls, elimina duplicats.
- **c)** Crea una columna `nota_mitjana_ciencies` (mitjana de mates, física i química).
- **d)** Classifica els estudiants en `'Excel·lent'` ($>9$), `'Notable'` ($7-9$), `'Aprovat'` ($5-7$), `'Suspès'` ($<5$).
- **e)** Analitza: quants estudiants hi ha per categoria? Quina és la mitjana de faltes per curs?
- **f)** Identifica els 3 millors estudiants de cada curs.
- **g)** Crea una visualització amb les notes mitjanes per curs.
- **h)** Exporta els resultats a CSV.

```python
import matplotlib.pyplot as plt

# a) Carregar les dades (15 estudiants)
np.random.seed(42)
escola = pd.DataFrame({
    'id_estudiant': range(1, 16),
    'nom': ['Estudiant_' + str(i) for i in range(1, 16)],
    'edat': np.random.randint(17, 21, 15),
    'curs': np.random.choice(['1r DAM', '2n DAM'], 15),
    'nota_mates': np.random.uniform(3.0, 10.0, 15),
    'nota_fisica': np.random.uniform(2.5, 10.0, 15),
    'nota_quimica': np.random.uniform(4.0, 10.0, 15),
    'nota_llengua': np.random.uniform(5.0, 10.0, 15),
    'faltes_assistencia': np.random.randint(0, 15, 15)
})

# b) Neteja de dades: eliminar duplicats i tractar valors nuls
escola = escola.drop_duplicates()
escola = escola.fillna(escola.mean(numeric_only=True))

# c) Columna 'nota_mitjana_ciencies'
escola['nota_mitjana_ciencies'] = (escola['nota_mates'] + escola['nota_fisica'] + escola['nota_quimica']) / 3

# d) Classificació dels estudiants
def classificar_estudiant(nota):
    if nota > 9:
        return 'Excel·lent'
    elif nota >= 7:
        return 'Notable'
    elif nota >= 5:
        return 'Aprovat'
    else:
        return 'Suspès'

escola['categoria'] = escola['nota_mitjana_ciencies'].apply(classificar_estudiant)

# e) Anàlisi
print("Estudiants per categoria:\n", escola['categoria'].value_counts())
print("\nMitjana de faltes per curs:\n", escola.groupby('curs')['faltes_assistencia'].mean())

# f) Top 3 millors estudiants per curs
top3_per_curs = escola.groupby('curs').apply(lambda x: x.nlargest(3, 'nota_mitjana_ciencies')).reset_index(drop=True)
print("\nTop 3 per curs:\n", top3_per_curs[['curs', 'nom', 'nota_mitjana_ciencies']])

# g) Visualització
mitjanes_curs = escola.groupby('curs')['nota_mitjana_ciencies'].mean()
plt.bar(mitjanes_curs.index, mitjanes_curs.values)
plt.title('Nota mitjana de ciències per curs')
plt.xlabel('Curs')
plt.ylabel('Nota mitjana')
plt.show()

# h) Exportar a CSV
escola.to_csv('resultats_escola.csv', index=False)
```