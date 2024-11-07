import scrapy
import time


class ElibrarySpider(scrapy.Spider):
    name = "elibrary"
    
    query = 'веб технологии'
    start_url = "https://elibrary.ru/query_results.asp"
    payload = f'querybox_name=&authors_all=&titles_all=&rubrics_all=&changed=1&queryid=&ftext={query}&where_name=on&where_abstract=on&where_keywords=on&where_references=&type_article=on&type_disser=on&type_book=on&type_report=on&type_conf=on&type_patent=on&type_preprint=on&type_grant=on&type_dataset=on&search_itemboxid=&search_morph=on&begin_year=0&end_year=0&issues=m6&orderby=rank&order=rev&queryboxid=0&save_queryboxid=0'
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_url+'?'+self.payload, callback=self.parse, method='POST', dont_filter = True)
    
    max_page_number = 1
    page_number = 1
    def parse(self, response):
        if response.xpath(".//form[@action='/check_captcha.asp']").get() != None:
            self.log("captcha!")
        
        self.log("!!!!!!")
        
        
        if max_pages:=response.xpath(".//td[@width='15%']//a[contains(text(), 'конец')]/@href").get():
            self.max_page_number = int(max_pages.split('=')[1])
            
        self.log(self.max_page_number)
        for publication in response.xpath(".//tr[@valign='middle' and contains(@id, 'a')]"):
            id = publication.xpath("./@id").get()
            title = publication.xpath(".//span//span/text()").get()
            citations = publication.xpath(".//td[@valign='middle']/text()").get()
            authors = publication.xpath(".//i/text()").get()
            source = ' '.join(publication.xpath(".//font[descendant::a]/text()").getall())
            yield dict(id=id, title=title, authors=authors, citations=citations, source=source)
        
        if self.page_number < self.max_page_number:
            self.page_number += 1
            next_page = f'https://elibrary.ru/query_results.asp?pagenum={self.page_number}'
            yield response.follow(next_page, callback=self.parse)
        
       
        

