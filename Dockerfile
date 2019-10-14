FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV LISTEN_PORT=5000
EXPOSE 5000

ENV UWSGI_INI uwsgi.ini

WORKDIR /app
ADD . /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt