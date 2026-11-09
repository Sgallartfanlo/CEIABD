import requests
import pandas as pd
import json

print("✅ Llibreries carregades correctament.")

url = 'https://swapi.info/api/planets'
resposta = requests.get(url)

print(f"Codi d'estat HTTP {resposta.status_code}")

if resposta.status_code == 200:
    planetes = resposta.json()
    print(f"S'han obtingut {len(planetes)} planetes.")
    
else:
    print("❌Error en la petició a l'API.")

df_planetes = pd.DataFrame(planetes)
cols_interes = ['name','climate','population']
df_filtrat = df_planetes[cols_interes].copy()

print('--- 📋 Primers 5 planetes ---')
print(df_filtrat.head())