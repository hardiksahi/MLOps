import mlflow
from pathlib import Path
import random
from functools import partial
from itertools import starmap
from more_itertools import consume

mlflow.set_tracking_uri(
    uri=(
        Path("/Users/hardiksahi/Personal/MLOps/tutorials/ml_flow") / "mlnestedruns"
    ).as_uri()
)

print(mlflow.get_tracking_uri())


def log_run(run_name):
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("param1", random.choice(["a", "b", "c"]))
        mlflow.log_param("param2", random.choice([1, 2, 3]))
        mlflow.log_metric("metric1", random.uniform(0, 1))
        mlflow.log_metric("metric2", abs(random.gauss(5, 2.5)))


def generate_run_names(test_no, num_runs=5):
    return [f"run_{i}_test_{test_no}" for i in range(num_runs)]


def execute_tuning(test_no):
    runs = starmap(log_run, [(run_name,) for run_name in generate_run_names(test_no)])
    consume(runs)


def execute_no_child_run_experiment():
    print("==== Naive approach ====")

    ## Count of parent runs: 5. Each parent run has 5 child runs (no as per this heirarchy here.)
    ## Analogy:
    ## - Experiment: Given dataset (e.g. 2023-2025)
    ## - Parent run: Logistic Regression, XGBoost (5 such options) (test_no)
    ## - Child run: Hyperparam combination per parent run (5 combo) (num_runs)

    ## Create experiment named No Child Runs
    no_child_experiment = mlflow.create_experiment(
        name="No Child Runs", tags={"mlflow.note.content": "No Child Runs"}
    )

    ## Set No Child Runs experiment as active experiment
    mlflow.set_experiment(experiment_name="No Child Runs")
    consume(starmap(execute_tuning, [(x,) for x in range(5)]))


## ***********************************************************************


def execute_parent_child_run_log_run(
    run_name, param_choice_dict, metric_choice_dict, parent_run_tag
):
    with mlflow.start_run(run_name=run_name, nested=True) as run:
        param_value_dict = {}
        for param_name, value_list in param_choice_dict.items():
            v = random.choice(value_list)
            mlflow.log_param(param_name, v)
            param_value_dict[param_name] = v

        metric_value_dict = {}
        for metric_name, value_tuple in metric_choice_dict.items():
            v = random.uniform(value_tuple[0], value_tuple[1])
            mlflow.log_metric(metric_name, v)
            metric_value_dict[metric_name] = v

        ## Child run is also tagged with parent_run_tag
        mlflow.set_tag("parent_run_identifier", parent_run_tag)

        return_metric_name = list(metric_value_dict.keys())[0]
        return (
            run.info.run_id,
            return_metric_name,
            metric_value_dict[return_metric_name],
            param_value_dict,
        )


def execute_parent_child_run_generate_run_names(
    parent_run_identifier, num_child_runs=5
):
    return [
        f"run_{i}_for_parent_{parent_run_identifier}" for i in range(num_child_runs)
    ]


def execute_parent_child_run_tuning(
    parent_run_identifier, param_choice_dict, metric_choice_dict
):
    best_metric1 = float("-inf")
    best_param_dict = None
    best_child_run = None
    with mlflow.start_run(run_name=f"parent_run_{parent_run_identifier}"):

        mlflow.set_tag("parent_run_identifier", parent_run_identifier)
        runs = list(
            starmap(
                execute_parent_child_run_log_run,
                [
                    (
                        run_name,
                        param_choice_dict,
                        metric_choice_dict,
                        parent_run_identifier,
                    )
                    for run_name in execute_parent_child_run_generate_run_names(
                        parent_run_identifier
                    )
                ],
            )
        )

        for run_id, metric_name, metric_value, param_value_dict in runs:
            if metric_value > best_metric1:
                best_metric1 = metric_value
                best_param_dict = param_value_dict
                best_child_run = run_id

        mlflow.log_metric(f"best_{metric_name}", best_metric1)
        mlflow.set_tag(key="best_child_run", value=best_child_run)

        for param_name, value in best_param_dict.items():
            mlflow.log_param(param_name, value)

        consume(runs)


def execute_parent_child_run_experiment(custom_param_test_count: int):
    print("====== Parent-child run association approach ======")

    # child_run_experimen_id = mlflow.create_experiment(
    #     name="Nested Child Association",
    #     tags={"mlflow.note.content": "Nested Child Association"},
    # )

    # mlflow.set_experiment(experiment_id=child_run_experimen_id)

    mlflow.set_experiment(experiment_name="Nested Child Association")

    model_type_dict = {}
    model_type_dict[f"lr_{custom_param_test_count}"] = {
        "param_choice_dict": {
            "penalty": ["l1", "l2", "a", "b"],
            "solver": ["lbfgs", "liblinear", "zzz"],
        },
        "metric_choice_dict": {"accuracy": [0, 1], "precision": [0, 1]},
    }

    model_type_dict[f"svm_{custom_param_test_count}"] = {
        "param_choice_dict": {
            "kernel": ["linear", "poly", "rbf", "ddd"],
            "decision_function_shape": ["ovo", "ovr"],
        },
        "metric_choice_dict": {"accuracy": [0, 1], "precision": [0, 1]},
    }
    consume(
        starmap(
            execute_parent_child_run_tuning,
            [
                (
                    model_type,
                    inner_dict["param_choice_dict"],
                    inner_dict["metric_choice_dict"],
                )
                for model_type, inner_dict in model_type_dict.items()
            ],
        )
    )


## https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/hyperparameter-tuning/part1-child-runs/
if __name__ == "__main__":
    # execute_no_child_run_experiment()
    # execute_parent_child_run_experiment()

    # experiment = mlflow.get_experiment_by_name(name="Nested Child Association")
    # mlflow.delete_experiment(experiment_id=experiment.experiment_id)

    ## The idea is that we can create parent and child runs
    execute_parent_child_run_experiment(custom_param_test_count=4)
