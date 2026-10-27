# MongoDB: Introducció i Operacions CRUD amb `mongosh`

> **Mòdul:** M5074 Sistemes de Big Data NoSQL  
> **Cicle Formatiu:** Curs d'Especialització en IA & BD (ASIX / DAW / DAM)  
> **Centre:** Institut Sa Palomera  
> **Curs acadèmic:** 2026/2027  
> **Autor:** Francesc Barragán Pascual  
> **Llicència:** CC BY-NC-SA  

---

## Taula de Continguts
1. [Objectius del Curs](#1-objectius-del-curs)
2. [Què és MongoDB?](#2-què-és-mongodb)
   - [Model Documental i Esquemes Dinàmics](#model-documental-i-esquemes-dinàmics)
   - [Atomicitat i Joins ($lookup)](#atomicitat-i-joins-lookup)
3. [Conceptes Fonamentals i Equivalència SQL](#3-conceptes-fonamentals-i-equivalència-sql)
4. [El Format BSON (Binary JSON)](#4-el-format-bson-binary-json)
   - [Característiques i Limitacions](#característiques-i-limitacions)
   - [L'identificador Únic `_id` i l'ObjectId](#lidentificador-únic-_id-i-lobjectid)
5. [Desplegament i Entorn de Treball](#5-desplegament-i-entorn-de-treball)
   - [Opcions d'Instal·lació (Atlas, Community, Enterprise)](#opcions-dinstal·lació-atlas-community-enterprise)
   - [Desplegament local amb Docker](#desplegament-local-amb-docker)
   - [Configuració a MongoDB Atlas (Cloud)](#configuració-a-mongodb-atlas-cloud)
6. [Eines de l'Ecosistema MongoDB](#6-eines-de-lecosistema-mongodb)
   - [L'intèrpret `mongosh`](#lintèrpret-mongosh)
   - [Database Tools (Import/Export/Dump/Restore)](#database-tools-importexportdumprestore)
   - [Eines Gràfiques (Compass, VS Code) i Monitorització](#eines-gràfiques-compass-vs-code-i-monitorització)
7. [Primeres Ordres i Execució d'Scripts](#7-primeres-ordres-i-execució-dscripts)
8. [Consulta i Recuperació de Dades (Read Operations)](#8-consulta-i-recuperació-de-dades-read-operations)
   - [Consultes Bàsiques: `find()` i `findOne()`](#consultes-bàsiques-find-i-findone)
   - [Operadors de Comparació](#operadors-de-comparació)
   - [Filtres Avançats (`$exists`, `$not`, `$type`, `$expr`, `$where`)](#filtres-avançats-exists-not-type-expr-where)
   - [Expressions Regulars i Cerca de Text](#expressions-regulars-i-cerca-de-text)
   - [Projeccions](#projeccions)
   - [Condicions Compostes (`$and`, `$or`, `$nor`, `$in`, `$nin`)](#condicions-compostes-and-or-nor-in-nin)
   - [Consultes sobre Documents Imbricats i Arrays](#consultes-sobre-documents-imbricats-i-arrays)
   - [Gestió de Dates i Formats](#gestió-de-dates-i-formats)
   - [Ús de Cursors: `sort()`, `skip()`, `limit()` i Comptatge](#ús-de-cursors-sort-skip-limit-i-comptatge)
9. [Modificació de Dades (Update Operations)](#9-modificació-de-dades-update-operations)
   - [`insertOne()`, `insertMany()`, `updateOne()`, `updateMany()`](#insertone-insertmany-updateone-updatemany)
   - [Operadors d'Actualització (`$set`, `$inc`, `$unset`, etc.)](#operadors-dactualització-set-inc-unset-etc)
   - [Reemplaçament (`replaceOne`) i Opció `upsert`](#reemplaçament-replaceone-i-opció-upsert)
   - [Operadors per a Arrays (`$push`, `$addToSet`, `$pull`, etc.)](#operadors-per-a-arrays-push-addtoset-pull-etc)
   - [Operador Posicional (`$`, `$[]`, `$[id]`)](#operador-posicional--id)
10. [Eliminació de Dades (Delete Operations)](#10-eliminació-de-dades-delete-operations)
11. [Resum Executiu](#11-resum-executiu)
12. [Enllaços i Referències d'Interès](#12-enllaços-i-referències-dinterès)

---

## 1. Objectius del Curs

* **Model Documental:** Entendre l'estructura de bases de dades, col·leccions i documents BSON.
* **Desplegament:** Posar en marxa entorns MongoDB usant Docker o serveis cloud com MongoDB Atlas, i realitzar connexions a través de l'intèrpret de línia d'ordres `mongosh`.
* **Ecosistema d'Eines:** Conèixer i utilitzar MongoDB Database Tools (`mongoimport`, `mongodump`, etc.), MongoDB Compass i l'extensió oficial per a Visual Studio Code.
* **Consultes Avançades (Read):** Masteritzar l'ús de `find()`, aplicant filtres de comparació, projeccions, manipulació d'arrays, tractament de dates i gestió eficient de cursors.
* **Escriptura i Modificació (CRUD):** Aplicar operadors atomicament modificadors de documents, gestió avançada d'arrays en profunditat i eliminació controlada de dades.

---

## 2. Què és MongoDB?

MongoDB és una de les bases de dades NoSQL orientada a documents més utilitzades a nivell mundial. El seu nom prové de la paraula anglesa **"huMONGOus"** (gegantí / enorme), reflectint la seva capacitat de gestionar grans volums de dades i escalar horitzontalment.

### Model Documental i Esquemes Dinàmics
A diferència de les bases de dades relacionals tradicionals (RDBMS) on totes les files d'una taula han de complir rigorosament amb una estructura fixa de columnes:
* MongoDB utilitza **esquemes dinàmics** (*schema-less*).
* Documents d'una mateixa col·lecció poden tenir atributs (camps) diferents.
* L'esquema pot evolucionar orgànicament a mesura que l'aplicació s'amplia, sense necessitat d'executar altes d'alteració d'estructura complexes (`ALTER TABLE`).

### Atomicitat i Joins (`$lookup`)
* **Atomicitat a nivell de document:** Tota operació d'inserció, modificació o eliminació sobre un únic document sencer és atòmica. Les transaccions ACID multi-document estan suportades però requereixen una gestió específica (habitualment a nivell de *driver* o en clusters de la versió 4.0+).
* **Joins amb `$lookup`:** Històricament, les bases de dades NoSQL evitaven les unions de taules. A MongoDB, mitjançant el *pipeline* d'agregació, l'operador `$lookup` permet relacionar col·leccions. Des de la versió 5.1, funcionalitat ampliada per a col·leccions particionades (*sharded collections*).

---

## 3. Conceptes Fonamentals i Equivalència SQL

| MongoDB | Equivalent Relacional (SQL) | Descripció |
| :--- | :--- | :--- |
| **Base de dades** | Base de dades | Contenidor d'alt nivell. Una instància pot albergar múltiples BDs. |
| **Col·lecció** | Taula | Grup de documents. Poden ser normals o *capped* (mida fixa circular). |
| **Document** | Fila / Registre | Registre individual en format BSON sense esquema fix. |
| **Camp** | Columna | Parella clau / valor continguda dins un document. |
| **Índex** | Índex | Estructura B-Tree per optimitzar les cerques de camps específics. |
| **Cursor** | Cursor | Punter al conjunt de resultats d'una consulta `find()`. |

---

## 4. El Format BSON (Binary JSON)

Internament, MongoDB no guarda el document com a text d'estil JSON pur, sinó serialitzat en **BSON** (Binary JSON). 

### Característiques i Limitacions
BSON s'ha dissenyat sota tres principis clau:
1. **Lleuger (*Lightweight*):** Minimitza l'espai addicional per transferència en xarxa.
2. **Navegable (*Traversable*):** Permet saltar camps ràpidament sense parsejar tot el document.
3. **Eficient (*Efficient*):** Utilitza tipus de dades primitius C per a una codificació/decodificació ultraràpida.

**Tipus de dades addicionals de BSON:**
* `ObjectId` (identificador únic)
* `Date` (data UTC en mil·lisegons des de l'època Unix)
* `Timestamp` (ús intern per a operacions de replika/oplog)
* `BinData` (arxius o fluxos de bytes en binari)
* `Decimal128` (precisió decimal d'alta fidelitat)

**Restriccions importants:**
* Mida màxima per document: **16 MB**.
* El nom dels camps pot contenir `$` o `.`, però és un antipatró desaconsellat.
* **Sensibilitat:** MongoDB és sensible als **tipus de dades** i a les **majúscules/minúscules**.
  - `{"edat": 18}` $\neq$ `{"edat": "18"}` $\neq$ `{"Edat": 18}`

### L'identificador Únic `_id` i l'ObjectId
El camp `_id` actua com a clau primària única i immutable dins la col·lecció. Si no s'especifica en inserir un document, MongoDB en genera un automàticament de tipus `ObjectId` de **12 bytes**:

$$\underbrace{\text{4 bytes}}_{\text{Timestamp (UTC)}} + \underbrace{\text{5 bytes}}_{\text{Valor aleatori (màquina/procés)}} + \underbrace{\text{3 bytes}}_{\text{Comptador incremental}}$$

```javascript
// Obtenir la data exacta de creació des d'un ObjectId des de mongosh:
db.people.findOne()._id.getTimestamp()
// Retorna: ISODate("2025-09-06T07:53:55.000Z")
```
> **Nota de rendiment:** Eviteu utilitzar `_id` com a criteri d'ordenació cronològica estricta en entorns distributed, ja que l'ObjectId el genera el *driver* del client i no el servidor central.

Si preferiu assignar el vostre propi `_id`:
```javascript
// Utilitzant un valor enter o un document com a clau primària
db.people.insertOne({ _id: 4, nom: "Marina", edat: 18 });
db.people.insertOne({ 
  _id: { nom: 'Bob', cognoms: 'Bob', twitter: '@bob' }, 
  ciutat: 'Blanes' 
});
```

---

## 5. Desplegament i Entorn de Treball

### Opcions d'Instal·lació
1. **MongoDB Atlas:** Servei Cloud totalment gestionat. Inclou una opció *Shared Free Tier* de 512 MB.
2. **Community Edition:** Versió Open Source on-premise per a Linux, macOS i Windows.
3. **Enterprise Advanced:** Versió de pagament amb suport enterprise, seguretat LDAP/Kerberos, monitorització avançada i auditoria.

### Desplegament local amb Docker
Per iniciar un entorn aïllat ràpidament:

```bash
# 1. Arrencar el contenidor de MongoDB (Port 27017)
docker run -p 127.0.0.1:27017:27017 --name iabd-mongo -d mongo

# En cas de processadors antics sense suport d'instruccions AVX, feu servir la versió 4.4:
# docker run -p 127.0.0.1:27017:27017 --name iabd-mongo -d mongo:4.4

# 2. Carregar les dades de mostra oficials d'Atlas (opcional)
curl https://atlas-education.s3.amazonaws.com/sampledata.archive -o sampledata.archive
docker cp sampledata.archive iabd-mongo:/tmp

# 3. Entrar al contenidor i restaurar les dades
docker exec -it iabd-mongo bash
mongorestore --archive=/tmp/sampledata.archive
mongosh
```

### Configuració a MongoDB Atlas (Cloud)
1. Crear un compte a MongoDB Atlas.
2. Deploy d'un **Shared Cluster** a la regió propera (ex. AWS Paris `eu-west-3`).
3. Crear un usuari i contrasenya de BD (*Database Access*).
4. Configurar la llista blanca d'IPs (*Network Access*) a `0.0.0.0/0` (entorn de proves).
5. Desplegar el **Sample Dataset** des del menú d'opcions del cluster.
6. Obtenir la URL de connexió amb format:
   `mongodb+srv://<usuari>:<password>@<cluster-host>/<database>`

---

## 6. Eines de l'Ecosistema MongoDB

### L'intèrpret `mongosh`
És la nova línia d'ordres interactiva basada en el motor de JavaScript Node.js.
```bash
# Connexió local
mongosh sample_training

# Connexió Cloud (Atlas)
mongosh "mongodb+srv://cluster0.xxxx.mongodb.net/" --apiVersion 1 --username iabd
```

### Database Tools
Eines independents de la línia d'ordres del sistema operatiu per a la gestió massiva de dades:

```bash
# Importar dades JSON o CSV/TSV
mongoimport -d iabd -c gent --file gent.json
mongoimport --type tsv -d test -c poblacio --headerline --drop pob.tsv

# Exportar una col·lecció a JSON
mongoexport -d iabd -c gent -o gent.json

# Backup binari (BSON) i restauració
mongodump --db=iabd --out=dump/
mongorestore --db=iabd dump/iabd

# Convertir BSON binari a JSON visible
bsondump fitxer.bson > fitxer.json
```

### Eines Gràfiques i Monitorització
* **MongoDB Compass:** GUI oficial per explorar esquemes, analitzar agregacions, validar data i utilitzar un CLI integrat.
* **MongoDB for VS Code:** Extensió de l'editor de codi per utilitzar playgrounds JS i explorar la BD.
* **`mongostat` i `mongotop`:** Utilitats de consola per analitzar l'estat i rendiment d'operacions d'E/S en temps real.

---

## 7. Primeres Ordres i Execució d'Scripts

### Comandes bàsiques a `mongosh`
```javascript
use iabd                    // Selecciona o crea la BD "iabd"
show dbs                    // Llista les BDs existents amb espai ocupat
show collections            // Llista les col·leccions de la BD activa
db                          // Mostra la BD actual
db.help()                   // Mostra l'ajuda de comandes
db.version()                // Versió del motor de MongoDB
db.dropDatabase()           // Elimina la BD actual en ús
```

### Inserció inicial ràpida
```javascript
db.people.insertOne({ nom: "Bob", edat: 30, professio: "Mecànic" });
db.people.findOne(); // Retorna el primer document trobat
```

### Execució d'scripts JS exteriors
Es poden carregar fitxers JavaScript per poblar la BD o executar tasques automatitzades:
```javascript
// Dins de mongosh:
load("scripts/dades.js");

// Des del terminal del sistema operatiu:
mongosh iabd dades.js
```

---

## 8. Consulta i Recuperació de Dades (Read Operations)

Per efectuar consultes fem servir el mètode `db.<colleccio>.find(criteri, projeccio)`.

### Consultes Bàsiques
```javascript
db.trips.find()     // Retorna tots els documents (en blocs de 20 via cursor)
db.trips.findOne()  // Retorna només el primer document trobat com objecte JSON
```

### Operadors de Comparació

Sintaxi general: `db.col.find({ camp: { $operador: valor } })`

| Operador | Significat |
| :--- | :--- |
| `$eq` | Igual a (*equal*) |
| `$ne` | Diferent de (*not equal*) |
| `$lt` | Menor que (*less than*) |
| `$lte` | Menor o igual que (*less than or equal*) |
| `$gt` | Més gran que (*greater than*) |
| `$gte` | Més gran o igual que (*greater than or equal*) |

```javascript
// Exemples:
db.trips.find({ tripduration: { $lt: 300 } });
db.trips.find({ tripduration: { $gt: 180, $lte: 300 } });
db.trips.find({ usertype: { $ne: "Subscriber" } });
```

### Filtres Avançats
* **`$exists`:** Filtra per l'existència física del camp (comprovació de valors no nuls en esquemes dinàmics).
  ```javascript
  db.people.find({ edat: { $exists: true } });
  ```
* **`$not` i `$mod`:** Negació lògica de l'operador contingut.
  ```javascript
  // Edats que NO són múltiples de 5
  db.people.find({ edat: { $not: { $mod: [5, 0] } } });
  ```
* **`$type`:** Filtra pel tipus de dada BSON especificat.
  ```javascript
  db.trips.find({ "start station name": { $type: "string" } });
  ```
* **`$expr`:** Permet avaluar expressions d'agregació dins del `find`, comparant camps del mateix document usant la notació `"$nomDelCamp"`.
  ```javascript
  // Viatges on l'estació d'origen i destí és la mateixa
  db.trips.find({ $expr: { $eq: ["$end station id", "$start station id"] } });
  ```
* **`$where`:** Executa expressions JavaScript arbitràries al servidor. *(Desaconsellat per motius de seguretat i rendiment, ja que no fa servir índexs).*

### Expressions Regulars i Cerca de Text
```javascript
// Cerques amb Regex (Sensible a majúscules)
db.trips.find({ "start station name": /Central Park/ });

// Regex insensitive (insensible a majúscules/minúscules)
db.trips.find({ "start station name": /central park/i });
db.trips.find({ "start station name": { $regex: /central park/i } });
```

### Projeccions
El segon argument de `find()` serveix per triar quins camps volem que ens retorni el servidor (`1` per incloure, `0` per excloure).
```javascript
// Incloure només tripduration (_id es mostra per defecte)
db.trips.find({ "start station id": 405 }, { tripduration: 1 });

// Excloure l'id explícitament
db.trips.find({ "start station id": 405 }, { tripduration: 1, _id: 0 });
```
> **Atenció:** No es poden barrejar inclusions (`1`) i meitat exclusions (`0`) en una mateixa projecció, excepte per al camp `_id`.

### Condicions Compostes
* **`$or` / `$nor`:** Disjunció lògica.
  ```javascript
  db.trips.find({ $or: [{ 'start station id': 405 }, { 'start station id': 146 }] });
  ```
* **`$in` / `$nin`:** Comprova si un camp equival a qualsevol dels elements d'una llista.
  ```javascript
  db.trips.find({ "birth year": { $in: [1977, 1980] } });
  ```
* **`$and`:** Conjunció lògica. Normalment implícita separant camps amb comes:
  ```javascript
  db.trips.find({ 'start station id': 405, 'end station id': 146 });
  ```

> **Consell de Rendiment en Indexació:**
> - En consultes **AND**, és recomanable avaluar o ordenar primer el filtre que retorni el conjunt de dades **més petit**.
> - En consultes **OR**, s'ha d'avaluar millor primer el conjunt de dades **més gran**.

### Consultes sobre Documents Imbricats i Arrays

Per accedir a propietats dins subdocuments s'utilitza la **notació per punt** (*dot notation*), que requereix anar entre cometes:
```javascript
// Cercar posts on l'autor del comentari és "Santiago Dollins"
db.posts.find({ "comments.author": "Santiago Dollins" });
```

**Operadors especials per a Arrays:**
* `$all`: Comprova si l'array conté tots els elements especificats.
* `$elemMatch`: Garanteix que almenys un element de l'array compleix **totes** les condicions especificades.
* `$size`: Filtra per la longitud exacta de l'array.
* `$slice`: Limita en la projecció el nombre d'elements retornats d'un array.

```javascript
// Conté les dues etiquetes simultàniament
db.posts.find({ tags: { $all: ["dream", "action"] } });

// Almenys un comentari compleix l'autor I l'email alhora
db.posts.find({ comments: { 
  $elemMatch: { author: "Santiago Dollins", email: "xnZKyvWD@jHfVKtUh.com" } 
}});

// Post amb exactament 10 etiquetes
db.posts.find({ tags: { $size: 10 } });

// Retornar només els primer 2 comentaris i les 3 primeres etiquetes
db.posts.find({ title: "US Constitution" }, { comments: { $slice: 2 }, tags: { $slice: 3 } });
```

### Gestió de Dates i Formats
```javascript
// Dates a JS/mongosh
var ara = new Date();
var dataISO = ISODate("2025-10-01T00:00:00Z");

// Filtratge per rang de dates
db.posts.countDocuments({
  date: { 
    $gt: ISODate("2012-11-20T05:05:00Z"), 
    $lte: ISODate("2012-11-20T05:05:16Z") 
  }
});

// Formatat de data en projecció ($dateToString)
db.posts.findOne({ author: "machine" }, {
  title: 1,
  data: { $dateToString: { date: "$date", format: "%Y-%m-%d" } }
});
```

### Obtenir Valors Unics (`distinct`)
```javascript
// Retorna un array de valors únics del camp especificat
db.trips.distinct("usertype");

// Amb un filtre addicional com a segon paràmetre
db.trips.distinct("usertype", { "birth year": { $gt: 1990 } });
```

### Ús de Cursors: `sort()`, `skip()`, `limit()` i Comptatge
La crida a `find()` no executa la cerca immediatament, sinó que construeix un **cursor**.

```javascript
// Paginació: Saltem 20 elements i obtenim els 10 següents (3a pàgina), ordenant de forma descendent (-1)
db.trips.find({ usertype: "Customer" })
  .sort({ tripduration: -1 })
  .skip(20)
  .limit(10);
```

**Comptatge de documents:**
* `countDocuments(filtre)`: Executa un comptatge exacte scanejant el conjunt corresponent al filtre.
* `estimatedDocumentCount()`: Molt ràpid, llegeix les metadades generals de la col·lecció (no admet filtres).
* *Eviteu utilitzar el mètode antic `.find().count()` (obsolet / deprecated).*

---

## 9. Modificació de Dades (Update Operations)

### Inserció de múltiples documents
```javascript
db.people.insertMany([
  { nom: "Francesc Barragan", edat: 45, professio: "Professor" },
  { nom: "Albert Barragan", edat: 45, professio: "Professor" },
  { nom: "Josep Barragan", edat: 12, professio: "Estudiant" }
]);
```

### Actualització Bàsica (`updateOne` / `updateMany`)
Des de les versions modernes de MongoDB, és obligatori utilitzar operadors d'actualització per modificar només camps concrets sense sobreescriure el document complet.

```javascript
db.people.updateOne(
  { nom: "Bob" },
  { $set: { nom: "Alice", professio: "Estudiant", salari: 50000 } }
);
```

### Operadors d'Actualització

| Operador | Funció |
| :--- | :--- |
| `$set` | Crea o modifica el valor d'un o diversos camps. |
| `$unset` | Elimina un camp d'un document. |
| `$inc` | Incrementa o decrementa valors numèrics. |
| `$mul` | Multiplica el valor numèric d'un camp. |
| `$rename` | Canvia el nom d'un camp. |
| `$min` / `$max` | Actualitza el camp només si el nou valor és menor/major que l'actual. |
| `$currentDate` | Estableix la data/hora actual al camp informat. |

```javascript
// Increment i decrement de salaris
db.people.updateOne({ nom: "Alice" }, { $inc: { salari: 1000 } });
db.people.updateOne({ nom: "Bob" }, { $inc: { salari: -500 } });

// Eliminar el camp 'twitter'
db.people.updateOne({ nom: "Alice" }, { $unset: { twitter: "" } });

// Reanomenar camps
db.people.updateMany({ _id: 1 }, { $rename: { 'nickname': 'alias', 'cell': 'mobil' } });
```

### Reemplaçament (`replaceOne`) i Opció `upsert`
* **`replaceOne`:** Substitueix l'estructura completa del document mantení l'identificador `_id`.
  ```javascript
  db.people.replaceOne(
    { nom: "Bob" },
    { nom: "Bob", cognoms: "Bob", aficions: ["bàsquet", "videojocs"] }
  );
  ```
* **`upsert` (`update` + `insert`):** Si la condició de cerca no troba cap document, en crea un de nou fusionant el filtre i les instruccions de l'update.
  ```javascript
  db.people.updateOne(
    { nom: "Bob Alice" },
    { $set: { nom: "Alice Bob", twitter: "@bobalice" } },
    { upsert: true }
  );
  ```

### Modificació Atòmica amb `findAndModify`
Permet trobar i modificar un document en una sola operació atòmica, retornant per defecte l'estat original (o el modificat usant `new: true`).

```javascript
db.people.findAndModify({
  query: { nom: "Alice" },
  update: { $inc: { salari: 100 } },
  new: true
});
```

### Operadors per a Arrays

```javascript
// Afegir un element ($push)
db.enllacos.updateMany({ titol: "www.google.es" }, { $push: { tags: "blog" } });

// Afegir varis elements ($push amb $each)
db.enllacos.updateMany({ titol: "www.google.es" }, { 
  $push: { tags: { $each: ["calendari", "email", "mapes"] } } 
});

// Afegir només si no existeix prèviament per evitar duplicats ($addToSet)
db.enllacos.updateMany({ titol: "www.google.es" }, { $addToSet: { tags: "cercador" } });

// Eliminar un element especificat ($pull)
db.enllacos.updateMany({ titol: "www.google.es" }, { $pull: { tags: "traductor" } });

// Eliminar múltiples elements específics ($pullAll)
db.enllacos.updateMany({ titol: "www.google.es" }, { $pullAll: { tags: ["calendari", "email"] } });

// Eliminar el primer element (-1) o l'últim (1) de l'array ($pop)
db.enllacos.updateMany({ titol: "www.google.es" }, { $pop: { tags: -1 } });
```

### Operador Posicional (`$`, `$[]`, `$[id]`)
* `$` : Referència el **primer element** de l'array que compleix el filtre de la consulta.
* `$[]` : Modifica **tots** els elements de l'array.
* `$[<identificador>]` : Modifica els elements que compleixen la condició indicada a la propietat `arrayFilters`.

```javascript
// Canviar el valor 80 per 82 en un array de números
db.students.updateOne(
  { _id: 1, notes: 80 },
  { $set: { "notes.$": 82 } }
);

// Canviar la propietat 'mitja' a 89 en un array d'objectes imbricats per al sub-element trobat
db.students.updateOne(
  { _id: 4, "notes.nota": 85 },
  { $set: { "notes.$.mitja": 89 } }
);
```

---

## 10. Eliminació de Dades (Delete Operations)

```javascript
// Eliminar el primer document trobat
db.people.deleteOne({ nom: "Bob" });

// Eliminar tots els documents que compleixin la condició
db.people.deleteMany({ professio: "Estudiant" });

// Eliminar TOTA la col·lecció (esborra dades i els seus índexs associats)
db.people.drop();

// Eliminar la base de dades completa
db.dropDatabase();
```

> **Nota sobre eliminació i referències:** Si teniu identificadors guardats en altres col·leccions que apunten a un document esborrat (referències), MongoDB no elimina automàticament les referències creuades (no existeixen claus foranes amb *Cascade Delete* en cascada per defecte).

---

## 11. Resum Executiu

1. **Model:** Base de Dades $\rightarrow$ Col·leccions $\rightarrow$ Documents BSON (Màxim 16 MB) amb esquemes flexibles i dinàmics.
2. **`_id`:** Clau primària única i immutable. Si no es defineix, MongoDB assigna automàticament un `ObjectId` de 12 bytes.
3. **`find()`:** Suporta operadors rics de filtre (`$gt`, `$in`, `$or`, `$elemMatch`...), projecció de camps i un cursor gestionat amb `sort()`, `skip()` i `limit()`.
4. **Cursors:** Les instruccions d'ordenació i paginació s'executen en el servidor abans de transmetre els resultats al client.
5. **`update`:** Exigeix l'ús d'operadors atomicament segurs (`$set`, `$inc`, `$push`, `$addToSet`...). L'opció `upsert: true` permet automatitzar insercions quan no hi ha coincidència prèvia.
6. **`delete`:** Permet operacions puntuals amb `deleteOne()`, massives amb `deleteMany()` o la purga completa d'estructures mitjançant `drop()`.

---

## 12. Enllaços i Referències d'Interès

* [Manual Oficial de MongoDB](https://www.mongodb.com/docs/manual/)
* [Mongosh Cheat Sheet Oficial](https://www.mongodb.com/developer/products/mongodb/cheat-sheet/)
* [Comparativa de sintaxi SQL vs MongoDB](https://www.mongodb.com/docs/manual/reference/sql-comparison/)
* [Especificació del format BSON](https://bsonspec.org/)
* [MongoDB University (Cursos Online Gratuïts)](https://learn.mongodb.com/)
* [Exercicis resolts de consultes MongoDB (w3resource)](https://www.w3resource.com/mongodb-exercises/)