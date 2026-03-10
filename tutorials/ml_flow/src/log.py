import mlflow
from pathlib import Path
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from mlflow.models import infer_signature

mlflow.set_tracking_uri(
    uri=(
        Path("/Users/hardiksahi/Personal/MLOps/tutorials/ml_flow") / "mlrunslogupdated"
    ).as_uri()
)

print(mlflow.get_tracking_uri())


if __name__ == "__main__":

    ## ======= 1. experiment and run to log param and metric  =======
    experiment_id = mlflow.create_experiment(
        name="log_experiment", tags={"description": "log values experiment"}
    )

    # with mlflow.start_run(run_name="log_run", experiment_id=experiment_id) as run:
    #     mlflow.log_param(key="param1", value=1)
    #     mlflow.log_param(key="param2", value=2)
    #     mlflow.log_metric(key="metric1", value=0.98)
    #     mlflow.log_metric(key="metric2", value=0.5)

    # =============================================================

    # ========= 2. MLFLOW client based experiment, run , log and termination ===========
    # client = mlflow.MlflowClient()
    # client_experiment_id = client.create_experiment(
    #     name="client_log_experiment",
    #     tags={"description": "client log values experiment"},
    # )

    # client_run = client.create_run(
    #     experiment_id=client_experiment_id, run_name="client_log_run"
    # )
    # client.log_param(run_id=client_run.info.run_id, key="param1", value=1)
    # client.log_param(run_id=client_run.info.run_id, key="param2", value=2)
    # client.log_metric(run_id=client_run.info.run_id, key="metric1", value=0.98)

    # client.set_terminated(run_id="be50cf9f97e84c9f81694d3c2a39a674")
    # =============================================================

    ## ============ 3. Logging artifacts to artifact path ==========================
    # experiment_id = mlflow.get_experiment_by_name(name="log_experiment").experiment_id
    # with mlflow.start_run(run_name="log_artifacts", experiment_id=experiment_id) as run:
    #     print(f"artifact path: {mlflow.get_artifact_uri()}")
    #     mlflow.log_artifact(
    #         local_path="/Users/hardiksahi/Personal/MLOps/tutorials/ml_flow/pyproject.toml",
    #         artifact_path="wow",
    #     )
    #     mlflow.log_artifacts(
    #         local_dir="/Users/hardiksahi/Personal/MLOps/tutorials/ml_flow/log_images",
    #         artifact_path="images",
    #     )

    #     mlflow.log_params({"param1": "p1", "param2": "p2"})
    #     mlflow.log_metrics({"metric1": 0.99, "metric2": 0.7})
    #     mlflow.log_dict(
    #         dictionary={"name": "hardik", "age": 33}, artifact_file="dict_dir/data.yaml"
    #     )

    # =============================================================================

    ## ============ 4. Logging ML model ==========================
    experiment_id = mlflow.get_experiment_by_name(name="log_experiment").experiment_id
    iris = load_iris(as_frame=True)
    X = iris.data
    y = iris.target
    model = RandomForestClassifier().fit(X, y)

    with mlflow.start_run(run_name="log_model", experiment_id=experiment_id) as run:
        signature = infer_signature(iris.data, model.predict(X))
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            serialization_format="cloudpickle",
            signature=signature,
            input_example=X.iloc[[0]],
            # registered_model_name="rf_model",
            name="rf_model",
        )

        mlflow.log_dict(
            dictionary={"name": "hardik", "age": 33}, artifact_file="dict_dir/data.yaml"
        )

        mlflow.log_artifacts(
            local_dir="/Users/hardiksahi/Personal/MLOps/tutorials/ml_flow/log_images",
            artifact_path="images",
        )

        loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)
        print(f"model_info.model_uri: {model_info.model_uri}")
        result = loaded_model.predict(X.iloc[[20]])

        print(result)
