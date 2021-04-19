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
    p = 0
    salary = 0
    quality = 0
    

    for tag in tags:
        for content in tag.find_all('p'):
            if content.text.startswith("Population:"):
                p = content.text.replace("Population:", "").strip()
                p = p.replace(",", '')   
         
            if content.text.startswith("Average annual salary:"):
                salary = content.text.replace("Average annual salary:", "").strip()[1:]
                salary = salary.replace(",", '')   

            if content.text.startswith("Quality of life:"):
                quality = content.text.replace("Quality of life:", "").strip()
            
        best_cities.append((tag.find('h2', class_="slide-title-text").text[2:].replace(".", "").strip(), int(p), int(salary), float(quality)))
    print(best_cities)
            

                
            
        
#        best_cities.append((tag.find('h2', class_="slide-title-text").text[2:].replace(".", "").strip(), tag.find_all('p')[2].text.replace("Population:", "").strip(), tag.find_all('p')[3].text.replace("Average annual salary:", "").strip(), tag.find_all('p')[4].text.replace("Quality of life:", "").strip(), tag.find_all('p')[5].text.replace("Value index:", "").strip()))
       #best_cities.append((tag.find('h2', class_="slide-title-text").text[2:].replace(".", "").strip(), float(population)))

       #, tag.find_all('p')[2].text, tag.find_all('p')[3].text, tag.find_all('p')[4].text.replace("Quality of life:", "").strip(), tag.find_all('p')[5].text))
    
#




def main():
    getTags()





class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(requests.get('https://www.businessinsider.com/us-news-best-places-to-live-in-america-2016-3').text, 'html.parser')



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
