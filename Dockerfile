FROM python:3.13-alpine
RUN apk add --no-cache git
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /app/src
ENV PYTHONPATH=/app/src
ENTRYPOINT ["python", "-m", "ant_pr.main"]
