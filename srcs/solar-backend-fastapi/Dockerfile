FROM python:3.12

WORKDIR /usr/src

COPY config/requirements.txt ./config/
RUN pip install --no-cache-dir -r config/requirements.txt

COPY . .