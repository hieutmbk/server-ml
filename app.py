# -*- coding: utf-8 -*-
from flask import Flask, request
from sklearn.pipeline import Pipeline
from feature_transformer import FeatureTransformer
import json
from underthesea import ner,word_tokenize
from sklearn.externals import joblib
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
        print(str)
        ner_word = ner(str)
        print(ner_word)
        search_word = ""
        qa_word = ""
        for i in range(len(ner_word)):
            if (ner_word[i][3] in ["B-PER","I-LOC", "I-PER","B-LOC","B-ORG"]):
                search_word = search_word + ner_word[i][0] + " ";

            if( ( (ner_word[i][1]=='N') & (ner_word[i][3]=='O') ) | ( (ner_word[i][1]=='V') & (ner_word[i][0] != 'là') ) | (ner_word[i][1]=='M')):
                first_word = ner_word[i][0][0]
                if(first_word.isupper()):
                    if( (ner_word[i][0] == "Quê") | (ner_word[i][0] == "GDP") ):

                        qa_word = qa_word + ner_word[i][0] + " ";
                    else:
                        search_word = search_word + ner_word[i][0] + " ";

                else:
                    qa_word = qa_word + ner_word[i][0] + " ";
            if ((ner_word[i][1] == 'A') & (ner_word[i][3] == 'O')):
                qa_word = qa_word + ner_word[i][0] + " ";
        search_word.strip()
        print(search_word)
        qa_word.strip()

        if (predict(pipe_line, str) in ["person","organization"]):
            wiki = wikipedia.page(search_word)
            result = {
                'str' : str,
                'predict': predict(pipe_line, str),
                'ner' : ner_tag(str.encode('utf-8')),
                'url_wiki' : wiki.url,
                'qa_word' : qa_word,
                'summary' : wiki.summary,

            }

            return json.dumps(result)
        else :
            result = {
                'str': str,
                'predict': predict(pipe_line, str),
                'ner': ner_tag(str.encode('utf-8'))
            }
            return json.dumps(result)

if __name__ == '__main__':
    app.run()

