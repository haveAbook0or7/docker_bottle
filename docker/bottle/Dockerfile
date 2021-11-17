FROM frolvlad/alpine-python3

RUN mkdir -p /usr/src/app
ADD ./src /usr/src/app
RUN pip install bottle
RUN pip install requests
RUN pip install mysql-connector-python
RUN pip install Beaker

WORKDIR /usr/src/app
EXPOSE 5000

CMD ["python3", "app.py"]