FROM python:3.9-slim

# Install Ansible AND Docker CLI (Client)
RUN apt-get update && apt-get install -y \
    ssh \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

# Train the model during build
RUN python train_model.py

CMD ["python", "main.py"]