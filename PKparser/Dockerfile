FROM python:3.8

RUN mkdir -p usr/src/app
WORKDIR usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./PKparser/requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./PKparser/__init__.py \
    ./PKparser/config.ini \
    ./PKparser/main.py \
    ./PKparser/parser.py \
    ./PKparser/
COPY ./PKdb/db_locations.py \
    ./PKdb/__init__.py \
    ./PKdb/

CMD python ./PKparser/main.py