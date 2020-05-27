import urllib2
import re
from bs4 import BeautifulSoup
import string
import nltk
#nltk.download()
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import ast
import re

from ast import literal_eval
translate_table = dict((ord(char), None) for char in string.punctuation)


def tokenize(poets):
    #tokenizing the words of each page
    #norep: a list of no repitation in words of the tokenized page
    translate_table = dict((ord(char), None) for char in string.punctuation)
    poet = poets.translate(translate_table)
    words = word_tokenize(poet)
    ps = PorterStemmer()
    swords = []
    for w in words:
        swords = swords + [ps.stem(w)]
    stop_words = set(stopwords.words('english'))
    filtered_words = []
    for w in swords:
        if w not in stop_words:
            filtered_words.append(w)
    norep=list(set(filtered_words))
    return norep


if __name__ == "__main__":
    #url: The website that we are going to get poetry pages from it.
    #linkfind: finds all the poetry pages from the url
    #myDict: a dictionary of all the tokinized texts from each poetry page that listed by document number
    url = 'https://www.biographyonline.net/poets.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = urllib2.Request(url, headers=headers)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    linkfind = soup.find_all('a', {'href': re.compile("^../poets")})
    myDict = dict()
    docnum = 0
    allurls = []
    for links in linkfind:
        link = links.get('href')
        path = url.replace('poets.html', '')
        linkend = link.replace('../', '')
        newurl = path + linkend
        allurls.append(newurl)

    norep = list(set(allurls))

    for url in norep:
        newreq = urllib2.Request(url, headers=headers)
        newpage = urllib2.urlopen(newreq)
        newsoup = BeautifulSoup(newpage, 'html.parser')

        for script in newsoup(["script"]):
            script.extract()
        content_sec = newsoup.find('section', attrs={'class': 'post-content clearfix'})
        content = content_sec.text
        content = content.translate(translate_table)
        poets = BeautifulSoup(content, "lxml").text
        cleanlist = tokenize(poets)
        myDict[docnum] = cleanlist
        docnum = docnum + 1

    for key, value in myDict.items():
        for words in value:
            print key , words