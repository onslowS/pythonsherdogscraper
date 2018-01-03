##My sherdog scraping code
from bs4 import BeautifulSoup
import urllib.request
import requests
import MySQLdb

fighter_records = []
#change this range to scrape more fighters by their id
for x in range(1, 3):
    url = "http://www.sherdog.com/fighter/" + str(x)
    resp = requests.get(url)
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    #array to store all the wins, losses, draws
    records = []
    #array to store all the fights, how they ended, where they happened
    results = []
    for link in soup.find_all('h1'):
        if(link['itemprop'] == 'name'):
            tempname = link.find('span').string
    for link in soup.find_all('div'):
        if link.has_attr('class'):
            if('bio_graph' in link['class']):
                tempwins = link.find_all('span')
                for templink in tempwins:
                    if('counter' in templink['class']):
                        records.append(templink.string)
            if('content' in link['class'] and 'table' in link['class']):
                counter = 0
                for templink in link.find_all('tr'):
                    datefound = False
                    if('odd' in templink['class'] or 'even' in templink['class']):
                        resulthow = str(templink.find_all('td')[3]).split('<br/>')
                        resulthow = resulthow[0].replace('<td>', '')
                        result = templink.find('span').string
                        opponent = templink.find('a').string
                        for templink2 in templink.find_all('span'):
                            if(templink2.has_attr('itemprop')):
                                if('award' in templink2['itemprop']):
                                    event = templink2.string
                            if templink2.has_attr('class'):
                                if('sub_line' in templink2['class']):
                                    if(datefound == False):
                                        date = templink2.string
                                        datefound = True
                        for templink3 in templink.find_all('a'):
                            if(templink3.has_attr('href')):
                                if(templink3['href'][1:6] == 'event'):
                                    event = templink3.string
                        
                        results.append([result, resulthow, opponent, event, date])
                    counter += 1
    tempwin = records[0]
    temploss = records[1]
    if(len(records) == 3):
        tempdraw = records[2]
        fighter_record = {'name': tempname, 'wins': tempwin, 'losses': temploss, 'draws': tempdraw, 'results': results}
    else:
        fighter_record = {'name': tempname, 'wins': tempwin, 'losses': temploss, 'draws': 0, 'results': results}
    fighter_records.append(fighter_record)

print(fighter_records)