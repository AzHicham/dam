# syntax=docker/dockerfile:1.9

FROM python:3.12-slim-bullseye AS python-requirements

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install poetry

WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export -f requirements.txt --output /tmp/requirements.txt --without-hashes

ENV PATH="/opt/venv/bin:$PATH"

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    python3 -m venv /opt/venv && \
    pip3 install -r /tmp/requirements.txt


FROM python:3.12-slim-bullseye AS production

RUN mkdir -p /opt/logs /data/cache

COPY --from=python-requirements /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /opt/damae/
COPY app /opt/damae/app
COPY settings.toml /opt/damae/settings.toml

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

