FROM alpine:latest
MAINTAINER matansilver@gmail.com

WORKDIR /app
COPY . .
RUN apk add --update python3 nodejs=6.9.5-r1
RUN node --version
RUN pip3 install pipenv
RUN pipenv install --system
RUN npm install gulp -g
RUN npm install gulp
RUN npm install
RUN gulp sass
EXPOSE 5000

CMD [ "python3", "app.py", "runserver" ]
#ENTRYPOINT ["python3","app.py","runserver"]