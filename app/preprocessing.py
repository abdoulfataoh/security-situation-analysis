# coding: utf8

import json
from pathlib import Path

class Preprepossing:
    _dataset_path: Path

    def __init__(self, dataset_path: Path) -> None:
        self._dataset_path = dataset_path
    
    def process(self):
        with open(self._dataset_path, 'r') as file:
            df = json.load(file)

            # transforme to lowcase
            for data in df:
                data['article_title'] = data.

        