
FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD ./app .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
