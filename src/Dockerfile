FROM debian:10-slim

RUN apt update
RUN apt install -y --no-install-recommends python3-dev python3-pip
RUN pip3 install -U pip

RUN pip3 install cobs_index

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .

CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0"]