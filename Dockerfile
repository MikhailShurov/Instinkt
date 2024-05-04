FROM python:3.11

WORKDIR /app

COPY requirements/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x scripts/*.sh
