import wikipedia
from underthesea import ner
from pyvi import ViTokenizer,ViPosTagger
import re
wikipedia.set_lang("vi")
sentences = "Ông Hoàng Minh Sơn (sinh năm 1969) nguyên là Phó hiệu trưởng Trường ĐH Bách khoa Hà Nội . Thứ trưởng Bộ GD-ĐT Bùi Văn Ga (đứng  Hiệu trưởng ĐH Bách Khoa Hà Nội: Không thể đi tắt đón đầu trong  Hoàng Minh Sơn - Hiệu trưởng trường Đại học Bách Khoa Hà Nội (một cái  Trần Quốc Thắng | World Bank Live dạy tại khoa Kỹ thuật vật liệu và luyện kim, Đại học Bách khoa Hà Nội. Giáo sư Trần Quốc Thắng tốt nghiệp Đại học Bách khoa Kharkov  Trường Đại học Bách khoa TP.HCM có hiệu trưởng mới 46 tuổi  TS Mai Thanh Phong giữ chức hiệu trưởng Trường ĐH Bách khoa,  tại đây của Hiệu trưởng Trường Đại học Bách khoa Hà Nội "
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