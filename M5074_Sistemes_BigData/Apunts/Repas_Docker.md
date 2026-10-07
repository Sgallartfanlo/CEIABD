# APUNTS EXTENSOS: INTRODUCCIÓ I GESTIÓ AVANÇADA DE DOCKER

## 1. Introducció a Docker i Comparativa amb Màquines Virtuals

* **Concepte de contenidor:** Els contenidors representen un mecanisme d'empaquetat lògic on les aplicacions disposen de tot allò necessari per executar-se. Són processos totalment aïllats de la màquina anfitriona (*host*) que comparteixen el nucli (*kernel*) del sistema operatiu.


* **Lleugeresa i rendiment:** A diferència de les màquines virtuals tradicionals (com VirtualBox, que utilitzen un hipervisor per virtualitzar maquinari sencer), els contenidors de Docker empren mecanismes d'aïllament del kernel de Linux com `cgroups` i `namespaces`. Això permet executar centenars de contenidors en un ordinador convencional amb un consum de recursos molt inferior.


* **Portabilitat i Immutabilitat:** Gràcies al *Docker Engine*, una imatge de Docker es pot executar en qualsevol infraestructura independentment del sistema operatiu subjacent. Les imatges són immutables: contenen el codi i les dependències tancades en capes, garantint que el comportament sigui idèntic en entorns de desenvolupament, proves i producció.



## 2. Components i Arquitectura de Docker

* **Docker Client:** L'eina de línia d'ordres (`docker`) que utilitza l'usuari per interactuar amb el dimoni mitjançant una API.


* **Docker Engine (Daemon):** El servei de fons (`dockerd`) encarregat de gestionar la creació, execució i cicle de vida de les imatges, contenidors, xarxes i volums.


* **Imatges vs Contenidors:** Una **imatge** és una plantilla de només lectura amb el sistema operatiu i programari preconfigurat (organitzada per capes). Un **contenidor** és la instància en execució d'aquesta imatge.



## 3. El Fitxer `Dockerfile`

Un `Dockerfile` és un fitxer de text pla que conté les instruccions seqüencials per automatitzar la construcció d'una imatge personalitzada. Les instruccions principals són:

* `FROM`: Defineix la imatge base.


* `LABEL`: Especifica l'autor o metadades.


* `RUN`: Executa comandes durant el procés de construcció (*build*) i guarda el resultat en una nova capa.


* `COPY` / `ADD`: Permet copiar fitxers o directoris locals/remots al contenidor.


* `ENV`: Defineix variables d'entorn.


* `EXPOSE`: Informa dels ports en què el contenidor escoltarà.


* `WORKDIR` / `USER`: Estableix el directori de treball o l'usuari d'execució.


* `CMD` / `ENTRYPOINT` Defineixen el comportament per defecte o l'executable principal en arrencar el contenidor.



Per construir una imatge s'empra l'ordre:

```bash
# docker image build -t nom_nova_imatge ruta_del_dockerfile

```

## 4. Emmagatzematge i Volums

Per defecte, les dades d'un contenidor són efímeres: si s'atura o s'elimina, la informació es perd. Per aconseguir **persistència de dades**, s'utilitzen els volums:

* Els volums s'allotgen a `/var/lib/docker/volumes`.


* Permeten compartir dades entre el *host* i el contenidor, o entre múltiples contenidors.


* Es munten amb l'opció `-v` o `--volume`:


```bash
# docker run -d -p 3306:3306 -v /ruta/host:/var/lib/mysql --name my_container imatge

```



## 5. Xarxes a Docker (`Docker Network`)

Docker crea automàticament tres xarxes per defecte:

* **`bridge`:** Xarxa predeterminada per als contenidors a través de la interfície virtual `docker0`.


* **`host`:** El contenidor comparteix directament la pila de xarxa de la màquina anfitriona.


* **`none`:** El contenidor queda totalment aïllat sense interfície de xarxa externa.



Es poden crear xarxes personalitzades per aïllar serveis (per exemple, separar entorns de producció i desenvolupament):

```bash
# docker network create --subnet 192.168.100.0/24 xarxa_personalitzada

```

---

# GUIA TUTORIAL: COM CREAR UN CONTENIDOR AMB MYSQL FUNCIONANT

Aquesta guia pas a pas detalla com descarregar, configurar i posar en marxa un contenidor Docker amb **MySQL** de manera persistent i segura.

## Pas 1: Comprovar i descarregar la imatge oficial de MySQL

Abans de crear el contenidor, és recomanable descarregar una versió específica de MySQL des de Docker Hub (per exemple, la versió `8.0`):

```bash
# docker image pull mysql:8.0

```

## Pas 2: Crear un volum per a la persistència de dades

Per evitar que les bases de dades es perdin en aturar o esborrar el contenidor, crearem un volum dedicat al directori de dades de MySQL (`/var/lib/mysql`):

```bash
# docker volume create mysql_data

```

## Pas 3: Executar el contenidor MySQL

Llançarem el contenidor configurant les variables d'entorn obligatòries per a l'administració (contrasenya de root), exposant el port per defecte (`3306`) i connectant el volum creat:

```bash
# docker run --name mysql-server \
  -e MYSQL_ROOT_PASSWORD=la_teva_contrasenya_segura \
  -e MYSQL_DATABASE=proves_db \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  -d mysql:8.0

```

* **Explicació dels paràmetres:**
* `--name mysql-server`: Assigna un nom identificatiu al contenidor.


* `-e MYSQL_ROOT_PASSWORD=...`: Defineix la contrasenya del superusuari `root` de MySQL.
* `-e MYSQL_DATABASE=proves_db`: Opcionalment, crea automàtica una base de dades inicial anomenada `proves_db`.
* `-p 3306:3306`: Associa el port 3306 de la màquina amfitriona al port 3306 del contenidor.


* `-v mysql_data:/var/lib/mysql`: Assegura la persistència de les dades de MySQL al volum `mysql_data`.
* `-d`: Executa el contenidor en segon pla (*background*).





## Pas 4: Comprovar que el contenidor està funcionant correctament

Per verificar l'estat del contenidor i veure si s'està executant:

```bash
# docker ps

```

Hauries de veure una sortida amb el contenidor `mysql-server` i el port `3306` actiu.

Si experimentes algun problema d'arrencada, pots revisar els registres d'error (*logs*) del contenidor:

```bash
# docker container logs mysql-server

```

## Pas 5: Connectar-se a MySQL des de la línia de comandes del contenidor

Per accedir a la consola interactiva de MySQL dins del contenidor i començar a crear consultes:

```bash
# docker exec -it mysql-server mysql -u root -p

```

*(Et demanarà introduir la contrasenya `la_teva_contrasenya_segura` que vas definir al pas 3).* Un cop dins, pots provar comandes SQL bàsiques:

```sql
SHOW DATABASES;
USE proves_db;
CREATE TABLE usuaris (id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(50));

```
