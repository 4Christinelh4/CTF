FROM postgres:13
EXPOSE 5432
COPY ./init_table.sql /docker-entrypoint-initdb.d/init.sql

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres


