ARG base_image=kms

FROM $base_image

COPY test-requirements.txt ./
RUN pip3 install --no-cache-dir -r test-requirements.txt
COPY . .

ENV INTEGRATION_TEST=true
CMD ["-m", "pytest", "-s"]