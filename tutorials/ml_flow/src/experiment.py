import mlflow
from pathlib import Path

## Set tracker uri
# mlflow.set_tracking_uri(uri=(Path("/Users/hardiksahi/Personal/MLOps/tutorials/ml_flow")/'mlruns').as_uri())
mlflow.set_tracking_uri("")  ## . Defaults to ./mlruns
print(mlflow.get_tracking_uri())

## Create experiment


if __name__ == "__main__":

    ## =========  1. Create a new experiment ====================
    # experiment_id = mlflow.create_experiment(
    #     name="experiment1",
    #     tags={"version": "v1", "priority": "P1", "topic": "experiment-management"},
    # )
    # experiment = mlflow.get_experiment(experiment_id)

    # print(f"Name: {experiment.name}")
    # print(f"Experiment Id: {experiment.experiment_id}")
    # print(f"Artifact location: {experiment.artifact_location}")

    ## ==========================================================

    ## =========== 2. Start a run but set no active experiment. ===============
    ## Starting a run but not setting an active experiment => will create run entry under default experiment 0
    # with mlflow.start_run(run_name="test_run") as run:
    #     print(f"Active run_id: {run.info.run_id}")
    ## ==========================================================

    ## ========== 3. Start a run that will be logged under an existing experiment ==========
    ## Start a run that will logged unde4r experiment experiment1
    # with mlflow.start_run(
    #     experiment_id=mlflow.get_experiment_by_name("experiment1").experiment_id
    # ) as run:
    #     print(f"Active run_id: {run.info.run_id}")
    ## ==========================================================

    ## ====== 4. Set active experiment and then log a run under it (creates a new experiment in case it does not exist)=====
    ## Set an experiment as active experiment and then log a run under it
    # experiment = mlflow.set_experiment(experiment_name="experiment_not_existing")
    # print(f"Active Experiment Id: {experiment.experiment_id}")

    # with mlflow.start_run() as run:
    #     print(f"Active run_id: {run.info.run_id}")
    ## ==========================================================

    ## =========== 5. Access/ Retreive experiments ======================
    # existing_experiment = mlflow.get_experiment_by_name(name="experiment1")
    # print(f"existing_experiment retreived by name: {existing_experiment.experiment_id}")
    # print(existing_experiment.to_proto())

    # existing_experiment_by_id = mlflow.get_experiment(
    #     experiment_id=existing_experiment.experiment_id
    # )
    # print(
    #     f"existing_experiment retreived by id: {existing_experiment_by_id.experiment_id}"
    # )
    ## ==========================================================

    ## =========== 6. Updating experiments ===========================
    # mlflow.set_experiment(experiment_name="experiment_not_existing")
    # mlflow.set_experiment_tags({"k1": "v1", "k2": "v2"})

    # updated_active_experiment = mlflow.get_experiment_by_name(
    #     name="experiment_not_existing"
    # )
    # print(updated_active_experiment.to_proto())
    ## ==========================================================

    ## =========== 7 We can also perform update operations via MlflowClient ==============
    client = mlflow.MlflowClient()
    client_experiment_id = client.create_experiment(name="client_experiment")
    print(f"Experiment id for client_experiment: {client_experiment_id}")

    client.set_experiment_tag(
        experiment_id=client.get_experiment_by_name(
            name="client_experiment"
        ).experiment_id,
        key="client_key1",
        value="client_value1",
    )

    ## The following directly sets description for an experiment
    client.set_experiment_tag(
        experiment_id=client.get_experiment_by_name(
            name="client_experiment"
        ).experiment_id,
        key="mlflow.note.content",
        value="This is the description set via set_experiment_tag",
    )
    ## ==========================================================

    ## =========== 8. Renaming experiment via MlflowClient ==============
    # exp_id = client.get_experiment_by_name(name="client_experiment").experiment_id
    # client.rename_experiment(
    #     experiment_id=exp_id,
    #     new_name="updated_client_experiment",
    # )
    # experiment = mlflow.get_experiment(experiment_id=exp_id)
    # print(experiment.to_proto())

    ## ========== 9. Delete experiment =======================
    ## Soft delete of experiment by moving it to ./mlruns/.trash folder and changing state to delete
    # exp_id = client.get_experiment_by_name(
    #     name="updated_client_experiment"
    # ).experiment_id
    # mlflow.delete_experiment(experiment_id=exp_id)
    # experiment = mlflow.get_experiment(experiment_id=exp_id)
    # print(experiment.to_proto())

    ## Cannot create an experiemnt with same name until unless it is deleted from trash folder as well.
    # mlflow.create_experiment(name="updated_client_experiment")
