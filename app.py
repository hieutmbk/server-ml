# -*- coding: utf-8 -*-
from flask import Flask, request
from sklearn.pipeline import Pipeline
from feature_transformer import FeatureTransformer
import json
from underthesea import ner
from sklearn.externals import joblib

PORT = 5000

app = Flask(__name__)

sav_filename = 'svm_model.sav'
filename_countvect = 'finalized_countvectorizer.sav'
filename_tfidf = 'finalized_tfidftransformer.sav'

clf_svm = joblib.load(sav_filename)
loaded_cvec = joblib.load(filename_countvect)
loaded_tfidf_transformer = joblib.load(filename_tfidf)
pipe_line = Pipeline([
    ("transformer", FeatureTransformer()),
    ("vect", loaded_cvec),
    ("tfidf", loaded_tfidf_transformer),
    ("clf-svm", clf_svm)
])

@app.route('/')
def home():
    return 'it works'


def predict(model, text):
    return model.predict([text])[0]


@app.route('/predict', methods=['GET'])
def extract():
    """Return the movie review sentiment score.
    
    Returns a JSON object :
    {
         "sentiment": "positive"
    }
    """
    if request.method == 'GET':
        description = request.args['str']
        print(description)
        result = {
            'predict': predict(pipe_line, description),
            'ner' : ner(description)
        }
        return json.dumps(result) 


if __name__ == '__main__':
    app.run()

