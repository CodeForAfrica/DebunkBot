# Multi-stage build

###############################################################################
## Python base image
###############################################################################
FROM python:3.8-slim as python-base

### Env
ENV APP_HOST=.
ENV APP_DOCKER=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

### Dependencies
#### System
####  Seems like we need libpq-dev in both build and final runtime image?
####  TODO(ascii-dev): Confirm the above and update comment if true
RUN apt-get update \
    && apt-get install libpq-dev -y \
    && apt-get clean

###############################################################################
## Python builder base image
###############################################################################
FROM python-base as python-builder-base

### Dependencies
#### System
RUN apt-get install gcc python-dev -y \
    && apt-get clean \
    && pip install --upgrade pip

###############################################################################
## Python builder image
###############################################################################
FROM python-builder-base as python-builder

### Dependencies
#### Python
COPY ${APP_HOST}/requirements.txt /tmp
RUN pip install --user -r /tmp/requirements.txt

###############################################################################
## App image
###############################################################################
FROM python-base as app

### Dependencies
#### Python (copy from python-builder)
COPY --from=python-builder /root/.local /root/.local

### Env
###  Seems like we need to manually add pgsql to path?
###  TODO(ascii-dev): Confirm the above and update comment if true
ENV PATH=/usr/pgsql-9.1/bin/:/root/.local/bin:$PATH

### Volumes
WORKDIR ${APP_DOCKER}
RUN mkdir media static logs
VOLUME ["${APP_DOCKER}/media/", "${APP_DOCKER}/logs/"]

### Setup app
COPY ${APP_HOST} ${APP_DOCKER}
COPY ${APP_HOST}/contrib/docker/*.sh /
RUN chmod +x /entrypoint.sh && \
    chmod +x /start.sh

### Run app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
