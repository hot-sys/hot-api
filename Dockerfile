FROM python:3.12-slim

WORKDIR /app

COPY requirements.prod.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    redis-server \
    && apt-get clean

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.prod.txt

COPY . .

COPY redis.conf /etc/redis/redis.conf

EXPOSE 10000

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]