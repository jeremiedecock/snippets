FROM python:3.10-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier les fichiers nécessaires
WORKDIR /app
COPY requirements.txt .
COPY app.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Définir le point d'entrée
CMD ["python", "app.py"]

