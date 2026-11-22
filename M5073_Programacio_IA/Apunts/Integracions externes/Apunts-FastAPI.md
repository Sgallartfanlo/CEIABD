# APUNTS EXTENSOS — FastAPI, Pydantic, Pandas i API del Titanic
---

## 1. Objectiu i mapa conceptual

Els dos fitxers expliquen una progressió natural: **crear una API mínima amb FastAPI** i, després, **construir una API de consulta i gestió de dades del Titanic**. La primera guia mostra com preparar un projecte amb `uv`, crear `FastAPI()` i definir tres rutes. La segona introdueix un CSV, un `DataFrame`, models de validació, filtres, paginació, estadístiques i operacions d'escriptura.

```text
Client (navegador / Swagger UI / curl)
             |
             | petició HTTP
             v
        Aplicació FastAPI
             |
     +-------+--------+
     |                |
  Pydantic          Endpoints
  validació        GET / POST / DELETE
                      |
                      v
                 Pandas DataFrame
                      |
                      v
                 titanic3.csv
          (carregat a l'inici; canvis en RAM)
```

**Idea fonamental:** FastAPI s'encarrega de publicar rutes HTTP i validar les entrades; Pandas s'encarrega de les dades tabulars. La llista d'usuaris de la primera guia i el `DataFrame` de la segona són exemples d'emmagatzematge en memòria, no pas bases de dades persistents.

### Què s'aprèn?

- Diferenciar rutes, paràmetres de ruta, paràmetres de consulta i cos JSON.
- Crear serveis amb `GET`, `POST` i `DELETE`.
- Validar dades amb `BaseModel`, `Field` i `Query`.
- Filtrar, paginar, seleccionar i agregar registres amb Pandas.
- Utilitzar errors HTTP adequats i entendre la documentació automàtica.
- Identificar límits d'una API acadèmica abans de desplegar-la.

## 2. Què és una API REST i què és FastAPI?

Una **API** (Application Programming Interface) defineix com poden comunicar-se diferents programes. En una API web, un client envia una petició HTTP a un servidor i rep una resposta, habitualment representada en JSON.

**REST** és un estil d'arquitectura per organitzar recursos accessibles mitjançant URL. En els exemples, `/users/` representa una col·lecció d'usuaris i `/passatgers` representa la col·lecció de passatgers. FastAPI és un framework de Python per crear interfícies HTTP, amb suport per a anotacions de tipus, validació i documentació OpenAPI.

No s'ha de confondre FastAPI amb Pandas: **FastAPI serveix dades; Pandas les processa**. Pydantic comprova si un objecte d'entrada s'ajusta a un esquema.

## 3. HTTP, JSON, rutes i codis de resposta

| Element | Significat | Exemple en els fitxers |
|---|---|---|
| `GET` | Consultar un recurs | `GET /passatgers` |
| `POST` | Crear un recurs | `POST /passatgers` |
| `DELETE` | Eliminar un recurs | `DELETE /passatgers/3` |
| Path parameter | Valor dins la ruta | `passatger_id` a `/passatgers/{passatger_id}` |
| Query parameter | Valor després de `?` | `?skip=0&limit=10` |
| Body | Objecte enviat al cos de la petició | JSON d'un passatger nou |
| JSON | Format de comunicació | `{"missatge":"Hola"}` |

**Codis que cal dominar:** `200 OK` indica una consulta correcta; `201 Created`, que s'ha creat un recurs; `404 Not Found`, que no s'ha trobat; `422`, que FastAPI no ha pogut validar correctament una petició; `500`, un error intern del servidor. Un `DELETE` en el codi original no especifica un codi especial, per tant retorna `200` quan acaba correctament.

## 4. Eines del projecte

| Eina | Funció |
|---|---|
| Python | Llenguatge amb què s'escriu el servidor |
| `uv` | Inicialització del projecte i instal·lació de dependències |
| FastAPI | Aplicació HTTP i definició d'endpoints |
| Pydantic | Models i validació de valors |
| Pandas | Càrrega del CSV i tractament del DataFrame |
| NumPy | Gestió de `np.nan` a la guia del Titanic |
| Jupyter / Colab | Entorn on es van redactar els scripts originals |
| `TestClient` | Eina importada al segon script per fer proves, però no usada en les rutes mostrades |

`json` també s'importa al script Titanic, però no hi ha cap crida explícita a `json.dumps` o `json.loads` en el codi compartit.

## 5. Instal·lació de FastAPI a Windows amb `uv`

### 5.1 Instal·lar `uv`

La guia inicial proposa executar **PowerShell**:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv -V
```

- `irm` descarrega el contingut de l'URL (`Invoke-RestMethod`).
- `iex` executa el contingut retornat (`Invoke-Expression`).
- `-ExecutionPolicy ByPass` modifica la política d'execució per a aquest procés.
- `uv -V` comprova que l'ordre està disponible.

**Precaució addicional:** executar directament un script remot comporta riscos. En entorns administrats, revisa'n l'origen i les polítiques abans d'executar-lo.

### 5.2 Crear el projecte

```powershell
uv init nom-projecte --bare
cd nom-projecte
uv add "fastapi[standard-no-fastapi-cloud-cli]"
```

`uv init` inicialitza un projecte; `--bare` crea una estructura mínima; `cd` canvia el directori; `uv add` registra i instal·la la dependència. El nom exacte de l'extra s'ha conservat tal com apareix al fitxer. Si un entorn o una versió no el reconeix, cal revisar les dependències admeses per la versió instal·lada.

### 5.3 Arrencar el servidor

La guia indica:

```powershell
uv run fastapi dev
```

Aquesta ordre executa el servidor en mode de desenvolupament, amb recàrrega automàtica quan es detecten canvis de codi, sempre que l'aplicació es descobreixi correctament. En una pràctica real pots haver d'especificar explícitament el mòdul, per exemple `uv run fastapi dev main.py` si l'aplicació és al fitxer `main.py`.

## 6. Primera API: rutes i paràmetres

### 6.1 Codi original de `guia_fastapi.py`

```python
from fastapi import FastAPI

app = FastAPI()

user = [{"name": "user1"}, {"name": "user2"}]

@app.get("/")
async def root():
    '''Ruta arrel'''
    return {"message": "Hello World"}

@app.get("/users/")
async def read_user():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user_id(user_id: int):
    return user[user_id - 1]
```

### 6.2 Desglossament

**`app = FastAPI()`** crea l'objecte que conté les rutes. **`@app.get("/")`** registra la funció `root()` com a resposta a `GET /`. **`async def`** declara una funció asíncrona, tot i que en aquests exemples no hi ha operacions `await`. **`user_id: int`** demana que el paràmetre es validi com a enter. **`user[user_id - 1]`** adapta els identificadors humans 1, 2... als índexs de llista 0, 1...

| Petició | Comportament del codi |
|---|---|
| `GET /` | Retorna `{"message": "Hello World"}` |
| `GET /users/` | Retorna literalment `{"user_id": "the current user"}`; no retorna tota la llista |
| `GET /users/1` | Retorna `{"name": "user1"}` |
| `GET /users/2` | Retorna `{"name": "user2"}` |
| `GET /users/3` | Accedeix fora de la llista i pot causar un error intern |
| `GET /users/abc` | Validació incorrecta del tipus enter; resposta `422` |

**Atenció:** el nom `read_user()` i el comentari de la guia poden suggerir un llistat d'usuaris, però el codi retorna un missatge fix. Igualment, la ruta per ID no implementa comprovació de límits. Són limitacions reals de l'exemple, no comportaments que hàgim de donar per implementats.

### 6.3 Millora opcional (no forma part del codi original)

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def consultar_usuari(user_id: int):
    if user_id < 1 or user_id > len(user):
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return user[user_id - 1]
```

Aquesta versió evita que un índex invàlid acabi com una excepció no controlada. S'hauria d'utilitzar **en substitució** de la ruta anterior amb el mateix camí, no registrar-les totes dues en la mateixa aplicació.

## 7. Proves amb navegador i documentació automàtica

Amb el servidor local en marxa, els URL habituals de desenvolupament són:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/users/1
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

`/docs` ofereix la interfície interactiva de Swagger UI i `/redoc` presenta la documentació alternativa. En aquestes pàgines es poden consultar mètodes, paràmetres i esquemes, i llançar proves de peticions. El port `8000` és el que acostuma a utilitzar el servidor de desenvolupament, però pot variar.

## 8. Del primer exemple al projecte Titanic

La segona guia passa d'una llista curta a un dataset tabular: `titanic3.csv`. A més de les rutes, incorpora tractament de valors nuls, filtres, paginació i agregacions. També es poden crear i eliminar files del DataFrame.

**Diferència essencial:** una variable global és compartida durant la vida del procés. En reiniciar l'aplicació, es torna a carregar el CSV original i els canvis que només s'han fet al DataFrame no es conserven automàticament.

## 9. Dataset `titanic3.csv` i càrrega amb Pandas

### Codi original

```python
import pandas as pd
import numpy as np
import json
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query
from fastapi.testclient import TestClient

DATASET_PATH = '/workspace/knowledge/titanic3.csv'
df_titanic = pd.read_csv(DATASET_PATH)
df_titanic = df_titanic.replace({np.nan: None})

print(f"Dataset carregat correctament amb {len(df_titanic)} passatgers i {len(df_titanic.columns)} columnes.")
df_titanic.head(3)
```

**`pd.read_csv`** llegeix les files del CSV i construeix un `DataFrame`; **`len(df_titanic)`** retorna les files; **`len(df_titanic.columns)`** retorna el nombre de columnes; **`head(3)`** consulta els tres primers registres. La crida `head(3)` sense `print` és útil en notebooks, perquè Jupyter en visualitza el resultat; en un script normal no imprimeix cap taula automàticament.

La ruta `/workspace/knowledge/titanic3.csv` pertany a l'entorn d'origen de la pràctica. Per executar-la en un altre equip, cal substituir-la per la ubicació real del dataset. Aquest CSV **no està inclòs** entre els dos fitxers `.py` aportats.

### Camps principals que utilitza l'API

| Camp | Tipus esperat | Funció |
|---|---|---|
| `pclass` | Enter entre 1 i 3 | Classe del passatger |
| `survived` | Enter 0 o 1 | Indicador de supervivència |
| `name` | Text | Nom complet |
| `sex` | Text | Sexe |
| `age` | Real opcional | Edat |
| `sibsp`, `parch` | Enter ≥ 0 | Familiars a bord |
| `ticket` | Text opcional | Número de bitllet |
| `fare` | Real opcional | Preu del bitllet |
| `cabin`, `embarked` | Text opcional | Cabina i port d'embarcament |

La guia assumeix que el CSV té com a mínim les columnes que utilitzen les rutes (`survived`, `pclass`, `sex`, `name`, `age`, `fare`). Si falten, s'hauran d'ajustar els endpoints.

## 10. Valors nuls i serialització JSON

Un `NaN` és habitual en dades numèriques de Pandas, però no és un valor JSON estàndard. En canvi, Python `None` se sol serialitzar com `null`.

### Intenció del fitxer original

```python
df_titanic = df_titanic.replace({np.nan: None})
```

Aquesta instrucció intenta substituir els valors absents. **Matís important:** segons el tipus de columna i les operacions posteriors, Pandas pot conservar o tornar a produir `NaN`/`NaT`; per tant, una única substitució inicial no garanteix per si sola que tots els resultats siguin serialitzables en JSON estricte.

**Millora conceptual:** revisar els nuls després de construir els registres i convertir-los a tipus compatibles abans de retornar-los. És especialment rellevant en endpoints que utilitzen `to_dict(orient="records")`.

## 11. Inicialització i metadades de l'API Titanic

### Codi original

```python
app = FastAPI(
    title="API RESTful del Titanic",
    description="API interactiva per consultar i gestionar passatgers del Titanic",
    version="1.0.0"
)

@app.get("/", tags=["General"])
def inici():
    return {
        "missatge": "Benvingut/da a l'API del Titanic!",
        "total_passatgers": len(df_titanic),
        "documentacio_interactiva": "/docs"
    }
```

A diferència del primer exemple, aquesta aplicació incorpora títol, descripció i versió, que apareixen a la documentació. L'etiqueta `tags=["General"]` agrupa visualment la ruta. El recompte de passatgers és dinàmic respecte al DataFrame que hi hagi en memòria en aquell moment.

## 12. Model `PassatgerCreate` amb Pydantic

### Codi original

```python
class PassatgerCreate(BaseModel):
    pclass: int = Field(..., ge=1, le=3, description="Classe del passatger (1, 2 o 3)")
    survived: int = Field(..., ge=0, le=1, description="Supervivència (0 = Mort, 1 = Supervivent)")
    name: str = Field(..., description="Nom complet del passatger")
    sex: str = Field(..., description="Sexe ('female' o 'male')")
    age: Optional[float] = Field(None, ge=0, description="Edat en anys")
    sibsp: int = Field(0, ge=0, description="Nombre de germans/cònjocs a bord")
    parch: int = Field(0, ge=0, description="Nombre de pares/fills a bord")
    ticket: Optional[str] = None
    fare: Optional[float] = Field(None, ge=0, description="Preu del bitllet")
    cabin: Optional[str] = None
    embarked: Optional[str] = Field(None, description="Port d'embarcament (C, Q, S)")
```

### Significat de la sintaxi

| Expressió | Interpretació |
|---|---|
| `BaseModel` | Classe base per definir un esquema |
| `Field(...)` | Camp obligatori, sense valor per defecte |
| `ge=1` | Valor major o igual que 1 |
| `le=3` | Valor menor o igual que 3 |
| `Field(0, ge=0)` | Si s'omet, pren zero; no accepta negatius |
| `Optional[float] = None` | Pot faltar o ser `null` |
| `description=...` | Documentació descriptiva del camp |

**Exemple vàlid:**

```json
{
  "pclass": 2,
  "survived": 1,
  "name": "Exemple de Passatger",
  "sex": "female",
  "age": 28,
  "sibsp": 0,
  "parch": 1,
  "fare": 25.5
}
```

Els camps `ticket`, `cabin` i `embarked` es poden ometre. **Exemple invàlid:** `{"pclass": 5, "survived": 4, "name": "X", "sex": "male"}`, perquè `pclass` i `survived` queden fora dels rangs permesos.

**Precisió important:** el codi comenta que `sex` ha de ser `female` o `male` i `embarked` ha de ser `C`, `Q` o `S`, però **no defineix cap restricció efectiva sobre aquestes cadenes**; Pydantic només exigeix que `sex` sigui un text i permet qualsevol text per a `embarked`. Per validar els valors concrets caldria afegir `Literal` o validacions personalitzades.

## 13. `GET /passatgers`: filtres i paginació

### Codi original

```python
@app.get("/passatgers", tags=["Passatgers"])
def llistar_passatgers(
    skip: int = Query(0, ge=0, description="Nombre de registres a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Nombre màxim de registres a retornar"),
    survived: Optional[int] = Query(None, ge=0, le=1, description="Filtrar per supervivència (0 o 1)"),
    pclass: Optional[int] = Query(None, ge=1, le=3, description="Filtrar per classe (1, 2 o 3)"),
    sex: Optional[str] = Query(None, description="Filtrar per sexe ('male' o 'female')"),
    search: Optional[str] = Query(None, description="Cerca textual pel nom")
):
    filtered = df_titanic.copy()

    if survived is not None:
        filtered = filtered[filtered['survived'] == survived]
    if pclass is not None:
        filtered = filtered[filtered['pclass'] == pclass]
    if sex:
        filtered = filtered[filtered['sex'].astype(str).str.lower() == sex.lower()]
    if search:
        filtered = filtered[filtered['name'].astype(str).str.contains(search, case=False, na=False)]

    total_coincidencies = len(filtered)
    resultats = filtered.iloc[skip : skip + limit].to_dict(orient="records")

    return {
        "total_coincidencies": total_coincidencies,
        "skip": skip,
        "limit": limit,
        "resultats": resultats
    }
```

### Com funciona?

1. FastAPI valida els paràmetres de la URL.
2. `copy()` crea un DataFrame separat per aplicar filtres sense modificar el global.
3. Cada `if` filtra les dades si el paràmetre existeix.
4. `len(filtered)` calcula el total de coincidències **abans** de paginar.
5. `iloc[skip:skip+limit]` recupera una finestra de files.
6. `to_dict(orient="records")` transforma les files en una llista de diccionaris.

### Exemples d'URL

```text
GET /passatgers
GET /passatgers?skip=20&limit=10
GET /passatgers?survived=1
GET /passatgers?pclass=1&survived=1
GET /passatgers?sex=female&search=Smith
```

`?limit=0` o `?limit=150` incompleix els límits i rep una resposta de validació. El filtre de nom empra `str.contains`; per defecte interpreta el patró com una expressió regular, cosa que cal tenir en compte si l'usuari escriu caràcters especials.

**Diferència clau:** `total_coincidencies` no és necessàriament igual al nombre de registres dins `resultats`, perquè el segon nombre està limitat per la paginació.

## 14. `GET /passatgers/{passatger_id}`: rutes i errors

### Codi original

```python
@app.get("/passatgers/{passatger_id}", tags=["Passatgers"])
def detall_passatger(passatger_id: int):
    if passatger_id < 0 or passatger_id >= len(df_titanic):
        raise HTTPException(
            status_code=404,
            detail=f"El passatger amb ID {passatger_id} no s'ha trobat a la base de dades."
        )

    passatger = df_titanic.iloc[passatger_id].to_dict()
    return {"passatger_id": passatger_id, "dades": passatger}
```

Aquesta ruta considera l'ID com la **posició actual de la fila**, començant per 0. `iloc` selecciona per posició i `HTTPException` genera el `404` quan el valor és negatiu o supera la llargada del DataFrame. No hi ha cap columna de clau primària estable associada a aquest ID.

**Exemples:** `/passatgers/0` selecciona la primera fila; `/passatgers/abc` incompleix el tipus `int`; un índex superior al nombre de files provoca `404`.

## 15. `GET /estadistiques`: analítica amb Pandas

### Codi original

```python
@app.get("/estadistiques", tags=["Analítica"])
def obtenir_estadistiques():
    total = len(df_titanic)
    supervivents = int(df_titanic['survived'].sum())

    sexe_stats = {}
    for s in ['female', 'male']:
        sub = df_titanic[df_titanic['sex'] == s]
        tot_s = len(sub)
        sup_s = int(sub['survived'].sum())
        sexe_stats[s] = {
            "total": tot_s,
            "supervivents": sup_s,
            "percentatge_supervivencia": round((sup_s / tot_s * 100), 2) if tot_s > 0 else 0
        }

    return {
        "total_passatgers": total,
        "total_supervivents": supervivents,
        "taxa_supervivencia_global_pct": round((supervivents / total * 100), 2),
        "edat_mitjana_anys": round(float(df_titanic['age'].dropna().mean()), 2),
        "preu_mitja_bitllet": round(float(df_titanic['fare'].dropna().mean()), 2),
        "supervivencia_per_sexe": sexe_stats
    }
```

### Formules

- **Supervivents** = suma de la columna `survived`, si els valors són 0 i 1.
- **Taxa global (%)** = `(supervivents / total) × 100`.
- **Mitjana d'edat** = mitjana de valors no nuls de `age`.
- **Preu mitjà** = mitjana de valors no nuls de `fare`.
- **Taxa per sexe (%)** = `(supervivents del grup / passatgers del grup) × 100`.

La funció `round(x, 2)` mostra dos decimals. La condició `if tot_s > 0 else 0` evita dividir per zero en els grups sense passatgers.

**Diferència entre descripció i codi:** el text inicial del segon script menciona percentatges desglossats per sexe **i classe**, però el codi compartit **només calcula el desglossament per sexe**. Les estadístiques per classe serien una ampliació addicional.

**Limitació:** si `df_titanic` és buit, la divisió global `supervivents / total` pot fallar. Si totes les edats o tarifes són nul·les, les mitjanes poden ser `NaN` i requerir tractament per servir-les com a JSON.

## 16. `POST /passatgers`: inserció de passatgers

### Codi original

```python
@app.post("/passatgers", status_code=201, tags=["Passatgers"])
def crear_passatger(passatger: PassatgerCreate):
    global df_titanic
    nou_dict = passatger.dict()
    df_titanic = pd.concat([df_titanic, pd.DataFrame([nou_dict])], ignore_index=True)
    nou_id = len(df_titanic) - 1
    return {
        "missatge": "Passatger afegit amb èxit",
        "passatger_id": nou_id,
        "dades": nou_dict
    }
```

**Flux:** FastAPI rep un JSON, Pydantic el valida i el converteix en `PassatgerCreate`; `.dict()` en crea el diccionari; `pd.DataFrame([nou_dict])` converteix el registre en una fila; `pd.concat` l'afegeix al DataFrame; `ignore_index=True` renumera l'índex; la resposta mostra l'ID posicional de la nova fila.

**Nota de compatibilitat:** `.dict()` apareix al codi original. En Pydantic v2 es prefereix `.model_dump()`; el canvi seria una actualització, no una transcripció literal.

**Limitació:** no s'escriu res sobre `titanic3.csv`. L'alta es perd si es reinicia el procés. Si el CSV té columnes addicionals que no apareixen al model, el nou registre tindrà valors absents en aquestes columnes.

## 17. `DELETE /passatgers/{passatger_id}`: eliminació

### Codi original

```python
@app.delete("/passatgers/{passatger_id}", tags=["Passatgers"])
def eliminar_passatger(passatger_id: int):
    global df_titanic
    if passatger_id < 0 or passatger_id >= len(df_titanic):
        raise HTTPException(status_code=404, detail="Passatger no trobat")

    df_titanic = df_titanic.drop(index=passatger_id).reset_index(drop=True)
    return {"missatge": f"Passatger amb ID {passatger_id} eliminat correctament."}
```

**Com funciona:** comprova que el número és vàlid, elimina la fila que té l'índex indicat i reconstrueix l'índex amb `reset_index(drop=True)`.

**Risc principal:** els IDs canvien després d'una eliminació. Si elimines l'índex `1`, la fila que abans ocupava l'índex `2` passa a ocupar l'índex `1`. Per això aquests IDs no s'han d'utilitzar com a identificadors persistents d'una API real.

## 18. Resum de tots els endpoints

| Endpoint | Mètode | Dades d'entrada | Resposta principal |
|---|---|---|---|
| `/` | GET | Cap | Missatge i total de passatgers |
| `/passatgers` | GET | `skip`, `limit`, `survived`, `pclass`, `sex`, `search` | Total de coincidències i llista paginada |
| `/passatgers/{passatger_id}` | GET | Identificador posicional | Dades del passatger o error 404 |
| `/estadistiques` | GET | Cap | Supervivència, edat, tarifa i estadístiques per sexe |
| `/passatgers` | POST | JSON validat per `PassatgerCreate` | Alta i ID posicional, amb 201 |
| `/passatgers/{passatger_id}` | DELETE | Identificador posicional | Missatge de confirmació o 404 |

La guia inicial també defineix `/`, `/users/` i `/users/{user_id}`, però forma una aplicació **diferent** i no s'han d'atribuir aquestes rutes a l'API del Titanic si no s'han afegit al seu codi.

## 19. Flux complet d'una petició HTTP

```text
Exemple: GET /passatgers?pclass=1&survived=1&skip=0&limit=5

1. El client envia la URL.
2. FastAPI identifica @app.get('/passatgers').
3. Query valida pclass=1, survived=1, skip=0, limit=5.
4. Pandas crea una còpia del DataFrame.
5. Es filtren passatgers de primera classe i supervivents.
6. Es compten totes les coincidències.
7. S'agafen les primeres 5 files amb iloc.
8. Les files es transformen a diccionaris.
9. FastAPI retorna la resposta HTTP en JSON.
```

Per a un `POST`, el pas 3 és la validació del **cos JSON amb Pydantic** i el pas 5 consisteix a concatenar una fila al DataFrame.

## 20. Codi de referència de l'API del Titanic

El bloc següent reuneix les parts executables del segon fitxer en l'ordre en què apareixen. És una **reproducció reorganitzada**, no una versió corregida o una API provada amb el dataset, que no està adjunt.

```python
import pandas as pd
import numpy as np
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query

DATASET_PATH = '/workspace/knowledge/titanic3.csv'
df_titanic = pd.read_csv(DATASET_PATH)
df_titanic = df_titanic.replace({np.nan: None})

app = FastAPI(
    title="API RESTful del Titanic",
    description="API interactiva per consultar i gestionar passatgers del Titanic",
    version="1.0.0"
)

class PassatgerCreate(BaseModel):
    pclass: int = Field(..., ge=1, le=3)
    survived: int = Field(..., ge=0, le=1)
    name: str
    sex: str
    age: Optional[float] = Field(None, ge=0)
    sibsp: int = Field(0, ge=0)
    parch: int = Field(0, ge=0)
    ticket: Optional[str] = None
    fare: Optional[float] = Field(None, ge=0)
    cabin: Optional[str] = None
    embarked: Optional[str] = None

@app.get("/", tags=["General"])
def inici():
    return {
        "missatge": "Benvingut/da a l'API del Titanic!",
        "total_passatgers": len(df_titanic),
        "documentacio_interactiva": "/docs"
    }

@app.get("/passatgers", tags=["Passatgers"])
def llistar_passatgers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    survived: Optional[int] = Query(None, ge=0, le=1),
    pclass: Optional[int] = Query(None, ge=1, le=3),
    sex: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    filtered = df_titanic.copy()
    if survived is not None:
        filtered = filtered[filtered['survived'] == survived]
    if pclass is not None:
        filtered = filtered[filtered['pclass'] == pclass]
    if sex:
        filtered = filtered[filtered['sex'].astype(str).str.lower() == sex.lower()]
    if search:
        filtered = filtered[filtered['name'].astype(str).str.contains(search, case=False, na=False)]
    total_coincidencies = len(filtered)
    resultats = filtered.iloc[skip:skip + limit].to_dict(orient="records")
    return {
        "total_coincidencies": total_coincidencies,
        "skip": skip,
        "limit": limit,
        "resultats": resultats
    }

@app.get("/passatgers/{passatger_id}", tags=["Passatgers"])
def detall_passatger(passatger_id: int):
    if passatger_id < 0 or passatger_id >= len(df_titanic):
        raise HTTPException(status_code=404, detail="Passatger no trobat")
    return {
        "passatger_id": passatger_id,
        "dades": df_titanic.iloc[passatger_id].to_dict()
    }

@app.get("/estadistiques", tags=["Analítica"])
def obtenir_estadistiques():
    total = len(df_titanic)
    supervivents = int(df_titanic['survived'].sum())
    sexe_stats = {}
    for s in ['female', 'male']:
        sub = df_titanic[df_titanic['sex'] == s]
        tot_s = len(sub)
        sup_s = int(sub['survived'].sum())
        sexe_stats[s] = {
            "total": tot_s,
            "supervivents": sup_s,
            "percentatge_supervivencia": round((sup_s / tot_s * 100), 2) if tot_s > 0 else 0
        }
    return {
        "total_passatgers": total,
        "total_supervivents": supervivents,
        "taxa_supervivencia_global_pct": round((supervivents / total * 100), 2),
        "edat_mitjana_anys": round(float(df_titanic['age'].dropna().mean()), 2),
        "preu_mitja_bitllet": round(float(df_titanic['fare'].dropna().mean()), 2),
        "supervivencia_per_sexe": sexe_stats
    }

@app.post("/passatgers", status_code=201, tags=["Passatgers"])
def crear_passatger(passatger: PassatgerCreate):
    global df_titanic
    nou_dict = passatger.dict()
    df_titanic = pd.concat([df_titanic, pd.DataFrame([nou_dict])], ignore_index=True)
    nou_id = len(df_titanic) - 1
    return {
        "missatge": "Passatger afegit amb èxit",
        "passatger_id": nou_id,
        "dades": nou_dict
    }

@app.delete("/passatgers/{passatger_id}", tags=["Passatgers"])
def eliminar_passatger(passatger_id: int):
    global df_titanic
    if passatger_id < 0 or passatger_id >= len(df_titanic):
        raise HTTPException(status_code=404, detail="Passatger no trobat")
    df_titanic = df_titanic.drop(index=passatger_id).reset_index(drop=True)
    return {"missatge": f"Passatger amb ID {passatger_id} eliminat correctament."}
```

### Diferències amb el script original

S'han omès les importacions de `json` i `TestClient` perquè no s'utilitzen en aquest bloc, així com `print` i `head(3)` de diagnòstic. Els missatges de validació que contenia el model complet s'han abreujat en aquest resum de codi. Per consultar-los, torna a l'apartat 12. El comportament essencial dels endpoints s'ha mantingut.

## 21. Execució local i comprovacions

**El fitxer del Titanic prové d'un notebook convertit a `.py`** i conté una ruta de dataset que pot no existir al teu PC. L'ordre següent és una proposta d'execució local, basada en l'entorn de `uv` de la primera guia.

```powershell
uv init fastapi-titanic --bare
cd fastapi-titanic
uv add "fastapi[standard-no-fastapi-cloud-cli]" pandas numpy
```

Desa el codi del Titanic com a `main.py`, copia `titanic3.csv` al directori del projecte i canvia la ruta de càrrega per:

```python
DATASET_PATH = "titanic3.csv"
```

Després:

```powershell
uv run fastapi dev main.py
```

Comprova `http://127.0.0.1:8000/docs`. **Aquesta seqüència és una adaptació d'estudi**, no una transcripció textual d'un únic fitxer original; no s'ha executat amb el CSV en aquest dossier.

### Comprovacions recomanades

1. La ruta `/` retorna el nombre de passatgers.
2. `/passatgers?limit=2` mostra com a màxim dues files.
3. `/passatgers?survived=1` filtra per supervivència.
4. `/passatgers/0` selecciona el primer registre.
5. `/estadistiques` retorna les agregacions.
6. Un `POST` vàlid retorna 201.
7. Un `POST` amb `pclass=5` retorna 422.
8. Un `DELETE` amb ID inexistent retorna 404.
9. Reiniciar el servidor restaura les dades llegides del fitxer, si no s'ha implementat persistència.

## 22. Exemples de peticions i respostes

### Consulta simple amb curl

```bash
curl http://127.0.0.1:8000/
curl 'http://127.0.0.1:8000/passatgers?survived=1&pclass=1&limit=5'
curl http://127.0.0.1:8000/estadistiques
```

### Crear passatger

```bash
curl -X POST http://127.0.0.1:8000/passatgers \
  -H 'Content-Type: application/json' \
  -d '{"pclass":2,"survived":1,"name":"Passatgera Exemple","sex":"female","age":29,"sibsp":0,"parch":0}'
```

### Eliminar passatger

```bash
curl -X DELETE http://127.0.0.1:8000/passatgers/0
```

**Precaució:** les peticions de modificació alteren el DataFrame de memòria. Els exemples assumeixen un servidor executant-se en local i són exercicis didàctics; no són proves realment executades contra el fitxer CSV.

## 23. Errors habituals i diagnosi

| Símptoma | Possible causa | Comprovació o correcció |
|---|---|---|
| `uv` no es reconeix | Instal·lació o PATH incomplet | Executar `uv -V`, revisar la instal·lació i reobrir el terminal |
| No es localitza l'aplicació | Fitxer o nom de mòdul incorrecte | Especificar `main.py` a `fastapi dev` |
| `ModuleNotFoundError: pandas` | Dependència absent | Afegir `pandas` amb `uv add` |
| `FileNotFoundError: titanic3.csv` | Ruta original de Colab no vàlida en local | Comprovar el directori i `DATASET_PATH` |
| Error 422 | Entrada incompatible amb l'esquema | Revisar cos JSON, paràmetres i `Field`/`Query` |
| Error 404 | ID fora del DataFrame | Comprovar que existeix i que comença per 0 |
| Error 500 a `/users/3` | Accés fora de límits a la llista original | Afegir comprovació prèvia |
| Error de serialització JSON | `NaN`, `NaT` o valors no serialitzables | Convertir els valors abans del retorn |
| Canvis desapareixen | Dades només a la memòria | Implementar persistència en fitxer o BD |
| ID canvia després de DELETE | `reset_index(drop=True)` | Definir identificadors estables |
| Resultats diferents després de reiniciar | Relectura del CSV inicial | Distingir memòria de persistència |
| Estadístiques fallen amb taula buida | Divisió entre zero | Comprovar `total > 0` |
| `KeyError` en filtrar | Falten columnes o el nom és diferent | Revisar `df_titanic.columns` |

## 24. Limitacions del codi original i millores possibles

Aquest apartat **no descriu funcionalitats implementades**; identifica possibles millores:

**A. Identificadors estables.** Els IDs actuals són posicions. En una aplicació real convindria conservar un identificador únic independent de l'índex de Pandas.

**B. Persistència.** Les altes i baixes queden en RAM. Es podria emprar una base de dades (p. ex. SQLite o PostgreSQL) i registrar cada modificació.

**C. Validació de valors de text.** `sex` i `embarked` tenen descripcions de valors admesos, però no restriccions reals. Es podrien introduir `Literal['male', 'female']` i `Literal['C', 'Q', 'S']`.

**D. Nuls i tipus.** Cal validar els tipus de columnes i la conversió final a JSON, incloent-hi casos `NaN` i `NaT`.

**E. Estadístiques per classe.** La guia inicial les anuncia, però l'endpoint només retorna dades per sexe. Es podria afegir un `groupby('pclass')`.

**F. Paginació estable.** Si s'insereixen o eliminen registres, l'ordre de les files i el resultat de `skip` poden canviar. En producció cal un criteri d'ordenació definit.

**G. Proves automatitzades.** S'importa `TestClient`, però no hi ha tests en el fragment compartit. Es podrien provar els codis 200, 201, 404 i 422.

**H. Seguretat.** Els exemples no incorporen autenticació ni autorització; no convé publicar els endpoints que modifiquen dades en una xarxa oberta sense protecció.

**I. Concurrència.** Modificar una variable global de Pandas pot comportar inconsistències amb diverses peticions o processos alhora.

**J. Noms i imports.** Es pot actualitzar `.dict()` a `.model_dump()` si es treballa amb Pydantic v2, i eliminar imports que no s'utilitzen.

## 25. Exercicis pràctics guiats

### Exercici 1. Primera API

**Objectiu:** reproduir les tres rutes de `guia_fastapi.py` i comprovar-ne les sortides. Prova els IDs 1, 2 i 3, i descriu la diferència entre un resultat correcte i un error d'índex.

**Resposta orientativa:** 1 i 2 retornen els respectius diccionaris; 3 queda fora de la llista i requereix gestió explícita d'errors.

### Exercici 2. Filtrar supervivents

**Petició:** `GET /passatgers?survived=1&limit=5`.

**Resposta orientativa:** la funció selecciona passatgers amb `survived == 1`, calcula les coincidències i retorna una pàgina de fins a cinc registres.

### Exercici 3. Filtrar per classe i sexe

**Petició:** `GET /passatgers?pclass=3&sex=female`.

**Resposta orientativa:** s'apliquen successivament els dos filtres. Si falta un paràmetre, el filtre corresponent no s'aplica.

### Exercici 4. Paginació

**Peticions:** `?skip=0&limit=10` i `?skip=10&limit=10`.

**Resposta orientativa:** amb el mateix ordre i dataset, són dues finestres consecutives de 10 files com a màxim.

### Exercici 5. Validació incorrecta

**Entrada:** un nou passatger amb `pclass=4`.

**Resposta orientativa:** `Field(le=3)` rebutja la dada i FastAPI retorna 422 abans d'executar el cos de la funció de creació.

### Exercici 6. Revisar l'estadística

**Objectiu:** comprovar que la taxa de supervivència és `(supervivents/total)*100`. Cal afegir control per a `total == 0` en una versió millorada.

### Exercici 7. Identificadors després d'eliminar

**Situació:** existeixen tres registres amb posicions 0, 1 i 2; s'elimina la posició 1.

**Resposta:** el registre antic 2 passa a tenir índex 1. Això demostra que la posició no és un ID estable.

### Exercici 8. Afegir estadístiques per classe (ampliació)

**Pista de solució:**

```python
for classe, grup in df_titanic.groupby('pclass'):
    total = len(grup)
    supervivents = int(grup['survived'].sum())
    percentatge = round(100 * supervivents / total, 2) if total else 0
    print(classe, percentatge)
```

### Exercici 9. Test d'endpoint (ampliació)

```python
from fastapi.testclient import TestClient
client = TestClient(app)

resposta = client.get('/')
assert resposta.status_code == 200
assert 'total_passatgers' in resposta.json()
```

Aquest test es pot afegir a un projecte de proves; encara no existeix en el script original.

### Exercici 10. Millorar el filtre de noms

**Problema:** `str.contains` interpreta expressions regulars. Una alternativa per a cerca literal és:

```python
filtered = filtered[
    filtered['name'].astype(str).str.contains(search, case=False, na=False, regex=False)
]
```

### Exercici 11. JSON nul

**Pregunta:** per què un `NaN` pot donar problemes? **Resposta:** JSON estricte no representa `NaN`; cal convertir-lo o sanejar la sortida.

### Exercici 12. Documentació automàtica

**Objectiu:** visitar `/docs`, localitzar `POST /passatgers` i inspeccionar quins camps són obligatoris.

**Resposta:** `pclass`, `survived`, `name` i `sex` es declaren obligatoris al model original.

## 26. Comparatives per a l'examen

### Path vs Query vs Body

| Element | On viatja | Exemple | Utilitat |
|---|---|---|---|
| Path | A la ruta | `/passatgers/4` | Identificar un recurs |
| Query | Després de `?` | `?limit=5` | Filtrar o paginar |
| Body | Cos de la petició | `{"name":"X",...}` | Crear o modificar dades |

### Pydantic vs Pandas

| Pydantic | Pandas |
|---|---|
| Defineix models d'entrada | Organitza files i columnes |
| Valida tipus i restriccions | Filtra, selecciona i agrega |
| Genera errors de validació | Manipula DataFrames |
| Exemple: `PassatgerCreate` | Exemple: `df_titanic` |

### GET vs POST vs DELETE

| GET | POST | DELETE |
|---|---|---|
| Consulta dades | Crea dades | Elimina dades |
| No hauria de modificar estat | Modifica estat | Modifica estat |
| Pot rebre `Query` i `Path` | Habitualment rep JSON | Identifica el recurs a la ruta |

### `iloc` vs `loc`

`iloc` selecciona per posició numèrica. `loc` selecciona per etiquetes d'índex. Al script, després de `reset_index(drop=True)`, les etiquetes tornen a ser consecutives des de zero; aquesta coincidència no implica que la posició sigui una clau primària estable.

## 27. 60 preguntes d'autoavaluació amb resposta

1. **Què és FastAPI?** Un framework de Python per crear API web.
2. **Què és una API?** Una interfície que defineix la comunicació entre programes.
3. **Què és JSON?** Un format textual de dades estructurades.
4. **Què representa una ruta?** Un recurs o punt d'entrada de l'aplicació.
5. **Per a què serveix GET?** Per consultar recursos.
6. **Per a què serveix POST?** Per crear un recurs en aquesta pràctica.
7. **Per a què serveix DELETE?** Per eliminar un recurs.
8. **Què fa `app = FastAPI()`?** Crea l'aplicació.
9. **Què fa `@app.get('/')`?** Registra una ruta GET arrel.
10. **Què significa `async def`?** Declara una funció asíncrona.
11. **Què és `uv`?** Una eina per gestionar projectes i dependències Python.
12. **Què comprova `uv -V`?** Que `uv` és accessible i mostra la versió.
13. **Què fa `uv init`?** Inicialitza el projecte.
14. **Què fa `uv add`?** Afegeix dependències al projecte.
15. **Què fa `uv run fastapi dev`?** Executa el servidor de desenvolupament en un entorn adequat.
16. **Què retorna `GET /` a la primera API?** `{"message":"Hello World"}`.
17. **Què retorna `GET /users/` originalment?** Un diccionari amb el text `the current user`.
18. **Per què es resta 1 a `user_id`?** Per adaptar IDs començant per 1 als índexs començant per 0.
19. **Què passa amb `/users/3` en la primera guia?** Pot generar un error d'índex perquè només hi ha dos usuaris.
20. **Què ofereix `/docs`?** Documentació interactiva de l'API.
21. **Què ofereix `/redoc`?** Una altra presentació de la documentació OpenAPI.
22. **Què és un DataFrame?** Una estructura tabular de Pandas.
23. **Què fa `pd.read_csv`?** Carrega un CSV en un DataFrame.
24. **Què fa `head(3)`?** Consulta les tres primeres files.
25. **Què significa `np.nan`?** Un valor numèric absent/no representable.
26. **Per què cal revisar `NaN` en JSON?** Perquè JSON estricte no l'admet.
27. **Què és Pydantic?** Una biblioteca de models i validació de dades.
28. **Què és `BaseModel`?** La base per definir models validats.
29. **Què significa `Field(...)`?** Camp obligatori.
30. **Què significa `ge=1`?** Major o igual que 1.
31. **Què significa `le=3`?** Menor o igual que 3.
32. **Què significa `Optional[float] = None`?** Camp opcional que pot ser nul.
33. **Quins camps obligatoris té `PassatgerCreate`?** `pclass`, `survived`, `name`, `sex`.
34. **La guia valida efectivament que `sex` sigui `male` o `female`?** No, només el descriu.
35. **Què fa `Query`?** Declara i valida paràmetres de consulta.
36. **Què representa `skip`?** El nombre de registres a saltar.
37. **Què representa `limit`?** El màxim de registres retornats.
38. **Quin valor per defecte té `limit`?** 10.
39. **Quin màxim permet `limit`?** 100.
40. **Què fa `df.copy()`?** Crea una còpia del DataFrame.
41. **Què filtra `survived=1`?** Passatgers supervivents.
42. **Què filtra `pclass=1`?** Passatgers de primera classe.
43. **Què fa `.str.lower()`?** Converteix textos a minúscules.
44. **Què fa `.str.contains()`?** Cerca coincidències dins de textos.
45. **Què fa `.iloc[skip:skip+limit]`?** Selecciona una franja de files per posició.
46. **Què fa `to_dict(orient='records')`?** Converteix cada fila en un diccionari.
47. **El total de coincidències és el nombre d'elements de la pàgina?** No necessàriament.
48. **Què és un paràmetre de ruta?** Un valor integrat en la URL.
49. **Què fa `HTTPException(404)`?** Retorna un error de recurs no trobat.
50. **Què indica 422?** Que la petició no supera la validació.
51. **Com calcula supervivents el codi?** Sumant `survived`.
52. **Com calcula la taxa global?** `supervivents / total * 100`.
53. **Què fa `dropna()`?** Exclou els valors nuls del càlcul corresponent.
54. **Quins desglossaments calcula realment `/estadistiques`?** Per sexe, no per classe.
55. **Quin codi HTTP declara POST quan funciona?** 201.
56. **Què fa `pd.concat`?** Uneix objectes Pandas, aquí per afegir una fila.
57. **Què fa `global df_titanic`?** Permet reassignar la variable global a la funció.
58. **Què fa `reset_index(drop=True)`?** Reconstrueix l'índex consecutiu i descarta l'antic.
59. **Els canvis del POST i DELETE queden al CSV?** No, el codi no els escriu al fitxer.
60. **Quina és la limitació principal dels IDs actuals?** Que representen posicions que canvien després d'eliminar files.

## 28. Glossari

**API:** interfície de comunicació entre programes.  
**Endpoint:** ruta concreta que respon a peticions.  
**FastAPI:** framework web basat en Python.  
**HTTP:** protocol de comunicació web.  
**GET:** mètode per obtenir dades.  
**POST:** mètode utilitzat per crear registres.  
**DELETE:** mètode per eliminar recursos.  
**JSON:** format textual d'intercanvi de dades.  
**Path parameter:** paràmetre dins la URL.  
**Query parameter:** paràmetre de cerca després del signe `?`.  
**Body:** contingut de la petició HTTP.  
**Pydantic:** biblioteca de validació de dades.  
**BaseModel:** classe base de models Pydantic.  
**Field:** declaració i restricció d'un camp.  
**Query:** definició de paràmetres de consulta a FastAPI.  
**HTTPException:** excepció per comunicar errors HTTP.  
**Pandas:** biblioteca de tractament de dades.  
**DataFrame:** taula de dades amb files i columnes.  
**`iloc`:** indexació per posicions.  
**`NaN`:** valor absent d'una estructura numèrica.  
**Serialització:** transformació d'objectes en un format transmetible.  
**Paginació:** retorn de resultats en pàgines limitades.  
**Filtre:** selecció de files que compleixen una condició.  
**Agregació:** càlcul resumit, com una suma o mitjana.  
**Swagger UI:** interfície interactiva de documentació i proves.  
**OpenAPI:** especificació descriptiva de les operacions de l'API.  
**Persistència:** emmagatzematge de canvis que sobreviuen al reinici.  
**TestClient:** client de proves integrat amb FastAPI.

## 29. Checklist final

- [ ] Sé distingir FastAPI, Pandas, Pydantic i `uv`.
- [ ] Sé inicialitzar un projecte i executar el servidor de desenvolupament.
- [ ] Sé diferenciar `GET`, `POST` i `DELETE`.
- [ ] Entenc els paràmetres de ruta, consulta i cos.
- [ ] Sé per què el model `PassatgerCreate` accepta o rebutja dades.
- [ ] Puc llegir un CSV i consultar-ne les columnes amb Pandas.
- [ ] Sé explicar `copy`, filtres, `iloc`, `to_dict` i `pd.concat`.
- [ ] Sé explicar totes les rutes de l'API Titanic.
- [ ] Sé calcular els percentatges de supervivència.
- [ ] Conec els codis 200, 201, 404 i 422.
- [ ] Puc identificar les limitacions d'una API que treballa en RAM.
- [ ] Entenc per què els índexs no són IDs permanents.
- [ ] Sé provar una ruta des de `/docs` o amb `curl`.
- [ ] Distingeixo els exemples originals de les ampliacions proposades.

---

## Referència de les fonts i abast

- **`guia_fastapi.py`**: instal·lació de `uv`, creació del projecte, API amb tres rutes i arrencada amb `uv run fastapi dev`.
- **`explicacio_fastapi_titanic.py`**: importacions, càrrega de `titanic3.csv`, aplicació FastAPI, `PassatgerCreate`, rutes GET de consulta i estadístiques, inserció amb POST i eliminació amb DELETE.

Aquest dossier és un material d'estudi basat en els dos fitxers aportats. Els exemples d'ampliació, els tests opcionals, les recomanacions de seguretat i els procediments locals són explicacions addicionals. **No s'ha comprovat l'execució de l'API sobre el dataset Titanic perquè aquest CSV no acompanya els dos scripts.**
