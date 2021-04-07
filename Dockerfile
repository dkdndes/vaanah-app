FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache --virtual .tmp gcc g++ libc-dev linux-headers zlib-dev jpeg-dev musl-dev libpq postgresql-dev postgresql-libs make openssl-dev libpq
RUN pip install --upgrade pip
RUN pip install --upgrade wheel
RUN pip install --ignore-installed pillow
RUN pip install psycopg2
RUN pip install psycopg2-binary
RUN pip install -r /requirements.txt
RUN apk del .tmp
RUN mkdir /app

COPY . /app

WORKDIR /app

COPY ./scripts /scripts

RUN chmod +x /scripts/*
RUN adduser -D user

USER user

CMD ["entrypoint.sh"]

EXPOSE 8080

# FROM python:3.8

# ENV PYTHONUNBUFFERED 1

# ENV APP_ROOT /vaanah-app

# WORKDIR ${APP_ROOT}

# RUN apt-get update

# RUN pip3 install -U pip

# COPY requirements.txt ${APP_ROOT}/requirements.txt

# RUN pip3 install -r ${APP_ROOT}/requirements.txt

# # Set the working directory to /app
# WORKDIR ${APP_ROOT}

# # Copy the current directory contents into the container at /app
# ADD . ${APP_ROOT}

# RUN chmod 775 -R ${APP_ROOT}

# CMD  ['python manage.py', '&&', '/bin/sh','-c','python manage.py runserver']

# EXPOSE 8080