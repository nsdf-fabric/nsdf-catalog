FROM docker.io/yandex/clickhouse-server

RUN mkdir app
WORKDIR /app

#ENV PATH="${PATH}:/root/.local/bin"
#ENV PYTHONPATH=.

COPY etc/clickhouse-server/config.d/enable_postgresql_interface.xml /etc/clickhouse-server/config.d
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt

#COPY src/ .
