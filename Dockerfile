FROM alpine:3.17.2
EXPOSE 8000
WORKDIR /app
RUN apk add --no-cache nginx \
    && rm /etc/nginx/http.d/default.conf \
    && chmod -R 777 /var/lib/nginx/ \
    && chmod -R 777 /var/log/nginx/
USER 1001
COPY nginx.conf /etc/nginx/
COPY index.html /app/
CMD ["nginx", "-g", "daemon off;"]