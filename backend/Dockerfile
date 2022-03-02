FROM python:alpine3.15
ENV PYTHONUNBUFFERED=1
ARG APP_PATH
WORKDIR $APP_PATH
ADD ./requirements.txt requirements.txt
RUN apk add --update --no-cache curl && pip install psycopg2-binary && pip install -r requirements.txt
ADD . .
ARG APP_MODE
ARG APP_PORT
ENV FLASK_APP=backend.py
ENV FLASK_ENV=$APP_MODE
ENV APP_PORT=$APP_PORT
CMD python $FLASK_APP