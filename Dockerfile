FROM apache/flink:1.17.1-scala_2.12-java11


COPY . /app
WORKDIR /app

RUN pip install python-dotenv
