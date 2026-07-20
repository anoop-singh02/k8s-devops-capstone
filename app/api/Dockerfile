# Multi-stage: build deps in a full image, run in slim as non-root.
FROM python:3.12-slim AS build
WORKDIR /install
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

FROM python:3.12-slim
RUN groupadd -r app && useradd -r -g app app
WORKDIR /srv
COPY --from=build /install/deps /usr/local
COPY app.py .
USER app
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:create_app()"]
