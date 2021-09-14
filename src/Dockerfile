FROM debian:10-slim

ARG MCCORTEX_VERSION='geno_kmer_count'

RUN apt update
RUN apt install -y --no-install-recommends python3-dev python3-pip git wget build-essential cmake zlib1g-dev
RUN pip3 install -U pip setuptools wheel

# Install Mykrobe for variant search
WORKDIR /usr/src
RUN git clone --branch feature/background-db-path https://github.com/Mykrobe-tools/mykrobe.git mykrobe-predictor
WORKDIR /usr/src/mykrobe-predictor
RUN git clone --recursive -b ${MCCORTEX_VERSION} https://github.com/Mykrobe-tools/mccortex && cd mccortex && make
WORKDIR /usr/src/mykrobe-predictor
RUN python3 -m pip install -r requirements.txt && python3 setup.py install
RUN mykrobe panels update_metadata && mykrobe panels update_species all

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
ENV PYTHONPATH=/usr/local/lib/python3.6/site-packages/vcf

ENTRYPOINT ["python3"]
CMD ["-m", "openapi_server"]