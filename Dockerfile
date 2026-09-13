FROM python:3.14-slim
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install "django<6" "whitenoise"
COPY src /src
WORKDIR /src
CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]