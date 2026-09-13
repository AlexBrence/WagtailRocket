#!/bin/bash

### You need to run this script one time only ###
docker compose run --rm --entrypoint certbot certbot certonly \
  --webroot -w /var/www/certbot \
  -d <CHANGE_ME>.com -d www.<CHANGE_ME>.com \
  --email CHANGE_ME@email_provider.com \
  --agree-tos --no-eff-email --non-interactive
