FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt install -y build-essential \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa

RUN apt-get install -y libfreetype6-dev libpng-dev
ENV MPLLOCALFREETYPE=1

RUN apt-get update && apt-get install -y python3.8
RUN apt-get install -y python3-pip python3-dev python3-venv python3-wheel
ENV PATH="/usr/bin/python3.8:${PATH}"

RUN apt-get install -y openjdk-8-jdk
ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:${PATH}"

RUN apt-get update && apt-get install -y git
ENV PATH="/usr/bin/git:${PATH}"

RUN mkdir /app
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN git clone https://github.com/benedettoscala/csDetector.git /tmp/temporary_directory

RUN mv /tmp/temporary_directory/* .
RUN rm -rf /tmp/temporary_directory

RUN git clone https://github.com/carlovend/CADOCS_II.git
RUN git clone https://github.com/leotodisco/culture-inspector.git

RUN python3.8 -m pip install --upgrade pip setuptools wheel
RUN python3.8 -m pip install --upgrade pip


RUN python3.8 -m pip install -r CADOCS_II/requirements.txt
RUN python3.8 -m pip install -r culture-inspector/requirements.txt
RUN python3.8 -m pip install -r requirements.txt


RUN python3.8 -m pip install spacy
RUN python3.8 -m spacy download en_core_web_sm

RUN echo "import nltk;" > nltk_setup.py \
    && echo "nltk.download('punkt')" >> nltk_setup.py \
    && python3.8 nltk_setup.py


ENV PAT='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'
ENV CSDETECTOR_URL_GETSMELLS='http://127.0.0.1:5001/getSmells'
ENV GEODISPERSION_URL='http://127.0.0.1:5004/compute_std_dev'

# Copia lo script nel container
COPY /run.sh /app/run.sh

# Rende lo script eseguibile
RUN chmod +x /app/run.sh


EXPOSE 5005
# Esegue lo script quando il container viene eseguito
CMD ["/app/run.sh"]

FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Installazione pacchetti base
RUN apt-get update && \
    apt-get install -y build-essential software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.8 python3-pip python3-venv python3-dev python3-wheel openjdk-8-jdk git libfreetype6-dev libpng-dev && \
    apt-get clean

# Variabili ambiente
ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

# Creazione cartelle
RUN mkdir -p /app/TOAD
WORKDIR /app/TOAD

# Clona TOAD
RUN git clone https://github.com/GuidaStefano/TOAD.git /app/TOAD

# Installa dipendenze TOAD
RUN python3.8 -m pip install --upgrade pip setuptools wheel
RUN python3.8 -m pip install -r requirements.txt
RUN python3.8 -m pip install Flask

# Copia il server wrapper
COPY server.py /app/TOAD/server.py

# Espone la porta del servizio API
EXPOSE 5000

# Avvio server TOAD wrapper
CMD ["python3.8", "server.py"]
