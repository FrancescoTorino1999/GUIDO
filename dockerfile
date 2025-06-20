FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
LABEL authors="benedettoscala"

RUN apt-get update && apt install -y build-essential \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y python3.11 python3-pip python3-dev python3-venv git

FROM python:3.11

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Clona TOAD
RUN git clone https://github.com/GuidaStefano/TOAD.git /app/TOAD

# Copia tutto il tuo progetto
COPY . /app

# Copia e rendi eseguibile lo script orchestratore
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Installa dipendenze
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
RUN pip install -r /app/TOAD/requirements.txt
RUN pip install Flask

EXPOSE 5005

CMD ["/app/run.sh"]
