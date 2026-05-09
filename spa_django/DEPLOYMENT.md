# Despliegue en produccion

1. Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```

   Si el entorno virtual local falla por rutas movidas o renombradas, recrealo:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Define variables de entorno usando `.env.example` como guia. No subas `.env` al repositorio.

3. Prepara la base de datos:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Publica archivos estaticos:

   ```bash
   python manage.py collectstatic --noinput
   ```

5. Ejecuta la aplicacion con WSGI:

   ```bash
   gunicorn config.wsgi:application
   ```

6. Antes de abrir al publico, valida la configuracion:

   ```bash
   python manage.py check --deploy
   ```

En produccion, sirve `MEDIA_ROOT` con el servidor web o con almacenamiento externo. WhiteNoise sirve los archivos estaticos recolectados en `staticfiles/`.
