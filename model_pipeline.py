"""Pipeline ML modulaire pour la prédiction du churn (Churn_Modelling.csv).

Chaque étape du notebook customer_churn.ipynb est encapsulée dans une fonction :
prepare_data, train_model, evaluate_model, save_model, load_model.
"""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

TARGET_COL = "Exited"
COLUMNS_TO_DROP = ["RowNumber", "CustomerId", "Surname", "Geography"]


def prepare_data(csv_path, test_size=0.2, random_state=1):
    """Charge le CSV, nettoie et prétraite les données, puis découpe en train/test.

    Args:
        csv_path (str): chemin du fichier CSV.
        test_size (float): proportion du jeu de test.
        random_state (int): graine pour un découpage reproductible.

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    df = pd.read_csv(csv_path)

    if TARGET_COL not in df.columns:
        raise ValueError(f"Colonne cible '{TARGET_COL}' introuvable dans {csv_path}")

    df = df.drop_duplicates()
    df["Gender"] = LabelEncoder().fit_transform(df["Gender"])
    df = df.drop(columns=COLUMNS_TO_DROP, errors="ignore")

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_model(X_train, y_train, n_estimators=100, random_state=42):
    """Entraîne un RandomForestClassifier et retourne le modèle entraîné."""
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Évalue le modèle : affiche accuracy, matrice de confusion et rapport.

    Returns:
        float: l'accuracy sur le jeu de test.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy score : {accuracy * 100:.2f} %")
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    return accuracy


def save_model(model, path="classifier.joblib"):
    """Sauvegarde le modèle entraîné avec joblib."""
    joblib.dump(model, path)
    print(f"Modèle sauvegardé dans : {path}")


def load_model(path="classifier.joblib"):
    """Charge un modèle sauvegardé avec joblib."""
    model = joblib.load(path)
    print(f"Modèle chargé depuis : {path}")
    return model
