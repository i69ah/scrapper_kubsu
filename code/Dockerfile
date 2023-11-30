FROM python:3.11.4

WORKDIR /app/code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y netcat-traditional

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /app/code/entrypoint.sh

COPY .. .

ENTRYPOINT ["/app/code/entrypoint.sh"]