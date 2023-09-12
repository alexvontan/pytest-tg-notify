import os.path
from pathlib import Path
import yaml


def read_yaml(name=None):
    loader = yaml.SafeLoader
    project = Path(__file__).parent.parent
    path = os.path.join(project, name)
    with open(path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=loader)
        return data

