FROM debian:10-slim

RUN apt update
RUN apt install -y --no-install-recommends python3-dev python3-pip git wget build-essential
RUN pip3 install -U pip setuptools

## Install Mykrobe for variant search
WORKDIR /usr/src
RUN git clone https://github.com/Mykrobe-tools/mykrobe.git
WORKDIR mykrobe
RUN git checkout cee6b8159eb313e98a95934cb662593698c76385
RUN wget -O mykrobe-data.tar.gz https://bit.ly/2H9HKTU && tar -zxvf mykrobe-data.tar.gz && rm -fr src/mykrobe/data && mv mykrobe-data src/mykrobe/data
RUN pip3 install .

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT ["python3"]
CMD ["-m", "openapi_server"]