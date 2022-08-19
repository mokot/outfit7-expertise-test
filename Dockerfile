# Select ubuntu
FROM ubuntu:latest

# Install all required packages
RUN \
  apt update && \
  apt install python3 -y && \
  apt install python3-pip -y && \
  apt install libpq-dev python3-dev -y

WORKDIR /app

# Install python dependencies
COPY requirements.pip.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python3", "./app/main.py"]