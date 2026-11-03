# -*- coding: utf-8 -*-
"""
Activitat Pràctica 2: Anàlisi de Dades, Visualització i Exportació JSON
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

# Fixar la llavor aleatòria
np.random.seed(42)

# ==========================================
# PAS 1: Generació de Dades Simulades
# ==========================================
dies = np.arange(1, 31)
temperatures = np.round(np.random.normal(loc=22.0, scale=4.5, size=30), 2)
humitat = np.round(np.random.uniform(low=40.0, high=85.0, size=30), 1)
radiacio = np.round(np.random.exponential(scale=4.5, size=30), 2)

# ==========================================
# PAS 2: Processament i Classificació
# ==========================================
df = pd.DataFrame({
    'dia': dies,
    'temperatura_c': temperatures,
    'humitat_pct': humitat,
    'radiacio_kwh': radiacio
})

df['index_confort'] = np.round(
    df['temperatura_c'] - (0.55 - 0.55 * (df['humitat_pct'] / 100)) * (df['temperatura_c'] - 14), 2
)

condicions = [
    df['temperatura_c'] >= 25.0,
    (df['temperatura_c'] >= 18.0) & (df['temperatura_c'] < 25.0),
    df['temperatura_c'] < 18.0
]
etiquetes = ['Calor', 'Templat', 'Fred']
df['categoria_clima'] = np.select(condicions, etiquetes, default='Desconegut')

# ==========================================
# REPTE 1: Sistema d'Alertes per Onades de Calor
# ==========================================
df['alerta_calor'] = (
    ((df['temperatura_c'] >= 25.0) & (df['humitat_pct'] >= 65.0)) | 
    (df['temperatura_c'] >= 28.0)
)

percentatge_alertes = (df['alerta_calor'].sum() / len(df)) * 100
dies_consecutius_3 = (df['alerta_calor'].rolling(3).sum() == 3).any()

print("--- REPTE 1 ---")
print(f"Percentatge de dies amb alerta de calor: {percentatge_alertes:.2f}%")
print(f"Hi ha hagut almenys 3 dies consecutius d'alerta?: {dies_consecutius_3}")

# ==========================================
# REPTE 2: Filtrat i Exportació JSON
# ==========================================
df_emergencies = df[df['alerta_calor']].copy()
df_emergencies['recomanacio'] = np.where(
    df_emergencies['temperatura_c'] >= 28.0,
    "Activar refugis climàtics",
    "Atenció a col·lectius vulnerables"
)

fitxer_emergencia = 'alertes_emergencia.json'
df_emergencies.to_json(fitxer_emergencia, orient='records', indent=4, force_ascii=False)

print("\n--- REPTE 2 ---")
print(f"S'han exportat {len(df_emergencies)} dies d'emergència a '{fitxer_emergencia}'.")

# ==========================================
# REPTE 3: Dashboard Visual Multipanell 2x2
# ==========================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. (1,1) Línia: Temperatura i Humitat
axes[0, 0].plot(df['dia'], df['temperatura_c'], marker='o', color='#e74c3c', label='Temperatura (°C)')
axes[0, 0].plot(df['dia'], df['humitat_pct'], marker='s', color='#3498db', label='Humitat (%)')
axes[0, 0].set_title('Evolució de Temperatura i Humitat', fontweight='bold')
axes[0, 0].set_xlabel('Dia del Mes')
axes[0, 0].grid(True, linestyle=':', alpha=0.6)
axes[0, 0].legend()

# 2. (1,2) Scatter: Humitat vs Índex Confort
axes[0, 1].scatter(df['humitat_pct'], df['index_confort'], color='#8e44ad', s=50)
axes[0, 1].set_title('Relació entre Humitat i Confort Tèrmic', fontweight='bold')
axes[0, 1].set_xlabel('Humitat (%)')
axes[0, 1].set_ylabel('Índex Confort')
axes[0, 1].grid(True, linestyle=':', alpha=0.6)

# 3. (2,1) Histograma: Radiació Solar
axes[1, 0].hist(df['radiacio_kwh'], bins=8, color='#f39c12', edgecolor='black', alpha=0.8)
axes[1, 0].set_title('Distribució de la Radiació Solar', fontweight='bold')
axes[1, 0].set_xlabel('Radiació (kWh/m²)')
axes[1, 0].set_ylabel('Freqüència')
axes[1, 0].grid(True, linestyle=':', alpha=0.6)

# 4. (2,2) Sectorial (Pie chart): Categories Climàtiques
recompte = df['categoria_clima'].value_counts()
axes[1, 1].pie(recompte.values, labels=recompte.index, autopct='%1.1f%%', colors=['#2ecc71', '#f39c12', '#3498db'])
axes[1, 1].set_title('Proporció de Categories Climàtiques', fontweight='bold')

plt.tight_layout()
plt.savefig('dashboard_climatic.png', dpi=150)

print("\n--- REPTE 3 ---")
print("Dashboard guardat com a 'dashboard_climatic.png'")
plt.show()
# ==========================================
# REPTE 4: Simulació de Consum Energètic
# ==========================================

# Es mostra cuan tanquem la finestra del gràfic
soroll_aleatori = np.random.normal(loc=0, scale=5, size=30)
df['consum_mwh'] = 100 + (df['temperatura_c'] * 3.5) + soroll_aleatori

correlacio = df['temperatura_c'].corr(df['consum_mwh'])

print("\n--- REPTE 4 ---")
print(f"Coeficient de correlació de Pearson entre Temperatura i Consum: {correlacio:.4f}")
print("Interpretació: Existeix una correlació positiva MOLT FORTA. A mesura que augmenta la temperatura, el consum d'energia s'incrementa significativament a causa de l'ús de climatitzadors.")