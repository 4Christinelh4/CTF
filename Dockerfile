FROM python:3.11

EXPOSE 5000
RUN apt-get -q -y update && apt-get install -y gcc
ENV WORKING_DIR=/app
WORKDIR ${WORKING_DIR}

COPY . /app
RUN pip3 install -r /app/ctf/requirements.txt
CMD python3 /app/ctf/app.py

