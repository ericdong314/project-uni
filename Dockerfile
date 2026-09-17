FROM python:3.14-slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY src /src
WORKDIR /src

RUN python manage.py collectstatic --noinput # Error if placed after the setting of DJANGO_DEBUG_FALSE.
ENV DJANGO_DEBUG_FALSE=1

RUN adduser --uid 1234 nonroot
USER nonroot

#CMD ["gunicorn", "--bind", ":8888", "uni.wsgi:application"]
# env vars are not treated as literal strings with the [] format
CMD gunicorn --certfile=$TLS_DIR/fullchain1.pem --keyfile=$TLS_DIR/privkey1.pem --bind :8888 uni.wsgi:application
