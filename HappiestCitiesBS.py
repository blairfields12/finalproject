#50 best places to live in America ranked

from bs4 import BeautifulSoup
import requests
import unittest



def getTags():
    url = 'https://www.businessinsider.com/us-news-best-places-to-live-in-america-2016-3'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    best_cities = []
    tags = soup.find_all('div', class_="slide-layout clearfix")
    for tag in tags:
        best_cities.append((tag.find('h2', class_="slide-title-text").text[2:].replace(".", "").strip(), tag.find_all('p')[2].text.replace("Population:", "").strip(), tag.find_all('p')[3].text.replace("Average annual salary:", "").strip(), tag.find_all('p')[4].text.replace("Quality of life:", "").strip(), tag.find_all('p')[5].text.replace("Value index:", "").strip()))
    print(best_cities)





def main():
    getTags()





class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(requests.get('https://www.businessinsider.com/us-news-best-places-to-live-in-america-2016-3').text, 'html.parser')



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
