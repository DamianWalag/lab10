import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import cv2
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_image(link, url):

    response = requests.get(url + link)
    img = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), cv2.BORDER_DEFAULT)
    return blurred, link

if __name__ == '__main__':
    url = 'http://www.if.pw.edu.pl/~mrow/dyd/wdprir/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    start = time.time()
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href.endswith(".png"):
            links.append(href)
    
    #sekwencyjnie 
    for link in links:     
        response = requests.get(url + link)
        img = np.array(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (15, 15), cv2.BORDER_DEFAULT)
        print("saving: ",link)
        cv2.imwrite(link, blurred)
    stop = time.time()
    
    print("regular time: ",stop-start)
    
    #osobne procesy
    start = time.time()
    with ProcessPoolExecutor(24) as executor:
        futures = [executor.submit(process_image, link, url) for link in links]
        for f in as_completed(futures):
            blurred, link = f.result()
            print("saving: ",link)
            cv2.imwrite('fast_' + link, blurred)
    stop = time.time()
    print('time with ProcessPoolExecutor: ', stop-start)


#regular time:  33.81510782241821
#time with ProcessPoolExecutor:  7.940021514892578