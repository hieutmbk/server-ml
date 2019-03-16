from pyvi import ViPosTagger,ViTokenizer
from sklearn.base import TransformerMixin, BaseEstimator

class FeatureTransformer(BaseEstimator, TransformerMixin) :
    def __init__(self):
        self.tokenizer = ViTokenizer
        self.pos_tagger = ViPosTagger

    def fit(self,*_):
        return self

    def transform(self,X,y=None,**fit_params):
        result = []
        for i in X :
            vitoken = ViPosTagger.postagging(ViTokenizer.tokenize(i))

            words = []
            for word in vitoken[0] :
                with open('stopwords.txt', encoding="utf-8") as f1:
                    if word not in f1.read():
                        words.append(word)
            str = ' '.join(words)

            result.append(str)

        return result