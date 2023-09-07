from bs4 import BeautifulSoup
import requests
import concurrent.futures
import pandas as pd
import os


base_url = 'https://www.yorubaname.com/alphabets/a'

home_page = requests.get(base_url)

urls = []
soup = BeautifulSoup(home_page.content, 'html.parser', from_encoding='UTF-8')
alphabets = soup.find_all(class_='alphabets')
alphabets_lst = [alpha.get_text().strip('\n') for alpha in alphabets][0].split('\n')
for alpha in alphabets_lst:
    urls.append(base_url[:-1]+alpha)

url_alphabet = list(zip(urls, alphabets_lst))


def scrape_data(url, alphabet):
    result = {}

    try:
        page = requests.get(url)
    except Exception as error_message:
        print(f'{error_message}')
    else:
        alphabet_soup = BeautifulSoup(page.content, 'html.parser', from_encoding='UTF-8')
        names = alphabet_soup.find_all(class_='alphabet-listing')
        name_list = [name.get_text().strip('\n') for name in names]
        result[url[-1]] = name_list[0].split('\n')

        df = pd.DataFrame(result)
        df.to_csv(f"./data/scraped_yoruba_names{alphabet}.csv", index=False)


def process_scrape_data():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda args: scrape_data(*args), url_alphabet)


if __name__ == '__main__':
    process_scrape_data()


