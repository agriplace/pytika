FROM python:3.7-alpine

# Install poetry
ENV POETRY_HOME=/etc/poetry
ENV PATH="/etc/poetry/bin:$PATH"

RUN apk add --no-cache --virtual .build-deps \
        libffi postgresql musl libxml2 libxslt jpeg zlib libcurl cargo \
        gcc g++ openssl-dev libffi-dev postgresql-dev musl-dev \
        libxml2-dev libxslt-dev jpeg-dev zlib-dev curl curl-dev python3-dev

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.2.2

# Install dependencies in first step to make use of caching
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --with dev

# Now we just copy in files so that test layer can be cached
COPY . .

# Setup host and port for Tika
ENV TIKA_HOST=localhost
ENV TIKA_PORT=9998
