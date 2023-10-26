FROM python:3.10

ARG UID=1005
ARG GID=1005

RUN addgroup --gid $GID util && \
    adduser --uid $UID --gid $GID util

RUN chown util /usr/local/bin

USER util

WORKDIR /app

COPY --chown=util ./requirements.txt ./requirements.txt

RUN python3 -m pip install --user -r ./requirements.txt

COPY --chown=util . /app/

EXPOSE 5006
CMD ["python3", "main.py"]