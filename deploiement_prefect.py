"""Déploiements Prefect : exécution à la demande et planifiée."""
from prefect import serve
from prefect.client.schemas.schedules import CronSchedule

from pipeline_prefect import (flow_all, flow_code, flow_evaluate,
                              flow_install, flow_train)

if __name__ == "__main__":
    serve(
        flow_all.to_deployment(
            name="ml-pipeline-all",
            schedules=[CronSchedule(cron="0 2 * * *", timezone="Africa/Tunis")],
            tags=["mlops", "full-pipeline"],
        ),
        flow_train.to_deployment(name="ml-pipeline-train", tags=["mlops", "training"]),
        flow_evaluate.to_deployment(name="ml-pipeline-evaluate", tags=["mlops", "evaluation"]),
        flow_install.to_deployment(name="ml-pipeline-install", tags=["mlops", "setup"]),
        flow_code.to_deployment(name="ml-pipeline-code", tags=["mlops", "quality"]),
    )
