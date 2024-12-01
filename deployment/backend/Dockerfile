FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt /backend

RUN apt-get update && apt-get -y install gcc mono-mcs && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get -y install g++ mono-mcs && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y gfortran libopenblas-dev liblapack-dev

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download ru_core_news_sm

COPY . /backend

EXPOSE 8000

CMD ["bash", "run.sh"]