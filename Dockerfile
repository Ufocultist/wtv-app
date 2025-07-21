FROM python:3.11-alpine

# Install necessary dependencies for mariadb
RUN apk update && \
    apk add --no-cache mariadb-connector-c-dev gcc musl-dev && \
    apk add --no-cache libffi-dev

#RUN apt update && \
#    apt install -y mariadb-client libmariadb-dev gcc musl-dev libffi-dev

WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uwsgi", "app.ini"]