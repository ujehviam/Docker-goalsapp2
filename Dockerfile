FROM python:3.13.7-alpine3.22 

WORKDIR /Docker-goalsApp2

COPY Backend/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "Backend/app.py" ]