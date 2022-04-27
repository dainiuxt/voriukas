import requests
from lxml import html
from modules.store import StoreItem
import pandas as pd

link = 'https://www.cvbankas.lt/?padalinys[0]=76&page=1'
adds = list()

def get_pages(page_url):
  r = requests.get(page_url)
  r.encoding = r.apparent_encoding
  source = html.fromstring(r.content)
  page_list = source.xpath("//ul[contains(@class, 'pages_ul_inner')]/li/a/text()")
  return page_list

def get_source(page_url):
  r = requests.get(page_url)
  r.encoding = r.apparent_encoding
  source = html.fromstring(r.content)
  articles = source.xpath("//article")
  return articles

pages = get_pages(link)

for page in range(int(pages[-1])):
  link = f'https://www.cvbankas.lt/?padalinys[0]=76&page={page+1}'
  article_list = get_source(link)

  for article in article_list:
    title = article.xpath(".//h3/text()")
    link = article.xpath(".//a[contains(@class, 'list_a')]/@href")
    calculations = article.xpath(".//div[contains(@class, 'jobadlist_list_cell_salary')]/text()")
    city = article.xpath(".//span[contains(@class, 'list_city')]/text()")
    old = article.xpath(".//span[contains(@class, 'txt_list_2')]/text()")

    if len(calculations) == 1:
      netgross = ['']
      salary = ['']
    else:
      salary = article.xpath(".//span[contains(@class, 'salary_amount')]/text()")
      netgross = article.xpath(".//span[contains(@class, 'salary_calculation')]/text()")

    add = StoreItem(title, link, salary, city, netgross, old)
    adds.append(add)

print(len(adds))
