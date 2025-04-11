@echo off
echo ================================
echo Initialisation de l'environnement...
echo ================================

:: Crée l'environnement virtuel
python -m venv venv

:: Active l'environnement virtuel
call venv\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Installe les dépendances
pip install django psycopg2-binary python-decouple

:: Crée un fichier .env s'il n'existe pas
IF NOT EXIST .env (
    echo DEBUG=True > .env
    echo DB_NAME=simulateur_db >> .env
    echo DB_USER=postgres >> .env
    echo DB_PASSWORD=motdepasse >> .env
    echo DB_HOST=localhost >> .env
    echo DB_PORT=5432 >> .env
    echo Fichier .env généré avec succès.
) ELSE (
    echo Fichier .env déjà présent.
)

:: Applique les migrations
python manage.py migrate

:: Lance le serveur de développement
python manage.py runserver
