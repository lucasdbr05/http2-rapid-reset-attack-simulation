FROM nginx:stable

COPY nginx-vulnerable.conf /etc/nginx/nginx.conf
COPY create-certs.sh /etc/nginx/create-certs.sh

RUN chmod +x /etc/nginx/create-certs.sh && /etc/nginx/create-certs.sh

CMD ["nginx", "-g", "daemon off;"]