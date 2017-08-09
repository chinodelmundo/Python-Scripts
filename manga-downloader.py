#! python3
# mangaDL.py - Downloads chapters of a manga.

import requests
import os
import bs4

url = 'http://www.mangareader.net'
print('Enter manga title: ')
title = input()

print('Searching: ' + title)
res = requests.get(url + '/search/?w=' + str(title))
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")
mangaResults = soup.select('.mangaresultitem .manga_name a')

print('Search Results:')
for i in range(len(mangaResults)):
    print('[{count}] {title}'.format(count=i, title=mangaResults[i].getText()))

print('Select the number of the manga to download')
selected = int(input())
selectedTitle = mangaResults[selected].getText()

os.makedirs(selectedTitle, exist_ok=True) # store images in folder named with the selected manga title

print('Starting Chapter:')
start_chapter = int(input())

res = requests.get(url + mangaResults[selected].attrs['href'] + '/' + str(start_chapter))
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")
imgElement = soup.select('#img')
img_title = (mangaResults[selected].attrs['href'] + '/1')[1:].replace('/', '-') + '.jpg'

while(len(imgElement) > 0):
    if imgElement == []:
        print('Could not find comic image.')
    else:
        imgUrl = imgElement[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (imgUrl))
        res = requests.get(imgUrl)
        res.raise_for_status()

        # Save the image
        imageFile = open(os.path.join(selectedTitle, os.path.basename(img_title)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    print(url + imgElement[0].parent.attrs['href']) #print me first - di pa sure
    res = requests.get(url + imgElement[0].parent.attrs['href'])
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    imgElement = soup.select('#img')
    img_title = (imgElement[0].parent.attrs['href'])[1:].replace('/', '-') + '.jpg'

print('Done')
