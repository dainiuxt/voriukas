import requests
from lxml import html
from modules.store import StoreItem

link = 'https://www.cvbankas.lt/?padalinys[0]=76&page=1'

# print(source.xpath("//span[contains(@class, 'salary_amount')]/text()"))

def get_source(page_url):
  r = requests.get(page_url)
  source = html.fromstring(r.content)
  # return source
  article_list = source.xpath("//article")
  return article_list
  
print(len(get_source(link)))
