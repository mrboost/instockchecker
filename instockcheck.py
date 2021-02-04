import requests
from bs4 import BeautifulSoup
from time import sleep
from discord_webhook import DiscordWebhook

def get_page_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    page = requests.get(url, headers=headers)
    print(page.status_code)
    return page.content


def check_item_in_stock(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    out_of_stock_divs = soup.findAll("span", {"class": "inventoryCnt"})  # Figure out where the "instock part is" in the html
    if 'Sold' in str(out_of_stock_divs):
        return
    else:
        return len(out_of_stock_divs) != 0
    

def check_inventory():
    url = "https://www.microcenter.com/product/630283/amd-ryzen-9-5900x-vermeer-37ghz-12-core-am4-boxed-processor" #link to microcenter
    page_html = get_page_html(url)
    while True:
      sleep(60)
      if check_item_in_stock(page_html):
          content = "@everyone" + url
          webhook = DiscordWebhook(url='PUT DISCORD WEBHOOK HERE', content=content)
          response = webhook.execute()
      else:
          print("Out of stock")

check_inventory()
