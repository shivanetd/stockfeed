FROM python:3.12.1

RUN apt-get update
RUN apt-get install -y --no-install-recommends

WORKDIR /stockfeed

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD [ "python", "main.py" ]
