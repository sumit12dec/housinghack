import bs4
import re
import sys
import nltk
import string
import urllib2
from collections import OrderedDict
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
def sum2(url):
    details = {}
    main_text = ""
    try:
        html = urllib2.urlopen(url).read()
        soup = bs4.BeautifulSoup(html)
    
        try:
            if 'usatoday' in url:
                main_text = re.sub('\s+',' '," ".join([ x.text for x in soup.find_all('p') ][14:]))
            elif 'gizmodo' in url:
                main_text = re.sub('\s+',' ',soup.find_all('div','Normal')[0].text)    
            elif 'thehindu' in url:
                articlelead = re.sub('\s+',' ',soup.find_all('div','articleLead')[0].text)
                main_text = re.sub('\s+',' '," ".join([ x.text for x in soup.find_all('p','body') ]))
            elif 'timesofindia' in url:
                if re.findall('<div class="Normal"',html):
                    main_text = re.sub('\s+',' ',soup.find_all('div','Normal')[0].text)
                if re.findall('<div class="data"',html):
                    main_text = re.sub('\s+',' ',soup.find_all('div','data')[0].text)
            else:
        	   main_text = re.sub('\s+',' '," ".join([ x.text for x in soup.find_all('p') ]))
            details['main_text'] = main_text
        except:
            try:
                main_text = re.sub('\s+',' '," ".join([ x.text for x in soup.find_all('p') ]))
            except:
                details['main_text'] = main_text
    except:
        details = {}
        details['main_text'] = ""
    details['main_text'] = main_text
    return details

