FROM python:3.14-slim AS base
RUN apt-get update && apt-get install -y gosu postgresql-client
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements/base.txt /tmp/requirements/base.txt
RUN pip install -r /tmp/requirements/base.txt
COPY src /src
WORKDIR /src

FROM base AS dev
COPY requirements/dev.txt /tmp/requirements/dev.txt
RUN pip install -r /tmp/requirements/dev.txt

FROM base AS prod
RUN chmod +x /src/entrypoint.sh
RUN adduser --uid 1234 nonroot