FROM nginx:latest

RUN rm /etc/nginx/nginx.conf
COPY ./config/nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf

COPY ./config/solar-backend.conf /etc/nginx/conf.d/
