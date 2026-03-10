import mlflow
from joblib import dump
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from mlflow.models import infer_signature
import mlflow.pyfunc
import mlflow.sklearn

mlflow.set_tracking_uri("http://localhost:9000")


class ModelWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self):
        self.model = None

    def load_context(self, context):
        ##Load logged model here
        model_uri = context.artifacts["model_uri"]
        self.model = mlflow.sklearn.load_model(model_uri=model_uri)

    def predict(self, context, model_input, params=None):
        params = params or {"predict_method": "predict"}
        predict_method = params.get("predict_method")

        if predict_method == "predict":
            return self.model.predict(model_input)
        elif predict_method == "predict_proba":
            return self.model.predict_proba(model_input)
        elif predict_method == "predict_log_proba":
            return self.model.predict_log_proba(model_input)
        else:
            raise ValueError(
                f"The prediction method '{predict_method}' is not supported."
            )


if __name__ == "__main__":
    print(f"tracking uri: {mlflow.get_tracking_uri()}")

    iris = load_iris()
    x = iris.data[:, 2:]
    y = iris.target

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=9001
    )

    model = LogisticRegression(random_state=0, max_iter=5_000, solver="newton-cg").fit(
        x_train, y_train
    )
    signature = infer_signature(
        model_input=x_train, model_output=model.predict(x_train)
    )

    # experiment_id = mlflow.create_experiment(
    #     name="log_custom_model", tags={"description": "log custom models"}
    # )

    with mlflow.start_run(
        run_name="customize_pyfunc_predict",
        experiment_id=mlflow.get_experiment_by_name(
            name="log_custom_model"
        ).experiment_id,
    ) as run:
        ## Logged model
        mlflow.sklearn.log_model(
            sk_model=model, name="linear_regression_model", signature=signature
        )
        run_id = run.info.run_id

    # loaded_model = mlflow.sklearn.load_model(
    #     model_uri=f"runs:/{run_id}/linear_regression_model"
    # )

    # result = loaded_model.predict(x[10, :].reshape(1, -1))

    # print(result)

    artifacts = {"model_uri": f"runs:/{run_id}/linear_regression_model"}
    # pyfunc_model = ModelWrapper()
    # pyfunc_model.load_context(artifacts)

    # predicted_label = pyfunc_model.predict(
    #     context=artifacts,
    #     model_input=x[10, :].reshape(1, -1),
    #     params={"predict_method": "predict"},
    # )

    # print(f"predicted_label: {predicted_label}")

    # predict_proba = pyfunc_model.predict(
    #     context=artifacts,
    #     model_input=x[10, :].reshape(1, -1),
    #     params={"predict_method": "predict_proba"},
    # )

    # print(f"predict_proba: {predict_proba}")

    # predict_log_proba = pyfunc_model.predict(
    #     context=artifacts,
    #     model_input=x[10, :].reshape(1, -1),
    #     params={"predict_method": "predict_log_proba"},
    # )

    # print(f"predict_log_proba: {predict_log_proba}")

    ## Log pyfunc nodel to mlflow
    with mlflow.start_run(run_id=run_id) as run:
        updated_signature = infer_signature(
            model_input=x_train, params={"predict_method": "predict_proba"}
        )

        print(f"updated_signature for pyfunc model: {updated_signature}")
        pyfunc_model = ModelWrapper()
        # pyfunc_model.load_context(artifacts)

        mlflow.pyfunc.log_model(
            name="pyfunc_linear_regression",
            python_model=pyfunc_model,
            signature=updated_signature,
            artifacts=artifacts,
            registered_model_name="registered_pyfunc_linear_regression",
        )

    logged_pyfunc_model = mlflow.pyfunc.load_model(
        model_uri=f"runs:/{run_id}/pyfunc_linear_regression"
    )

    predicted_label = logged_pyfunc_model.predict(
        data=x[10, :].reshape(1, -1),
        params={"predict_method": "predict"},
    )

    print(f"[logged_pyfunc_model] predicted_label: {predicted_label}")

    predict_proba = logged_pyfunc_model.predict(
        data=x[10, :].reshape(1, -1),
        params={"predict_method": "predict_proba"},
    )

    print(f"[logged_pyfunc_model] predict_proba: {predict_proba}")

    predict_log_proba = logged_pyfunc_model.predict(
        data=x[10, :].reshape(1, -1),
        params={"predict_method": "predict_log_proba"},
    )

    print(f"[logged_pyfunc_model] predict_log_proba: {predict_log_proba}")

    ## Load registed model

    # registred_pyfunc_model = mlflow.pyfunc.load_model(
    #     model_uri=f"models:/registered_pyfunc_linear_regression@best_model_till_now"
    # )

    # predicted_label = registred_pyfunc_model.predict(
    #     data=x[10, :].reshape(1, -1),
    #     params={"predict_method": "predict"},
    # )

    # print(f"[registred_pyfunc_model] predicted_label: {predicted_label}")

    # predict_proba = registred_pyfunc_model.predict(
    #     data=x[10, :].reshape(1, -1),
    #     params={"predict_method": "predict_proba"},
    # )

    # print(f"[registred_pyfunc_model] predict_proba: {predict_proba}")

    # predict_log_proba = registred_pyfunc_model.predict(
    #     data=x[10, :].reshape(1, -1),
    #     params={"predict_method": "predict_log_proba"},
    # )

    # print(f"[registred_pyfunc_model] predict_log_proba: {predict_log_proba}")
