import requests
from bs4 import BeautifulSoup
import csv
import time
import json
import urllib3
import finder as fy

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


start = time.time()

timestr = time.strftime("%Y%m%d-%H%M%S")

fileName = 'discount_tag_'+timestr+'.csv'

fieldname = ['state', 'discount_details', 'url']

failed_lst = list()

with open(fileName, 'a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames = fieldname)
    writer.writeheader()
 
with open('url.csv', newline='', encoding='utf=8') as f:
    reader = csv.reader(f)
    urlList = list(reader)[1:]

def discountDetails(url, the_word):
    r = requests.get(url, verify=False, allow_redirects=True)
    soup = BeautifulSoup(r.content, 'lxml')
    words = soup.find(text=lambda text: text and the_word[0] in text or the_word[1] in text or the_word[2] in text or the_word[3] in text)
    print(words)
    return words
 
def contData(state, discount, url):
    with open(fileName, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = fieldname)
        writer.writerow({'state': state, 'discount_details': discount, 'url': url})

for i in urlList:
    try:
        url = i[1]
        state = i[0]
        word = ['Discount', 'discount', 'Discounts', 'discounts']
        urlListNew = fy.crawl(url)
        for i in urlListNew:
            discount = discountDetails(i, word)
            print('\nUrl: {}\ncontains word: {}'.format(i, word))
            contData(state, discount, i)
    except Exception as e:
        print('Error: {}'.format(e))
        failed_data = {
            'state': state,
            'url': url,
            'error': str(e)
        }
        failed_lst.append(failed_data)

# for i in urlList:
#     try:
#         url = i[1]
#         state = i[0]
#         word = 'Discount'
#         discount = discountDetails(url, word)
#         print('\nUrl: {}\ncontains word: {}'.format(url, word))
#         contData(state, discount, url)
#     except Exception as e:
#         print('Error: {}'.format(e))
#         failed_data = {
#             'state': state,
#             'url': url,
#             'error': str(e)
#         }
#         failed_lst.append(failed_data)
    

"""SAVE FAILED TO FILE"""
if failed_lst:
    with open('error.json', 'w') as json_file:
        json_file.write(json.dumps(failed_lst))

end = time.time()
print(f"Runtime of the code is {end - start}")

