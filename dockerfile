FROM python:3.10-alpine

WORKDIR /app
COPY . .
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt

CMD ["python main.py"]