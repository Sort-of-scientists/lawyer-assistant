FROM python:3.10-slim

WORKDIR /llm

COPY requirements.txt /llm

RUN pip install --no-cache-dir -r requirements.txt

COPY . /llm

EXPOSE 8000

CMD ["bash", "run.sh"]