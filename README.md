# Readme - TP03

## Installation

Pour configurer l'environnement nécessaire et lancer l'application Flask, exécuter les commandes suivantes dans le dossier où se trouve ce fichier.  Ces commandes supposent que les paquets `virtualenv`, `python3` et `python3-pip` sont déjà installés.

```bash
virtualenv -p python3 venv
source /venv/bin/activate
pip3 install -r requirements.txt

export FLASK_APP=my_code.py
flask run
```

## Utilisation

L'application est disponible à l'adresse suivante: http://127.0.0.1:5000  

Au lancement de l'application, un utilisateur administrateur existe.  Pour se connecter, utiliser `root` comme identifiant et comme mot de passe.

Par défaut, aucune tâche n'existe dans l'application.  Pour en ajouter une, cliquer sur l'onget `Add task` et saisir l'intitulé et la date d'échéance de la tâche.  Une description facultative peut être ajoutée.  Valider avec le bouton `Add task`.  
Le statut d'une tâche peut être modifié en cliquant sur le satut actuel (`To do` ou `Done`). 
Pour modifier une tâche, cliquer sur le bouton `Edit` en regard de la tâche.  Effectuer les modifications et valider avec `Save task`.  

Lorsque l'utilisateur connecté est administrateur, il peut modifier le statut des autres utilisateurs en se rendant dans l'onglet `Admin`.

Les dates doivent être entrées au format `JJ/MM/AAAA`.

