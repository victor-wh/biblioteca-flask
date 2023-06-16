## Instalación

1. Crear entorno

```
 virtualenv venv --python=python3.10
```

2. Instalar requerimientos

```
pip install -r requirements.txt
```

3. Exportar variables

```
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development
```

4. Iniciar proyecto

```
flask run
```