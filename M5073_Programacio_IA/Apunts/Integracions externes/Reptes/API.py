import requests
import pandas as pd
import json

print("✅ Llibreries carregades correctament.")

url = 'https://swapi.info/api/people/'
resposta = requests.get(url)

print(f"Codi d'estat HTTP {resposta.status_code}")

if resposta.status_code == 200:
    personatges = resposta.json()
    print(f"S'han obtingut {len(personatges)} personatges.")
    
else:
    print("❌Error en la petició a l'API.")

df_personatges = pd.DataFrame(personatges)
cols_interes = ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender']
df_filtrat = df_personatges[cols_interes].copy()

print('--- 📋 Primers 5 personatges ---')
print(df_filtrat.head())

df_filtrat['height'] = pd.to_numeric(df_filtrat['height'], errors='coerce')
df_filtrat['mass'] = pd.to_numeric(df_filtrat['mass'].str.replace(',', ''), errors='coerce')

#Personatges de mes de 180 cm d'alçada
personatges_alts = df_filtrat[df_filtrat['height'] > 180]
print(f"--- ✅ S'han trobat {len(personatges_alts)} personatges amb més de 180 cm d'alçada. ---")
print(personatges_alts[['name', 'height', 'gender']].head())