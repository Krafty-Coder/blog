FROM ubuntu:16.04
MAINTAINER Krafty Coder "kraftycoder@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY ./ ./app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install Flask-MySQLdb
ENTRYPOINT ["python"]
CMD ["run.py"]
