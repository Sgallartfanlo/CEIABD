# Compilació de Scripts i Consultes SQL - VendesBigData

Aquest document recull tots els scripts T-SQL i consultes d'optimització desenvolupats durant la realització dels exercicis 3, 4, 5 i 6.

---

## Exercici 3: Optimització amb Índexs

### 3.1 Índexs per a Consultes Freqüents

```sql
USE VendesBigData;
GO

-- Consulta A: Comandes d'un client específic
CREATE NONCLUSTERED INDEX IX_Comandes_ClientID 
ON dbo.Comandes(ClientID);
GO

-- Consulta B: Productes d'una categoria actius
CREATE NONCLUSTERED INDEX IX_Productes_Jerarquia_Actiu 
ON dbo.Productes(JerarquiaProducteID, Actiu);
GO

-- Consulta C: Factures pendents de pagament
CREATE NONCLUSTERED INDEX IX_Factures_Estat_DataVenciment 
ON dbo.Factures(Estat, DataVenciment);
GO
```

### 3.2 Covering Index

```sql
USE VendesBigData;
GO

-- Covering Index per eliminar Key Lookups a la consulta de comandes lliurades
CREATE NONCLUSTERED INDEX IX_Comandes_Estat_DataComanda_Covering
ON dbo.Comandes (Estat, DataComanda)
INCLUDE (NumeroComanda, ClientID, ImportTotal);
GO
```

### 3.3 Filtered Index

```sql
USE VendesBigData;
GO

-- Índex filtrat només per a estats actius
CREATE NONCLUSTERED INDEX IX_Comandes_EstatsActius
ON dbo.Comandes (DataComanda, ClientID)
INCLUDE (ImportTotal)
WHERE Estat IN ('Pendent', 'Processat', 'Enviat');
GO
```

---

## Exercici 4: Columnstore Indexes

### 4.1 Creació de la Taula Analítica Denormalitzada

```sql
USE VendesBigData;
GO

-- 1. Crear taula denormalitzada per a analítica
IF OBJECT_ID('dbo.VendesAnalisi', 'U') IS NOT NULL 
    DROP TABLE dbo.VendesAnalisi;
GO

SELECT 
    c.ComandaID,
    c.DataComanda,
    YEAR(c.DataComanda) AS Anyo,
    MONTH(c.DataComanda) AS Mes,
    DATEPART(QUARTER, c.DataComanda) AS Trimestre,
    DATENAME(WEEKDAY, c.DataComanda) AS DiaSetmana,
    c.ClientID,
    cl.TipusClient,
    jc.NomNivell1 AS Departament,
    lc.ProducteID,
    p.NomProducte,
    lc.Quantitat,
    lc.ImportLinia,
    c.ImportTotal
INTO dbo.VendesAnalisi
FROM dbo.Comandes c
INNER JOIN dbo.Clients cl ON c.ClientID = cl.ClientID
INNER JOIN dbo.JerarquiaClients jc ON cl.JerarquiaClientID = jc.JerarquiaClientID
INNER JOIN dbo.LiniesComanda lc ON c.ComandaID = lc.ComandaID
INNER JOIN dbo.Productes p ON lc.ProducteID = p.ProducteID;
GO

-- 2. Afegir Columnstore Clustered Index
CREATE CLUSTERED COLUMNSTORE INDEX CCI_VendesAnalisi 
ON dbo.VendesAnalisi;
GO
```

### 4.3 Nonclustered Columnstore Index (HTAP)

```sql
USE VendesBigData;
GO

-- Afegir incapacitat analítica a la taula transaccional Comandes
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCI_Comandes
ON dbo.Comandes (DataComanda, ClientID, ImportTotal, Estat);
GO
```

---

## Exercici 5: Particionament de Taules

### 5.1 Definició de Particionament Trimestral

```sql
USE VendesBigData;
GO

-- 1. Crear la funció de particionament per trimestres
CREATE PARTITION FUNCTION PF_Factures_Trimestral (DATETIME2)
AS RANGE RIGHT FOR VALUES (
    '2024-01-01', '2024-04-01', '2024-07-01', '2024-10-01',
    '2025-01-01', '2025-04-01', '2025-07-01', '2025-10-01',
    '2026-01-01'
);
GO

-- 2. Crear el Partition Scheme
CREATE PARTITION SCHEME PS_Factures_Trimestral
AS PARTITION PF_Factures_Trimestral
ALL TO ([PRIMARY]);
GO

-- 3. Crear la taula particionada
CREATE TABLE dbo.FacturesParticionades (
    FacturaID INT IDENTITY(1,1) NOT NULL,
    DataFactura DATETIME2 NOT NULL,
    ClientID INT NOT NULL,
    ImportTotal DECIMAL(18,2) NOT NULL,
    Estat VARCHAR(20) NOT NULL,
    CONSTRAINT PK_FacturesParticionades PRIMARY KEY CLUSTERED (FacturaID, DataFactura)
) ON PS_Factures_Trimestral(DataFactura);
GO
```

### 5.3 Stored Procedure per a Sliding Window

```sql
USE VendesBigData;
GO

CREATE OR ALTER PROCEDURE dbo.sp_SlidingWindowFactures
    @DataNovaBoundary DATETIME2,   -- Nova data límit a afegir
    @DataAntigaBoundary DATETIME2  -- Data límit antiga a eliminar
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        -- 1. Designar el filegroup per al nou límit
        ALTER PARTITION SCHEME PS_Factures_Trimestral NEXT USED [PRIMARY];

        -- 2. SPLIT: Afegir el nou límit futur
        ALTER PARTITION FUNCTION PF_Factures_Trimestral()
        SPLIT RANGE (@DataNovaBoundary);

        -- 3. MERGE: Fusionar la partició antiga fora de la finestra de 2 anys
        ALTER PARTITION FUNCTION PF_Factures_Trimestral()
        MERGE RANGE (@DataAntigaBoundary);

        COMMIT TRANSACTION;
        PRINT 'Sliding Window executat correctament.';
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO
```

### 5.4 Script de Càrrega Ràpida amb SWITCH Partition

```sql
USE VendesBigData;
GO

-- 1. Recrear la taula Staging amb la restricció CHECK alineada a la Partició 9 (2026-01-01 a 2026-02-01)
IF OBJECT_ID('dbo.FacturesStaging', 'U') IS NOT NULL
    DROP TABLE dbo.FacturesStaging;
GO

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

-- 2. Carregar dades a Staging
INSERT INTO dbo.FacturesStaging (DataFactura, ClientID, ImportTotal, Estat)
SELECT DataComanda, ClientID, ImportTotal, Estat
FROM dbo.Comandes
WHERE DataComanda >= '2026-01-01' AND DataComanda < '2026-02-01';
GO

-- 3. Crear l'índex secundari no agrupat alineat
CREATE NONCLUSTERED INDEX IX_FacturesStaging_ClientID 
ON dbo.FacturesStaging(ClientID);
GO

-- 4. Buidar la partició destí per complir amb la condició de metadades
TRUNCATE TABLE dbo.FacturesParticionades WITH (PARTITIONS (9));
GO

-- 5. Executar el SWITCH
SET STATISTICS TIME ON;

ALTER TABLE dbo.FacturesStaging 
SWITCH TO dbo.FacturesParticionades PARTITION 9;

SET STATISTICS TIME OFF;
GO
```

---

## Exercici 6: Optimització Avançada i Manteniment

### 6.1 Reescriptura d'Índexs i Consulta Complexa

```sql
USE VendesBigData;
GO

-- Índexs de suport per a la consulta complexa
CREATE NONCLUSTERED INDEX IX_Comandes_ClientID_DataComanda
ON dbo.Comandes (ClientID, DataComanda)
INCLUDE (ImportTotal);
GO

CREATE NONCLUSTERED INDEX IX_LiniesComanda_ComandaID_ProducteID
ON dbo.LiniesComanda (ComandaID)
INCLUDE (ProducteID, Quantitat, ImportLinia);
GO

-- Consulta optimitzada utilitzant CTEs i ROW_NUMBER()
WITH ClientsFiltre AS (
    SELECT 
        c.ClientID,
        c.NomClient
    FROM dbo.Clients c
    INNER JOIN dbo.JerarquiaClients jc ON c.JerarquiaClientID = jc.JerarquiaClientID
    WHERE jc.Nivell1 = 'Empresa'
),
ComandesUltimAny AS (
    SELECT 
        co.ClientID,
        co.ComandaID,
        co.ImportTotal,
        co.DataComanda
    FROM dbo.Comandes co
    WHERE co.DataComanda >= DATEADD(YEAR, -1, GETDATE())
),
ProductesAgg AS (
    SELECT 
        co.ClientID,
        lc.ProducteID,
        SUM(lc.Quantitat) AS TotalQty,
        ROW_NUMBER() OVER (PARTITION BY co.ClientID ORDER BY SUM(lc.Quantitat) DESC) AS Rn
    FROM ComandesUltimAny co
    INNER JOIN dbo.LiniesComanda lc ON co.ComandaID = lc.ComandaID
    GROUP BY co.ClientID, lc.ProducteID
)
SELECT 
    cf.ClientID,
    cf.NomClient,
    COUNT(DISTINCT co.ComandaID) AS NumComandes,
    COUNT(DISTINCT lc.ProducteID) AS ProductesUnics,
    SUM(lc.Quantitat) AS TotalUnitats,
    SUM(lc.ImportLinia) AS TotalGastat,
    AVG(co.ImportTotal) AS MitjanaComanda,
    MAX(co.DataComanda) AS DarreraCompra,
    p.NomProducte AS ProducteFavorit
FROM ClientsFiltre cf
INNER JOIN ComandesUltimAny co ON cf.ClientID = co.ClientID
INNER JOIN dbo.LiniesComanda lc ON co.ComandaID = lc.ComandaID
LEFT JOIN ProductesAgg pa ON cf.ClientID = pa.ClientID AND pa.Rn = 1
LEFT JOIN dbo.Productes p ON pa.ProducteID = p.ProducteID
GROUP BY cf.ClientID, cf.NomClient, p.NomProducte
HAVING COUNT(DISTINCT co.ComandaID) > 5
ORDER BY TotalGastat DESC;
GO
```

### 6.2 Configuració i Consulta de Query Store

```sql
USE VendesBigData;
GO

-- Activar Query Store
ALTER DATABASE VendesBigData SET QUERY_STORE = ON (
    OPERATION_MODE = READ_WRITE,
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),
    DATA_FLUSH_INTERVAL_SECONDS = 900,
    MAX_STORAGE_SIZE_MB = 1000,
    INTERVAL_LENGTH_MINUTES = 60
);
GO

-- Consulta de monitorització de consultes lentes
SELECT 
    qsq.query_id,
    qsqt.query_sql_text,
    qsrs.count_executions,
    qsrs.avg_duration / 1000.0 AS avg_duration_ms,
    qsrs.avg_logical_io_reads,
    qsp.plan_id,
    qsp.is_forced_plan
FROM sys.query_store_query qsq
JOIN sys.query_store_query_text qsqt ON qsq.query_text_id = qsqt.query_text_id
JOIN sys.query_store_plan qsp ON qsq.query_id = qsp.query_id
JOIN sys.query_store_runtime_stats qsrs ON qsp.plan_id = qsrs.plan_id
WHERE qsrs.last_execution_time >= DATEADD(HOUR, -1, GETDATE())
ORDER BY qsrs.avg_duration DESC;
GO
```

### 6.3 Procediments Emmagatzemats de Manteniment Automàtic

```sql
USE VendesBigData;
GO

-- 1. Manteniment Diari
CREATE OR ALTER PROCEDURE dbo.sp_MantenimentDiari
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        UPDATE STATISTICS dbo.Comandes WITH RESAMPLE;
        UPDATE STATISTICS dbo.LiniesComanda WITH RESAMPLE;
        UPDATE STATISTICS dbo.FacturesParticionades WITH RESAMPLE;

        DECLARE @SQL NVARCHAR(MAX) = '';

        SELECT @SQL += 'ALTER INDEX ' + QUOTENAME(i.name) + ' ON ' + QUOTENAME(SCHEMA_NAME(t.schema_id)) + '.' + QUOTENAME(t.name) + ' REORGANIZE; '
        FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') s
        JOIN sys.tables t ON s.object_id = t.object_id
        JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
        WHERE s.avg_fragmentation_in_percent BETWEEN 10 AND 30 
          AND i.name IS NOT NULL;

        IF @SQL <> '' EXEC sp_executesql @SQL;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH;
END;
GO

-- 2. Manteniment Setmanal
CREATE OR ALTER PROCEDURE dbo.sp_MantenimentSetmanal
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        DECLARE @SQL NVARCHAR(MAX) = '';

        SELECT @SQL += 'ALTER INDEX ' + QUOTENAME(i.name) + ' ON ' + QUOTENAME(SCHEMA_NAME(t.schema_id)) + '.' + QUOTENAME(t.name) + ' REBUILD WITH (ONLINE = ON, FILLFACTOR = 85); '
        FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') s
        JOIN sys.tables t ON s.object_id = t.object_id
        JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
        WHERE s.avg_fragmentation_in_percent > 30 
          AND i.name IS NOT NULL;

        IF @SQL <> '' EXEC sp_executesql @SQL;

        IF OBJECT_ID('dbo.FacturesStaging', 'U') IS NOT NULL
            TRUNCATE TABLE dbo.FacturesStaging;

        SELECT 
            OBJECT_NAME(s.object_id) AS Taula,
            i.name AS IndexNom,
            s.user_seeks AS CercaDirectes,
            s.user_scans AS Escanejos,
            s.user_lookups AS CercaClau,
            s.user_updates AS Actualitzacions
        FROM sys.dm_db_index_usage_stats s
        JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
        WHERE s.database_id = DB_ID()
        ORDER BY Actualitzacions DESC;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH;
END;
GO

-- 3. Manteniment Mensual
CREATE OR ALTER PROCEDURE dbo.sp_MantenimentMensual
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        DECLARE @DataNova DATETIME2 = DATEADD(MONTH, 1, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0));
        DECLARE @DataAntiga DATETIME2 = DATEADD(YEAR, -2, @DataNova);

        EXEC dbo.sp_SlidingWindowFactures 
            @DataNovaBoundary = @DataNova, 
            @DataAntigaBoundary = @DataAntiga;

        SELECT 
            t.name AS Taula,
            SUM(p.rows) AS TotalFiles,
            CAST(SUM(a.total_pages) * 8 / 1024.0 AS DECIMAL(10,2)) AS MidaTotalMB
        FROM sys.tables t
        JOIN sys.partitions p ON t.object_id = p.object_id
        JOIN sys.allocation_units a ON p.partition_id = a.container_id
        GROUP BY t.name
        ORDER BY MidaTotalMB DESC;

        SELECT 
            OBJECT_NAME(i.object_id) AS Taula,
            i.name AS IndexNoUtilitzat,
            s.user_updates AS CostManteniment,
            ISNULL(s.user_seeks + s.user_scans + s.user_lookups, 0) AS TotalLectures
        FROM sys.indexes i
        LEFT JOIN sys.dm_db_index_usage_stats s 
            ON i.object_id = s.object_id AND i.index_id = s.index_id AND s.database_id = DB_ID()
        WHERE i.type_desc = 'NONCLUSTERED'
          AND i.is_primary_key = 0
          AND i.is_unique_constraint = 0
          AND (s.user_seeks IS NULL OR (s.user_seeks = 0 AND s.user_scans = 0 AND s.user_lookups = 0))
        ORDER BY CostManteniment DESC;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH;
END;
GO
```