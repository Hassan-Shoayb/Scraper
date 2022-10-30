# Imports
import scrapy
import re

# pattern that reads all the characters inside an HTML tag
pattern='<[^<]+?>'

class SaasSpider(scrapy.Spider):
    name = 'saas'
    start_urls = ['https://getlatka.com/saas-companies',
                  ]
    
    def parse(self, response):
        count = 0
    
        for saas in response.css('tbody tr'):
            myString = response.css('.cells_name__pBrsJ')[count].get()
            myCash = response.css('.cells_cell-2__QbD4E')[count].get()
            name = response.css(f'tbody tr section a::text')[count].get()
            industry = response.css('.saas-companies_ellipses__Y9AeV::text').get()
            founder  = re.sub(pattern, "", myString)
            cash = re.sub(pattern, "", myCash)
            count = count + 1
            
            yield {
                'Name':name, 'Cash Flow':cash, 'Founder':founder, 'Industry':industry
            }
        
        for x in range(1, 1310):
            page = f'?page={x}'
            next_page = response.urljoin(page)
            yield scrapy.Request(next_page, callback=self.parse)
        