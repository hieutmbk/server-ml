import wikipedia
from underthesea import ner, word_tokenize
from pyvi import ViTokenizer,ViPosTagger
import re
wikipedia.set_lang("vi")
sentences = "VnExpress Địa điểm, chi phí và chất lượng học tập là mối quan tâm hàng đầu của phụ huynh khi cho con em đi du học. Hiện, xứ sở bò tót là lựa chọn của nhiều người với  THÀNH PHỐ MADRID - NIỀM TỰ HÀO CỦA XỨ SỞ BÒ TÓT  Saul, niềm hy vọng của xứ sở bò tót - Bongdaplus.vn Saul, niềm hy vọng của xứ sở bò tót. 1. Saul có khá nhiều điểm hao hao giống Raul, từ cái tên, dáng người mảnh khảnh cho đến cái chân trái  Tây Ban Nha - Xứ sở bò tót với nhiều điểm đến hấp dẫn! Khi đến đây, du khách hãy dành thời gian khám phá những địa điểm thú vị ở xứ sở bò tót này, chắc chắn bạn sẽ có những trải nghiệm vô cùng đáng nhớ đó! TÂY BAN NHA - XỨ SỞ BÒ TÓT | Tours4u.vn - thương hiệu bán lẻ  du khách hãy dành thời gian khám phá những địa điểm thú vị ở xứ sở bò tót  Bò tót Tây Ban Nha – Wikipedia tiếng Việt Bò tót Tây Ban Nha hay tên gọi chính xác là bò đấu Tây Ban Nha (Toro . một con bò Navarro, và công tước xứ Veragua đóng góp một Ojinegro Castaño. . xem Raton trình diễn, chủ sở hữu của con bò khẳng định rằng kinh phí là giá trị nó. Tapas, món ăn vặt đặc biệt của xứ sở bò tót xứ sở bò tót | Báo Dân trí xứ sở bò tót | Dân trí - Trang tổng hợp tin tức, hình ảnh, video clip, bình luận,  đấu bò đã vừa bị trọng thương khi tham gia lễ hội đấu bò tót truyền thống của Tây  Rượu Sangria - thức uống quốc dân của xứ sở bò tót Nếu đến với Tây Ban Nha, du khách cũng đừng quên thưởng cho mình một ly rượu Sangria - thức uống thơm ngon nức tiếng của xứ sở bò tót  Tapas, kho báu nhỏ của ẩm thực xứ sở bò tót "
print(ViPosTagger.postagging(ViTokenizer.tokenize(sentences)))
tokenize = word_tokenize(sentences);
for idx,item in enumerate(tokenize):
    tokenize[idx] = tokenize[idx].replace(" ","_")
str = " ".join(tokenize)
print(ner(str))
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