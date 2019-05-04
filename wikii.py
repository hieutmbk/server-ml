import wikipedia
from underthesea import ner, word_tokenize
from pyvi import ViTokenizer,ViPosTagger
import re
wikipedia.set_lang("vi")
sentences = "há Bảnh tên thật 21h00 18 giờ 12 là Ngô 21h Bá Khá 8h45, biệt danh 8:35 là Khá Bảnh. Sinh ngày 27 - 11 - 1993 tại Từ 2174 diễn ra vào lúc 21 giờ tháng 8 năm 2018"
tokenize = ner(sentences);
# print(tokenize)
# for idx,item in enumerate(tokenize):
#     tokenize[idx] = tokenize[idx].replace(" ","_")
# str = " ".join(tokenize)


regex = ["(\d{1,2}\:\d{1,2})","\d{1,2}\sgiờ\s\d{1,2}","\d{1,2}\sgiờ","\d{1,2}h\d{0,2}","(\d{1,2}\stháng\s\d{1,2}\snăm\s\d{4})","(\d{1,2}\stháng\s\d{1,2})","\d{1,2}\snăm\s\d{4}","\d{1,2}\s\-\s\d{1,2}\s\-\s\d{4}","\d{1,2}\s\-\s\d{1,2}","\d{4}"]
list = []
for r in regex :
    x = re.findall(r, sentences)
    if(x) :
        for i in x:
            list.append(i.replace(" ","").replace(":","h").replace("giờ","h").replace("tháng","/").replace("năm","/").replace("-","/"))
            sentences = sentences.replace(i, "")


        # sentences = sentences.replace(x.group(),"")
print(list)