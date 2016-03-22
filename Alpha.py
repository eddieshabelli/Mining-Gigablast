import os
import requests
import json
import urllib
import urllib.request as ur
from bs4 import BeautifulSoup
import time

print('Accessing Terms.rtf')
time.sleep(2)

#Used RTF file instead of TXT... TXT was not working for some reason
textf = textf = open(r'terms.rtf','r')
terms = textf.readlines()
terms = []
response_list = []
pages = [0,10,20]
textf = open(r'terms.rtf','r')
terms = textf.readlines()

for term in terms:
    
    ###Place Gigablast API Credentials here
    user_id = 'xx'
    my_code = 'xxxxxxxxx'
    
    resultnum = 10
    formatting = 'json'
    query = term.strip('\n')
    url_list = []
    print("Currently processing ", term)
    count = 1

    for page in pages:
        urls = []
        payload = {'q': query, 'n': resultnum, 'format': formatting, 's': page, 'userid': user_id, 'code': my_code}
        response = requests.get('https://www.gigablast.com/search?c=main&index=search&hacr=1', params=payload)
        string = response.text
        json_page = json.loads(string)

        ### HTML to text files ###
        for result in json_page['results']:
            print("Currently parsing %s" % result['url'])
            
            try:
                if "http://" in result['url'] or "https://" in result['url']:
                    r = ur.urlopen(result['url']).read()
                    soup = BeautifulSoup(r, "html.parser")
                else:
                    r = ur.urlopen("http://%s" % result['url']).read()
                    soup = BeautifulSoup(r, "html.parser")
                term = term.rstrip()
                file_name = str(term)
            except urllib.error.HTTPError as err:
                print("there was a HTTP error for %s" % result['url'])
                print(err.code)
            except ConnectionResetError as err2:
                print("The connection to ",result['url']," was refused.")
            except urllib.error.URLError as err3:
                print("There was an SSL error for ",result['url'])
                
            h = open("" + str(count) + str(file_name) + ".txt",'wb')
            
            try:
                h.write(soup.encode("utf-8"))
            except:
                print("There was and error processing %s" % result['url'])
                pass
            count = count + 1

        urls = [result['url'] for result in json_page['results']]
        url_list.append(str(urls).replace(',', '\n'))

    print('')
    #print('%s urls for ' % count + term)
    print('%i urls for ' % int(count - 1) + term)
    print('')
   
print("The program ran succesfully.")
