# coding: utf-8

import json
from pathlib import Path
from app import settings

class DatasetManager:
    _tampon: int

    def __init__(self):
        ...
    
    def add_record(self, data: dict) -> bool:
        dataset_path = settings.DATASET_PATH / 'dataset.json'
        if not Path(dataset_path).is_file():
            with open(dataset_path, 'w') as file:
                file.write('[]')

        with open(dataset_path, 'r') as file:
            df = json.load(file)
            df.append(data)
            
        with open(dataset_path, 'w') as file:
            json.dump(df, file, indent=2, ensure_ascii=False)
        return True




