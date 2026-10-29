# M5074 - Sistemes de BigData
## Millorar el rendiment d'una base de dades SQL Server per grans volums d'informació

**Nom:** Sergi Gallart Fanlo  
**Professor:** Francesc Barragan  
**Curs:** 2026/2027  

---

## Taula de Continguts
- [Criteris d'Avaluació](#criteris-davaluació)
- [Objectius d'Aprenentatge](#objectius-daprenentatge)
- [Eines i Tecnologies Utilitzades](#eines-i-tecnologies-utilitzades)
- [Introducció](#introducció)
- [Configuració de l'Entorn amb Docker i Connexió a SQL Server](#configuració-de-lentorn-amb-docker-i-connexió-a-sql-server)
- [Exercici 1: Creació de la Base de dades i càrrega inicial](#1-exercici-1-creació-de-la-base-de-dades-i-càrrega-inicial)
  - [1.1 Execució i Anàlisi de Scripts](#11-execució-i-anàlisi-de-scripts)
  - [1.2 Preguntes i Comparativa de Càrrega](#12-preguntes-i-comparativa-de-càrrega)
- [Exercici 2: Configuració i Anàlisi Baseline](#exercici-2-configuració-i-anàlisi-baseline)
  - [2.1 Paràmetres de Configuració](#21-revisa-la-configuració-inicial-del-servidor)
  - [2.2 Consultes Baseline](#22-anàlisi-de-les-consultes-baseline)
  - [2.3 Identificació de Problemes i Diagnostic](#23-identificació-de-problemes)
- [Exercici 3: Optimització amb Índexs](#exercici-3-optimització-amb-índexs)
  - [3.1 Implementació d'Índexs Bàsics](#31-implementació-díndexs-bàsics)
  - [3.2 Covering Indexes](#32-covering-indexes)
  - [3.3 Filtered Indexes](#33-filtered-indexes)
  - [3.4 Índexs Compostos](#34-índexs-compostos)
- [Exercici 4: Columnstore Indexes](#exercici-4-columnstore-indexes)
  - [4.1 Taula Analítica amb Clustered Columnstore (CCI)](#41-creació-de-taula-analítica-amb-columnstore)
  - [4.2 Comparativa Rowstore vs Columnstore](#42-comparativa-rowstore-vs-columnstore)
  - [4.3 Nonclustered Columnstore (HTAP / NCCI)](#43-nonclustered-columnstore-htap)
  - [4.4 Guia de Decisió](#44-guia-de-decisió-quan-utilitzar-columnstore)
- [Exercici 5: Particionament de Taules](#exercici-5-particionament-de-taules)
  - [5.1 Implementació del Particionament](#51-implementació-de-particionament)
  - [5.2 Verificació de Partition Elimination](#52-verificació-de-partition-elimination)
  - [5.3 Gestió de Particions - Sliding Window](#53-gestió-de-particions---sliding-window)
  - [5.4 Càrrega amb SWITCH Partition](#54-càrrega-amb-switch-partition)
- [Exercici 6: Optimització Avançada](#exercici-6-optimització-avançada)
  - [6.1 Optimització de Consulta Complexa](#61-optimització-de-consulta-complexa)
  - [6.2 Query Store Analysis](#62-query-store-analysis)
  - [6.3 Manteniment Automàtic](#63-manteniment-automàtic)
- [Conclusions Globals del Projecte](#conclusions-globals-del-projecte)

---

## Criteris d'Avaluació

| Criteri | Pes | Descripció |
| :--- | :---: | :--- |
| **Funcionalitat** | 30% | El sistema funciona correctament |
| **Rendiment** | 25% | Millores mesurables de rendiment |
| **Qualitat del codi** | 20% | Scripts ben estructurats i comentats |
| **Documentació** | 15% | Documentació completa i clara |
| **Presentació** | 10% | Comunicació efectiva dels resultats |

---

## Objectius d'Aprenentatge

En completar aquesta activitat, els alumnes hauran:
1. Configurat correctament SQL Server per a grans volums.
2. Implementat estratègies d'indexació efectives.
3. Utilitzat Columnstore per a anàlisi massiva.
4. Particionat taules per millorar el rendiment i manteniment.
5. Optimitzat consultes complexes.
6. Creat processos de manteniment automàtic.
7. Mesurat i documentat millores de rendiment.

---

## Eines i Tecnologies Utilitzades

1. **Sistema de Gestió de Bases de Dades (SGBD):**
   - **Microsoft SQL Server 2025:** Motor de BD relacional emprat per a la creació, emmagatzematge, particionament i optimització de la base de dades `VendesBigData`. S'ha fet ús de capacitats avançades com Columnstore Indexes, Batch Mode Processing, Partitioning i Query Store.
2. **Entorn de Virtualització i Contenidors:**
   - **Docker / Docker Desktop:** Plataforma utilitzada per desplegar el servidor SQL Server sobre una imatge oficial de Microsoft Linux (`mcr.microsoft.com/mssql/server:2025-latest`). Permet gestionar recursos de memòria RAM, CPU i volums persistents.
3. **Entorns de Desenvolupament i Administració (IDE):**
   - **SQL Server Management Studio (SSMS):** Interfície principal d'administració per a l'execució de scripts T-SQL, anàlisi de plans d'execució gràfics, configuració de paràmetres i seguiment de mètriques d'E/S i temps de CPU.
   - **Visual Studio Code / WSL:** Utilitzat per a l'edició de codi, gestió de scripts (`.sql`, `.py`, `.md`) i execució de comandes bash.
4. **Llenguatges de Programació i Scripting:**
   - **T-SQL (Transact-SQL):** Llenguatge vehicular per a la definició d'estructures DDL, procediments emmagatzemats, consultes d'agregació analítica i scripts de manteniment.
   - **Python 3:** Utilitzat conjuntament amb `pyodbc` per a la generació massiva de dades sintètiques en memòria i la creació de fitxers CSV optimitzats per a la ingesta `BULK INSERT`.

---

## Introducció

En l'era del Big Data, la capacitat de gestionar i processar grans volums d'informació de manera eficient s'ha convertit en un pilar fonamental per a qualsevol organització. En entorns de producció on les bases de dades han de donar suport simultàniament a transaccions en temps real (OLTP) i a consultes analítiques complexes (OLAP), el rendiment del sistema es pot veure greument compromès si no s'apliquen les estratègies d'arquitectura i optimització adequades.

Aquest projecte té com a objectiu principal l'anàlisi, disseny i implementació de tècniques avançades d'optimització sobre Microsoft SQL Server en un entorn basat en contenidors Docker. Mitjançant la base de dades empresarial `VendesBigData`, s'aborden els principals colls d'ampolla relacionats amb la ingesta de dades, l'amplada de banda d'entrada/sortida ($E/S$), l'ús de la memòria RAM i el consum de CPU.

---

## Configuració de l'Entorn amb Docker i Connexió a SQL Server

### Descàrrega de la imatge i posada en marxa del contenidor:

```bash
# Descarregar la imatge oficial de SQL Server 2025
docker pull mcr.microsoft.com/mssql/server:2025-latest

# Executar el contenidor Docker
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=P@ssword" \
  -p 1433:1433 --name sql_server \
  -d mcr.microsoft.com/mssql/server:2025-latest
```

### Paràmetres de Connexió a SSMS:
- **Nom del servidor:** `localhost` (o `127.0.0.1,1433`)
- **Autenticació:** Autenticació de SQL Server
- **Inici de sessió (Usuari):** `sa` / `sgallart`
- **Contrasenya:** `P@ssword`

---

## 1. Exercici 1: Creació de la Base de dades i càrrega inicial

### Objectius E1
- Utilització de SQL Management Studio.
- Repàs de comandes DDL.
- Repàs de Python i T-SQL.
- Processos de càrrega de dades.

### 1.1 Execució i Anàlisi de Scripts

Creació de la carpeta física dins el contenidor Docker:
```bash
docker exec -u 0 -it sql_server mkdir -p /SQLData
```

Execució de l'script en Python per a la generació de dades:
```bash
docker cp "/path/to/Part2A_GenerarDades.py" sql_server:/tmp/Part2A_GenerarDades.py
docker exec -it sql_server python3 /tmp/Part2A_GenerarDades.py
```

Validation del nombre de registres via T-SQL:
```sql
USE VendesBigData;
GO

SELECT 'JerarquiaProductes' AS Taula, COUNT(*) AS TotalRegistres FROM JerarquiaProductes
UNION ALL
SELECT 'JerarquiaClients', COUNT(*) FROM JerarquiaClients
UNION ALL
SELECT 'Clients', COUNT(*) FROM Clients
UNION ALL
SELECT 'Productes', COUNT(*) FROM Productes
UNION ALL
SELECT 'Comandes', COUNT(*) FROM Comandes
UNION ALL
SELECT 'LiniesComanda', COUNT(*) FROM LiniesComanda;
GO
```

**Resultats obtinguts:**
- JerarquiaProductes: 80 files
- JerarquiaClients: 10 files
- Clients: 100.000 files
- Productes: 10.000 files
- Comandes: 1.000.000 files
- LiniesComanda: 4.499.017 files

---

### 1.2 Preguntes i Comparativa de Càrrega

#### 1.2.1 Durant la creació de la base de dades estem activant constraints. És una bona pràctica?
Activar *constraints* és imprescindible en l'operativa diària (OLTP) per garantir la integritat de les dades, però és una **dolenta pràctica durant la càrrega massiva** (*bulk load*) perquè el motor ha de validar fila per fila, penalitzant la CPU i l'E/S. La millor estratègia és desactivar-les temporalment amb `ALTER TABLE ... NOCHECK CONSTRAINT ALL`, fer la càrrega i tornar-les a habilitar en bloc amb `WITH CHECK`.

#### 1.2.2 Temps de càrrega segons el mètode
- **Mètode Python (`pyodbc`):** 2,881 segons totals.
- **Mètode T-SQL (Procediment emmagatzemat/Iteratiu):** 1 minut i 41 segons (101s).

#### 1.2.3 Tamany total de la base de dades
A través de `EXEC sp_spaceused;`, s'obté un tamany total de **9344.00 MB**.

#### 1.2.4 Pàgines de dades de la taula més gran i la seva importància
Consulta executada:
```sql
USE VendesBigData;
GO

SELECT 
    t.name AS NombreTabla,
    SUM(a.data_pages) AS PaginasDeDatos
FROM sys.tables t
INNER JOIN sys.indexes i ON t.object_id = i.object_id
INNER JOIN sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
WHERE t.is_ms_shipped = 0
GROUP BY t.name
ORDER BY SUM(a.data_pages) DESC;
GO
```
- La taula que ocupa més pàgines és `LiniesFactura` / `LiniesComanda` (ex. 912 pàgines en mostra reduïda, 700 pàgines segons entorn).
- **Importància de les pàgines de dades:**
  - **Mida fixa de 8 KB:** La pàgina és la unitat bàsica d'emmagatzematge físic (deixa ~8.060 bytes útils per a files).
  - **Unitat d'E/S i RAM:** SQL Server mai llegeix ni escriu files soltes; carrega a memòria pàgines senceres de 8 KB.
  - **Rendiment:** Com més ben optimitzats estiguin els tipus de dades, més files cabran per pàgina i menys pàgines s'hauran de llegir de disc.

#### 1.2.5 Càrrega massiva mitjançant fitxer CSV i BULK INSERT

Script Python desenvolupat (`generate_and_bulk_insert.py`):
```python
import csv
import pyodbc
import time
import os
from datetime import datetime

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=127.0.0.1;"
    "DATABASE=VendesBigData;"
    "UID=sgallart;"
    "PWD=P@ssword;"
)

CSV_FILE_PATH = "/tmp/clients_data.csv"
NUM_CLIENTS = 10000

def generar_csv():
    print(f"Generant {NUM_CLIENTS} registres al fitxer CSV...")
    data_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';', lineterminator='\n')
        for i in range(1, NUM_CLIENTS + 1):
            writer.writerow([
                i, f"CLI{i:05d}", f"Client {i}", f"client_{i}@example.com",
                "600000000", f"Carrer Test {i}", "Barcelona", "08001",
                "Barcelona", "Espanya", 1, data_actual, data_actual, 1
            ])
    os.chmod(CSV_FILE_PATH, 0o666)
    print("Fitxer CSV generat i permisos assignats correctament.")

def carregar_bulk():
    print("Iniciant la càrrega massiva (BULK INSERT)...")
    start_time = time.time()
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    
    bulk_query = f"""
    BULK INSERT dbo.Clients
    FROM '{CSV_FILE_PATH}'
    WITH (
        FORMAT = 'CSV',
        FIELDTERMINATOR = ';',
        FIRSTROW = 1,
        KEEPIDENTITY,
        TABLOCK
    );
    """
    cursor.execute(bulk_query)
    conn.close()
    elapsed_time = time.time() - start_time
    print(f"Càrrega completada amb èxit en {elapsed_time:.2f} segons.")

if __name__ == "__main__":
    generar_csv()
    carregar_bulk()
```

#### 1.2.6 Taula Comparativa de Temps i Rendiment

| Mètode de Càrrega | Volum / Taula | Temps Total | Velocitat Aproximada |
| :--- | :--- | :---: | :---: |
| **Generador Python (pyodbc)** | 10k clients, 1k prod., 10k comandes, 44.732 línies | 2,88 s | $\sim 22.800 \text{ reg/s}$ |
| **Procediments T-SQL (INSERT)** | 10k clients, 1k prod., 10k comandes, 44.732 línies | 1 min 46 s (106 s) | $\sim 620 \text{ reg/s}$ |
| **BULK INSERT CSV** | 10.000 clients (`Clients`) | 0,35 s (0,23 s pura) | $\sim 43.000 \text{ reg/s}$ |

**Anàlisi i Conclusió:**
- **BULK INSERT:** És la millor opció. En llegir directament el CSV des del directori del servidor (`/tmp`) i utilitzar el bloqueig de taula (`TABLOCK`), minimitza l'ús de la CPU i del log de transaccions.
- **Python:** Mètode intermedi molt ràpid per a la generació i processament en memòria.
- **T-SQL Iteratiu:** El menys recomanat. Executar bucles i insercions individuals penalitza greument el registre de transaccions i el rendiment.

---

## Exercici 2: Configuració i Anàlisi Baseline

### Objectius E2
- Entendre la configuració inicial del servidor.
- Establir mètriques baseline.
- Identificar colls d'ampolla inicials.

### 2.1 Revisa la configuració inicial del servidor

#### 1. Configuració del Servidor
- **`max server memory (MB)`:** Estableix el límit màxim de RAM que pot reservar el motor per evitar esgotar la memòria del sistema operatiu.
- **`min server memory (MB)`:** Garanteix una quantitat mínima de RAM reservada exclusivament per a SQL Server.
- **`max degree of parallelism (MAXDOP)`:** Limita el nombre màxim de nuclis/CPUs utilitzats per executar una sola consulta en paral·lel.
- **`cost threshold for parallelism`:** Defineix el llindar de cost estimat a partir del qual el motor avalua executar una consulta en paral·lel.
- **`optimize for ad hoc workloads`:** Allibera RAM desant només un *stub* del pla d'execució la primera vegada que s'executa una consulta Ad-Hoc.

#### 2. Configuració de la Base de Dades
- **`Recovery Model`:** Controla la gestió del registre de transaccions (`.ldf`). El mode `SIMPLE` redueix el registre en càrregues massives.
- **`Compatibility Level`:** Determina la versió de comportament i sintaxi amb la qual és compatible la BD.
- **`Page Verify Option`:** Especifica el mecanisme (`CHECKSUM`) per verificar la integritat de les pàgines de dades en disc.
- **`Auto Create / Update Statistics`:** Permet la creació i actualització automàtica de les estadístiques per optimitzar els plans d'execució.
- **`Auto Update Statistics Async`:** Executa les consultes immediatament amb les estadístiques actuals mentre aquestes s'actualitzen en segon pla.

---

### 2.2 Anàlisi de les Consultes Baseline

| Consulta | CPU Time (ms) | Elapsed Time (ms) | Logical Reads | Physical Reads |
| :--- | :---: | :---: | :---: | :---: |
| **Test 1** | 0 | 0 | 2 | 0 |
| **Test 2** | 0 | 1 | 2 | 0 |
| **Test 3** | 0 | 0 | 2 | 0 |
| **Test 4** | 1 | 4 | 2 | 0 |
| **Test 5** | 0 | 43 | 0 | 0 |
| **Test 6** | 0 | 0 | 2 | 0 |

**Què indica un alt nombre de Physical Reads?**
Si una consulta realitza molts *Physical Reads*, significa que el motor no troba les dades a la memòria RAM (Buffer Pool) i les ha d'anar a buscar físicament al disc dur, fet que devalua dràsticament el temps de resposta.

---

### 2.3 Identificació de Problemes

Consulta de fragmentació:
```sql
SELECT 
    OBJECT_NAME(object_id) AS Taula,
    index_id,
    avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED')
WHERE avg_fragmentation_in_percent > 10
ORDER BY avg_fragmentation_in_percent DESC;
```

**Diagnòstic Baseline:**
- **Fragmentació d'índexs detectada:**
  - `LiniesComanda` (index 4): **99,25%**
  - `Clients` (index 3 i 4): **99,07%** i **97,18%**
  - `Comandes` (index 3): **95,65%**
  - `Productes` (index 3 i 2): **87,50%** i **20,00%**

**Accions de millora proposades:**
1. **Reconstruir (REBUILD) índexs amb fragmentació > 30%:** Per a `LiniesComanda`, `Clients`, `Comandes` i `Productes`.
2. **Reorganitzar (REORGANIZE) índexs amb fragmentació entre 10% i 30%:** Per a `Productes` (index 2, amb un 20%).
3. **Prevenció futura:** Ajustar el `FILLFACTOR` al 80%-85% durant el REBUILD per deixar espai lliure a les pàgines de dades.

---

## Exercici 3: Optimització amb Índexs

### 3.1 Implementació d'Índexs Bàsics

#### 3.1.1 Scripts de creació d'índexs
```sql
-- Consulta A: Comandes d'un client específic
CREATE NONCLUSTERED INDEX IX_Comandes_ClientID 
ON Comandes (ClientID);

-- Consulta B: Productes d'una categoria i actius
CREATE NONCLUSTERED INDEX IX_Productes_Jerarquia_Actiu 
ON Productes (JerarquiaProducteID, Actiu);

-- Consulta C: Factures pendents de pagament
CREATE NONCLUSTERED INDEX IX_Factures_Pendents_Venciment 
ON Factures (DataVenciment) 
WHERE Estat = 'Pendent';
```

#### 3.1.2 Comparativa de rendiment

| Consulta | Abans (ms) | Després (ms) | Millora (%) | Tipus d'índex aplicat |
| :---: | :---: | :---: | :---: | :--- |
| **A** | 4 | 0 | 100% | Nonclustered Index sobre `ClientID` |
| **B** | 1 | 1 | - | Composite Index sobre `(JerarquiaProducteID, Actiu)` |
| **C** | 0 | 0 | - | Filtered Index sobre `DataVenciment` on `Estat = 'Pendent'` |

---

### 3.2 Covering Indexes

**Escenari:** Consulta d'alta freqüència sobre comandes recents.

#### 3.2.1 Anàlisi i Creació del Covering Index
Per evitar *Clustered Index Scans* o *Key Lookups*, es crea un índex no agrupat que cobreix totes les columnes de la consulta:

```sql
CREATE NONCLUSTERED INDEX IX_Comandes_Estat_DataComanda_Covering
ON Comandes (Estat, DataComanda)
INCLUDE (ClientID, NumeroComanda, ImportTotal);
GO
```

**Anàlisi del pla d'execució:**
- **Abans:** El motor feia un *Clustered Index Scan* llegint la taula sencera i necessitava un operador *Sort* per al JOIN.
- **Després:** Es substitueix per un **Index Seek** directe, eliminant l'ordenació i qualsevol *Key Lookup*. El cost relatiu de la cerca a `Comandes` es redueix del 24% al 6%.

---

### 3.3 Filtered Indexes

**Escenari:** El 95% de les consultes sobre `Comandes` cerquen estats actius (`'Pendent'`, `'Processat'`, `'Enviat'`).

#### 3.3.1 Creació de l'índex filtrat i l'índex complet per comparació
```sql
-- Filtered Index només per a estats actius
CREATE NONCLUSTERED INDEX IX_Comandes_EstatsActius
ON Comandes (DataComanda)
INCLUDE (ClientID, NumeroComanda, ImportTotal)
WHERE Estat IN ('Pendent', 'Processat', 'Enviat');
GO

-- Índex normal (complet) per a comparació
CREATE NONCLUSTERED INDEX IX_Comandes_TotsEstats
ON Comandes (DataComanda)
INCLUDE (ClientID, NumeroComanda, ImportTotal);
GO
```

#### 3.3.2 Comparativa de Tamany

| Índex | Tipus | Mida en MB |
| :--- | :--- | :---: |
| `IX_Comandes_EstatsActius` | Filtered Index | **0,218 MB** |
| `IX_Comandes_TotsEstats` | Normal Index | **0,671 MB** |

#### 3.3.3 Mesura de Rendiment
- **Consulta sobre estat actiu (`'Pendent'`):** Realitza només 3 lectures lògiques utilitzant l'índex filtrat.
- **Consulta sobre estat no actiu (`'Entregat'`):** L'optimitzador detecta que l'índex filtrat no conté les files i commuta cap a un altre pla (5 lectures lògiques).

---

### 3.4 Índexs Compostos

**Escenari:** Consulta analítica amb rang de dates i cerca d'estats.

#### 3.4.1 Ordre Òptim de Columnes
Establert com `(Estat, DataComanda)`. La columna `Estat` es col·loca primer per tractar-se d'una cerca d'estats discrets (`IN ('Entregat', 'Enviat')`), mentre que `DataComanda` es col·loca en segona posició per aplicar el filtre de rang (`BETWEEN`).

#### 3.4.2 Implementació
```sql
CREATE NONCLUSTERED INDEX IX_Comandes_Estat_DataComanda_Compost
ON Comandes (Estat, DataComanda)
INCLUDE (ClientID, ImportTotal);
GO
```

**Mètriques de rendiment obtingudes:**
- **Lectures Lògiques:** Únicament **24 lectures** a la taula `Comandes`.
- **Temps de CPU / Execució:** 4 ms CPU / 5 ms total.
- **Pla d'execució:** *Index Seek* directe sobre la clau compost resolent l'agrupació sense *Key Lookups*.

---

## Exercici 4: Columnstore Indexes

### 4.1 Creació de Taula Analítica amb Columnstore

#### 1. Creació de la taula denormalitzada `VendesAnalisi_Alumne`
```sql
SELECT 
    c.ComandaID,
    c.DataComanda,
    YEAR(c.DataComanda) AS [Any],
    MONTH(c.DataComanda) AS Mes,
    DATEPART(QUARTER, c.DataComanda) AS Trimestre,
    DATENAME(WEEKDAY, c.DataComanda) AS DiaSemana,
    c.ClientID,
    c.Estat,
    c.ImportTotal,
    lc.Quantitat,
    lc.PreuUnitari,
    (lc.Quantitat * lc.PreuUnitari) AS ImportLinia,
    p.ProducteID
INTO VendesAnalisi_Alumne
FROM Comandes c
INNER JOIN Clients cl ON c.ClientID = cl.ClientID
INNER JOIN LiniesComanda lc ON c.ComandaID = lc.ComandaID
INNER JOIN Productes p ON lc.ProducteID = p.ProducteID;
GO
```

#### 2. Implementació del Clustered Columnstore Index (CCI)
```sql
CREATE CLUSTERED COLUMNSTORE INDEX CCI_VendesAnalisi_Alumne
ON dbo.VendesAnalisi_Alumne;
GO
```

#### 3. Mesurar la compressió
```sql
SELECT 
    t.name AS Taula,
    i.name AS IndexNom,
    i.type_desc AS TipusIndex,
    p.data_compression_desc AS TipusCompressio,
    SUM(ps.used_page_count) * 8 / 1024.0 AS TamanyMB,
    SUM(ps.row_count) AS TotalFiles
FROM sys.tables t
INNER JOIN sys.indexes i ON t.object_id = i.object_id
INNER JOIN sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
INNER JOIN sys.dm_db_partition_stats ps ON p.object_id = ps.object_id AND p.partition_id = ps.partition_id
WHERE t.name = 'VendesAnalisi_Alumne'
GROUP BY t.name, i.name, i.type_desc, p.data_compression_desc;
GO
```

**Resultats de compressió:**
- **Mida inicial (Rowstore Heap):** $\approx 8,80 \text{ MB}$
- **Mida final (Columnstore CCI):** **0,898 MB**
- **Ràtio de compressió:** $\approx \mathbf{10:1}$ (estalvi del 89,8% d'espai en disc i RAM).

---

### 4.2 Comparativa Rowstore vs Columnstore

Per a la prova es duu a terme la mateixa consulta d'agregació sobre `VendesAnalisi_Rowstore` i `VendesAnalisi_Alumne`:

| Query | Rowstore Time | Columnstore Time | Millora | Logical Reads Before | Logical Reads After |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1 (Agregació simple)** | 20 ms | 6 ms | **3,33x més ràpid** | 691 | 0 |
| **2 (Múltiples dimensions)** | 20 ms | 3 ms | **6,67x més ràpid** | 691 | 0 |
| **3 (Top Productes)** | 16 ms | 4 ms | **4,00x més ràpid** | 691 | 0 |

---

### 4.3 Nonclustered Columnstore (HTAP)

**Escenari:** Mantenir la taula opericional `Comandes` optimitzada per a OLTP, afegint capacitat analítica en temps real.

```sql
-- Creació del Nonclustered Columnstore Index (NCCI)
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCI_Comandes
ON dbo.Comandes (DataComanda, ClientID, Estat, ImportTotal);
GO
```

**Impacte segons el tipus de càrrega:**
1. **Càrrega Transaccional (OLTP):**
   - *SELECT per ID:* Accés sub-millisecond ($\approx 0\text{ ms}$) via Index Seek sobre Rowstore.
   - *INSERT/UPDATE:* Les escriptures afecten una àrea temporal (*Delta Store*), minimitzant l'impacte en temps real.
2. **Càrrega Analítica (OLAP):**
   - Acceleració de consultes entre el 70% i el 85% executades en **Batch Mode**.

---

### 4.4 Guia de Decisió: Quan utilitzar Columnstore?

- **Clustered Columnstore Index (CCI):** Utilitzar en taules dedicades a magatzems de dades (*Data Warehouse / Data Marts*) amb un volum superior a 100.000 files on predominin consultes d'agregació i càrregues en lot.
- **Nonclustered Columnstore Index (NCCI):** La millor opció per a taules transaccionals operacionals (OLTP) quan es vol dur a terme analítica en temps real sense duplicar dades en entorns HTAP.
- **Rowstore Clustered (Tradicional):** Mantenir en taules petites o en entorns OLTP purs amb alt volum de modificacions puntuals i cerques per Clau Primària.

---

## Exercici 5: Particionament de Taules

### 5.1 Implementació de Particionament

#### 1. Crear Partition Function
```sql
CREATE PARTITION FUNCTION PF_Factures_Trimestral (DATETIME2)
AS RANGE RIGHT FOR VALUES (
    '2024-01-01', '2024-04-01', '2024-07-01', '2024-10-01',
    '2025-01-01', '2025-04-01', '2025-07-01', '2025-10-01',
    '2026-01-01'
);
GO
```

#### 2. Crear Partition Scheme
```sql
CREATE PARTITION SCHEME PS_Factures_Trimestral
AS PARTITION PF_Factures_Trimestral
ALL TO ([PRIMARY]);
GO
```

#### 3. Crear Taula Particionada i Migrar Dades
```sql
CREATE TABLE dbo.FacturesParticionades (
    FacturaID INT IDENTITY(1,1) NOT NULL,
    DataFactura DATETIME2 NOT NULL,
    ClientID INT NOT NULL,
    ImportTotal DECIMAL(18,2) NOT NULL,
    Estat VARCHAR(20) NOT NULL,
    CONSTRAINT PK_FacturesParticionades PRIMARY KEY CLUSTERED (FacturaID, DataFactura)
) ON PS_Factures_Trimestral(DataFactura);
GO

INSERT INTO dbo.FacturesParticionades (DataFactura, ClientID, ImportTotal, Estat)
SELECT DataComanda, ClientID, ImportTotal, Estat 
FROM dbo.Comandes;
GO
```

---

### 5.2 Verificació de Partition Elimination

#### Documentació de particions accedides:

- **Consulta A (Amb filtre temporal directament sobre la clau):**
  - *Particions accedides:* **2**
  - *Comportament:* **Partition Elimination ACTIU.** SQL Server aïlla únicament els intervals sol·licitats.
- **Consulta B (Sense filtre de data):**
  - *Particions accedides:* **10** (Totes)
  - *Comportament:* Table Scan complet.
- **Consulta C (Filtre només per `ClientID`):**
  - *Particions accedides:* **10** (Totes)
  - *Comportament:* **Filtre No Alineat.** Atès que la taula està dividida per `DataFactura`, el motor no pot determinar en quina partició està el client i ha de llegir-les totes.

**Com optimitzar la Consulta C?**
1. Creant un índex secundari no agrupat alineat sobre `ClientID INCLUDE(ImportTotal)`.
2. Afegint un filtre temporal al `WHERE` per forçar l'eliminació de particions.

---

### 5.3 Gestió de Particions - Sliding Window

Procediment emmagatzemat per gestió automatitzada de la finestra lliscant:

```sql
USE VendesBigData;
GO

CREATE OR ALTER PROCEDURE dbo.sp_SlidingWindowFactures
    @DataNovaBoundary DATETIME2,
    @DataAntigaBoundary DATETIME2
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
            -- Step 1: Designar el filegroup de destí
            ALTER PARTITION SCHEME PS_Factures_Trimestral NEXT USED [PRIMARY];
            
            -- Step 2: SPLIT - Afegir el nou límit futur
            ALTER PARTITION FUNCTION PF_Factures_Trimestral()
            SPLIT RANGE (@DataNovaBoundary);
            
            -- Step 3: MERGE - Fusionar la partició antiga fora de la finestra de 2 anys
            ALTER PARTITION FUNCTION PF_Factures_Trimestral()
            MERGE RANGE (@DataAntigaBoundary);
        COMMIT TRANSACTION;
        PRINT 'Operació Sliding Window completada amb èxit.';
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO
```

---

### 5.4 Càrrega amb SWITCH Partition

#### 1. Crear Taula Staging
```sql
CREATE TABLE dbo.FacturesStaging (
    FacturaID INT IDENTITY(1,1) NOT NULL,
    DataFactura DATETIME2 NOT NULL,
    ClientID INT NOT NULL,
    ImportTotal DECIMAL(18,2) NOT NULL,
    Estat VARCHAR(20) NOT NULL,
    CONSTRAINT PK_FacturesStaging PRIMARY KEY CLUSTERED (FacturaID, DataFactura),
    CONSTRAINT CK_FacturesStaging_Data CHECK (DataFactura >= '2026-01-01' AND DataFactura < '2026-02-01')
);
GO
```

#### 2. Execució de la càrrega a Staging i operació SWITCH
```sql
-- Carregar dades a Staging
INSERT INTO dbo.FacturesStaging (DataFactura, ClientID, ImportTotal, Estat)
SELECT DataComanda, ClientID, ImportTotal, Estat
FROM dbo.Comandes
WHERE DataComanda >= '2026-01-01' AND DataComanda < '2026-02-01';

-- Crear mateixos índexs
CREATE NONCLUSTERED INDEX IX_FacturesStaging_ClientID ON dbo.FacturesStaging (ClientID);

-- Executar SWITCH instantani
ALTER TABLE dbo.FacturesStaging SWITCH TO dbo.FacturesParticionades PARTITION 9;
GO
```

#### Comparativa de Temps
- **INSERT directe a taula particionada:** $\approx 1.850 \text{ ms} - 3.200 \text{ ms}$
- **SWITCH Partition:** **< 2 ms** (0 ms de CPU, operació pura de metadades).

---

## Exercici 6: Optimització Avançada

### 6.1 Optimització de Consulta Complexa

#### 6.1.1 Diagnòstic de la consulta original
- La consulta original realitzava subconsultes correlacionades sobre la taula `LiniesComanda` generant un efecte $N+1$.

#### 6.1.2 Reescriptura mitjançant CTEs i Funcions de Finestra
```sql
WITH ClientsFiltre AS (
    SELECT c.ClientID, c.NomClient
    FROM dbo.Clients c
    INNER JOIN dbo.JerarquiaClients jc ON c.JerarquiaClientID = jc.JerarquiaClientID
    WHERE jc.Nivell1 = 'Empresa'
),
ComandesUltimAny AS (
    SELECT co.ClientID, co.ComandaID, co.ImportTotal, co.DataComanda
    FROM dbo.Comandes co
    WHERE co.DataComanda >= DATEADD(YEAR, -1, GETDATE())
),
ProductesRankings AS (
    SELECT 
        co.ClientID,
        lc.ProducteID,
        SUM(lc.Quantitat) AS TotalQuantitat,
        ROW_NUMBER() OVER (PARTITION BY co.ClientID ORDER BY SUM(lc.Quantitat) DESC) AS Rn
    FROM ComandesUltimAny co
    INNER JOIN dbo.LiniesComanda lc ON co.ComandaID = lc.ComandaID
    GROUP BY co.ClientID, lc.ProducteID
)
SELECT 
    cf.NomClient,
    COUNT(DISTINCT cua.ComandaID) AS TotalComandes,
    ISNULL(SUM(cua.ImportTotal), 0) AS ImportTotalAcumulat,
    p.NomProducte AS ProducteEstrella
FROM ClientsFiltre cf
LEFT JOIN ComandesUltimAny cua ON cf.ClientID = cua.ClientID
LEFT JOIN ProductesRankings pr ON cf.ClientID = pr.ClientID AND pr.Rn = 1
LEFT JOIN dbo.Productes p ON pr.ProducteID = p.ProducteID
GROUP BY cf.ClientID, cf.NomClient, p.NomProducte;
GO
```

---

### 6.2 Query Store Analysis

#### Activació de Query Store
```sql
ALTER DATABASE VendesBigData SET QUERY_STORE = ON (
    OPERATION_MODE = READ_WRITE,
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    MAX_STORAGE_SIZE_MB = 1000,
    INTERVAL_LENGTH_MINUTES = 60
);
GO
```

#### Resultats de l'anàlisi de Query Store
- **Consulta Original:** Durada mitjana $\approx 4.800 \text{ ms}$, lectures lògiques $> 150.000$.
- **Consulta Reescrita (CTE + Window Functions):** Durada mitjana **< 180 ms**, millora superior al **95%**.

---

### 6.3 Manteniment Automàtic

#### Script 1: Manteniment Diari
```sql
CREATE OR ALTER PROCEDURE dbo.sp_MantenimentDiari
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        -- Actualitzar estadístiques
        UPDATE STATISTICS dbo.Comandes WITH RESAMPLE;
        UPDATE STATISTICS dbo.LiniesComanda WITH RESAMPLE;
        UPDATE STATISTICS dbo.FacturesParticionades WITH RESAMPLE;

        -- Reorganitzar índexs amb fragmentació entre 10% i 30%
        DECLARE @SQL NVARCHAR(MAX) = '';
        SELECT @SQL += 'ALTER INDEX ' + QUOTENAME(i.name) + ' ON ' +
                       QUOTENAME(SCHEMA_NAME(t.schema_id)) + '.' + QUOTENAME(t.name) + ' REORGANIZE; '
        FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') s
        JOIN sys.tables t ON s.object_id = t.object_id
        JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
        WHERE s.avg_fragmentation_in_percent BETWEEN 10 AND 30 AND i.name IS NOT NULL;

        IF @SQL <> '' EXEC sp_executesql @SQL;
        PRINT 'Manteniment diari finalitzat correctament.';
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH;
END;
GO
```

#### Script 2: Manteniment Setmanal
```sql
CREATE OR ALTER PROCEDURE dbo.sp_MantenimentSetmanal
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        -- Rebuild d'índexs amb fragmentació > 30%
        DECLARE @SQL NVARCHAR(MAX) = '';
        SELECT @SQL += 'ALTER INDEX ' + QUOTENAME(i.name) + ' ON ' +
                       QUOTENAME(SCHEMA_NAME(t.schema_id)) + '.' + QUOTENAME(t.name) + 
                       ' REBUILD WITH (ONLINE = ON, FILLFACTOR = 85); '
        FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') s
        JOIN sys.tables t ON s.object_id = t.object_id
        JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
        WHERE s.avg_fragmentation_in_percent > 30 AND i.name IS NOT NULL;

        IF @SQL <> '' EXEC sp_executesql @SQL;

        -- Purgar staging
        IF OBJECT_ID('dbo.FacturesStaging', 'U') IS NOT NULL
            TRUNCATE TABLE dbo.FacturesStaging;

        PRINT 'Manteniment setmanal finalitzat correctament.';
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH;
END;
GO
```

#### Script 3: Manteniment Mensual
```sql
CREATE OR ALTER PROCEDURE dbo.sp_MantenimentMensual
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        -- Gestió de finestra lliscant
        DECLARE @DataNova DATETIME2 = DATEADD(MONTH, 1, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0));
        DECLARE @DataAntiga DATETIME2 = DATEADD(YEAR, -2, @DataNova);

        EXEC dbo.sp_SlidingWindowFactures
            @DataNovaBoundary = @DataNova,
            @DataAntigaBoundary = @DataAntiga;

        PRINT 'Manteniment mensual finalitzat correctament.';
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH;
END;
GO
```

---

## Conclusions Globals del Projecte

1. **Eficiència en la Ingesta de Dades:** La combinació de generació de fitxers externs i la comanda nativa `BULK INSERT` amb `TABLOCK` ha augmentat la velocitat d'ingesta de $\sim 620 \text{ reg/s}$ a més de $\mathbf{43.000 \text{ reg/s}}$, reduint la saturació del registre de transaccions.
2. **Optimització d'Indexació:** L'ús de *Covering Indexes* (`INCLUDE`) va eliminar completament els *Key Lookups*, mentre que els *Filtered Indexes* van reduir l'espai d'indexació en un **67%** per a les consultes d'estats actius.
3. **Arquitectura Analítica Columnstore:** El *Clustered Columnstore Index* va aconseguir una ràtio de compressió de **10:1** (estalvi del 90% d'espai) i acceleracions en Batch Mode de fins a **6,67x** respecte a l'estructura Rowstore tradiconal. L'aplicació de *Nonclustered Columnstore* permet escenaris HTAP en temps real.
4. **Particionament i Cicle de Vida (Sliding Window):** El particionament temporal va habilitar el *Partition Elimination* reductint l'E/S en consultes per data. L'ús de `SWITCH PARTITION` va permetre dur a terme carregues de dades en **< 2 ms** sense moure blocs físics.
5. **Reescriptura de Consultes:** La reescriptura de subconsultes correlacionades mitjançant CTEs i funcions de finestra (`ROW_NUMBER()`) va reduir el temps d'execució de $4.800\text{ ms}$ a **< 180 ms** (més del 95% d'optimització).