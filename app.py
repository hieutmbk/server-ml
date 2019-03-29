# -*- coding: utf-8 -*-
from flask import Flask, request
from sklearn.pipeline import Pipeline
from feature_transformer import FeatureTransformer
import json
from underthesea import ner
from sklearn.externals import joblib
from crawl_wiki_summary import MySpider
from scrapy.crawler import CrawlerProcess
import wikipedia

wikipedia.set_lang("vi")
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
def ner_tag(str) :
    return ner(str)

@app.route('/predict', methods=['GET'])
def extract():

    if request.method == 'GET':
        str = request.args['str']
        ner_word = ner(str)
        word_search = ""
        for i in range(len(ner_word)):

            if (ner_word[i][3] in ["B-PER","I-LOC", "I-PER","B-LOC"]):
                word_search = word_search + ner_word[i][0] + " ";
        word_search.strip()

        wiki = wikipedia.page(word_search)
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(MySpider, myurls=[
            wiki.url
        ])
        process.start()

        with open('data.json', 'r') as f:
            datastore = json.load(f)

        result = {
            'str' : str,
            'predict': predict(pipe_line, str),
            'ner' : ner_tag(str.encode('utf-8')),
            'summary' : wiki.summary,
            'infor' : datastore
        }
        return json.dumps(result) 


if __name__ == '__main__':
    app.run()

