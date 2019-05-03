import wikipedia
from underthesea import ner
from pyvi import ViTokenizer,ViPosTagger
import re
wikipedia.set_lang("vi")
sentences = "Chiều cao 1,72m giúp Noo "
print(ner(ViTokenizer.tokenize(sentences)))
regex = ["([0-9]{1,2}\:[0-9]{1,2})","([0-9]{1,2}\stháng\s[0-9]{1,2}\snăm\s[0-9]{4})","([0-9]{1,2}\stháng\s[0-9]{1,2})"]
list = []
for r in regex :
    x = re.findall(r, sentences)
    if(x) :
        for i in x:
            list.append(i)
            sentences = sentences.replace(i, "")


        # sentences = sentences.replace(x.group(),"")
print(list)