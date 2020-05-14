# The build image
FROM python:3.8.0-slim as builder
RUN apt-get update \
    && apt-get install gcc python-dev libpq-dev -y \
    && apt-get clean

COPY ./requirements.txt /app/requirements.txt
WORKDIR app
RUN pip install --upgrade pip \
    && pip install --user -r requirements.txt

COPY . /app

# The app image
FROM python:3.8.0-slim as app
RUN apt-get update && apt-get install libpq-dev -y
ENV PATH=/usr/pgsql-9.1/bin/:/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /src
WORKDIR src
COPY ./contrib/docker/start.sh /start.sh
COPY ./contrib/docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh && \
    chmod +x /start.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
