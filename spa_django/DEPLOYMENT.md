# Despliegue en Azure VM Debian

Este proyecto mantiene `config/settings.py` para desarrollo local y usa
`config/settings_prod.py` para produccion.

## 1. Paquetes del sistema

Instala Python 3.12 o superior para Django 6, ademas de Nginx y librerias para
compilar `mysqlclient`:

```bash
sudo apt update
sudo apt install nginx build-essential default-libmysqlclient-dev pkg-config
```

Si tu Debian no trae Python 3.12+, instalalo antes de crear el entorno virtual.

## 2. Proyecto

Clona o copia el proyecto en `/srv/spa_django`:

```bash
cd /srv/spa_django
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Variables de entorno

Crea `/etc/spa_django.env` tomando `.env.example` como guia:

```bash
DJANGO_SETTINGS_MODULE=config.settings_prod
DJANGO_SECRET_KEY=una-clave-larga-y-secreta
DJANGO_ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,IP_PUBLICA
DJANGO_CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
DB_ENGINE=django.db.backends.mysql
DB_NAME=spa_db
DB_USER=spa_user
DB_PASSWORD=tu-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

## 4. Base de datos y estaticos

```bash
set -a
source /etc/spa_django.env
set +a
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py check --deploy
```

## 5. Gunicorn

Copia `deploy/gunicorn.service.example`:

```bash
sudo cp deploy/gunicorn.service.example /etc/systemd/system/spa_django.service
sudo systemctl daemon-reload
sudo systemctl enable --now spa_django
sudo systemctl status spa_django
```

## 6. Nginx

Copia `deploy/nginx.conf.example`, cambia `server_name` y activa el sitio:

```bash
sudo cp deploy/nginx.conf.example /etc/nginx/sites-available/spa_django
sudo ln -s /etc/nginx/sites-available/spa_django /etc/nginx/sites-enabled/spa_django
sudo nginx -t
sudo systemctl reload nginx
```

En Azure abre los puertos 80 y 443 en el Network Security Group de la VM.

## 7. HTTPS

Cuando el dominio apunte a la VM, instala Certbot y emite el certificado:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Nginx sirve `media/` y `staticfiles/`. Gunicorn solo ejecuta Django.
