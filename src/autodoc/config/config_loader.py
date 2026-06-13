import yaml

from autodoc.datamodels.repo_config import RepoConfig
from autodoc.config.runtime_config import Config


def load_config(path: str) -> Config:
    """
    Load configuration from a YAML file.

    Args:
        path (str): Path to the YAML configuration file.

    Returns:
        Config: Parsed configuration object.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        yaml.YAMLError: If the configuration file contains invalid YAML.
        ValueError: If required configuration keys are missing.
    """
    try:
        with open(path, "r") as f:
            config_data = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in configuration file: {e}")

    required_keys = {"repos", "model", "worktree_root"}
    if not required_keys.issubset(config_data.keys()):
        missing = required_keys - config_data.keys()
        raise ValueError(f"Missing required configuration keys: {missing}")

    repos = [RepoConfig(**repo) for repo in config_data["repos"]]

    return Config(
        repos=repos,
        model=config_data["model"],
        worktree_root=config_data["worktree_root"],
    )