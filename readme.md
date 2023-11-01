# 2023 COMP6841 My awesome project
## Overview of attacks
Players may find that they can perform a bunch of cyber attackers to this vulnerable website. All the attacks can be found in OWASP top 10 [OWASP TOP10](https://owasp.org/www-project-top-ten/).
1. SQL Injection
···* Warm up, can you print out all users' names and passwords?
···* Shhhhh... there's a top secret in this website...
2. XSS (stored & reflected)
···* Stored XSS: typically refering to the XSS attack where malicious scripts are stored in the server(database), and executed on the user's browser.
···* Reflected XSS: unlike the stored XSS executing on the user's server, a reflected XSS attack executes on the server. Can you perform both XSS on /view-course page?
3. Broken access control
4. CSRF


## Structure
The website is built from Python3 flask as the backend, with html/css frontend and postgreSQL database. Most of the frontend template is from [https://github.com/bearlike/Pixel-Portfolio-Webite].


## Getting started
```
mkdir myctf
cd myctf
git clone git@github.com:4Christinelh4/CTF.git
```
### Running pgsql in docker
To make player's life easier and to let them focus more on attacking the website, the pgsql database is on docker. Players do not need to install and config pgsql on their machines. Follow the steps:

1. Download and install docker on your machine [docker](https://www.docker.com/)
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

### Start the server
```
pip3 install -r ctf/requirements.txt
python3 ctf/app.py 5044
```
*Note that in previous step, port 5432 (the port where pgsql in docker is listening on) maps to port 5044 on host machine.*


## Spoiler alert 😈
### 🌶 SQL injection 1
### 🥓 SQL injection 2
### 🚨 CSRF
### 🛸 Reflected XSS
