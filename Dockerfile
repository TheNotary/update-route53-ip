FROM ruby:latest

RUN gem install fpm

RUN apt-get update && apt-get install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY . /build

ARG PKG_NAME
ARG DESCRIPTION
ARG VERSION
ARG ARCHITECTURE=all

RUN ./build_package.sh
