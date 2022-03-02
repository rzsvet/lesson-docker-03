FROM nginx:1.21-alpine
COPY ./index.html /usr/share/nginx/html
COPY ./default.conf /etc/nginx/conf.d/default.conf
ARG APP_MODE
ARG APP_PORT
RUN apk add --update --no-cache curl && sed -i 's/{{ mode }}/'"$APP_MODE"'/g' /usr/share/nginx/html/index.html && sed -i 's/{{ APP_PORT }}/'"$APP_PORT"'/g' /etc/nginx/conf.d/default.conf