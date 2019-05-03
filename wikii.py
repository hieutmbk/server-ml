import wikipedia
from underthesea import ner
from pyvi import ViTokenizer,ViPosTagger
import re
wikipedia.set_lang("vi")
sentences = "Từ đây, anh được các hãng băng nhạc săn đón, các bài hát được sáng tác từ lúc mới đi hát  . Bài hát Tình Cha được chính ca sĩ Ngọc Sơn viết lời và thể hiện.  . thì Nhật ký của mẹ một sáng tác của nhạc sĩ Nguyễn Văn Chung là bài hát mà các bạn không thể bỏ qua. . Tình Cha. Tác giả: Ngọc Sơn (trẻ)  . Lời bài hát Tình Cha - Ngọc Sơn - Tình Cha ấm áp như vầng Thái Dương Ngọt ngào như giòng nước tuôn đầu nguồn Suốt đời vì  . Ngọc Sơn cho biết từ ngày bố mất, anh dành mọi thời gian để sáng tác bài hát. . Papa – Paul Anka: Bài hát kể lại kỷ niệm thời thơ ấu của tác giả với người cha của mình. . Cầu Cho Ông Bà Cha Mẹ. Upload 01/08/2019 by HH. Bài Hát, Tác Giả, Imp, Date. Bao La Tình Mẹ Cha, Nguyễn Chánh, Feb 04. Biết Tìm Đâu Mẹ Cha Midi  . Tình Cha - Trường Vũ | Tình Cha Tác giả: Ngọc Sơn Ca sĩ: Ngọc Sơn Tình Cha ấm áp như vầng Thái Dương Ngọt  . Một số bài cùng tác giả . . Bài hát cùng tác giả. Đêm cuối  . "
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