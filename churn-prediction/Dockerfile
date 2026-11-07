FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir --only-binary=:all: -r requirements.txt || pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "src/09_inference.py"]