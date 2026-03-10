import mlflow
import mlflow.pyfunc

from pathlib import Path
from typing import Any
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mlflow.models import infer_signature

mlflow.set_tracking_uri(
    uri=(
        Path("/Users/hardiksahi/Personal/MLOps/tutorials/ml_flow")
        / "mlrunslogcustommodel"
    ).as_uri()
)


class AddN(mlflow.pyfunc.PythonModel):
    def __init__(self, n):
        self.n = n

    def predict(self, context, model_input, params: dict[str, Any] | None = None):
        return model_input.apply(lambda column: column + self.n)


class Lissagous(mlflow.pyfunc.PythonModel):
    def __init__(self, A, B, num_points=1000):
        self.A = A  ## amplitude along x axis
        self.B = B  ## amplitude along y axis
        self.num_points = num_points
        self.t_range = (0, 2 * np.pi)

    def generate_curve(self, a, b, delta):
        ## a, b are angular frequenceis along x and y respectively
        t = np.linspace(self.t_range[0], self.t_range[1], self.num_points)
        x = self.A * np.sin(a * t + delta)
        y = self.B * np.sin(b * t)
        return pd.DataFrame({"x": x, "y": y})

    def predict(self, context, model_input, params: dict[str, Any] | None = None):

        ## 1. Get frequencies a and b
        a = model_input["a"].iloc[0]
        b = model_input["b"].iloc[0]

        ## 2. Get delta
        delta = params.get("delta", 0)

        df = self.generate_curve(a=a, b=b, delta=delta)

        sns.set_theme()

        ## 3. Plot
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(df["x"], df["y"])
        ax.set_title("Lissajous Curve")

        # Define the annotation string
        annotation_text = f"""
        A = {self.A}
        B = {self.B}
        a = {a}
        b = {b}
        delta = {np.round(delta, 2)} rad
        """

        ax.annotate(
            annotation_text,
            xy=(1.05, 0.5),
            xycoords="axes fraction",
            fontsize=12,
            bbox={
                "boxstyle": "round,pad=0.25",
                "facecolor": "aliceblue",
                "edgecolor": "black",
            },
        )

        # Adjust plot borders to make space for the annotation
        plt.subplots_adjust(right=0.65)
        plt.close()

        return fig


## https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/creating-custom-pyfunc/notebooks/
if __name__ == "__main__":
    print(mlflow.get_tracking_uri())

    # experiment_id = mlflow.create_experiment(
    #     name="log_custom_model", tags={"description": "log custom models"}
    # )

    ## ======= 1. Create a custom model AddN and log it to a run =======
    # model_path = "/tmp/add_n_model2"
    # add_5_model = AddN(n=5)

    # ## Save model
    # mlflow.pyfunc.save_model(path=model_path, python_model=add_5_model)

    # ## Load model
    # loaded_model = mlflow.pyfunc.load_model(model_path)

    # ## Perform prediction
    # model_output = loaded_model.predict(pd.DataFrame([range(10)]))
    # print(model_output)

    # with mlflow.start_run(
    #     run_name="log_AddN(n=5)_model",
    #     experiment_id=mlflow.get_experiment_by_name(
    #         name="log_custom_model"
    #     ).experiment_id,
    # ):
    #     model_info = mlflow.pyfunc.log_model(name="model", python_model=AddN(5))
    #     print(f"Model saved to : {model_info.model_uri}")

    #     run_id = mlflow.active_run().info.run_id

    # # loaded_model = mlflow.pyfunc.load_model(model_uri=model_info.model_uri)
    # loaded_model = mlflow.pyfunc.load_model(model_uri=f"runs:/{run_id}/model")

    # model_output = loaded_model.predict(pd.DataFrame([range(10)]))
    # print(model_output)

    ## =====================================================================

    ## ======= 2. Create a custom model Lissagous and log it to a run =======
    # l_model = Lissagous(
    #     A=1, B=1, num_points=10_000
    # )  ## Fixed model for given amplitudes A and B

    # df = l_model.generate_curve(a=1, b=2, delta=np.pi / 5)
    # print(df.head())

    signature = infer_signature(
        pd.DataFrame([{"a": 1, "b": 2}]), params={"delta": np.pi / 5}
    )

    with mlflow.start_run(
        run_name="log_Lissagous_model",
        experiment_id=mlflow.get_experiment_by_name(
            name="log_custom_model"
        ).experiment_id,
    ) as run:
        mlflow.pyfunc.log_model(
            name="lissajous_model",
            signature=signature,
            python_model=Lissagous(1, 1, 10_000),
        )
        run_id = mlflow.active_run().info.run_id

    loaded_model = mlflow.pyfunc.load_model(model_uri=f"runs:/{run_id}/lissajous_model")

    fig = loaded_model.predict(pd.DataFrame({"a": [3], "b": [2]}), {"delta": np.pi / 3})
    ##fig.savefig("/Users/hardiksahi/Downloads/plot.png", dpi=150)
    ## =====================================================================
