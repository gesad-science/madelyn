#Dockerfile app

FROM python:3.10.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7000

CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "7000"]

