import glob
import os
import pickle

from ml_experiments.artifacts import Artifact


class Result:
    """Result contains the result of an experiment.

    Usage:
    ```python
    return ml_experiments.Result(
        name='testing-123',
        artifacts=[
            ml_experiments.artifacts.KerasHistory(history, name="fit_history"),
            ml_experiments.artifacts.Metrics(metrics, name="eval_metrics"),
        ],
    )
    ```

    Args:
        name: string identifier for the experiment
        artifacts: (Optional) list of `ml_experiments.artifacts.Artifact` to be included in the
            result.
    """

    def __init__(self, name, artifacts=None):
        if not _all_artifacts(artifacts):
            raise ValueError(
                "Expected all of `artifacts` to be subclasses of "
                "`ml_experiments.artifacts.Artifact`.  Instead, got "
                f"artifacts={artifacts}."
            )
        if not isinstance(name, str):
            raise ValueError(f"Expected `name` to be a string, instead got name={name}")
        self.name = name
        self.artifacts = artifacts or []

    def get(self, name):
        for artifact in self.artifacts:
            if artifact.name == name:
                return artifact
        raise ValueError(
            f"Didn't find an artifact with name `name={name}`. "
            "Instead, found artifacts with the following names: "
            f"[{', '.join([a.name for a in self.artifacts])}]"
        )

    @staticmethod
    def load(path):
        with open(f"{path}/results.p", "rb") as f:
            result = pickle.load(f)
        return result

    @staticmethod
    def load_collection(path):
        return [Result.load(path) for path in glob.glob(f"{path}/*")]

    def serialize_to(self, artifacts_dir):
        subdir = f"{artifacts_dir}/{self.name}"
        os.makedirs(subdir, exist_ok=True)

        # TODO(lukewood): pickle.load/dump/etc!
        for artifact in self.artifacts:
            artifact.serialize_to(subdir)


def _all_artifacts(artifacts):
    return all([isinstance(x, Artifact) for x in artifacts])
