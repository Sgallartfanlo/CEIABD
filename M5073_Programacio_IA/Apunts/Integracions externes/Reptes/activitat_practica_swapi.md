# 🚀 Activitat Pràctica: Consum d'una API RESTful amb Python i SWAPI

## 🎯 Objectius de l'activitat
1. **Realitzar peticions HTTP GET** a una API RESTful pública ([Star Wars API](https://swapi.info/api/people)).
2. **Validar els codis d'estat** de la resposta (`status_code == 200`).
3. **Processar i estructurar les dades JSON** obtingudes utilitzant la llibreria **Pandas**.
4. **Resoldre reptes** de filtratge i exploració de dades.

---

## 🛠️ Pas 1: Carregar les llibreries necessàries

Importem `requests` per realitzar connexions HTTP i `pandas` per organitzar i analitzar les dades en taules.

```python
import requests
import pandas as pd
import json

print('✅ Llibreries carregades correctament.')
```

---

## 🌐 Pas 2: Consultar l'API pública SWAPI

Fem una petició `GET` a l'endpoint de personatges.

```python
url = 'https://swapi.info/api/people'
resposta = requests.get(url)

print(f"Codi d'estat HTTP: {resposta.status_code}")

if resposta.status_code == 200:
    personatges = resposta.json()
    print(f"✅ S'han obtingut dades de {len(personatges)} personatges.")
else:
    print('❌ Error en la petició a l\'API.')
```

---

## 🐼 Pas 3: Convertir la resposta JSON a un DataFrame de Pandas

Transformem la llista de diccionaris JSON en una taula estructurada.

```python
df_personatges = pd.DataFrame(personatges)
cols_interes = ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender']
df_filtrat = df_personatges[cols_interes].copy()

print('--- 📋 Primers 5 personatges ---')
df_filtrat.head()
```

---

## 🔍 Pas 4: Anàlisi i Filtratge de Dades

Convertim les columnes d'alçada (`height`) i massa (`mass`) a valors numèrics per poder fer filtratges.

```python
df_filtrat['height'] = pd.to_numeric(df_filtrat['height'], errors='coerce')
df_filtrat['mass'] = pd.to_numeric(df_filtrat['mass'].str.replace(',', ''), errors='coerce')

# Personatges de més de 180 cm
personatges_alts = df_filtrat[df_filtrat['height'] > 180]
print(f"Nombre de personatges > 180 cm: {len(personatges_alts)}")
personatges_alts[['name', 'height', 'gender']].head()
```

---

## ✏️ Reptes per a l'Alumnat

### **Repte 1:**
Fes una petició `GET` a l'endpoint de planetes (`https://swapi.info/api/planets`) i mostra en un DataFrame el nom (`name`), el clima (`climate`) i la població (`population`) dels primers 5 planetes.

### **Repte 2:**
Filtra la llista de planetes per trobar aquells que tinguin un clima que contingui la paraula **`arid`**.

```python
# Resolució dels reptes per part de l'alumne:
```