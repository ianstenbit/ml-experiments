import ml_collections


def get_config():

    config = ml_collections.ConfigDict()
    # initialize model types

    config.artifact_dir = FLAGS.artifact_dir
    config.log_dir = f"{config.artifact_dir}/logs"

    config.model_type = ml_experiments.Sweep(["resnet50", "efficientnetv2"])
    config.augmenter_type = ml_experiments.Sweep(["basic", "optimized"])
    return config
