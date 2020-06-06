import requests
from bs4 import BeautifulSoup
import pandas as pd
headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get("https://www.dictionary.com/browse/melt?s=t", headers=headers)
# print(page.status_code)

# print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
block = soup.find('div',{'class':'css-1urpfgu e16867sm0'})
print(block)