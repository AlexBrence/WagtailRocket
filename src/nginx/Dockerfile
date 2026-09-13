FROM nginx:1.27.0-alpine

# Copy both configs into a templates folder
COPY http.conf /etc/nginx/templates/http.conf
COPY https.conf     /etc/nginx/templates/https.conf
COPY entrypoint.sh  /entrypoint.sh

RUN chmod +x /entrypoint.sh \
 && mkdir -p /var/www/certbot

EXPOSE 80 443

ENTRYPOINT ["/entrypoint.sh"]