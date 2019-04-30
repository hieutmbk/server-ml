import wikipedia
from underthesea import ner
from pyvi import ViTokenizer
wikipedia.set_lang("vi")
sentences = "Tôn giáo tại Việt Nam khá đa dạng, gồm có các nhánh Phật giáo như Đại thừa, Tiểu thừa, Hòa Hảo, một số nhánh Kitô giáo như Công giáo Rôma"
print(ner(sentences))