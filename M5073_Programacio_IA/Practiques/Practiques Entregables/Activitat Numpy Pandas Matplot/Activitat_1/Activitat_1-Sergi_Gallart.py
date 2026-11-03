# -*- coding: utf-8 -*-
"""
Activitat Pràctica 1: Monitoratge de Servidors i Detecció d'Anomalies
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fixem la llavor per reproductibilitat
np.random.seed(42)


# PAS 1: Generació de Dades Sintètiques (NumPy)
n_hores = 720
dates = pd.date_range(start="2026-09-01", periods=n_hores, freq="h")

# CPU base amb distribució normal (mitjana=45, desv_std=10)
cpu_base = np.random.normal(loc=45, scale=10, size=n_hores)

# Cicle diari sinusoïdal
hores_dia = np.tile(np.arange(24), 30)
cicle_diari = 15 * np.sin(2 * np.pi * hores_dia / 24)

# Combineu la base, el cicle i injecció d'anomalies (15 pics)
cpu = cpu_base + cicle_diari
indexs_anomalies = np.random.choice(n_hores, size=15, replace=False)
cpu[indexs_anomalies] += np.random.uniform(30, 45, size=15)
cpu = np.clip(cpu, 0, 100)

print(f"S'han generat {len(cpu)} registres d'ús de CPU.")


# PAS 2: Processament i Resum de Dades (Pandas)

df = pd.DataFrame({
    'DataHora': dates,
    'CPU_Uso': cpu
})
df.set_index('DataHora', inplace=True)

# Mitjana mòbil de 24 hores i detecció d'anomalies (> 85%)
df['Mitjana_Mobil_24h'] = df['CPU_Uso'].rolling(window=24, min_periods=1).mean()
LLINDAR_CRITIC = 85.0
df['Anomalia'] = df['CPU_Uso'] > LLINDAR_CRITIC


# EXERCICI 1: Simulació de Memòria RAM (NumPy)

soroll_ram = np.random.normal(loc=10, scale=5, size=n_hores)
ram = 0.7 * df['CPU_Uso'] + soroll_ram
ram = np.clip(ram, 0, 100)
df['RAM_Uso'] = ram

print("\n--- EXERCICI 1: Primeres files amb la nova columna RAM_Uso ---")
print(df[['CPU_Uso', 'RAM_Uso']].head())


# EXERCICI 2: Anàlisi per Dia de la Setmana (Pandas)

df['Dia_Setmana'] = df.index.day_name()
mitjana_per_dia = df.groupby('Dia_Setmana')['CPU_Uso'].mean().sort_values(ascending=False)

print("\n--- EXERCICI 2: Mitjana d'ús de CPU per dia de la setmana ---")
print(mitjana_per_dia)
print(f"\nEl dia amb la mitjana de CPU més alta és: {mitjana_per_dia.index[0]} ({mitjana_per_dia.iloc[0]:.2f}%)")


# EXERCICI 3: Panell Subplots (Matplotlib)

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=False)

# Subgràfic 1: Línia temporal de CPU i RAM
axes[0].plot(df.index, df['CPU_Uso'], label='Ús de CPU (%)', color='#2b5c8f', alpha=0.7, linewidth=1)
axes[0].plot(df.index, df['RAM_Uso'], label='Ús de RAM (%)', color='#2ea043', alpha=0.7, linewidth=1)
axes[0].set_title('Evolució Temporal de CPU i RAM', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Ús (%)')
axes[0].set_ylim(0, 105)
axes[0].grid(True, linestyle=':', alpha=0.6)
axes[0].legend(loc='upper right')

# Subgràfic 2: Histograma de la distribució de la CPU
axes[1].hist(df['CPU_Uso'], bins=30, color='#2b5c8f', edgecolor='black', alpha=0.7)
axes[1].set_title('Distribució de l\'Ús de CPU (Histograma)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Ús de CPU (%)')
axes[1].set_ylabel('Freqüència (Hores)')
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()