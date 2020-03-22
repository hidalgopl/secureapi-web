FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -qq -y build-essential libpq-dev postgresql-client python3-cffi --no-install-recommends

RUN addgroup --system django \
    && adduser  --system --group django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start
COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/start"]
