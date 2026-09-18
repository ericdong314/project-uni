FROM python:3.14-slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY src /src
WORKDIR /src

# collectstatic reads settings.py and throws an exception if an env var has no placeholder value.
RUN python manage.py collectstatic --noinput

RUN adduser --uid 1234 nonroot
USER nonroot