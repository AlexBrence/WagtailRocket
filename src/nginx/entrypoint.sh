#!/bin/sh
set -e

DOMAIN="wagtailrocket.com"
CERT_FILE="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"

mkdir -p /var/www/certbot

if [ -f "$CERT_FILE" ]; then
  echo ">>> SSL certificate found → enabling HTTPS"
  cp /etc/nginx/templates/https.conf /etc/nginx/conf.d/default.conf
else
  echo ">>> No SSL certificate found → running in HTTP mode"
  cp /etc/nginx/templates/http.conf /etc/nginx/conf.d/default.conf
fi

exec nginx -g "daemon off;"