FROM python:3.12-slim

WORKDIR /app

COPY requirements.prod.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    && apt-get clean

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.prod.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:${PORT:-10000}"]