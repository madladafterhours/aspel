import requests as req
from bs4 import BeautifulSoup as bs
from csv import reader
from datetime import datetime

global requests
requests = req.Session()

#Pull and sort all art from the csv
artlist = []
with open('catalog.csv', 'r', encoding="utf8") as c:
    csvr = reader(c)
    for row in csvr:
        artlist.append(row)
artlist.pop(0)

#NATIONAL GALLERY OF ART
def nga():
    global caption
    global filename
    while True:
        i = 0
        while True:
            try:
                nga_page = str(requests.get(f'https://www.random.org/integers/?num=1&min=1&max=123255&col=1&base=10&format=plain&rnd=new', timeout=300).json())
                break
            except:
                i+=1
                if i >9:
                    raise
        i = 0
        while True:
            try:
                html = bs(requests.get(f'https://www.nga.gov/collection/art-object-page.{nga_page}.html', timeout=300).text, 'html.parser')
                break
            except:
                i+=1
                if i >9:
                    raise    
        
        raw_name = html.find('h1', class_='object-title')
        if raw_name == None:
            continue
        raw_img = html.find("img", {"class":"mainImg object-image"})
        if raw_img == None or raw_img['src'] == '/content/dam/ngaweb/placeholders/placeholder-lg.svg':
            continue
        img = raw_img['src']
        name = html.find('h1', class_='object-title').find('em').get_text()
        author = html.find('p', class_='attribution').get_text()
        filename = f'{datetime.now().strftime("%d%m%Y%H%M%S")}.{img.split(".")[-1]}'
        with open(filename, 'wb') as f:
            i = 0
            while True:
                try:
                    f.write(requests.get(img, timeout=300).content)
                    break
                except:
                    i+=1
                    if i >9:
                        raise    
        caption = f'{name} | {author}'
        break
    print(caption)

#WIKIART
def wa():
    global caption
    global filename
    while True:
        i = 0
        while True:
            try:
                html = bs(requests.get(f'https://www.wikiart.org', timeout=300).text, 'html.parser')
                break
            except:
                i+=1
                if i >9:
                    raise
        unparsed_data = html.find('section', class_='wiki-layout-left-menu').find('main')['ng-init']
        year = unparsed_data[unparsed_data.index('"CompletitionYear" : "'):unparsed_data.index('", "ViewUrl" : "')].replace('"CompletitionYear" : "', '')
        if year == '?':
            year = ''
        else:
            if int(year) > 1950:
                continue
            year = f', {year}'
        author = unparsed_data[unparsed_data.index('", "ArtistName" : "'):unparsed_data.index('", "CompletitionYear" : "')].replace('", "ArtistName" : "', '')
        title = unparsed_data[unparsed_data.index('", "Title" : "'):unparsed_data.index('", "ArtistName" : "')].replace('", "Title" : "', '')
        caption = f'{title}{year} | {author}'
        img = unparsed_data[unparsed_data.index('https://uploads'):unparsed_data.index('", "IsPlaceholder"')].replace('!Large.jpg', '')
        filename = f'{datetime.now().strftime("%d%m%Y%H%M%S")}.{img.split(".")[-1]}'
        with open(filename, 'wb') as f:
            i = 0
            while True:
                try:
                    f.write(requests.get(img, timeout=300).content)
                    break
                except:
                    i+=1
                    if i >9:
                        raise     
        break
    print(caption)

#WEB GALLERY OF ART
def wga():
    global caption
    global filename
    i = 0
    while True:
        try:
            pull = artlist[requests.get(f'https://www.random.org/integers/?num=1&min=0&max={len(artlist)-1}&col=1&base=10&format=plain&rnd=new', timeout=300).json()]
            break
        except:
            i+=1
            if i >9:
                raise   
    img = f"{pull[6].replace('https://www.wga.hu/html', 'https://www.wga.hu/art').replace('.html', '.jpg')}"
    date = '' if pull[3] == '-' else pull[3]
    title = pull[2]
    if len(pull[0].split(', ')) > 1:
        author = str(pull[0].split(', ')[1]+' '+pull[0].split(', ')[0].lower().capitalize())
    else:
        author = pull[0].lower().capitalize()
    caption = f'{title}, {date} | {author}' if date != '' else f'{title} | {author}'
    filename = f'{datetime.now().strftime("%d%m%Y%H%M%S")}.{img.split(".")[-1]}'
    with open(filename, 'wb') as f:
        i = 0
        while True:
            try:
                f.write(requests.get(img, timeout=300).content)
                break
            except:
                i+=1
                if i >9:
                    raise
    print(caption)

def run():
    i = 0
    while True:
        try:
            pick = int(requests.get(f'https://www.random.org/integers/?num=1&min=1&max=3&col=1&base=10&format=plain&rnd=new', timeout=300).json())
            break
        except:
            i+=1
            if i >9:
                raise    
    if pick == 1:
        nga()
    elif pick == 2:
        wga()
    else:
        wa()
run()