FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Standard: Offline-Modus mit Beispieldaten
CMD ["python", "sortierer.py", "daten/anfragen.csv", "--mode", "regel"]
