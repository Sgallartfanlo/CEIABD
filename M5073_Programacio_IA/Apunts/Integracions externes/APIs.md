# APIs RESTful i Dades Remotes
**Arquitectura, Mètodes HTTP, Codis d'Estat i Integració en Python**  
*Unitat Teòrica d'Accés a Dades Externes*

---

## 1. Introducció a les APIs RESTful

### Concepte Fonamental
Les **APIs RESTful** formen la base de la comunicació en entorns web distribuïts moderns. Permeten la interconnexió i l'intercanvi de dades entre diferents aplicacions (clients i servidors) de manera eficient, independentment de les tecnologies o llenguatges utilitzats en cada extrem.

### Què és una API REST?
- **REST** són les sigles de **Representational State Transfer** (Transferència d'Estat Representacional).
- És un **estil arquitectònic** definit per **Roy Fielding** l'any 2000 en la seva tesi doctoral per a sistemes hipermèdia distribuïts.
- Utilitza els estàndards existents del protocol **HTTP** per establir mecanismes de comunicació unificats.

### Concepte de Recurs (*Resource*)
En REST, qualsevol entitat o dada manipulable (usuaris, productes, factures, informes, etc.) es considera un **recurs**.
- Cada recurs s'identifica de forma única mitjançant una **URI / URL** (*Uniform Resource Identifier / Uniform Resource Locator*).
- *Exemple:* `https://api.example.com/v1/estudiants/101` identifica l'estudiant amb l'ID `101`.

### Principals Avantatges
1. **Escalabilitat:** Desacoblament total entre el client i el servidor, permetent escalar cada part de manera independent.
2. **Portabilitat i Interoperabilitat:** Compatible amb qualsevol llenguatge de programació (Python, JavaScript, Java, Go, etc.) i plataforma (Web, Mobile, IoT).
3. **Eficiència:** Aprofita els mecanismes nativament integrats al protocol HTTP, com la memòria cau (*caching*).
4. **Estandardització:** Empra formats estructurats d'intercanvi de dades universals, principalment **JSON** o XML.

---

## 2. Principis Arquitectònics REST

Perquè un servei web sigui considerat **RESTful**, ha de complir les quatre regles arquitectòniques fonamentals:

### 1. Client-Servidor
Separació clara de responsabilitats (*Separation of Concerns*):
- **Client:** Es nodreix de les dades i s'encarrega de gestionar la interfície d'usuari (UI) i l'experiència d'usuari (UX).
- **Servidor:** S'encarrega de la lògica de negoci, el processament i l'emmagatzematge persistent de les dades.

### 2. Sense Estat (*Stateless*)
- Cada petició enviada des del client al servidor ha de contenir **TOTA la informació necessària** per ser entesa i processada completament.
- El servidor **no desa cap context de sessió** del client entre peticions consecutives. Això millora notablement l'escalabilitat del servei.

### 3. Memòria Cau (*Cacheable*)
- Les respostes del servidor han de ser catalogades explícitament com a **desables o no desables** en memòria cau (*cache*).
- Si una resposta es pot desar en memòria cau, el client pot reutilitzar-la per a peticions equivalents posteriors, reduint la càrrega de la xarxa i del servidor.

### 4. Interfície Uniforme
- Ús estandarditzat d'URIs lògiques i mètodes HTTP ben definits.
- Permet realitzar accions sobre els recursos de manera predictible i coherent a tota l'API.

---

## 3. Mètodes i Verbs HTTP

Els mètodes HTTP determinen el tipus d'operació que el client vol dur a terme sobre un recurs concret (operacions **CRUD**: *Create, Read, Update, Delete*).

| Mètode HTTP | Acció CRUD | Descripció i Ús | Idempotent |
| :--- | :--- | :--- | :---: |
| **GET** | **Read** (Lectura) | Recupera un recurs o una llista de recursos sense modificar l'estat del servidor. | **Sí** |
| **POST** | **Create** (Creació) | Envia dades al servidor per a la creació d'un nou recurs. | **No** |
| **PUT** | **Update** (Reemplaç) | Reemplaça completament un recurs existent amb les noves dades proporcionades. | **Sí** |
| **PATCH** | **Modify** (Parcial) | Aplica modificacions o actualitzacions parcials sobre un recurs existent. | **No** |
| **DELETE** | **Delete** (Eliminació) | Elimina el recurs especificat a la URI del servidor. | **Sí** |

### Nota sobre la Idempotència
Un mètode és **idempotent** si realitzar la mateixa petició múltiples vegades produeix exactament el mateix efecte o resultat al servidor que fer-la una sola vegada.
- *Exemple:* Reenviar un `DELETE` diverses vegades eliminarà el recurs el primer cop; els següents cops no canviaran l'estat de la base de dades. En canvi, reenviar un `POST` pot crear múltiples registres duplicats.

---

## 4. Codis d'Estat HTTP i Format JSON

### Codis d'Estat HTTP Habituals
Els codis d'estat (*status codes*) són respostes numèriques que el servidor retorna per indicar el resultat de la petició enviada pel client:

- **200 OK:** La petició s'ha completat amb èxit i es retornen les dades demanades.
- **201 Created:** S'ha creat un nou recurs de manera satisfactòria (resposta habitual davant d'un `POST`).
- **400 Bad Request:** La petició té una sintaxi incorrecta, paràmetres invàlids o dades mal estructurades.
- **401 Unauthorized:** Cal autenticació prèvia o bé no s'ha après un token d'accés vàlid.
- **404 Not Found:** El recurs sol·licitat a la URL no existeix al servidor.
- **500 Internal Server Error:** Error intern inesperat al servidor web al processar la petició.

### El Format JSON (*JavaScript Object Notation*)
**JSON** és el format lleuger i l'estàndard *de facto* per a l'intercanvi de dades estructurades entre clients i servidors en entorns web.

#### Exemple d'Estructura JSON:
```json
{
  "id_estudiant": 101,
  "nom": "Anna Garcia",
  "curs": "2ESO",
  "notes": {
    "mates": 9.5,
    "fisica": 9.0
  },
  "actiu": true
}
```

---

## 5. Consum d'APIs RESTful amb Python

A continuació es mostra com integrar i consultar una API RESTful utilitzant el mòdul `requests` de Python.

### Codi Python d'Exemple

```python
import requests

# URL del recurs i capçaleres d'autenticació
url = "https://api.example.com/v1/estudiants"
headers = {
    "Authorization": "Bearer TOKEN_D_AUTENTICACIO",
    "Content-Type": "application/json"
}

try:
    # Petició HTTP GET amb temps d'espera límit (timeout)
    response = requests.get(url, headers=headers, timeout=5)
    
    # Comprovació del codi d'estat
    if response.status_code == 200:
        dades = response.json()
        print(f"S'han rebut {len(dades)} registres.")
    else:
        print(f"Error HTTP: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de connexió: {e}")
```

### Punts Clau de la Integració

1. **Mòdul `requests`:** És la biblioteca estàndard *de facto* a Python per fer peticions HTTP d'una manera senzilla i intuïtiva.
2. **Capçaleres (*Headers*):** S'utilitzen per enviar informació contextual, com tokens d'autenticació (`Bearer Tokens`) o indicar el tipus de format (`Content-Type`).
3. **Mètode `.json()`:** Converteix automàticament la resposta codificada en JSON a estructures de dades natives de Python (dict, list, etc.).
4. **Control d'Errors:** Cal comprovar sempre el `status_code` i utilitzar blocs `try-except` per capturar excepcions de xarxa o de temps d'espera (`RequestException`).