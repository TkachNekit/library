FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends make && \
    apt-get clean && apt-get autoclean

# dynamic layer 2: app workdir files
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

RUN python3 manage.py makemigrations && python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

