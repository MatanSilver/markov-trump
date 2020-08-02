FROM alpine
# init
RUN mkdir /app
WORKDIR /app
# setup
RUN adduser -D deploy
RUN apk update
RUN apk upgrade
RUN apk --no-cache add \
    python3 \
    py3-pip \
    python3-dev \
    build-base \
    gettext
RUN pip install --upgrade pip
RUN pip install gunicorn
COPY requirements.txt /app/
RUN pip install -r requirements.txt
# clean
RUN apk del -r python3-dev
# prep
COPY . /app/
CMD ["python3", "app.py"]
