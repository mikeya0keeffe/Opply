FROM python:3.9-slim-buster as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /server

RUN apt-get update && apt-get install -y build-essential

COPY ./server/requirements.txt /server/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /server/wheels -r requirements.txt

FROM python:3.9-slim-buster as runner

WORKDIR /server

RUN apt-get update && apt-get install -y netcat

COPY --from=builder /server/wheels /server/wheels
COPY --from=builder /server/requirements.txt .
RUN pip install --no-cache /server/wheels/*
RUN pip install uvicorn

COPY . /server/

EXPOSE 8000

CMD uvicorn server.app.main:app --host 0.0.0.0 --port 8000
