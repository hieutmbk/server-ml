import wikipedia
from underthesea import ner
from pyvi import ViTokenizer
wikipedia.set_lang("vi")
sentences = "Nguyễn Công Phượng sinh ở đâu"
print(ner(sentences))