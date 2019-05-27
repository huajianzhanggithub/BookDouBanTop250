from lxml import etree
import requests
import csv

fp = open('BookDouBanTop250.csv','w',newline='',encoding='utf-8')
writer = csv.writer(fp)
writer.writerow(('name','url','author','publisher'
                 ,'date','price','rate','persons','comment'))

urls = ['https://book.douban.com/top250?start={}'.format(str(i)) for 
      i in range(0,250,25)]

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)'
   + ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132'
  + ' Mobile Safari/537.36'
    }

for url in urls:
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//tr[@class="item"]')
    for info in infos:
        name = info.xpath('td/div/a/@title')[0]
        url = info.xpath('td/div/a/@href')[0]
        book_infos = info.xpath('td/p/text()')[0].split('/')
        price = book_infos.pop()
        pbdate = book_infos.pop()
        publisher = book_infos.pop()
        author = str(book_infos)[1:-2]
        rate = info.xpath('td/div/span[2]/text()')[0]
        persons = info.xpath('td/div/span[3]/text()')[0]
        comments = info.xpath('td/p/span[@class="inq"]/text()')
        comment = comments[0] if len(comments) != 0 else "空"
        writer.writerow((name , url , author , publisher 
                 , pbdate , price , rate , persons , comment))
fp.close()