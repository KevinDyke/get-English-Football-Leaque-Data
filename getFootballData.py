# program to download English football data from http://www.football-data.co.uk/englandm.php
# website saves each season using a name such as E0.csv so save the program saves the data with a more
# meaning name such as PremierLeague-17-18.csv [ Premier League Season 2017-2018]
 
baseurl = 'http://www.football-data.co.uk/'           # home page of the web site
base_dir = 'C:\\Data Science\\Football Data\\'        # bsse directory used to store programs and data
data_dir = base_dir + 'Data\\'                        # directory to store data in
english_page = 'englandm.php'                         # page with english league data
english_url = baseurl + english_page                  # web page with English league data
notes = ''notes.txt'                                  # name of the file containing a description of each column

import urllib.request
from bs4 import BeautifulSoup
import re

def download_page(url):
   """ download web page and return the html """
   try:
      response = urllib.request.urlopen(url)
      html = response.read()
   except urllib.error.HTTPError as e:  
      print(e.code)
      print(e.read())
      html = None
   finally: 
      return html

def read_webpage(filename):   
   """ read in a html page from a file """
   with open(filename, mode='rb') as file: # b is important -> binary
      html = file.read()
   return html
   
def save_html(filename,html):
   """ save a html page as a file """
   f = open(filename,'wb')
   f.write(html)
   f.close
   
def download(url,filename):
   """ download data from an url and save as a file """
   print("Download from {0}: ".format(url))
   results = download_page(url)
   print("Saved to {0}".format(filename))
   save_html(filename,results)
   
def extract_and_save_data(html):
   """ read in the html of the data page, build a list of urls to download, download and store """
   soup = BeautifulSoup(html, 'lxml')
   
   # obtain a list of the urls of the data files
   links = []
   for link in soup.findAll('a', attrs={'href': re.compile("^mmz4281")}):
       links.append(str(link))
    
   # download files
   for link in links:
       # extract the url and leaque data
       matched = re.search('mmz4281/([0-9]{2})([0-9]{2})/E([0-9|C]).csv">(.*)</a>',str(link))
       if matched:
          token = matched.groups()
          url = baseurl + 'mmz4281/' + token[0] + token[1] + '/E' + token[2] + '.csv'
          filename = data_dir + token[3].replace(' ','') + '-' + token[0] + '-' + token[1] + '.csv'
          download(url,filename)
   
   # downlad the notes
   print("Downloading the notes")   
   download(baseurl + notes, data_dir + notes) 
   
if __name__ == '__main__':
   """ download web page from the web (A) or read it from a file (C).  Could do both by uncommenting (A), (B) and (C) """
   html = download_page(english_url)  # download web page (A)
   #if html is not None:  # (B)
   #   save_html(base_dir + english_page, html) 
   #html = read_webpage(base_dir + 'englandm.php') # read webpage from file (C)
   extract_and_save_data(html) # get the data and save as csv
   
 
      
      