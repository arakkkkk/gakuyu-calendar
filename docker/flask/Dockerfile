FROM python:3.7

RUN pip install --upgrade pip

COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8081

CMD bash -c "python app.py"

