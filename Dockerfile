FROM postgres:15

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-15-pgvector \
    postgresql-15-postgis \
    postgresql-15-cron \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5432

CMD ["postgres"]