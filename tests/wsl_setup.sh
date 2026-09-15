#!/bin/bash
# Installs ownCloud 10 from the Laragon copy into WSL and serves it on :8023.
# Run as root inside WSL Ubuntu 20.04:
#   wsl -d Ubuntu-20.04 -u root -e bash /mnt/c/Users/tomku/PycharmProjects/asyntai/plugins/owncloud/tests/wsl_setup.sh
set -e

SRC=/mnt/c/laragon/www/owncloud10
DST=/var/www/owncloud
PORT=8023

# The rig's own admin password. Set OC_ADMIN_PASS before you run this, and use
# the same value when you run the tests.
if [ -z "$OC_ADMIN_PASS" ]; then
    echo "Set OC_ADMIN_PASS first, for example: OC_ADMIN_PASS=... bash $0"
    exit 1
fi

if [ ! -f "$DST/config/config.php" ]; then
    rm -rf "$DST"
    cp -r "$SRC" "$DST"
    mkdir -p "$DST/data"
    chown -R www-data:www-data "$DST"
    cd "$DST"
    sudo -u www-data php occ maintenance:install --database sqlite \
        --admin-user admin --admin-pass "$OC_ADMIN_PASS" --data-dir "$DST/data" | tail -2
    sudo -u www-data php occ config:system:set trusted_domains 1 --value="localhost:$PORT"
    sudo -u www-data php occ config:system:set overwrite.cli.url --value="http://localhost:$PORT"
fi

cat > /etc/apache2/sites-available/owncloud.conf <<EOF
Listen $PORT
<VirtualHost *:$PORT>
    DocumentRoot $DST
    <Directory $DST>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF
a2enmod rewrite headers env dir mime >/dev/null
a2ensite owncloud >/dev/null
a2dissite 000-default >/dev/null 2>&1 || true
apachectl -k graceful 2>/dev/null || apachectl -k start 2>&1 | grep -v AH00558 || true
sleep 2
echo "login page: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:$PORT/login)"
