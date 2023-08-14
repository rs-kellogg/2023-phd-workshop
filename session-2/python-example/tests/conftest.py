import os
import pytest
import yaml
import pandas as pd
from pathlib import Path
from typing import Dict


dir_path = Path(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def config() -> Dict:
    config_file = dir_path / "config.yml"
    with open(config_file) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
        return conf

@pytest.fixture(scope="session")
def sample_1() -> pd.DataFrame:
    return pd.read_csv(dir_path/"sample-1.csv")


@pytest.fixture(scope="session")
def sample_100() -> pd.DataFrame:
    return pd.read_csv(dir_path/"sample-100.csv")