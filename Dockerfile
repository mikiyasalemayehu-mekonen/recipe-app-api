FROM python:3.9-slim
LABEL maintainer="Miki Liland"

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip

ARG DEV=false
RUN /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp

COPY ./app /app
WORKDIR /app

# Comment out or remove the non-root user for development
# RUN useradd --system --no-create-home django-user

ENV PATH="/py/bin:$PATH"

# Don't switch to non-root user in development
# USER django-user

EXPOSE 8000