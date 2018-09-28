FROM python:3.7-alpine3.7
LABEL maintainer 'Juracy Filho <juracy at gmail.com>'

ARG VERSION=master

ENV PYTHONUNBUFFERED 1

RUN \
    apk add --no-cache unzip wget ca-certificates gcc openldap-dev binutils-libs binutils gmp isl libgomp libatomic libgcc pkgconf pkgconfig mpfr3 mpc1 libstdc++ libc-dev musl-dev mariadb-dev postgresql-dev nginx gettext jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
