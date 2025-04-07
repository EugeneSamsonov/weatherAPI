FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt upgrade && pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000/tcp

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]