FROM debian:10-slim

RUN apt update
RUN apt install -y --no-install-recommends python3-dev python3-pip

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir cobs_index

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT ["python3"]
CMD ["-m", "openapi_server"]