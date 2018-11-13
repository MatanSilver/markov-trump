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
EXPOSE 80

#CMD [ "python3", "app.py", "runserver" "--port=5000"]
ENTRYPOINT ["python3","app.py","runserver","--port=5000"]
