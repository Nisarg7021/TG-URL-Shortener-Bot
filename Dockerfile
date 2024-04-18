FROM python:3.10-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
RUN pip install domainer
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /TG-URL-Shortener-Bot
WORKDIR /TG-URL-Shortener-Bot
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
