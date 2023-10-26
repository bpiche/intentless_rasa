FROM rasa/rasa:3.6.13

WORKDIR /app/

COPY requirements.txt /app/

COPY training/ /app/

USER root

RUN pip install -r requirements.txt

CMD ["run", "--enable-api"]

USER 1001