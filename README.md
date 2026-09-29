# MLOps Project - Machine Learning Pipeline

## Description

Ce projet met en œuvre un pipeline de Machine Learning structuré et automatisé dans le cadre des ateliers MLOps.

Le projet est réalisé en plusieurs étapes :

- **Atelier 2 : Modularisation du code**
- **Atelier 3 : Création et automatisation d'un pipeline avec Prefect**

L'objectif est de transformer un script de Machine Learning en un projet Python modulaire, testable et automatisable à l'aide de Prefect.

Le projet utilise un modèle de classification appliqué au jeu de données **Churn Modelling**.

---

## Structure du projet

```text
MLOps-Project/
│
├── model_pipeline.py
├── main.py
├── test_pipeline.py
├── pipeline_prefect.py
├── deploiement_prefect.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── Churn_Modelling.csv
└── classifier.joblib
```

> `Churn_Modelling.csv` et `classifier.joblib` sont des fichiers générés/utilisés localement et ne sont pas versionnés dans Git.

---

# Atelier 2 - Modularisation du code

## Objectif

L'objectif de l'Atelier 2 est de transformer un script Jupyter de Machine Learning en code Python modulaire et réutilisable.

Le pipeline est séparé en plusieurs fonctions correspondant aux différentes étapes du processus Machine Learning.

## Fonctions principales

### `prepare_data()`

Cette fonction permet de :

- charger le fichier de données CSV ;
- préparer les données ;
- séparer les variables explicatives et la variable cible ;
- diviser les données en ensembles d'entraînement et de test.

### `train_model()`

Cette fonction permet d'entraîner le modèle de Machine Learning à partir des données d'entraînement.

### `evaluate_model()`

Cette fonction permet d'évaluer les performances du modèle sur les données de test.

Les métriques utilisées comprennent notamment :

- Accuracy ;
- matrice de confusion ;
- Precision ;
- Recall ;
- F1-score.

### `save_model()`

Cette fonction permet de sauvegarder le modèle entraîné dans un fichier `joblib`.

Le fichier généré est :

```text
classifier.joblib
```

### `load_model()`

Cette fonction permet de charger un modèle précédemment sauvegardé afin de pouvoir l'utiliser pour l'évaluation ou la prédiction.

---

## Fichier `model_pipeline.py`

Le fichier `model_pipeline.py` contient les différentes fonctions réutilisables du pipeline Machine Learning :

```text
prepare_data()
train_model()
evaluate_model()
save_model()
load_model()
```

Cette organisation permet de séparer la logique Machine Learning de la logique d'exécution.

---

## Fichier `main.py`

Le fichier `main.py` constitue le point d'entrée principal du projet.

Il permet d'exécuter les différentes étapes du pipeline à l'aide d'arguments en ligne de commande.

Exemples :

```bash
python main.py --step prepare
```

```bash
python main.py --step train
```

```bash
python main.py --step evaluate
```

Cette organisation rend les différentes étapes du pipeline indépendantes et facilement exécutables.

---

# Tests

Le fichier `test_pipeline.py` permet de tester les différentes fonctions du pipeline.

Les tests vérifient notamment :

- la préparation des données ;
- l'entraînement du modèle ;
- l'évaluation du modèle ;
- la sauvegarde du modèle ;
- le chargement du modèle.

Pour exécuter les tests :

```bash
python test_pipeline.py
```

Résultat attendu :

```text
Tous les tests sont passés.
```

---

# Atelier 3 - Pipeline avec Prefect

## Objectif

L'Atelier 3 permet d'automatiser les différentes étapes du pipeline Machine Learning avec **Prefect**.

Le pipeline permet d'organiser et d'exécuter automatiquement les étapes suivantes :

```text
Installation des dépendances
        ↓
Formatage / Qualité / Sécurité / Tests
        ↓
Préparation des données
        ↓
Entraînement du modèle
        ↓
Sauvegarde du modèle
        ↓
Évaluation
```

---

# `pipeline_prefect.py`

Le fichier `pipeline_prefect.py` utilise Prefect pour transformer les différentes étapes du projet en tâches et en flows.

Les principales tâches comprennent :

- installation des dépendances ;
- préparation des données ;
- entraînement du modèle ;
- sauvegarde du modèle ;
- chargement du modèle ;
- évaluation ;
- tests ;
- vérification de la qualité du code ;
- vérification de la sécurité.

---

## Flows Prefect

Plusieurs flows sont disponibles.

### Flow `all`

Le flow `all` permet d'exécuter le pipeline principal de bout en bout.

Commande :

```bash
python pipeline_prefect.py --flow all
```

Il réalise notamment :

```text
Installation des dépendances
        ↓
Tests
        ↓
Préparation des données
        ↓
Entraînement
        ↓
Sauvegarde
        ↓
Évaluation
```

---

### Flow `train`

Le flow `train` permet de préparer les données puis d'entraîner le modèle.

Commande :

```bash
python pipeline_prefect.py --flow entrainement
```

---

### Flow `evaluate`

Le flow `evaluate` permet de charger le modèle sauvegardé et d'évaluer ses performances.

Commande :

```bash
python pipeline_prefect.py --flow evaluate
```

---

### Flow `code`

Le flow `code` regroupe les contrôles liés à la qualité du projet.

Il permet notamment d'exécuter :

- le formatage ;
- les contrôles de qualité du code ;
- l'analyse de sécurité ;
- les tests unitaires.

Commande :

```bash
python pipeline_prefect.py --flow code
```

---

# Qualité et sécurité du code
Le projet intègre plusieurs contrôles automatisés afin de vérifier la qualité du code.

Les fichiers principaux concernés sont :

```text
model_pipeline.py
main.py
pipeline_prefect.py
```

Les contrôles permettent de détecter les problèmes potentiels avant l'exécution du pipeline principal.

---

# Déploiement avec Prefect

Le fichier `deploiement_prefect.py` permet de créer les deployments Prefect.

Le serveur Prefect peut être démarré avec :

```bash
prefect server start
```

L'interface Prefect est ensuite accessible localement à :

```text
http://127.0.0.1:4200
```

---

## Configuration de l'API Prefect

Dans un terminal :

```bash
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
```

Puis :

```bash
python deploiement_prefect.py
```
---

## Vérifier les deployments

Pour afficher les deployments disponibles :

```bash
prefect deployment ls
```

Les deployments permettent ensuite de lancer les flows depuis Prefect.

Exemple :

```bash
prefect deployment run 'all/ml-pipeline-all'
```

---

# Récupération du projet depuis Git

Le projet est versionné avec Git et hébergé sur GitHub.

Le dépôt permet de récupérer le projet sur une nouvelle machine avec :

```bash
git clone https://github.com/joulen-rejeb/MLOps-Project.git
```

Une copie locale du projet peut ensuite être utilisée pour installer les dépendances et exécuter le pipeline.

---

# Reproduction du projet

## 1. Cloner le dépôt

```bash
git clone https://github.com/joulen-rejeb/MLOps-Project.git
```

Puis :

```bash
cd MLOps-Project
```

---

## 2. Créer l'environnement virtuel

```bash
python -m venv venv
```

Activer l'environnement :

```bash
source venv/bin/activate
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 4. Ajouter le dataset

Le fichier :

```text
Churn_Modelling.csv
```

est nécessaire pour exécuter le pipeline.

Il est volontairement exclu du dépôt Git et doit être disponible localement.

---

## 5. Exécuter les tests

```bash
venv/bin/python test_pipeline.py
```

Le résultat attendu est :

```text
Tous les tests sont passés.
```

---

## 6. Exécuter le pipeline complet

```bash
python pipeline_prefect.py --flow all
```

Le pipeline réalise automatiquement les différentes étapes du processus Machine Learning.

---
# Résultats

Lors de l'exécution du pipeline complet, les principales étapes sont exécutées avec succès :

```text
Installation des dépendances
OK : prepare_data
OK : train_model
OK : evaluate_model
OK : save_model / load_model
Tous les tests sont passés.
```

Lors de l'évaluation du modèle, une accuracy d'environ **85 %** est obtenue sur l'ensemble de test.

Exemple d'exécution :

```text
Accuracy score : 85.55 %
```

La matrice de confusion obtenue est :

```text
[[1535   50]
 [ 239  176]]

```

Les valeurs peuvent légèrement varier selon l'exécution et l'environnement.

---

# Gestion des fichiers non versionnés

Les fichiers suivants ne sont pas versionnés dans Git :

```text
Churn_Modelling.csv
classifier.joblib
venv/
__pycache__/
*.pyc
.pytest_cache/
```

Ils sont exclus à l'aide du fichier `.gitignore`.

Le modèle `classifier.joblib` est généré automatiquement pendant l'exécution du pipeline lorsque le modèle est entraîné et sauvegardé.

---

# Technologies utilisées

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Matplotlib
- Pytest
- Prefect
- Git
- GitHub
- WSL

---

# Architecture du projet

L'architecture globale peut être représentée ainsi :

```text
                GitHub
                   │
                   ▼
             Clone du projet
                   │
                   ▼
          Environnement Python
                   │
                   ▼
            pipeline_prefect
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
  Contrôle du code       Pipeline ML
        │                     │
        ▼                     ▼
 Tests / Qualité       Préparation données
 / Sécurité                    │
                               ▼
                         Entraînement
                               │
                               ▼
                         Sauvegarde
                               │
                               ▼
                          Évaluation
```

---

# Conclusion

Ce projet met en œuvre une démarche MLOps progressive.

L'Atelier 2 permet de transformer le code Machine Learning initial en un code modulaire composé de fonctions réutilisables.

L'Atelier 3 permet ensuite d'automatiser l'exécution de ces différentes étapes avec Prefect, d'intégrer des tests et des contrôles de qualité et de sécurité, puis de déployer les flows avec Prefect.

Le projet peut également être récupéré depuis un dépôt Git distant et exécuté dans un nouvel environnement Python.
