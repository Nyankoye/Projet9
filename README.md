# Projet9
Réalisation d’une application web à l’aide de django permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.
# Execution du code
 1. Cloner ce dépôt de code à l'aide de la commande $ git clone https://github.com/Nyankoye/Projet9.git 
 2. Créez un environnement virtuel dans le projet en utilisant la commande: python -m venv env
 3. Activez l'environnement virtuel en utilisant la commande: source env/bin/activate 
 4. Installer les paquets Python répertoriés dans le fichier requirements.txt en utilisant la commande : pip install -r requirements.txt
 5. Deplacez-vous  dans le fichier lit_review_project en utilisant la commande : cd lit_review_project
 6. Charger le contenu de la base de données en utilisant la commande : python manage.py migrate
 7. Lancer le serveur en utilisant la commande : python manage.py runserver
 8. Tapez cette adresse : http://127.0.0.1:8000/ dans votre navigateur pour commencer à utiliser la l'application web

## Génération Fichier flake8
 Pour généner un fichier flake8 vous devez utiliser les commandes suivantes:
 * generer le fichier avec la commande: flake8 --max-line-length 119 review/ --exclude migrations --format=html --htmldir=flake-report
