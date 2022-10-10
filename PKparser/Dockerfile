FROM python:3.8

RUN mkdir -p usr/src/app
WORKDIR usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY __init__.py config.ini main.py parser.py db_locations.py ./

#EXPOSE 27017

CMD python main.py -r n