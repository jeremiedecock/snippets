FROM python:3.10-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Créer un répertoire de travail
WORKDIR /app

# Copier uniquement requirements.txt pour installer les dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Ajouter un placeholder pour les scripts montés
RUN echo "print('Container ready for development')" > app.py

# Définir le point d'entrée par défaut
CMD ["python", "app.py"]

