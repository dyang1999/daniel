import requests
from bs4 import BeautifulSoup

# from urllib.request import unquote

# target URL
url = 'https://www.adrc.asia/publication.php'

# make HTTP GET request to the target URL
print('HTTP GET: %s', url)
response = requests.get(url)

# parse content
content = BeautifulSoup(response.text, 'lxml')

# extract URLs referencing PDF documents
all_urls = content.find_all('a')
#number = 0
# loop over all URLs
for url in all_urls:
    # try URLs containing 'href' attribute
    try:
        # pick up only those URLs containing 'pdf'
        # within 'href' attribute
        if 'pdf' in url['href']:
            # init PDF url
            pdf_url = url['href']
            # make HTTP GET request to fetch PDF bytes
            print('HTTP GET: %s', pdf_url)
            pdf_response = requests.get(pdf_url)
            filename = pdf_url.split('/')[-1].split('.pdf')[0]

            #number += 1
            #filename = str(number)

            # write PDF to local file
            with open('./pdf/' + filename, 'wb') as f:
                # write PDF to local file
                f.write(pdf_response.content)
                f.close()

    # skip all the other URLs
    except:
        pass
