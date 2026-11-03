# Guia de Desplegament del Projecte

Com desplegar el projecte pas a pas:

## 1. Crear i activar un nou entorn virtual

```bash
python -m venv venv
```

* **En Windows:**
  ```cmd
  venv\Scripts\activate
  ```

* **En macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

## 2. Instal·lar totes les dependències automàticament

```bash
pip install -r requirements.txt
```

## 3. Executar l'aplicació

```bash
python main.py
```
*(o el fitxer principal corresponent)*