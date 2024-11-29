FROM python:3.10-slim

WORKDIR /summarizer

COPY requirements.txt /summarizer

RUN pip install --no-cache-dir -r requirements.txt

COPY . /summarizer

EXPOSE 8000

CMD ["bash", "run.sh"]