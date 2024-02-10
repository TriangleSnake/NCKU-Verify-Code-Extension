FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=127.0.0.1
ENV FLASK_RUN_PORT=5001

CMD ["flask","run"]
