FROM python:3.10-slim

WORKDIR /generator

COPY requirements.txt /generator

RUN pip install --no-cache-dir -r requirements.txt

COPY . /generator

EXPOSE 8000

CMD ["bash", "run.sh"]