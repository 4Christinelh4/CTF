
FROM python:3.11

EXPOSE 5000
RUN apt-get -q -y update && apt-get install -y gcc
ENV WORKING_DIR=/home/ctf-app
WORKDIR ${WORKING_DIR}

COPY . ctf
COPY requirements.txt .

RUN pip3 install -r requirements.txt
CMD python3 ctf/app.py

