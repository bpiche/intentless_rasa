"""
"""
import os
import spacy
import numpy as np
import pandas as pd
from tqdm import tqdm

from pathlib import Path

tqdm.pandas()


nlp = spacy.load('en_core_web_lg', 
                 exclude=["tagger", 
                          "parser", 
                          "senter", 
                          "attribute_ruler", 
                          "lemmatizer", 
                          "ner"])


# TODO: keep track of the category that the document came from 
def vectorize_faqs(filetype, path, acronyms=None):
    """
    """
    # read all the FAQ csv files from gcp
    docs = Path(path).glob(f'*.{filetype}')
    # and concatenate them into a single dataframe
    df = pd.concat([pd.read_csv(f) for f in docs])
    # vectorize the questions
    df['sent_vectors'] = df.Question.progress_apply(lambda x: nlp(x).vector)
    df = df[['Question', 'Answer', 'sent_vectors']]
    return df


def compare_faqs(query, df):
    """
    """
    # compare vectorized user input to vectorized questions
    query_vect = nlp(query).vector
    # compare the vectorized user input to the vectorized questions
    df['similarity'] = df.sent_vectors.apply(lambda x: np.dot(x, query_vect) / (np.linalg.norm(x) * np.linalg.norm(query_vect)))
    results_df = df.sort_values('similarity', ascending=False)[0:10]
    response = {'question': query,
                'answer': results_df.iloc[0]['Answer'],
                # TODO: can't return a float32 with flask, cast it as double
                # 'similarity': results_df.iloc[0]['similarity'],
    }
    return response


if __name__ == "__main__":
    """
    """
    pass