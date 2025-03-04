FROM python:3.10

WORKDIR /api_bdd

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "init_es.py"]