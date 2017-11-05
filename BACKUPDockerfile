FROM alpine:latest
MAINTAINER matansilver@gmail.com

WORKDIR /app
COPY . .
RUN apk add --update python3
RUN pip3 install pipenv
RUN pipenv install --system
EXPOSE 5000
ENTRYPOINT ["python3", "app.py", "runserver"]