import wikipedia
from underthesea import ner
from pyvi import ViTokenizer,ViPosTagger
wikipedia.set_lang("vi")
sentences = "Thăng Điệp. 22/03/2019 08:18. Năm nay là năm thứ hai liên tiếp Phần Lan được xếp hạng là quốc gia hạnh phúc nhất thế giới, hãng tin Bloomberg cho biết.x"

vitoken = ViPosTagger.postagging(ViTokenizer.tokenize(sentences))

words = []
for word in vitoken[0]:
    with open('stopwords.txt', encoding="utf-8") as f1:
        if word not in f1.read():
            words.append(word)
str = ' '.join(words)
print(str)