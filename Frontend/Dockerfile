FROM nginx:1.28.0-alpine-slim

WORKDIR /usr/share/nginx/html

RUN rm -rf /usr/share/nginx/html/*

COPY . /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80


