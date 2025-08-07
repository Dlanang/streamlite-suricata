#!/bin/bash
if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

if [ -z "$DOMAIN" ]; then
  echo "Please set DOMAIN environment variable."
  exit 1
fi

read -p "Email for Let's Encrypt registration: " email

mkdir -p "./deployment/certbot/conf/live/$DOMAIN"

docker-compose run --rm --entrypoint "\
  certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  --email $email \
  --agree-tos \
  --no-eff-email \
  -d $DOMAIN" certbot
