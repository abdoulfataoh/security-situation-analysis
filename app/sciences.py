# coding: utf-8

import json
import string
from statistics import mean

import pandas as pd

class Sciences:
    _dataset: pd
    _cleaned_dataset: pd
    _dataset_dict: dict

    def __init__(self, dataset_path) -> None:
        with open(dataset_path, 'r') as f:
            df_json = json.load(f)
            self._dataset_dict = df_json
            self._dataset = pd.DataFrame(df_json)
            self._format_dataset()
            self._clean_dataset()
    
    def _format_dataset(self):
        data_types = {
            'article_type': 'object',
            'article_title': 'object',  
            'published_date': 'datetime64',   
            'origin': 'object',          
            'url': 'object',           
            'content': 'object', 
            'comments_number': 'int',        
            'comments': 'object',           
        }
        self._dataset = self._dataset.astype(data_types)
    
    def _clean_dataset(self):
        self._cleaned_dataset = self._dataset.copy()
        self._cleaned_dataset['article_title'] = self._cleaned_dataset['article_title'].apply(lambda x: self.cleaner(x))
        self._cleaned_dataset['content'] = self._cleaned_dataset['content'].apply(lambda x: self.cleaner(x))
        self._cleaned_dataset['comments'] = self._cleaned_dataset['comments'].apply(lambda x: self.cleaner(x))

    
    def cleaner(self, data):
        if type(data) == str:
            clean_data = data.lower()
            clean_data = clean_data.replace('\n', ' ')
            clean_data = [char for char in clean_data if char not in string.punctuation]
            clean_data = ''.join(clean_data)
            clean_data = ' '.join(clean_data.split())
        elif type(data) == list:
            clean_data = []
            for comment in data:
                comment = comment.lower()
                comment = comment.replace('\n', ' ')
                comment = [char for char in comment if char not in string.punctuation]
                comment = ''.join(comment)
                comment = ' '.join(comment.split())
                comment = ' '.join(comment.split())
                clean_data.append(comment)
        return clean_data
    
    def describe_dataset(self):
        comments_number = self._dataset['comments_number']
        row_numb = int(self._dataset.shape[0])
        col_numb = int(self._dataset.shape[1])
        comments_sum = int(sum(comments_number))
        comments_min = int(min(comments_number))
        comment_max = int(max(comments_number))
        comment_mean = int(mean(comments_number))
        
        s = {
            'nombre de lignes': row_numb,
            'nombre de colonnes': col_numb,
            'nombre de commentaires': comments_sum,
            'nombre min de commentaire': comments_min,
            'nombre max de commentaire': comment_max,
            'moyenne commentaire / article': comment_mean
        }

        return s
    
    def get_samples(self):
        return self._dataset_dict

    def get_dataset(self):
        return self._dataset
