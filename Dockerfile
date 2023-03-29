FROM alpine:3.17.2
EXPOSE 8000
WORKDIR /app
RUN apk add --no-cache nginx \
    && rm /etc/nginx/http.d/default.conf \
    && chmod -R 777 /var/lib/nginx/ \
    && chmod -R 777 /var/log/nginx/
RUN echo $' \n\
pid       /tmp/nginx.pid; \n\
error_log /dev/stdout; \n\
\n\
events { \n\
} \n\
http { \n\
    server { \n\
        listen       8000; \n\
        server_name  localhost; \n\
        access_log /dev/stdout; \n\
        client_body_temp_path /tmp/client_body; \n\
        fastcgi_temp_path /tmp/fastcgi_temp; \n\
        proxy_temp_path /tmp/proxy_temp; \n\
        scgi_temp_path /tmp/scgi_temp; \n\
        uwsgi_temp_path /tmp/uwsgi_temp; \n\
        location / { \n\
          root /app; \n\
          index  index.html index.htm; \n\
        } \n\
    } \n\
}' > /etc/nginx/nginx.conf
#COPY nginx.conf /etc/nginx/
#COPY index.html /app/
USER 1001
CMD ["nginx", "-g", "daemon off;"]