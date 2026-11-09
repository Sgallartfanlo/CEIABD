import pandas as pd
import requests


url = 'https://swapi.info/api/planets'
resposta = requests.get(url, timeout=30)
resposta.raise_for_status()

planetes = resposta.json()
df_planetes = pd.DataFrame(planetes)
planetes_arids = df_planetes[
    df_planetes['climate'].str.contains('arid', case=False, na=False)
]

print(f"S'han trobat {len(planetes_arids)} planetes amb un clima àrid:")
print(planetes_arids[['name', 'climate']].to_string(index=False))