from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote

def get_all_titles(page_num):
    url = 'https://www.goodreads.com/review/list/121457483-mansi-jain?shelf=to-read&&page='+str(page_num)
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find("tbody").children
    titles = set()
    for row in rows:
        if row.findNext("td", class_="field title") is not None:
            titles.add(row.findNext("td", class_="field title").div.a.get_text())
    return titles

def get_availablity(titles):
    ebooks = []
    paperback = []
    for title in titles:

        # e-book
        url = 'https://bpl.bibliocommons.com/v2/search?query=' + quote(title) + '&searchType=keyword&f_FORMAT=EBOOK&f_STATUS=_online_'
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page, 'html.parser')
        avail = soup.find("span", class_="cp-availability-status available")
        if avail is not None:
            if avail.get_text() == 'Available':
                ebooks.append(title)

        # paperback
        url = 'https://bpl.bibliocommons.com/v2/search?query=' + quote('The Arctic Fury') + '&searchType=keyword&f_FORMAT=BK&f_STATUS=3'
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page, 'html.parser')
        avail = soup.find("button", class_="cp-btn btn btn-transactional cp-request-item-button btn-block")
        if avail is not None:
            if avail.get_text().startswith('Place hold'):
                paperback.append(title)

    return {
        'ebooks': ebooks,
        'paperback': paperback
    }

books = set

for page in [1, 2, 3]:
    x = get_all_titles(page)
    books = books.union(x)
    print(len(x))

avialable_titles = get_availablity(books)
print(avialable_titles['ebooks'])
