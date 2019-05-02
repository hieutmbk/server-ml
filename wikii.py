import wikipedia
from underthesea import ner
from pyvi import ViTokenizer,ViPosTagger
wikipedia.set_lang("vi")
sentences = "Vi\\u1ec7t_Nam d\\u00e2n_t\\u1ed9c anh_em Th\\u00f4ng_th\\u01b0\u1eddng \u0111\u00e0i b\u00e1o ti_vi quen_thu\u1ed9c : Vi\u1ec7t_Nam 54 d\u00e2n_t\u1ed9c"
vitoken = ViPosTagger.postagging(ViTokenizer.tokenize(sentences))


print(sentences.encode('latin1').decode('utf8'))