#!/bin/bash
set -e

# ============================================
# Скрипт деплоя Stael Di на Ubuntu VPS
# Запускать от root: bash setup_server.sh
# ============================================

DOMAIN="staeldi.uz"
PROJECT_DIR="/home/door/site"
DB_NAME="door_db"
DB_USER="door_user"
DB_PASSWORD="$(openssl rand -base64 16)"
SECRET_KEY="$(openssl rand -base64 50 | tr -dc 'a-zA-Z0-9!@#$%^&*' | head -c 50)"

echo "========================================="
echo "  Деплой Stael Di на $DOMAIN"
echo "========================================="

# 1. Обновление системы
echo "[1/10] Обновление системы..."
apt update && apt upgrade -y

# 2. Установка пакетов
echo "[2/10] Установка пакетов..."
apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib \
    nginx \
    git curl ufw \
    libpq-dev \
    certbot python3-certbot-nginx

# 3. Настройка PostgreSQL
echo "[3/10] Настройка PostgreSQL..."
systemctl start postgresql
systemctl enable postgresql

sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "БД уже существует"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || echo "Пользователь уже существует"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'Asia/Tashkent';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"

echo "  PostgreSQL настроен. Пароль БД: $DB_PASSWORD"

# 4. Создание пользователя
echo "[4/10] Создание пользователя door..."
id -u door &>/dev/null || useradd -m -s /bin/bash door
usermod -aG www-data door

# 5. Клонирование проекта
echo "[5/10] Клонирование проекта..."
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR"
    sudo -u door git pull origin main
else
    sudo -u door git clone https://github.com/defffffender/door.git "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# 6. Настройка виртуального окружения
echo "[6/10] Настройка виртуального окружения..."
sudo -u door python3 -m venv "$PROJECT_DIR/venv"
sudo -u door "$PROJECT_DIR/venv/bin/pip" install --upgrade pip
sudo -u door "$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

# 7. Создание .env файла
echo "[7/10] Создание .env файла..."
cat > "$PROJECT_DIR/.env" << EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,77.83.206.183
DATABASE_URL=postgres
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432
CSRF_TRUSTED_ORIGINS=http://$DOMAIN,https://$DOMAIN,http://www.$DOMAIN,https://www.$DOMAIN,http://77.83.206.183
EOF
chown door:door "$PROJECT_DIR/.env"

# 8. Django: миграции, контент, статика
echo "[8/10] Django: миграции, контент, статика..."
cd "$PROJECT_DIR"
sudo -u door "$PROJECT_DIR/venv/bin/python" manage.py migrate
sudo -u door "$PROJECT_DIR/venv/bin/python" manage.py populate_content
sudo -u door "$PROJECT_DIR/venv/bin/python" manage.py collectstatic --noinput

# 9. Настройка Gunicorn
echo "[9/10] Настройка Gunicorn..."
mkdir -p /var/log/gunicorn
chown door:www-data /var/log/gunicorn

cp "$PROJECT_DIR/deploy/gunicorn.service" /etc/systemd/system/gunicorn.service
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn

# 10. Настройка Nginx
echo "[10/10] Настройка Nginx..."
cp "$PROJECT_DIR/deploy/nginx.conf" "/etc/nginx/sites-available/$DOMAIN"
ln -sf "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl restart nginx
systemctl enable nginx

# Firewall
echo "Настройка фаервола..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo ""
echo "========================================="
echo "  ДЕПЛОЙ ЗАВЕРШЁН УСПЕШНО!"
echo "========================================="
echo ""
echo "  Сайт: http://$DOMAIN"
echo "  IP: http://77.83.206.183"
echo ""
echo "  Админ-панель: http://$DOMAIN/panel/"
echo "  Логин: admin"
echo "  Пароль: admin123"
echo ""
echo "  PostgreSQL:"
echo "  БД: $DB_NAME"
echo "  Пользователь: $DB_USER"
echo "  Пароль: $DB_PASSWORD"
echo ""
echo "  ВАЖНО: Смените пароли после деплоя!"
echo ""
echo "  Для SSL сертификата выполните:"
echo "  certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo "========================================="
