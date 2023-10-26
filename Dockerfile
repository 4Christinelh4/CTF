FROM postgres:13
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB comp6841db
COPY init_table.sql /docker-entrypoint-initdb.d/