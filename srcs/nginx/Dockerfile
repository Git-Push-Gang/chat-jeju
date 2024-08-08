FROM nginx
COPY ./config/nginx.conf /etc/nginx/nginx.conf
COPY ./html/index.html /usr/share/nginx/html/index.html

ENTRYPOINT ["nginx", "-g", "daemon off;"]