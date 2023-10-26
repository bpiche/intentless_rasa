FROM python:3.10

ARG UID=1005
ARG GID=1005

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y

RUN addgroup --gid $GID gate && \
    adduser --uid $UID --gid $GID gate

RUN chown gate /usr/local/bin

USER gate

WORKDIR /app

COPY --chown=gate ./requirements.txt ./requirements.txt

RUN python3 -m pip install --user -r ./requirements.txt

COPY --chown=gate . /app/

EXPOSE 5000
CMD ["python3", "main.py"]