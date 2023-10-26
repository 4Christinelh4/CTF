# 2023 COMP6841 My awesome project

## overview of attacks
Players may find that they can perform a bunch of cyber attackers to this vulnerable website:
1. a couple of SQL injections
2. XSS (stored & reflected)
3. Broken access control

## structure
The website is built on Flask, python3, with html/css frontend and postgreSQL database.

## running pgsql in docker
To make player's life easier and to let them focus more on attacking the website, the pgsql database is on docker. Players do not need to install and config pgsql on their machines. Follow the steps:

1. Download and install docker on your machine https://www.docker.com/
2. Build docker image
```
[docker build -t <image name> <path to the directory where the Dockerfile is in>]
docker build -t pgsqldocker .
```
3. Create the container
```
[docker run -d --name <name of your container> -p <host port:container port> <name of the image>]
docker run -d --name pgsqlctf -p 5044:5432 pgsqldocker
```
4. Go in the container as user postgres, where there the database is
```
docker exec -it pgsqlctf psql -U postgres
```
