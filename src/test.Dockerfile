FROM kms

RUN pip3 install pytest hypothesis

ENTRYPOINT ["pytest"]