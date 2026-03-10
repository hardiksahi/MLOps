import mlflow
from pathlib import Path
import json

mlflow.set_tracking_uri(
    uri=(
        Path("/Users/hardiksahi/Personal/MLOps/tutorials/ml_flow") / "mlruns2"
    ).as_uri()
)

print(mlflow.get_tracking_uri())

if __name__ == "__main__":
    ## ====== 1. Start a run without associating with an experiment =======
    # with mlflow.start_run() as run:
    #     print(f"Type of run: {type(run)}")
    #     print(f"Info: {run.info.to_proto()}")
    #     print(f"Experiment id for run {run.info.run_id} -> {run.info.experiment_id}")
    #     print(f"Run dict: {json.dumps(run.to_dictionary(), indent=4)}")
    ## ===========================================================

    ## ======= 2. Create an experiment and associate a run with it. ========
    # experiment_id = mlflow.create_experiment(name="experiment1", tags={"version": 1})
    # mlflow.set_experiment(experiment_id=experiment_id)

    # with mlflow.start_run(run_name="run1") as run:
    #     mlflow.log_params(params={"c": 0.1, "n_trees": 100})
    #     mlflow.log_metrics(metrics={"accuracy": 0.95, "f1": 0.7})
    ## ===========================================================

    ## ======= 3. Get run that already exists [only by id] ==========
    # experiment_object = mlflow.set_experiment(
    #     experiment_id=mlflow.get_experiment_by_name(name="experiment1")
    # )
    # run_object = mlflow.get_run(run_id="c4e063f8336a428fba9dc230d8ac1f90")
    # print(json.dumps(run_object.to_dictionary(), indent=4))
    ## ===========================================================

    ## ======= 4. Create a run and add tag to it ==========
    # mlflow.set_experiment(experiment_name="experiment1")
    # with mlflow.start_run(run_name="run2") as run:
    #     mlflow.log_params({"p1": 1, "p2": 2})
    #     mlflow.log_metrics({"m1": 0.99, "m2": 0.5})
    #     mlflow.set_tags({"tag1": "val1", "tag2": "val2"})

    #     print(json.dumps(run.to_dictionary(), indent=4))
    ## ===========================================================

    ## ======== 5. Access failed run and check its status  = FAILED ==========
    # failed_run_object = mlflow.get_run(run_id="e067e6be453b47cbba487a341d0cb487")
    # print(f"status: {failed_run_object.info.status}")
    # print(f"lifecycle_stage: {failed_run_object.info.lifecycle_stage}")
    # print(json.dumps(failed_run_object.to_dictionary(), indent=4))

    # mlflow.delete_run(run_id="e067e6be453b47cbba487a341d0cb487")
    # deleted_run_object = mlflow.get_run(run_id="e067e6be453b47cbba487a341d0cb487")
    ## ===========================================================

    ## 6. ======= Run with different status ==========
    ## start_run => Start a new MLflow run, setting it as the active run under which metrics and parameters will be logged.
    # with mlflow.start_run(
    #     run_name="run3",
    #     experiment_id=mlflow.get_experiment_by_name("experiment1").experiment_id,
    # ) as run:

    #     print(f"[RUN] Status: {run.info.status}")
    #     print(f"[RUN] Lifecycle: {run.info.lifecycle_stage}")

    #     corr_exp = mlflow.get_experiment(experiment_id=run.info.experiment_id)
    #     print(f"[EXPERIMENT] Lifecycle: {corr_exp.lifecycle_stage}")

    #     mlflow.log_params({"p1": 1, "p2": 2})
    #     mlflow.log_metrics({"m1": 0.5, "m2": 0.99})

    # run_object = mlflow.get_run(run_id=run.info.run_id)
    # print(f"[Outside context][RUN] Status: {run_object.info.status}")
    # print(f"[Outside context][RUN] Lifecycle: {run_object.info.lifecycle_stage}")
    # print(f"[Outside context][EXPERIMENT] Lifecycle: {corr_exp.lifecycle_stage}")
    ## ===========================================================

    ## 7.  ======= Create run using MLFlowClient ==========
    ## This creates a RUNNING status run object => equivalent to mlflow.start_run() without with statement
    ## Explicitly terminate run using client.set_terminated
    client = mlflow.MlflowClient()
    # client_run_obj = client.create_run(
    #     experiment_id=mlflow.get_experiment_by_name("experiment1").experiment_id,
    #     run_name="client_run6",
    # )
    # print(f"client_run_obj type: {type(client_run_obj)}")
    # print(
    #     f"client_run_obj details: {json.dumps(client_run_obj.to_dictionary(), indent=4)}"
    # )

    # mlflow.log_metrics(
    #     {"accuracy": 10}, run_id=client_run_obj.info.run_id
    # )  ## Does not work since run is not an active run
    # mlflow.log_params({"p1": 100}, run_id=client_run_obj.info.run_id)
    # client.set_terminated(client_run_obj.info.run_id)
    ## ===========================================================

    ## ========== 8. Delete run ==============================
    # client.delete_run(run_id="20d7281cb5394ffb87537eed4542af3f")
    # client.delete_run(run_id="a133f22f24f24aea8932a22fe7fe49a4")
    # client.delete_run(run_id="9763b1a5d26045439ae5cdae9e84f9fe")
    # client.delete_run(run_id="8627e71549aa4db1ae2ff71cd12a21d6")
    ## ===========================================================

    ## ==========  9. Get rin by run_id ==============================
    # mlflow.get_run(run_id=...)
    # client.get_run(run_id=...)
    ## ===========================================================

    ## ==========  10. Get active run ==============================
    # current_run = mlflow.start_run(run_name="active_run")  ## Creates an active run
    # print(f"run id: {current_run.info.run_id}")

    # active_run = mlflow.active_run()
    # print(f"active run id: {active_run.info.run_id}")

    # client_run = client.create_run(
    #     experiment_id="0", run_name="non_active_run"
    # )  ## Just creates a run (non active)

    # updated_active_run = mlflow.active_run()
    # print(f"updated run id: {updated_active_run.info.run_id}")
    ## ===========================================================

    ## ==========  11. Add tags to runs ==============================
    ### Start a new run under experiment1 and name it tag_run
    with mlflow.start_run(
        run_name="tag_run",
        experiment_id=mlflow.get_experiment_by_name(name="experiment1").experiment_id,
    ) as run:
        ## Add tags to it
        mlflow.set_tags({"t1": "v1", "t2": "v2"})

    ## Get active run => NONE since it is outside with block
    active_run = mlflow.active_run()
    print(f"active_run: {active_run}")

    ## Get last active run and print its tags
    last_run = mlflow.last_active_run()
    print(f"run tags: {json.dumps(last_run.to_dictionary(), indent=4)}")

    ## Restart last run and add more tags to it.
    with mlflow.start_run(run_id=last_run.info.run_id) as run:
        mlflow.set_tags({"updated_t3": "t3", "updated_t4": "t4"})

    ## Get last active run and print its tags
    updated_last_run = mlflow.last_active_run()
    print(f"run tags: {json.dumps(updated_last_run.to_dictionary(), indent=4)}")
    ## ===========================================================
