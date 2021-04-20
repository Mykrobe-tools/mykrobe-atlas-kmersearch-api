ARG base_image=kms

FROM $base_image

COPY test-requirements.txt ./
RUN pip3 install --no-cache-dir -r test-requirements.txt
COPY . .

RUN mkdir -p /data/classic/9000000 /data/classic/10000000

ENV INTEGRATION_TEST=true
CMD ["-m", "pytest"]