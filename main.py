import requests
from lxml import html
from modules.store import StoreItem
import pandas as pd

link = 'https://www.cvbankas.lt/?padalinys[0]=76&page=1'
adds = list()

def get_pages(page_url):
  r = requests.get(page_url)
  source = html.fromstring(r.content)
  page_list = source.xpath("//ul[contains(@class, 'pages_ul_inner')]/li/a/text()")
  return page_list

def get_source(page_url):
  r = requests.get(page_url)
  source = html.fromstring(r.text)
  articles = source.xpath("//article")
  return articles

pages = get_pages(link)

for page in range(int(pages[-1])):
  link = f'https://www.cvbankas.lt/?padalinys[0]=76&page={page+1}'
  article_list = get_source(link)

  for article in article_list:
    title = article.xpath(".//h3/text()")[0]
    company = article.xpath(".//span[contains(@class, 'dib')]/text()")[0]
    link = article.xpath(".//a[contains(@class, 'list_a')]/@href")[0]
    calculations = article.xpath(".//div[contains(@class, 'jobadlist_list_cell_salary')]/text()")
    city = article.xpath(".//span[contains(@class, 'list_city')]/text()")[0]
    old = article.xpath(".//span[contains(@class, 'txt_list_2')]/text()")
    if len(old) == 0:
      old = ''
    else:
      old = old[0]

    if len(calculations) == 2:
      salary = article.xpath(".//span[contains(@class, 'salary_amount')]/text()")[0]
      netgross = article.xpath(".//span[contains(@class, 'salary_calculation')]/text()")[0]
    else:
      netgross = ''
      salary = ''

    add = StoreItem(title, link, salary, city, netgross, old, company)
    adds.append(add)

df = pd.DataFrame(
  {
    "company": [add.company for add in adds],
    "old": [add.old for add in adds],
    "title": [add.title for add in adds],
    "link": [add.link for add in adds],
    "salary": [add.salary for add in adds],
    "netgross": [add.netgross for add in adds],
    "city": [add.city for add in adds],
  }
)

df.to_csv("adds.csv", index=False)
