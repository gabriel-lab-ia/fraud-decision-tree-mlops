from importlib.metadata import PackageNotFoundError, version

PACKAGE_NAME = "fraud-decision-tree-mlops"


def get_project_version() -> str:
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "0.3.0"
