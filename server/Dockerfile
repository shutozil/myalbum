FROM python:3.9.7

# Pillow 10系はtextsizeが使えない
RUN pip3 install \
    "boto3" \
    "cryptography"

RUN pip3 install awscli --upgrade

WORKDIR /project
