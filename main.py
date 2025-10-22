import requests
from bs4 import BeautifulSoup
import pandas as pd
link="https://books.toscrape.com/"
requesicao=requests.get(link)
site=BeautifulSoup(requesicao.text,"html.parser")
title=[tag["title"] for tag in site.find_all("a")  if "title" in tag.attrs]
price=[p.text for p in site.find_all("p",class_="price_color")]
stock=[s.text.strip() for s in site.find_all("p",class_="instock availability")]

data=pd.DataFrame({
    "title":title,
    "price":price,
    "availability":stock
})
data.to_excel("books.xlsx",index=False)