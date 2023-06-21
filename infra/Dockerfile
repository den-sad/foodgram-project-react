
FROM nginx:1.19.3
WORKDIR /usr/share/nginx/html
COPY ./infra/nginx.conf /etc/nginx/conf.d/default.conf
RUN mkdir -p /usr/share/nginx/api/data
COPY ./docs /usr/share/nginx/api/docs
