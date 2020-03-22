FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -qq -y build-essential libpq-dev postgresql-client python3-cffi --no-install-recommends

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY . /app

WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["/entrypoint"]
