import wikipedia
from underthesea import ner
from pyvi import ViTokenizer
wikipedia.set_lang("vi")
sentences = "câu lạc bộ Barcelona vô địch C1 năm nào"
print(ner(sentences))