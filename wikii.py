import wikipedia
from underthesea import ner
from pyvi import ViTokenizer
wikipedia.set_lang("vi")
sentences = "Sơn Tùng MTP"
print(ner(sentences))