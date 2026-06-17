# Utiliser une image Python officielle légère comme base
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Définir les variables d'environnement Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

# Installer les dépendances
# On copie d'abord uniquement requirements.txt pour profiter du cache Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . /app/

# Créer un dossier data vide au cas où pour SQLite
RUN mkdir -p /app/data

# Le bot est un processus persistant via schedule, on lance simplement main.py
CMD ["python", "main.py"]
