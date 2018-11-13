FROM alpine:latest
MAINTAINER matansilver@gmail.com

WORKDIR /app
COPY . .
RUN apk add --update python3 nodejs
RUN node --version
RUN pip3 install pipenv
RUN pipenv install --system
RUN npm install gulp -g
RUN npm install
RUN gulp sass
EXPOSE 5000

#CMD [ "gunicorn" "app:app"]
ENTRYPOINT ["gunicorn","app:app"]
