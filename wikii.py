import wikipedia
from underthesea import ner, word_tokenize
from pyvi import ViTokenizer,ViPosTagger
import re
wikipedia.set_lang("vi")
sentences = "tiếng Việt Tháng 5 1425 Lê Lợi lại sai Đinh Lễ đem quân  đánh  Châu, . Bài 19 : Cuộc   (1418-1427) | Học trực tuyến   toàn thắng (cuối  1426 - cuối  1427). 1. . Nguyễn Trãi – Wikipedia tiếng Việt Thanh Hóa chuẩn bị kỷ niệm 600    và Lễ  Thanh Hóa chuẩn bị kỷ niệm 600    và Lễ hội Lam  Hội thề Lũng Nhai – Wikipedia tiếng Việt Kỷ niệm 600    | Văn hóa - Giáo dục | Báo  Phần hội  nay có chủ đề “  - Thiên anh hùng ca giữ nước”.  Lê Tư Tề – Wikipedia tiếng Việt Sử sách không chép Lê Tư Tề sinh  vào  nào, khi    , Lê Tư Tề đã theo cha đánh quân Minh. Sách Đại Việt thông sử nhận xét  Liên tiếp đánh bại quân Minh ở nhiều mặt trận,    'Trận Bồ Đằng sấm vang chớp giật'   ở đâu? - Tư vấn - ZING.VN Cuộc   bùng nổ vào  nào? 1415; 1416; 1417; 1418. Lý thuyết   (1418 - 1427) sử 7 "
tokenize = ner(sentences);
# print(tokenize)
# for idx,item in enumerate(tokenize):
#     tokenize[idx] = tokenize[idx].replace(" ","_")
# str = " ".join(tokenize)


regex = ["(\d{1,2}\:\d{1,2})","\d{1,2}\sgiờ\s\d{1,2}","\d{1,2}\sgiờ","\d{1,2}h\d{0,2}","","(\d{1,2}\stháng\s\d{1,2}\snăm\s\d{4})","(\d{1,2}\stháng\s\d{1,2})","\d{1,2}\snăm\s\d{4}","\d{1,2}\s\-\s\d{1,2}\s\-\s\d{4}","\d{1,2}\s\-\s\d{1,2}","\d{4}"]
list = []
for r in regex :
    x = re.findall(r, sentences)
    if(x) :
        for i in x:
            list.append(i.replace(" ","").replace(":","h").replace("giờ","h").replace("tháng","/").replace("năm","/").replace("-","/"))
            sentences = sentences.replace(i, "")


        # sentences = sentences.replace(x.group(),"")
print(list)