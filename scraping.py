import requests
from bs4 import BeautifulSoup

Stock_Name = "^GSPC"
Stock_url = "https://finance.yahoo.com/quote/"+Stock_Name+"?p="+Stock_Name+"&.tsrc=fin-srch"
#Stock_url = "https:/finance.yahoo.com/quote/"+Stock_Name+"/history?p="+ Stock_Name

print(Stock_url)

response = requests.get(Stock_url)

print(response)

soup = BeautifulSoup(response.text, 'html.parser')

#data = soup.find(id="")
#print(data)

data = soup.find(id="quote-header-info")
final_price = data.find("fin-streamer",class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").getText()
print(final_price)