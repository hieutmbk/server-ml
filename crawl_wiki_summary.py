import scrapy
import json
from scrapy.http.request import Request
class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, *args, **kwargs):
        self.myurls = kwargs.get('myurls', [])
        super(MySpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.myurls:
            yield Request(url, self.parse)
    def parse(self, response):
        items = DictionaryItem()
        name_classs = ["infobox","infobox vcard","infobox geography vcard"]
        table=""
        for name in name_classs:
            if(len(response.selector.xpath('//div[@class="mw-parser-output"]/table[@class="'+name+'"]/tbody/tr')) > 2):
                table = response.selector.xpath('//div[@class="mw-parser-output"]/table[@class="'+name+'"]')
                list_tr = table.xpath('./tbody/tr')
                arr_th = []
                arr_td = []
                for tag in list_tr:
                    th = tag.xpath('./th//text()').extract()
                    list_td = tag.xpath('./td')
                    if((len(th) == 0) & (len(list_td) == 1)):
                        tag_b = list_td.xpath('.//b//text()').extract()
                        if(len(tag_b)==2):
                            if(list_td.xpath('.//li//text()').extract()):
                                arr_th.append(tag_b[0].replace("\xa0"," "))
                                joinString(arr_td,list_td.xpath('.//li//text()').extract())
                            else:
                                arr_th.append(tag_b[0])
                                arr_td.append(tag_b[1])

                    elif ((len(th) == 0) & (len(list_td) == 2)):
                        arr_th.append(
                            "".join(list_td[0].xpath('.//text()').extract()).replace("\xa0", " ").replace("\n", ""))
                        list_text = list_td[1].xpath('.//text()').extract()
                        joinString(arr_td, list_text)
                    elif ((len(th) == 0) & (len(list_td) == 3)):
                        arr_th.append("".join(list_td[1].xpath('.//text()').extract()).replace("\xa0", " "))
                        list_text = list_td[2].xpath('.//text()').extract()
                        joinString(arr_td, list_text)
                    elif ((len(th) > 0) & (len(list_td) > 0)):
                        arr_th.append("".join(th).replace("\xa0", " "))

                        for list in list_td:
                            list_text = list.xpath('.//text()').extract()
                            joinString(arr_td, list_text)
                dictionary = dict(zip(arr_th, arr_td))
                with open('data.json', 'w') as outfile:
                    json.dump(dictionary, outfile)
                outfile.close()
                break;
            else :
                dictionary = "None"
                with open('data.json', 'w') as outfile:
                    json.dump(dictionary, outfile)
                outfile.close()


def joinString(arr_td,list_text):

    for i,item in enumerate(list_text):
        if(item == "\xa0"):
            list_text[i]="none"
        if(("&0000000000000" in item) | ("&-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1" in item) | ("\ufeff /" in item)):
            list_text.remove(item)
    text = " ".join(list_text)
    text = text.replace("\n", "").replace("\xa0", "").replace("  ", " ").replace("none","").replace("   ","")
    for i in range(10):
        x = "[" + str(i) + "]"

        text = text.replace(x, "")
    if (text != ''):
        arr_td.append(text)


