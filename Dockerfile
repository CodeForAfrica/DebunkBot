# Multi-stage build

###############################################################################
## Python base image
###############################################################################
FROM python:3.8-slim AS python-base

### Env
ENV APP_HOST=.
ENV APP_DOCKER=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

### Dependencies
#### System
####  We need libpq-dev in both build and final runtime image
RUN apt-get update \
    && apt-get install libpq-dev --no-install-recommends -y \
    && apt-get clean

###############################################################################
## Python builder base image
###############################################################################
FROM python-base AS python-builder-base

### Dependencies
#### System
RUN apt-get install gcc python-dev --no-install-recommends -y \
    && apt-get clean \
    && pip install --upgrade pip

###############################################################################
## Python builder image

FROM python-builder-base AS python-builder

### Dependencies
#### Python
COPY ${APP_HOST}/requirements.txt /tmp
RUN pip install --user -r /tmp/requirements.txt

###############################################################################
## App image
###############################################################################
FROM python-base AS app

### Dependencies
#### Python (copy from python-builder)
COPY --from=python-builder /root/.local /root/.local

### Env
ENV PATH=/root/.local/bin:$PATH

# Expose server port
EXPOSE 8000

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
