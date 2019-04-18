import wikipedia
from underthesea import ner
from pyvi import ViTokenizer
wikipedia.set_lang("vi")
sentences = "địa chỉ IBM tại Việt Nam"
print(ner(sentences))