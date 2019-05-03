# -*- coding: utf-8 -*-
from os import abort

from flask import Flask, request
from sklearn.pipeline import Pipeline
from feature_transformer import FeatureTransformer
import json
import random
from underthesea import ner
from sklearn.externals import joblib
import pickle
import wikipedia
import re
from pyvi import ViTokenizer,ViPosTagger

wikipedia.set_lang("vi")
PORT = 5000

app = Flask(__name__)

sav_filename = 'model_classfication/model_1/svm_model.sav'
filename_countvect = 'model_classfication/model_1/finalized_countvectorizer.sav'
filename_tfidf = 'model_classfication/model_1/finalized_tfidftransformer.sav'

sav_filename_2 = 'model_classfication/model_2/svm_model.sav'
filename_countvect_2 = 'model_classfication/model_2/finalized_countvectorizer.sav'
filename_tfidf_2 = 'model_classfication/model_2/finalized_tfidftransformer.sav'

clf_svm = joblib.load(sav_filename)
loaded_cvec = joblib.load(filename_countvect)
loaded_tfidf_transformer = joblib.load(filename_tfidf)

clf_svm_2 = joblib.load(sav_filename_2)
loaded_cvec_2 = joblib.load(filename_countvect_2)
loaded_tfidf_transformer_2 = joblib.load(filename_tfidf_2)
pipe_line = Pipeline([
    ("transformer", FeatureTransformer()),
    ("vect", loaded_cvec),
    ("tfidf", loaded_tfidf_transformer),
    ("clf-svm", clf_svm)
])

pipe_line_2 = Pipeline([
    ("transformer", FeatureTransformer()),
    ("vect", loaded_cvec_2),
    ("tfidf", loaded_tfidf_transformer_2),
    ("clf-svm", clf_svm_2)
])

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word[-1:]': word[-1:],
        'word[0]' : word[0:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


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
        print(predict(pipe_line, str))
        if (predict(pipe_line, str) == "entity"):
            crf = pickle.load(open("model_ner/ner_entity_model.pkl", 'rb'))
            search_word = ""
            qa_word = ""
            ner_tags = []
            list = []
            x = ner(str)
            for i in x:
                ner_tags.append((i[0].replace(" ", "_"), i[1]))
            tags = crf.predict([sent2features(ner_tags)])[0]

            for i in range(len(ner_tags)):
                ner_tags[i] = (ner_tags[i][0].replace("_"," "), ner_tags[i][1], tags[i])
            print(ner_tags)
            for tag in ner_tags:
                if(tag[2] in ["B-PER","I-PER","B-LOC","I-LOC","B-ORG","I-ORG"]):
                    if (" sinh" in tag[0]):
                        search_word = search_word + tag[0].replace(" sinh","") + " ";
                        qa_word = qa_word + "sinh "
                        list.append(tag[0].replace(" sinh",""))
                        list.append("sinh")
                    elif (" quê" in tag[0]):
                        search_word = search_word + tag[0].replace(" quê", "") + " ";
                        qa_word = qa_word + "quê "
                        list.append(tag[0].replace(" quê", ""))
                        list.append("quê")
                    else:
                        search_word = search_word + tag[0]+ " ";
                        list.append(tag[0])
                if ( (((tag[1] == 'N') | (tag[1] == 'Np')) & (tag[2] == 'O')) | ((tag[1] == 'V') & (tag[0] != 'là')) | ((tag[1] == 'M') & (tag[2] == 'O')) | (tag[1] == 'A') | (tag[1] == 'FW')):
                    qa_word = qa_word + tag[0] + " "
                    list.append(tag[0])

            search_word.strip()
            search_word=search_word.replace("_sinh","")
            print(search_word)
            qa_word.strip()
            url = ""
            summary = ""
            if(search_word == ""):
                url = "null"
                summary="null"
            else:
                try:
                    wiki = wikipedia.page(wikipedia.search(search_word)[0])
                except wikipedia.DisambiguationError as e:
                    s = random.choice(e.options)
                    wiki = wikipedia.page(s)
                url = wiki.url
                summary = wiki.summary
            result = {
                'str' : str,
                'predict': predict(pipe_line, str),
                'predict_2': predict(pipe_line_2, str),
                'list' : list,
                'ner' : ner_tags,
                'url_wiki' : url,
                'qa_word' : qa_word,
                'summary' : summary,

            }

            return json.dumps(result)
        elif(predict(pipe_line, str) == "news") :
            crf = pickle.load(open("model_ner/ner_news_model.pkl", 'rb'))
            word_ner = ""
            x = ner(str)
            ner_tags = []
            for i in x:
                ner_tags.append((i[0].replace(" ", "_"), i[1]))
            tags = crf.predict([sent2features(ner_tags)])[0]
            for i in range(len(ner_tags)):
                ner_tags[i] = (ner_tags[i][0].replace("_"," "), ner_tags[i][1], tags[i])
            print(ner_tags)
            for tag in ner_tags:
                if (tag[2] in ["B-NEWS", "I-NEWS"]):
                    word_ner = word_ner+ tag[0]+" ";
            word_ner.strip().replace("_"," ")
            result = {
                'str': str,
                'predict': predict(pipe_line, str),
                'word_ner': word_ner,
            }

            return json.dumps(result)
        elif (predict(pipe_line, str) == "location"):
            crf = pickle.load(open("model_ner/ner_location_model.pkl", 'rb'))
            word_ner = ""
            x = ner(str)
            ner_tags = []
            for i in x:
                ner_tags.append((i[0].replace(" ", "_"), i[1]))
            tags = crf.predict([sent2features(ner_tags)])[0]
            for i in range(len(ner_tags)):
                ner_tags[i] = (ner_tags[i][0].replace("_"," "), ner_tags[i][1], tags[i])
            print(ner_tags)
            for tag in ner_tags:
                if (tag[2] in ["B-PLACE", "I-PLACE","B-LOC","I-LOC"]):
                    word_ner = word_ner + tag[0] + " ";
            word_ner.strip().replace("_"," ")
            result = {
                'str': str,
                'predict': predict(pipe_line, str),
                'word_ner': word_ner,
            }

            return json.dumps(result)
        elif (predict(pipe_line, str) == "product"):
            crf = pickle.load(open("model_ner/ner_product_model.pkl", 'rb'))
            word_ner = ""
            locaion = ""
            x = ner(str)
            ner_tags = []
            for i in x:
                ner_tags.append((i[0].replace(" ", "_"), i[1]))
            tags = crf.predict([sent2features(ner_tags)])[0]
            for i in range(len(ner_tags)):
                ner_tags[i] = (ner_tags[i][0].replace("_"," "), ner_tags[i][1], tags[i])
            for tag in ner_tags:
                if (tag[2] in ["B-PROD", "I-PROD"]):
                    word_ner = word_ner + tag[0] + " ";
                if (tag[2] in ["B-LOC","I-LOC"]):
                    locaion = locaion + tag[0] + " ";
            word_ner.strip().replace("_"," ")
            locaion.strip().replace("_"," ")
            result = {
                'str': str,
                'predict': predict(pipe_line, str),
                'word_ner': word_ner,
                'location': locaion

            }

            return json.dumps(result)
        elif (predict(pipe_line, str) == "time"):
            result = {
                'str': str,
                'predict': predict(pipe_line, str),

            }

            return json.dumps(result)


@app.route('/ner', methods=['GET'])
def action():
    if request.method == 'GET':
        str = request.args['str']
        predict = request.args['predict']
        if ((predict == "time_2") |(predict == "number") ) :
            regex = ["([0-9]{1,2}\sgiờ\s[0-9]{1,2})","([0-9]{1,2}\:[0-9]{1,2})","([0-9]{1,2}\stháng\s[0-9]{1,2}\snăm\s[0-9]{4})","([0-9]{1,2}\stháng\s[0-9]{1,2})"]
            sentence = str
            list = []
            for r in regex:
                x = re.findall(r, sentence)
                if (x):
                    for i in x:
                        sentence = sentence.replace(i, "")
                        if("tháng" in i):
                            i=i.replace(" tháng ","/")
                        if ("năm" in i):
                            i=i.replace(" năm ", "/")
                        if ("giờ" in i):
                            i=i.replace(" giờ ", ":")
                        list.append(i)

            sentence=ViTokenizer.tokenize(sentence.replace("  "," "))

            x= sentence.split(" ")
            for i in x :
                if (i[0].isdigit()):
                    list.append(i)
            for idx, item in enumerate(list):
                list[idx] = list[idx].replace(" ","_")

            # vitoken = ViPosTagger.postagging(ViTokenizer.tokenize(str))
            #
            # words = []
            # for word in vitoken[0]:
            #     with open('stopwords.txt', encoding="utf-8") as f1:
            #         if word not in f1.read():
            #             words.append(word)
            str = ' '.join(list)
            print(str)
            result = {
                'str': str

            }
            return json.dumps(result)
        else:
            list_ner=ner(ViTokenizer.tokenize(str))
            list = []
            for i in list_ner:
                if (i[3] in ["B-LOC","I-LOC","B-PER","I-PER","B-ORG","I-ORG"]) :
                        list.append(i[0])
                if(i[0][0].isdigit()):
                    list.append(i[0])
            # vitoken = ViPosTagger.postagging(ViTokenizer.tokenize(str))
            # words = []
            # for word in vitoken[0]:
            #     with open('stopwords.txt', encoding="utf-8") as f1:
            #         if word not in f1.read():
            #             words.append(word)
            str = ' '.join(list)
            print(str)
            result = {
                'str': str

            }
            return json.dumps(result)

@app.route('/foo', methods=['POST'])
def foo():
    if not request.json:
        abort(400)

    str = request.json["str"]
    predict = request.json["predict"]
    if ((predict == "time_2") | (predict == "number")):
        regex = ["([0-9]{1,2}\sgiờ\s[0-9]{1,2})", "([0-9]{1,2}\:[0-9]{1,2})",
                 "([0-9]{1,2}\stháng\s[0-9]{1,2}\snăm\s[0-9]{4})", "([0-9]{1,2}\stháng\s[0-9]{1,2})"]
        sentence = str
        list = []
        for r in regex:
            x = re.findall(r, sentence)
            if (x):
                for i in x:
                    sentence = sentence.replace(i, "")
                    if ("tháng" in i):
                        i = i.replace(" tháng ", "/")
                    if ("năm" in i):
                        i = i.replace(" năm ", "/")
                    if ("giờ" in i):
                        i = i.replace(" giờ ", ":")
                    list.append(i)

        sentence = ViTokenizer.tokenize(sentence.replace("  ", " "))

        x = sentence.split(" ")
        for i in x:
            if (i[0].isdigit()):
                list.append(i)
        for idx, item in enumerate(list):
            list[idx] = list[idx].replace(" ", "_")

        # vitoken = ViPosTagger.postagging(ViTokenizer.tokenize(str))
        #
        # words = []
        # for word in vitoken[0]:
        #     with open('stopwords.txt', encoding="utf-8") as f1:
        #         if word not in f1.read():
        #             words.append(word)
        str = ' '.join(list)
        print(str)
        result = {
            'str': str

        }
        return json.dumps(result)
    else:

        vitoken = ViPosTagger.postagging(ViTokenizer.tokenize(str))
        words = []
        for word in vitoken[0]:
            with open('stopwords.txt', encoding="utf-8") as f1:
                if word not in f1.read():
                    words.append(word)
        str = ' '.join(words)
        list_ner = ner(str)
        list = []
        for i in list_ner:
            if (i[3] in ["B-LOC", "I-LOC", "B-PER", "I-PER", "B-ORG", "I-ORG"]):
                list.append(i[0])
            elif (i[0][0].isupper()):
                list.append(i[0])
            elif (i[0][0].isdigit()):
                list.append(i[0])
        str = ' '.join(list)
        print(str)
        result = {
            'str': str

        }
        return json.dumps(result)
if __name__ == '__main__':
    app.run()

