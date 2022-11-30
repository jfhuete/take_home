FROM python:3.10.0-buster

# Configure python environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir

WORKDIR /app

# Update pip to last versión

RUN python -m pip install -U pip

COPY requirements.txt ./
COPY requirements_dev.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_dev.txt

# Copy project files

COPY ./api .

# Copy test script

COPY ./scripts/container_test.sh .
