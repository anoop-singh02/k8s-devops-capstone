FROM nginx:1.30-alpine
# nginx worker processes drop privileges; listening on 8080 (not 80)
# lets the pod run without NET_BIND_SERVICE.
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 8080
