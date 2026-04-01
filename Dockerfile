FROM postgres:16.13

ENV POSTGRES_USER=psotgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=speedrun

EXPOSE 5432

VOLUME [ "/var/lib/postgresql/data" ]