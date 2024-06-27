# Projet Django

Ce repository contient un projet Django destiné à résumer des articles en utilisant l'API OpenAI.

## Prérequis

Avant de commencer, assurez-vous d'avoir Python 3.x installé sur votre machine.

## Installation

1. **Clonage du Repository**
git clone <url_du_repository>
cd nom_du_projet

## Configuration

1. **Configuration de l'API OpenAI**

- Obtenez une clé API OpenAI à partir de [OpenAI](https://openai.com).
- Ajoutez cette clé dans le fichier `config.py` à la racine du projet :

  ```python
  # config.py
  
  OPENAI_API_KEY = 'votre_clé_api_openai'
  ```

## Lancement du Projet

Pour lancer le projet, suivez ces étapes :

1. **Compiler les fichiers Tailwind CSS**

python manage.py tailwind start


2. **Lancer le Serveur de Développement Django**
python manage.py runserver

Atention il faut lancer les deux commende en meme temps 

## Utilisation

- Accédez à l'application à l'adresse `http://localhost:8000/`.
- Ajoutez de nouveaux articles et résumez-les en sélectionnant la langue de votre choix.
- Consultez les résumés générés et accédez aux détails de chaque article.

## Participant 

Charles Devif

