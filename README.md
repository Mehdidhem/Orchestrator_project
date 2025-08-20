
# Hera-MI - Outil d'Orchestration de Logs

Ce projet en collaboration avec Hera-MI vise à développer un outil d'orchestration de logs. Cet outil a pour objectif de simplifier la gestion, la collecte, l'analyse et la visualisation des logs générés par nos expériences et analyses dans le domaine de l'intelligence artificielle appliquée à l'imagerie médicale.

## Table des matières

- [Introduction](#introduction)

- [Fonctionnalités](#fonctionnalités)

- [Démarage et configuration](#démarage-et-configuration)

## Introduction

Hera-MI est une équipe de recherche dédiée à l'intelligence artificielle appliquée à l'imagerie médicale pour le diagnostic du cancer du sein. Dans le cadre de nos travaux, nous devons identifier un moyen de centraliser, d'analyser et de partager efficacement les résultats des expériences de Hera-Mi.

L'outil d'orchestration de logs que nous développons vise à simplifier cette tâche en collectant les logs générés par les expériences, en les stockant de manière sécurisée, en les analysant pour détecter des anomalies et en les présentant à l'aide de Tensorboard.

## Fonctionnalités

- Récupération Automatisée : Les logs sont récupérés automatiquement depuis les serveurs dédiés à l'apprentissage profond via SSH.
- Stockage Structuré : Les données sont organisées dans une structure de dossiers qui reflète l'origine et le contexte de chaque ensemble de logs.
- Mises à Jour en Temps Réel : Les logs sont mis à jour en temps réel dans TensorBoard dès qu'ils sont disponibles.
- Parallélisation : Les opérations de récupération des logs sont exécutées en parallèle pour une efficacité optimisée.
- Notifications et Alertes : Les utilisateurs sont notifiés des nouvelles données et des anomalies détectées.
<img width="1231" height="760" alt="image" src="https://github.com/user-attachments/assets/10d4d7cf-5e4c-4b62-967c-36ea2a7e07f4" />

## Démarage et configuration

Se connecter sur les serveurs d'apprentissage et y mettre la clé publique :
```bash
    echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDEg5ViiBpbMDbjDCpKcS5cOVC6q9h6TYUesInqUIBjTB2qbrhTX0Fln42HLXXIB+Z456XCLTq5SCkB/HDfm0ihkbJIDLtZhpmeyht6zGZz34NByx1Il8wxW7L+I/kaI8MkS774PLivO17I2DAVw7xCLcM+8wrtb0yW1Zp2zdQ06SDAuyWn+BCpl8ECs8GbDYoEAKQOaSMh8iGcRGhrDET3PA7mvVbD/7bZHKlK7EqsEMmgMzl9iDRfRszp9he20os3+H3U0bqwGVvHJBPCPOJIpQkh5OZweCGigNw+OYVcbz/jtJac9AVzyHxVciLrbRksmKEgLssU9/HJ5hXzUzXQ824CKuBa+8ZY3moFCvocgHXTdk+Kmh26QPnvokxg+3iIUxcFOJT331VWd7RWG4FK8apj7sfapzDsXcC4tcUKsLgEPxmybASHkJkB1CL4c+npERIFYbRDQhj0SmczZG19dMcSWhuRn1b560GSLnKy2tgpz6OnB4pexqvtPix/ZGk= mehdi@AsusMehdi
" >> /home/user/.ssh/authorized_keys
```

Dans le script python mettre les differents serveurs d'apprentissage dans la liste des serveurs à énumerer

Importer le projet et lancer les conteneurs : 
```bash
    git clone git@github.com:Mehdidhem/Orchestrator_project.git
    cd src (#les sous dossiers iterations vont etre supprimés seul la version finale importera)
    docker-compose up --build
```

Se connecter sur l'instance Tensorboard lancé : 
http://localhost:6006/
