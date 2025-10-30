from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession

PROJECT_PACKAGE_NAME = "kedro2package"


def run_kedro(pipeline_name: str = None, tags: list[str] = None, env: str = "base"):
    """
    Programmatically run a Kedro pipeline and return its outputs.

    Args:
        pipeline_name (str, optional): Name of the pipeline to run.
        tags (list[str], optional): Tags to filter which nodes to run.

    Returns:
        dict: A dictionary mapping dataset names to outputs.
    """
    configure_project(PROJECT_PACKAGE_NAME)

    with KedroSession.create(env=env) as session:
        output = session.run(pipeline_name=pipeline_name, tags=tags)
    return output


if __name__ == "__main__":
    # Example 1: run the default pipeline
    result = run_kedro(pipeline_name="data_processing")

    # Example 2: run a specific pipeline or tagged subset
    # result = run_kedro(pipeline_name="data_science", tags=["train"])

    print("✅ Kedro pipeline finished successfully.")
    print(f"Available outputs: {list(result.keys())}")
