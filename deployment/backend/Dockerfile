FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt /backend

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download ru_core_news_sm

COPY . /backend

EXPOSE 8000

CMD ["bash", "run.sh"]