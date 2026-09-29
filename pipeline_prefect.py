"""Pipeline Prefect : orchestration des étapes du projet ML."""

import argparse
import subprocess  # nosec B404
from pathlib import Path

from prefect import flow, get_run_logger, task

VENV_DIR = Path("venv")
PYTHON_BIN = VENV_DIR / "bin" / "python"
MAIN_PY = Path("main.py")
# Le sujet impose de ne cibler que ces 3 fichiers pour qualité/sécurité
CODE_FILES = ["model_pipeline.py", "main.py", "pipeline_prefect.py"]


def _run(cmd):
    """Exécute une commande, journalise la sortie, échoue si code != 0."""
    logger = get_run_logger()
    logger.info("Commande : %s", " ".join(cmd))
    result = subprocess.run(
        cmd, capture_output=True, text=True, check=False
    )  # nosec B603
    if result.stdout:
        logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(f"Échec ({result.returncode}) : {' '.join(cmd)}")


# ---------- TASKS ----------
@task(name="install-dependencies")
def install_dependencies():
    _run([str(PYTHON_BIN), "-m", "pip", "install", "-r", "requirements.txt"])


@task(name="format-code")
def format_code():
    _run([str(PYTHON_BIN), "-m", "black", *CODE_FILES])


@task(name="check-quality")
def check_quality():
    _run([str(PYTHON_BIN), "-m", "flake8", "--max-line-length", "100", *CODE_FILES])


@task
def check_security():
    _run(
        [
            "venv/bin/python",
            "-m",
            "bandit",
            "-q",
            "-ll",
            "model_pipeline.py",
            "main.py",
            "pipeline_prefect.py",
        ]
    )


@task(name="run-tests")
def run_tests():
    _run([str(PYTHON_BIN), "test_pipeline.py"])


@task(name="prepare-data")
def prepare_data():
    _run([str(PYTHON_BIN), str(MAIN_PY), "--step", "prepare"])


@task(name="train-model")
def train_model():
    _run([str(PYTHON_BIN), str(MAIN_PY), "--step", "train"])


@task(name="save-model")
def save_model():
    # Adapter si ton main.py a une étape dédiée (ex: --step save)
    get_run_logger().info("Modèle sauvegardé par l'étape train (classifier.joblib).")


@task(name="load-model")
def load_model():
    # Adapter si ton main.py a une étape dédiée (ex: --step load)
    _run(
        [
            str(PYTHON_BIN),
            "-c",
            "from model_pipeline import load_model; load_model('classifier.joblib'); "
            "print('Modèle chargé')",
        ]
    )


@task(name="evaluate-model")
def evaluate_model():
    _run([str(PYTHON_BIN), str(MAIN_PY), "--step", "evaluate"])


# ---------- FLOWS ----------
@flow(name="install", log_prints=True)
def flow_install():
    install_dependencies()


@flow(name="code", log_prints=True)
def flow_code():
    format_code()
    check_quality()
    check_security()
    run_tests()


@flow(name="train", log_prints=True)
def flow_train():
    prepare_data()
    train_model()


@flow(name="evaluate", log_prints=True)
def flow_evaluate():
    load_model()
    evaluate_model()


@flow(name="all", log_prints=True)
def flow_all():
    install_dependencies()
    format_code()
    check_quality()
    check_security()
    run_tests()
    prepare_data()
    train_model()
    save_model()
    evaluate_model()


FLOWS = {
    "install": flow_install,
    "code": flow_code,
    "train": flow_train,
    "entrainement": flow_train,
    "evaluate": flow_evaluate,
    "all": flow_all,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Prefect")
    parser.add_argument("--flow", choices=FLOWS.keys(), default="all")
    args = parser.parse_args()
    FLOWS[args.flow]()
