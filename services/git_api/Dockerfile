FROM python:3.10-slim

WORKDIR /github-repo-recommendation

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "your_script.py"]