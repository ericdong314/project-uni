FROM python:3.14-slim
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install "django<6" whitenoise gunicorn
COPY src /src
WORKDIR /src
CMD ["gunicorn", "--bind", ":8888", "uni.wsgi:application"]