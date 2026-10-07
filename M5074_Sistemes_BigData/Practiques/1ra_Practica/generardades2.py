"""
M5074 - BigData i IA
Activitat: Optimització de Bases de Dades
Part 2A: Generació de dades fake amb Python (versió per a equips amb poca RAM)

    pip install faker pyodbc

Provat a nivell de disseny per a: Python 3.9+, pyodbc 4.0.24+ (recomanat 5.x),
Faker 18+, "ODBC Driver 17/18 for SQL Server", SQL Server 2016 o superior.
"""

import random
import time
from datetime import datetime, timedelta

import pyodbc
from faker import Faker

# ----------------------------------------------------------------------------
# Configuració
# ----------------------------------------------------------------------------
SERVER = '192.168.56.1'
DATABASE = 'VendesBigData'
USUARI = 'alumne'
CONTRASENYA = 'Password123!'

NUM_CLIENTS = 20_000
NUM_PRODUCTES = 2_000
NUM_COMANDES = 200_000

BATCH_SIZE = 1_000        # files per executemany() i per commit
BLOC_ESBORRAT = 50_000    # files per cada DELETE de la reinicialització
MAX_CHARS = 4_000         # límit que es reserva per fila per a columnes (MAX)

# True  -> insercions ràpides (arrays de paràmetres ODBC), amb mides acotades
# False -> insercions fila a fila: més lent, però amb consum de RAM mínim
USAR_FAST_EXECUTEMANY = True

fake = Faker('es_ES')
Faker.seed(42)
random.seed(42)

TIPUS_TEXT = {
    pyodbc.SQL_CHAR, pyodbc.SQL_VARCHAR, pyodbc.SQL_LONGVARCHAR,
    pyodbc.SQL_WCHAR, pyodbc.SQL_WVARCHAR, pyodbc.SQL_WLONGVARCHAR,
}
TIPUS_UNICODE = {pyodbc.SQL_WCHAR, pyodbc.SQL_WVARCHAR, pyodbc.SQL_WLONGVARCHAR}


# ----------------------------------------------------------------------------
# Connexió
# ----------------------------------------------------------------------------
def crear_connexio():
    """Tria el millor driver ODBC instal·lat i obre la connexió."""
    global USAR_FAST_EXECUTEMANY
    instal_lats = pyodbc.drivers()
    driver = next(
        (d for d in ('ODBC Driver 18 for SQL Server',
                     'ODBC Driver 17 for SQL Server',
                     'SQL Server') if d in instal_lats),
        None,
    )
    if driver is None:
        raise RuntimeError(f"No hi ha cap driver ODBC de SQL Server. Trobats: {instal_lats}")

    extra = ''
    if driver == 'ODBC Driver 18 for SQL Server':
        # El driver 18 xifra per defecte; cal acceptar el certificat autosignat
        extra = 'Encrypt=yes;TrustServerCertificate=yes;'
    elif driver == 'SQL Server':
        # Driver antic (2000): fast_executemany hi dona problemes, el desactivem
        print("  AVÍS: driver antic 'SQL Server'. Es desactiva fast_executemany.")
        print("        Instal·la 'ODBC Driver 18 for SQL Server' per anar més ràpid.")
        USAR_FAST_EXECUTEMANY = False

    print(f"Driver ODBC: {driver}")
    return pyodbc.connect(
        f'DRIVER={{{driver}}};SERVER={SERVER};DATABASE={DATABASE};'
        f'UID={USUARI};PWD={CONTRASENYA};{extra}'
    )


# ----------------------------------------------------------------------------
# Insercions amb memòria acotada
# ----------------------------------------------------------------------------
def preparar_insercio(cur_ins, cur_q, taula, columnes):
    """
    Construeix l'INSERT i, en mode ràpid, fixa la mida de cada paràmetre.

    Aquesta és la clau del problema de memòria: amb fast_executemany pyodbc
    reserva un buffer de (files del lot x mida de la columna). Si una columna
    és NVARCHAR(MAX)/VARCHAR(MAX), la mida és enorme i salta MemoryError.
    Amb setinputsizes() li diem la mida real que volem reservar.
    """
    query = (f"INSERT INTO {taula} ({', '.join(columnes)}) "
             f"VALUES ({', '.join('?' * len(columnes))})")

    cur_ins.setinputsizes(None)
    cur_ins.fast_executemany = USAR_FAST_EXECUTEMANY
    if not USAR_FAST_EXECUTEMANY:
        return query

    meta = {f.column_name.lower(): f
            for f in cur_q.columns(table=taula, schema='dbo').fetchall()}
    mides = []
    for col in columnes:
        f = meta[col.lower()]
        mida = f.column_size or 0
        if f.data_type in TIPUS_TEXT:
            tipus = pyodbc.SQL_WVARCHAR if f.data_type in TIPUS_UNICODE else pyodbc.SQL_VARCHAR
            if mida == 0 or mida > MAX_CHARS:      # columnes (MAX)
                mida = MAX_CHARS
            mides.append((tipus, mida, 0))
        else:
            mides.append((f.data_type, mida, f.decimal_digits or 0))
    cur_ins.setinputsizes(mides)
    return query


def inserir(conn, cur_ins, query, files):
    """Insereix una llista de files en lots de BATCH_SIZE, amb commit per lot."""
    global USAR_FAST_EXECUTEMANY
    for i in range(0, len(files), BATCH_SIZE):
        lot = files[i:i + BATCH_SIZE]
        try:
            cur_ins.executemany(query, lot)
        except (MemoryError, pyodbc.Error) as e:
            if not cur_ins.fast_executemany:
                raise
            # Pla B: tornem a provar el lot en mode lent i ja ens hi quedem
            print(f"  AVÍS: el mode ràpid ha fallat ({e}). Es passa al mode lent.")
            conn.rollback()
            USAR_FAST_EXECUTEMANY = False
            cur_ins.fast_executemany = False
            cur_ins.setinputsizes(None)
            cur_ins.executemany(query, lot)
        conn.commit()


# ----------------------------------------------------------------------------
# Reinicialització
# ----------------------------------------------------------------------------
def esborrar_en_blocs(conn, cur, taula):
    """DELETE en blocs petits: evita una transacció gegant i que creixi el log."""
    while True:
        cur.execute(f"DELETE TOP ({BLOC_ESBORRAT}) FROM {taula}")
        esborrades = cur.rowcount
        conn.commit()
        if esborrades < BLOC_ESBORRAT:
            break


def reinicialitzar_bd(conn, cur):
    print("\nReinicialitzant base de dades...")
    # LiniesComanda no és referenciada per cap FK: TRUNCATE és immediat
    cur.execute("TRUNCATE TABLE LiniesComanda")
    conn.commit()
    for taula in ('Comandes', 'Productes', 'Clients',
                  'JerarquiaClients', 'JerarquiaProductes'):
        esborrar_en_blocs(conn, cur, taula)
        cur.execute(f"DBCC CHECKIDENT ('dbo.{taula}', RESEED, 0)")
        conn.commit()
    print("  ✓ Base de dades neta")


def obtenir_ids(cur, query):
    return [fila[0] for fila in cur.execute(query).fetchall()]


# ----------------------------------------------------------------------------
# Generadors
# ----------------------------------------------------------------------------
def generar_jerarquies_productes(conn, cur_ins, cur_q):
    print("\n1. Generant jerarquies de productes...")
    departaments = {
        'Electrònica': ['Ordinadors', 'Telèfons', 'Tauletes', 'Accessoris'],
        'Llar': ['Mobles', 'Decoració', 'Il·luminació', 'Tèxtil'],
        'Moda': ['Roba Home', 'Roba Dona', 'Calçat', 'Complements'],
        'Esports': ['Fitness', 'Ciclisme', 'Outdoor', 'Natació'],
        'Llibres': ['Novel·la', 'Tècnic', 'Infantil', 'Comics'],
    }
    subcategories = ['Premium', 'Estàndard', 'Econòmic', 'Oferta']
    files = [(dept, cat, sub, 1)
             for dept, cats in departaments.items()
             for cat in cats
             for sub in subcategories]
    query = preparar_insercio(cur_ins, cur_q, 'JerarquiaProductes',
                              ['Nivell1', 'Nivell2', 'Nivell3', 'Actiu'])
    inserir(conn, cur_ins, query, files)
    print(f"  ✓ {len(files)} jerarquies de productes creades")


def generar_jerarquies_clients(conn, cur_ins, cur_q):
    print("\n2. Generant jerarquies de clients...")
    files = [
        ('Particular', 'Premium', 'VIP', 1),
        ('Particular', 'Premium', 'Gold', 1),
        ('Particular', 'Estàndard', 'Silver', 1),
        ('Particular', 'Estàndard', 'Regular', 1),
        ('Particular', 'Bàsic', 'Nou', 1),
        ('Empresa', 'Gran Empresa', 'Nacional', 1),
        ('Empresa', 'Gran Empresa', 'Internacional', 1),
        ('Empresa', 'PIME', 'Mitjana', 1),
        ('Empresa', 'PIME', 'Petita', 1),
        ('Empresa', 'Autònom', 'Professional', 1),
    ]
    query = preparar_insercio(cur_ins, cur_q, 'JerarquiaClients',
                              ['Nivell1', 'Nivell2', 'Nivell3', 'Actiu'])
    inserir(conn, cur_ins, query, files)
    print(f"  ✓ {len(files)} jerarquies de clients creades")


def generar_clients(conn, cur_ins, cur_q, num_clients):
    print(f"\n3. Generant {num_clients:,} clients...")
    inici = time.time()
    provincies = ['Barcelona', 'Madrid', 'València', 'Sevilla', 'Saragossa',
                  'Màlaga', 'Múrcia', 'Palma', 'Bilbao', 'Alacant']
    jerarquia_ids = obtenir_ids(cur_q, "SELECT JerarquiaClientID FROM JerarquiaClients")
    query = preparar_insercio(cur_ins, cur_q, 'Clients', [
        'CodiClient', 'NomClient', 'Email', 'Telefon', 'Direccio', 'Poblacio',
        'CodiPostal', 'Provincia', 'Pais', 'JerarquiaClientID', 'Actiu'])

    for start in range(0, num_clients, BATCH_SIZE):
        end = min(start + BATCH_SIZE, num_clients)
        lot = [(
            f"CLI-{i + 1:08d}",
            fake.company() if random.random() > 0.7 else fake.name(),
            fake.email(),
            fake.phone_number(),
            fake.street_address(),
            fake.city(),
            fake.postcode(),
            random.choice(provincies),
            'Espanya',
            random.choice(jerarquia_ids),
            1,
        ) for i in range(start, end)]
        inserir(conn, cur_ins, query, lot)
        print(f"  Processats {end:,}/{num_clients:,}")

    t = time.time() - inici
    print(f"  ✓ Completat en {t:.2f} s ({num_clients / t:.0f} reg/s)")


def generar_productes(conn, cur_ins, cur_q, num_productes):
    print(f"\n4. Generant {num_productes:,} productes...")
    inici = time.time()
    prefixos = ['Pro', 'Super', 'Mega', 'Ultra', 'Max', 'Premium', 'Elite', 'Smart']
    sufixos = ['Plus', 'Pro', 'Advanced', 'Deluxe', 'Standard', 'Basic', 'Lite']
    jerarquia_ids = obtenir_ids(cur_q, "SELECT JerarquiaProducteID FROM JerarquiaProductes")
    query = preparar_insercio(cur_ins, cur_q, 'Productes', [
        'CodiProducte', 'NomProducte', 'Descripcio', 'JerarquiaProducteID',
        'PreuUnitari', 'Cost', 'StockActual', 'Actiu'])

    for start in range(0, num_productes, BATCH_SIZE):
        end = min(start + BATCH_SIZE, num_productes)
        lot = []
        for i in range(start, end):
            preu = round(random.uniform(5, 2000), 2)
            lot.append((
                f"PROD-{i + 1:08d}",
                f"{random.choice(prefixos)} {fake.word().capitalize()} {random.choice(sufixos)}",
                fake.text(max_nb_chars=200),
                random.choice(jerarquia_ids),
                preu,
                round(preu * random.uniform(0.4, 0.7), 2),
                random.randint(0, 1000),
                1,
            ))
        inserir(conn, cur_ins, query, lot)
        print(f"  Processats {end:,}/{num_productes:,}")

    t = time.time() - inici
    print(f"  ✓ Completat en {t:.2f} s ({num_productes / t:.0f} reg/s)")


def generar_comandes_i_linies(conn, cur_ins, cur_q, num_comandes):
    """
    Treballa bloc a bloc (BATCH_SIZE comandes): genera les línies, calcula
    l'import de cada comanda, insereix les comandes ja amb l'import correcte,
    recupera els ComandaID reals i insereix les línies. Així:
      - mai hi ha més d'un bloc a la RAM de Python
      - no cal l'UPDATE massiu final (una sola transacció de 200K files)
      - no se suposa que els ComandaID van d'1 a N
    """
    print(f"\n5. Generant {num_comandes:,} comandes amb línies...")
    inici = time.time()

    estats = ['Pendent', 'Processat', 'Enviat', 'Entregat', 'Cancel·lat']
    pesos_estats = [0.05, 0.10, 0.15, 0.65, 0.05]
    # Sense microsegons: evita errors de precisió si la columna és DATETIME
    data_inici = datetime.now().replace(microsecond=0) - timedelta(days=3 * 365)

    client_ids = obtenir_ids(cur_q, "SELECT ClientID FROM Clients")
    producte_ids = obtenir_ids(cur_q, "SELECT ProducteID FROM Productes")

    cols_comandes = ['NumeroComanda', 'ClientID', 'DataComanda', 'DataEnviament',
                     'DataEntrega', 'Estat', 'ImportTotal', 'Descompte', 'ImportNet']
    cols_linies = ['ComandaID', 'NumeroLinia', 'ProducteID', 'Quantitat',
                   'PreuUnitari', 'Descompte', 'ImportLinia']

    darrer_id = cur_q.execute("SELECT ISNULL(MAX(ComandaID), -1) FROM Comandes").fetchone()[0]
    total_linies = 0

    for start in range(0, num_comandes, BATCH_SIZE):
        end = min(start + BATCH_SIZE, num_comandes)
        comandes = []
        linies_per_numero = {}

        for i in range(start, end):
            num_comanda = f"COM-{i + 1:010d}"
            data_comanda = data_inici + timedelta(days=random.randint(0, 3 * 365))
            estat = random.choices(estats, weights=pesos_estats)[0]
            data_enviament = (data_comanda + timedelta(days=random.randint(1, 5))
                              if estat in ('Enviat', 'Entregat') else None)
            data_entrega = (data_enviament + timedelta(days=random.randint(1, 3))
                            if estat == 'Entregat' else None)

            linies = []
            total = 0.0
            for num_linia in range(1, random.randint(1, 8) + 1):
                quantitat = random.randint(1, 10)
                preu = round(random.uniform(10, 500), 2)
                descompte = random.choice([0, 0, 0, 5, 10, 15])
                import_linia = round(quantitat * preu * (1 - descompte / 100), 2)
                total += import_linia
                linies.append((num_linia, random.choice(producte_ids), quantitat,
                               preu, descompte, import_linia))
            total = round(total, 2)
            linies_per_numero[num_comanda] = linies
            comandes.append((num_comanda, random.choice(client_ids), data_comanda,
                             data_enviament, data_entrega, estat, total, 0, total))

        # 1) Comandes del bloc
        query = preparar_insercio(cur_ins, cur_q, 'Comandes', cols_comandes)
        inserir(conn, cur_ins, query, comandes)

        # 2) ComandaID reals del bloc (cerca per clau primària, no escaneja la taula)
        files_linies = []
        for comanda_id, numero in cur_q.execute(
                "SELECT ComandaID, NumeroComanda FROM Comandes WHERE ComandaID > ?",
                darrer_id).fetchall():
            darrer_id = max(darrer_id, comanda_id)
            for linia in linies_per_numero[numero]:
                files_linies.append((comanda_id,) + linia)

        # 3) Línies del bloc
        query = preparar_insercio(cur_ins, cur_q, 'LiniesComanda', cols_linies)
        inserir(conn, cur_ins, query, files_linies)
        total_linies += len(files_linies)

        if end % (BATCH_SIZE * 10) == 0 or end == num_comandes:
            print(f"  Processades {end:,}/{num_comandes:,} comandes "
                  f"({total_linies:,} línies)")

    t = time.time() - inici
    print(f"  ✓ Completat en {t:.2f} s")
    print(f"    - {num_comandes:,} comandes creades")
    print(f"    - {total_linies:,} línies creades")


# ----------------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("GENERADOR DE DADES MASSIVES - VendesBigData (poca RAM)")
    print("=" * 60)

    conn = crear_connexio()
    cur_q = conn.cursor()     # consultes i DDL
    cur_ins = conn.cursor()   # només insercions (té les mides de paràmetres)
    print("Connexió establerta amb SQL Server")

    try:
        reinicialitzar_bd(conn, cur_q)

        cur_q.execute("ALTER TABLE LiniesComanda NOCHECK CONSTRAINT ALL")
        cur_q.execute("ALTER TABLE Comandes NOCHECK CONSTRAINT ALL")
        conn.commit()
        try:
            generar_jerarquies_productes(conn, cur_ins, cur_q)
            generar_jerarquies_clients(conn, cur_ins, cur_q)
            generar_clients(conn, cur_ins, cur_q, NUM_CLIENTS)
            generar_productes(conn, cur_ins, cur_q, NUM_PRODUCTES)
            generar_comandes_i_linies(conn, cur_ins, cur_q, NUM_COMANDES)
        finally:
            # WITH CHECK revalida les dades: les FK queden "trusted" i
            # l'optimitzador les pot fer servir als plans d'execució
            print("\nRehabilitant constraints...")
            conn.rollback()
            cur_q.execute("ALTER TABLE LiniesComanda WITH CHECK CHECK CONSTRAINT ALL")
            cur_q.execute("ALTER TABLE Comandes WITH CHECK CHECK CONSTRAINT ALL")
            conn.commit()

        print("\n" + "=" * 60)
        print("GENERACIÓ COMPLETADA!")
        print("=" * 60)
        for etiqueta, taula in (('Clients', 'Clients'), ('Productes', 'Productes'),
                                ('Comandes', 'Comandes'), ('Línies comanda', 'LiniesComanda')):
            n = cur_q.execute(f"SELECT COUNT(*) FROM {taula}").fetchone()[0]
            print(f"{etiqueta}: {n:,}")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()