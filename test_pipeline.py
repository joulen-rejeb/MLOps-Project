"""Tests simples du pipeline. Lancer : python test_pipeline.py"""
import os
import tempfile

from model_pipeline import (
    evaluate_model,
    load_model,
    prepare_data,
    save_model,
    train_model,
)

CSV = "Churn_Modelling.csv"


def test_prepare_data():
    X_train, X_test, y_train, y_test = prepare_data(CSV)
    assert len(X_train) == 8000 and len(X_test) == 2000
    assert "Exited" not in X_train.columns
    print("OK : prepare_data")


def test_train_model():
    X_train, _, y_train, _ = prepare_data(CSV)
    model = train_model(X_train, y_train, n_estimators=10)
    assert hasattr(model, "predict")
    print("OK : train_model")


def test_evaluate_model():
    X_train, X_test, y_train, y_test = prepare_data(CSV)
    model = train_model(X_train, y_train, n_estimators=10)
    accuracy = evaluate_model(model, X_test, y_test)
    assert 0.7 < accuracy <= 1.0
    print("OK : evaluate_model")


def test_save_and_load_model():
    X_train, X_test, y_train, _ = prepare_data(CSV)
    model = train_model(X_train, y_train, n_estimators=10)
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test_model.joblib")
        save_model(model, path)
        loaded = load_model(path)
    assert (model.predict(X_test) == loaded.predict(X_test)).all()
    print("OK : save_model / load_model")


if __name__ == "__main__":
    test_prepare_data()
    test_train_model()
    test_evaluate_model()
    test_save_and_load_model()
    print("Tous les tests sont passés.")
