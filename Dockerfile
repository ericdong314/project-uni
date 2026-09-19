FROM python:3.14-slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY src /src
WORKDIR /src

RUN chmod +x /src/entrypoint.sh

RUN adduser --uid 1234 nonroot

ENTRYPOINT ["/src/entrypoint.sh"]
CMD ["gunicorn", "-c", "./gunicorn.conf.py"]
