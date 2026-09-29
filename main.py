"""Point d'entrée : exécute les étapes du pipeline ML via des arguments CLI.

Exemples :
    python main.py --step prepare
    python main.py --step train
    python main.py --step evaluate
    python main.py --step all
"""

import argparse

from model_pipeline import (
    evaluate_model,
    load_model,
    prepare_data,
    save_model,
    train_model,
)


def main():
    parser = argparse.ArgumentParser(description="Pipeline ML - Churn Modelling")
    parser.add_argument("--data", default="Churn_Modelling.csv", help="Fichier CSV")
    parser.add_argument(
        "--model", default="classifier.joblib", help="Fichier du modèle"
    )
    parser.add_argument(
        "--step",
        choices=["prepare", "train", "evaluate", "all"],
        default="all",
        help="Étape à exécuter",
    )
    args = parser.parse_args()

    X_train, X_test, y_train, y_test = prepare_data(args.data)
    print(f"Données prêtes : {len(X_train)} lignes train / {len(X_test)} lignes test")
    if args.step == "prepare":
        return

    if args.step in ("train", "all"):
        model = train_model(X_train, y_train)
        save_model(model, args.model)

    if args.step in ("evaluate", "all"):
        model = load_model(args.model)
        evaluate_model(model, X_test, y_test)


if __name__ == "__main__":
    main()
