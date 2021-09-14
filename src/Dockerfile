FROM debian:10-slim

RUN apt update
RUN apt install -y --no-install-recommends python3-dev python3-pip git wget build-essential cmake zlib1g-dev
RUN pip3 install -U pip setuptools wheel

# Install Mykrobe for variant search
WORKDIR /usr/src
RUN git clone https://github.com/Mykrobe-tools/mykrobe.git
WORKDIR mykrobe
RUN git checkout feature/background-db-path
RUN pip3 install requests && pip3 install . && mykrobe panels update_metadata && mykrobe panels update_species all

# Install COBS
WORKDIR /usr/src
RUN git clone --recursive https://github.com/iqbal-lab-org/cobs.git
WORKDIR cobs/build
RUN cmake .. && make
WORKDIR ..
RUN pip install .

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install .

ENV COBS_FALSE_POSITIVE_RATE=0.3
ENV DEBUG=0

ENTRYPOINT ["python3"]
CMD ["-m", "openapi_server"]