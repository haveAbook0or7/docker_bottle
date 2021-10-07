FROM frolvlad/alpine-python3

RUN mkdir -p /usr/src/app
ADD ./src /usr/src/app
RUN pip install bottle
RUN pip install requests

WORKDIR /usr/src/app
EXPOSE 5000