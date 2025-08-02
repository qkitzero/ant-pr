FROM python:3.13-alpine
RUN apk add --no-cache git
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src/ant_pr.py /app/ant_pr.py
ENTRYPOINT ["python", "/app/ant_pr.py"]
