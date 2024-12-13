# Hotel Management System (HMS)

Url : https://hot-api-v3lf.onrender.com

## Project Overview
A Django-based Hotel Management System designed to streamline Hotel management.

## Prerequisites
- Python 3.10+
- Docker
- Docker Compose
- Postman (optional, for API testing)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/hot-sys/hot-api.git
cd hot-api
```

### 2. Environment Configuration
Create a `.env` file in the project root:
```env
DB_NAME=hms
DB_USER=user
DB_PASSWORD=your-database-password
DB_HOST=host
DB_PORT=port
```

### 3. Docker Deployment
```bash
# Build and start the services
docker-compose up --build

# Stop services
docker-compose down
```

### 4. Local Python Environment Setup
#### 1. Create Virtual Environment
```bash
# For Unix/macOS
python3 -m venv venv

# For Windows
python -m venv venv
```

#### 2. Activate Virtual Environment
```bash
# For Unix/macOS
source venv/bin/activate

# For Windows
venv\Scripts\activate
```

#### 3. Install Requirements

##### Standard Installation
```bash
# Upgrade pip
pip install --upgrade pip

# Install production requirements
pip install -r requirements.prod.txt

# Install development requirements
pip install -r requirements.dev.txt
```

## API Testing
- Import `collection.v1.json` in Postman
- Test endpoints and verify functionality